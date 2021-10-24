# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import logging.handlers
import multiprocessing
import os
from pathlib import PosixPath
from typing import List, Tuple, Union

import ctc_segmentation as cs
import numpy as np


def get_segments(
    log_probs: np.ndarray,
    path_wav: Union[PosixPath, str],
    transcript_file: Union[PosixPath, str],
    output_file: str,
    vocabulary: List[str],
    window_size: int = 8000,
    frame_duration_ms: int = 10,
) -> None:
    """
    Segments the audio into segments and saves segments timings to a file

    Args:
        log_probs: Log probabilities for the original audio from an ASR model, shape T * |vocabulary|.
                   values for blank should be at position 0
        path_wav: path to the audio .wav file
        transcript_file: path to
        output_file: path to the file to save timings for segments
        vocabulary: vocabulary used to train the ASR model, note blank is at position 0
        window_size: the length of each utterance (in terms of frames of the CTC outputs) fits into that window.
        frame_duration_ms: frame duration in ms
    """
    print('log_probs:', log_probs.shape)
    config = cs.CtcSegmentationParameters()
    config.char_list = vocabulary
    config.min_window_size = window_size
    config.index_duration = 0.0799983368347339
    config.blank = len(vocabulary) - 1
    # config.space = "▁"

    with open(transcript_file, "r") as f:
        text = f.readlines()
        text = [t.strip() for t in text if t.strip()]

    # add corresponding original text without pre-processing
    transcript_file_no_preprocessing = transcript_file.replace('.txt', '_with_punct.txt')
    if not os.path.exists(transcript_file_no_preprocessing):
        raise ValueError(f'{transcript_file_no_preprocessing} not found.')

    with open(transcript_file_no_preprocessing, "r") as f:
        text_no_preprocessing = f.readlines()
        text_no_preprocessing = [t.strip() for t in text_no_preprocessing if t.strip()]

    # add corresponding normalized original text
    transcript_file_normalized = transcript_file.replace('.txt', '_with_punct_normalized.txt')
    if not os.path.exists(transcript_file_normalized):
        raise ValueError(f'{transcript_file_normalized} not found.')

    with open(transcript_file_normalized, "r") as f:
        text_normalized = f.readlines()
        text_normalized = [t.strip() for t in text_normalized if t.strip()]

    if len(text_no_preprocessing) != len(text):
        raise ValueError(f'{transcript_file} and {transcript_file_no_preprocessing} do not match')

    if len(text_normalized) != len(text):
        raise ValueError(f'{transcript_file} and {transcript_file_normalized} do not match')

    # words = []
    # for t in text:
    #     words.extend(t.split())
    # text = words
    # text_normalized = words
    # text_no_preprocessing = words

    """
    # 10/11
    # make words
    from prepare_bpe import prepare_text_default, get_config
    config, tokenizer = get_config()
    vocabulary = config.char_list
    text_processed = []
    for i in range(len(text)):
        text_processed.append(" ".join(["▁" + x for x in text[i].split()]))
    ground_truth_mat, utt_begin_indices = prepare_text_default(config, text_processed)
    _print(ground_truth_mat, vocabulary)
    stride = 1/3.2
    """


    # works for sentences CitriNet
    from prepare_bpe import prepare_tokenized_text_nemo_works_modified
    # asr_model = "/home/ebakhturina/data/segmentation/models/ru/CitriNet-512-8x-Stride-Gamma-0.25-RU-e100_wer25.nemo"
    asr_model = "stt_en_citrinet_512_gamma_0_25"
    asr_model = "/home/ebakhturina/data/segmentation/models/de/best_stt_de_citrinet_1024.nemo"
    asr_model = "stt_en_citrinet_512_gamma_0_25"
    asr_model = "stt_es_citrinet_512"
    stride = 1
    ground_truth_mat, utt_begin_indices, vocabulary = prepare_tokenized_text_nemo_works_modified(text, asr_model)
    _print(ground_truth_mat, vocabulary)
    """

    # QN
    from prepare_bpe import prepare_text_default, get_config_qn
    config = get_config_qn()
    config.min_window_size = window_size
    config.index_duration = 0.019990723562152132 #0.02
    ground_truth_mat, utt_begin_indices = prepare_text_default(config, text)
    _print(ground_truth_mat, config.char_list)
    stride = 1
    """
    #
    logging.debug(f"Syncing {transcript_file}")
    logging.debug(
        f"Audio length {os.path.basename(path_wav)}: {log_probs.shape[0]}. "
        f"Text length {os.path.basename(transcript_file)}: {len(ground_truth_mat)}"
    )

    timings, char_probs, char_list = cs.ctc_segmentation(config, log_probs, ground_truth_mat)
    segments = cs.determine_utterance_segments(config, utt_begin_indices, char_probs, timings, text)
    # import pdb;
    # pdb.set_trace()
    for i, (word, segment) in enumerate(zip(text, segments)):
        if i < 10:
            print(f"{segment[0]:.2f} {segment[1]:.2f} {segment[2]:3.4f} {word}")

    write_output(output_file, path_wav, segments, text, text_no_preprocessing, text_normalized, stride)


def _print(ground_truth_mat, vocabulary):
    chars = []
    for row in ground_truth_mat:
        chars.append([])
        for ch_id in row:
            if ch_id != -1:
                chars[-1].append(vocabulary[int(ch_id)])

    [print(x) for x in chars[:100]]


def write_output(
    out_path: str,
    path_wav: str,
    segments: List[Tuple[float]],
    text: str,
    text_no_preprocessing: str,
    text_normalized: str,
    stride: float = 1,
):
    """
    Write the segmentation output to a file

    out_path: Path to output file
    path_wav: Path to the original audio file
    segments: Segments include start, end and alignment score
    text: Text used for alignment
    text_no_preprocessing: Reference txt without any pre-processing
    text_normalized: Reference text normalized
    stride: Stride applied to an ASR input
    """
    # Uses char-wise alignments to get utterance-wise alignments and writes them into the given file
    with open(str(out_path), "w") as outfile:
        outfile.write(str(path_wav) + "\n")

        for i, (start, end, score) in enumerate(segments):
            outfile.write(
                f'{start/stride} {end/stride} {score} | {text[i]} | {text_no_preprocessing[i]} | {text_normalized[i]}\n'
            )


#####################
# logging utils
#####################
def listener_configurer(log_file, level):
    root = logging.getLogger()
    h = logging.handlers.RotatingFileHandler(log_file, 'w')
    f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    h.setFormatter(f)
    ch = logging.StreamHandler()
    root.addHandler(h)
    root.setLevel(level)
    root.addHandler(ch)


def listener_process(queue, configurer, log_file, level):
    configurer(log_file, level)
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.setLevel(logging.INFO)
            logger.handle(record)  # No level or filter logic applied - just do it!

        except Exception:
            import sys
            import traceback

            print('Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


def worker_configurer(queue, level):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(level)


def worker_process(
    queue, configurer, level, log_probs, path_wav, transcript_file, output_file, vocabulary, window_len
):
    configurer(queue, level)
    name = multiprocessing.current_process().name
    innerlogger = logging.getLogger('worker')
    innerlogger.info(f'{name} is processing {path_wav}, window_len={window_len}')
    get_segments(log_probs, path_wav, transcript_file, output_file, vocabulary, window_len)
    innerlogger.info(f'{name} completed segmentation of {path_wav}, segments saved to {output_file}')
