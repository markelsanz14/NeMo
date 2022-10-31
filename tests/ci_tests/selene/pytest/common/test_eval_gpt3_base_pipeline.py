import os
import json
import glob
import pytest

CI_JOB_RESULTS = os.environ.get("RESULTS_DIR")

class TestEvalBaseGpt3Pipeline:

    margin = 0.05
    job_name = CI_JOB_RESULTS.rsplit("/",1)[1]
    file_name = job_name + ".json" #eg eval_gpt3_126m_tp1_pp1_lambada.json
    run_model = "gpt3" if file_name.split("_")[1] == "gpt3" else "prompt_gpt3"
    test_key = "lambada" if run_model == "gpt3" else "prompt"
    file_directory =  run_model + "_result_files" # Since the file name will be prompt_learn_gpt3_..
    expected_metrics_file = os.path.join("tests/ci_tests/selene/pytest/eval", file_directory, file_name)
    expected = None
    if os.path.exists(expected_metrics_file):
        with open(expected_metrics_file) as f:
            expected = json.load(f)

    def test_ci_eval_gpt3(self):
        if self.expected is None:
            raise FileNotFoundError("Use `CREATE_TEST_DATA=True` to create baseline files.")
        # Results are stored in /lustre/fsw/joc/big_nlp/bignlp_ci/5667649/results/eval_gpt3_126m_tp1_pp1_lambada/results/eval_gpt3_126m_tp1_pp1_lambada_2022-08-17_10-22-49_7Ba/predictions/metrics.json
        result_files = glob.glob(os.path.join(CI_JOB_RESULTS, '*/metrics.json'))
        result_files += glob.glob(os.path.join(CI_JOB_RESULTS, 'results/*/metrics.json'))
        assert len(result_files) == 1, f"Only one metrics.json file should be present inside {CI_JOB_RESULTS}"

        actual_metrics_file = result_files[0]
        assert os.path.exists(actual_metrics_file), f"metrics.json file does not exist: {actual_metrics_file}"

        with open(actual_metrics_file) as json_file:
            full_metrics = json.load(json_file)
            print(full_metrics)
            metrics = full_metrics[self.test_key]
            expected_lambada = self.expected[self.test_key]
            assert metrics["ppl"] == pytest.approx(expected=expected_lambada["ppl"], rel=self.margin), f"Lambada PPL should be {expected_lambada['ppl']} but it is {metrics['ppl']}"
            assert metrics["ppl_stderr"] == pytest.approx(expected=expected_lambada["ppl_stderr"], rel=self.margin), f"Lambada PPL StdErr should be {expected_lambada['ppl_stderr']} but it is {metrics['ppl_stderr']}"
            assert metrics["acc"] == pytest.approx(expected=expected_lambada["acc"], rel=self.margin), f"Lambada Accuracy should be {expected_lambada['acc']} but it is {metrics['acc']}"
            assert metrics["acc_stderr"] == pytest.approx(expected=expected_lambada["acc_stderr"], rel=self.margin), f"Lambada Accuracy StdErr should be {expected_lambada['acc_stderr']} but it is {metrics['acc_stderr']}"