from omegaconf import OmegaConf


class TestTrainingGPT3Config:
    def test_training_gpt3_config_126m(self):
        conf = OmegaConf.load("conf/training/gpt3/126m.yaml")
        s = """
        run:
          name: gpt3_126m
          results_dir: ${base_results_dir}/${.name}
          time_limit: "1-00:00:00"
          dependency: "singleton"

        trainer:
          num_nodes: 8
          devices: 8
          accelerator: gpu
          precision: bf16
          logger: False
          enable_checkpointing: False
          replace_sampler_ddp: False
          max_epochs: null
          max_steps: 600000
          max_time: "00:23:30:00"
          log_every_n_steps: 10
          val_check_interval: 2000
          limit_val_batches: 50
          limit_test_batches: 50
          accumulate_grad_batches: 1
          gradient_clip_val: 1.0

        exp_manager:
          explicit_log_dir: ${training.run.results_dir}/results
          exp_dir: null
          name: megatron_gpt
          create_wandb_logger: False
          wandb_logger_kwargs:
            project: nemo_gpt3
            name: ${training.run.name}
          resume_if_exists: True
          resume_ignore_no_checkpoint: True
          create_checkpoint_callback: True
          checkpoint_callback_params:
            monitor: val_loss
            save_top_k: 10
            mode: min
            always_save_nemo: False
            save_nemo_on_train_end: False
            filename: 'megatron_gpt--{val_loss:.2f}-{step}-{consumed_samples}'
            model_parallel_size: ${multiply:${training.model.tensor_model_parallel_size}, ${training.model.pipeline_model_parallel_size}}
          log_step_timing: True
          step_timing_kwargs:
            sync_cuda: True
            buffer_size: 5

        model:
          # model parallelism 
          micro_batch_size: 4
          global_batch_size: 256
          tensor_model_parallel_size: 1
          pipeline_model_parallel_size: 1
          resume_from_checkpoint: null

          # model architecture
          encoder_seq_length: 2048
          max_position_embeddings: 2048
          num_layers: 12
          hidden_size: 768
          ffn_hidden_size: ${multiply:4, ${.hidden_size}}
          num_attention_heads: 12
          init_method_std: 0.023
          hidden_dropout: 0.1
          kv_channels: null
          apply_query_key_layer_scaling: True
          layernorm_epsilon: 1e-5
          make_vocab_size_divisible_by: 128
          pre_process: True
          post_process: True
          persist_layer_norm: True
          grad_div_ar_fusion: True
          gradient_as_bucket_view: True
          gradient_accumulation_fusion: True
          activations_checkpoint_granularity: full
          activations_checkpoint_method: block
          activations_checkpoint_num_layers: 0
          sequence_parallel: False

          tokenizer:
            library: 'megatron'
            type: 'GPT2BPETokenizer'
            model: null
            delimiter: null
            vocab_file: ${data_dir}/bpe/vocab.json
            merge_file: ${data_dir}/bpe/merges.txt

          # precision
          native_amp_init_scale: 4294967296
          native_amp_growth_interval: 1000
          hysteresis: 2
          fp32_residual_connection: False
          fp16_lm_cross_entropy: False
          
          # Megatron O2-style half-precision
          megatron_amp_O2: True
          grad_allreduce_chunk_size_mb: 125

          # miscellaneous
          seed: 1234
          use_cpu_initialization: False
          onnx_safe: False
          apex_transformer_log_level: 30

          optim:
            name: distributed_fused_adam
            lr: 6e-4
            weight_decay: 0.1 
            betas: 
            - 0.9
            - 0.95
            sched:
              name: CosineAnnealing
              warmup_steps: 636
              constant_steps: 100000
              min_lr: 6e-5

          nsys_profile:
            enabled: False
            trace: [nvtx,cuda]
            start_step: 10  # Global batch to start profiling
            end_step: 10 # Global batch to end profiling
            ranks: [0] # Global rank IDs to profile
            gen_shape: False # Generate model and kernel details including input shapes

          data:
            data_impl: mmap
            splits_string: "99990,8,2"
            seq_length: 2048
            skip_warmup: True
            num_workers: 2
            dataloader_type: single
            reset_position_ids: False
            reset_attention_mask: False
            eod_mask_loss: False
            index_mapping_dir: null
            data_prefix:
              - .0333
              - ${data_dir}/my-gpt3_00_text_document
              - .0333
              - ${data_dir}/my-gpt3_01_text_document
              - .0333
              - ${data_dir}/my-gpt3_02_text_document
              - .0333
              - ${data_dir}/my-gpt3_03_text_document
              - .0333
              - ${data_dir}/my-gpt3_04_text_document
              - .0333
              - ${data_dir}/my-gpt3_05_text_document
              - .0333
              - ${data_dir}/my-gpt3_06_text_document
              - .0333
              - ${data_dir}/my-gpt3_07_text_document
              - .0333
              - ${data_dir}/my-gpt3_08_text_document
              - .0333
              - ${data_dir}/my-gpt3_09_text_document
              - .0333
              - ${data_dir}/my-gpt3_10_text_document
              - .0333
              - ${data_dir}/my-gpt3_11_text_document
              - .0333
              - ${data_dir}/my-gpt3_12_text_document
              - .0333
              - ${data_dir}/my-gpt3_13_text_document
              - .0333
              - ${data_dir}/my-gpt3_14_text_document
              - .0333
              - ${data_dir}/my-gpt3_15_text_document
              - .0333
              - ${data_dir}/my-gpt3_16_text_document
              - .0333
              - ${data_dir}/my-gpt3_17_text_document
              - .0333
              - ${data_dir}/my-gpt3_18_text_document
              - .0333
              - ${data_dir}/my-gpt3_19_text_document
              - .0333
              - ${data_dir}/my-gpt3_20_text_document
              - .0333
              - ${data_dir}/my-gpt3_21_text_document
              - .0333
              - ${data_dir}/my-gpt3_22_text_document
              - .0333
              - ${data_dir}/my-gpt3_23_text_document
              - .0333
              - ${data_dir}/my-gpt3_24_text_document
              - .0333
              - ${data_dir}/my-gpt3_25_text_document
              - .0333
              - ${data_dir}/my-gpt3_26_text_document
              - .0333
              - ${data_dir}/my-gpt3_27_text_document
              - .0333
              - ${data_dir}/my-gpt3_28_text_document
              - .0334
              - ${data_dir}/my-gpt3_29_text_document
        """
        expected = OmegaConf.create(s)
        assert (
            expected == conf
        ), f"conf/training/gpt3/126m.yaml must be set to {expected} but it currently is {conf}."

    def test_training_config_5b(self):
        conf = OmegaConf.load("conf/training/gpt3/5b.yaml")
        s = """
        run:
          name: gpt3_5b
          results_dir: ${base_results_dir}/${.name}
          time_limit: "6-00:00:00"
          dependency: "singleton"

        trainer:
          num_nodes: 16
          devices: 8
          accelerator: gpu
          precision: bf16
          logger: False
          enable_checkpointing: False
          replace_sampler_ddp: False
          max_epochs: null
          max_steps: 75000
          max_time: "05:23:30:00"
          log_every_n_steps: 10
          val_check_interval: 2000
          limit_val_batches: 50
          limit_test_batches: 50
          accumulate_grad_batches: 1
          gradient_clip_val: 1.0

        exp_manager:
          explicit_log_dir: ${training.run.results_dir}/results
          exp_dir: null
          name: megatron_gpt
          create_wandb_logger: False
          wandb_logger_kwargs:
            project: nemo_gpt3
            name: ${training.run.name}
          resume_if_exists: True
          resume_ignore_no_checkpoint: True
          create_checkpoint_callback: True
          checkpoint_callback_params:
            monitor: val_loss
            save_top_k: 10
            mode: min
            always_save_nemo: False
            save_nemo_on_train_end: False
            filename: 'megatron_gpt--{val_loss:.2f}-{step}-{consumed_samples}'
            model_parallel_size: ${multiply:${training.model.tensor_model_parallel_size}, ${training.model.pipeline_model_parallel_size}}
          log_step_timing: True
          step_timing_kwargs:
            sync_cuda: True
            buffer_size: 5

        model:
          micro_batch_size: 2
          global_batch_size: 2048
          tensor_model_parallel_size: 1
          pipeline_model_parallel_size: 1
          resume_from_checkpoint: null

          # model architecture
          encoder_seq_length: 2048
          max_position_embeddings: 2048
          num_layers: 24
          hidden_size: 4096
          ffn_hidden_size: ${multiply:4, ${.hidden_size}}
          num_attention_heads: 32
          init_method_std: 0.01
          hidden_dropout: 0.1
          kv_channels: null
          apply_query_key_layer_scaling: True
          layernorm_epsilon: 1e-5
          make_vocab_size_divisible_by: 128
          pre_process: True
          post_process: True
          persist_layer_norm: True
          grad_div_ar_fusion: True
          gradient_as_bucket_view: True
          gradient_accumulation_fusion: True
          activations_checkpoint_granularity: full
          activations_checkpoint_method: block
          activations_checkpoint_num_layers: 0
          sequence_parallel: False

          tokenizer:
            library: 'megatron'
            type: 'GPT2BPETokenizer'
            model: null
            delimiter: null # only used for tabular tokenizer
            vocab_file: ${data_dir}/bpe/vocab.json
            merge_file: ${data_dir}/bpe/merges.txt

          # precision
          native_amp_init_scale: 4294967296
          native_amp_growth_interval: 1000
          hysteresis: 2
          fp32_residual_connection: False
          fp16_lm_cross_entropy: False

          # Megatron O2-style half-precision
          megatron_amp_O2: True
          grad_allreduce_chunk_size_mb: 125

          # miscellaneous
          seed: 1234
          use_cpu_initialization: False
          onnx_safe: False
          apex_transformer_log_level: 30

          optim:
            name: distributed_fused_adam
            lr: 1.5e-4
            weight_decay: 0.1
            betas:
            - 0.9
            - 0.95
            sched:
              name: CosineAnnealing
              warmup_steps: 115
              constant_steps: 12500
              min_lr: 1.5e-5

          nsys_profile:
            enabled: False
            trace: [nvtx,cuda]
            start_step: 10  # Global batch to start profiling
            end_step: 10 # Global batch to end profiling
            ranks: [0] # Global rank IDs to profile
            gen_shape: False # Generate model and kernel details including input shapes

          data:
            data_impl: mmap
            splits_string: "99990,8,2"
            seq_length: 2048
            skip_warmup: True
            num_workers: 2
            dataloader_type: single
            reset_position_ids: False
            reset_attention_mask: False
            eod_mask_loss: False
            index_mapping_dir: null
            data_prefix:
              - .0333
              - ${data_dir}/my-gpt3_00_text_document
              - .0333
              - ${data_dir}/my-gpt3_01_text_document
              - .0333
              - ${data_dir}/my-gpt3_02_text_document
              - .0333
              - ${data_dir}/my-gpt3_03_text_document
              - .0333
              - ${data_dir}/my-gpt3_04_text_document
              - .0333
              - ${data_dir}/my-gpt3_05_text_document
              - .0333
              - ${data_dir}/my-gpt3_06_text_document
              - .0333
              - ${data_dir}/my-gpt3_07_text_document
              - .0333
              - ${data_dir}/my-gpt3_08_text_document
              - .0333
              - ${data_dir}/my-gpt3_09_text_document
              - .0333
              - ${data_dir}/my-gpt3_10_text_document
              - .0333
              - ${data_dir}/my-gpt3_11_text_document
              - .0333
              - ${data_dir}/my-gpt3_12_text_document
              - .0333
              - ${data_dir}/my-gpt3_13_text_document
              - .0333
              - ${data_dir}/my-gpt3_14_text_document
              - .0333
              - ${data_dir}/my-gpt3_15_text_document
              - .0333
              - ${data_dir}/my-gpt3_16_text_document
              - .0333
              - ${data_dir}/my-gpt3_17_text_document
              - .0333
              - ${data_dir}/my-gpt3_18_text_document
              - .0333
              - ${data_dir}/my-gpt3_19_text_document
              - .0333
              - ${data_dir}/my-gpt3_20_text_document
              - .0333
              - ${data_dir}/my-gpt3_21_text_document
              - .0333
              - ${data_dir}/my-gpt3_22_text_document
              - .0333
              - ${data_dir}/my-gpt3_23_text_document
              - .0333
              - ${data_dir}/my-gpt3_24_text_document
              - .0333
              - ${data_dir}/my-gpt3_25_text_document
              - .0333
              - ${data_dir}/my-gpt3_26_text_document
              - .0333
              - ${data_dir}/my-gpt3_27_text_document
              - .0333
              - ${data_dir}/my-gpt3_28_text_document
              - .0334
              - ${data_dir}/my-gpt3_29_text_document
        """
        expected = OmegaConf.create(s)
        assert (
            expected == conf
        ), f"conf/training/gpt3/5b.yaml must be set to {expected} but it currently is {conf}."

    def test_training_config_20b(self):
        conf = OmegaConf.load("conf/training/gpt3/20b.yaml")
        s = """
        run:
          name: gpt3_20b
          results_dir: ${base_results_dir}/${.name}
          time_limit: "7-00:00:00"
          dependency: "singleton"

        trainer:
          devices: 8
          num_nodes: 64
          accelerator: gpu
          precision: bf16
          logger: False
          enable_checkpointing: False
          replace_sampler_ddp: False
          max_epochs: null
          max_steps: 75000
          max_time: "06:23:30:00"
          log_every_n_steps: 10
          val_check_interval: 2000
          limit_val_batches: 50
          limit_test_batches: 50
          accumulate_grad_batches: 1
          gradient_clip_val: 1.0


        exp_manager:
          explicit_log_dir: ${training.run.results_dir}/results
          exp_dir: null
          name: megatron_gpt
          create_wandb_logger: False
          wandb_logger_kwargs:
            project: nemo_gpt3
            name: ${training.run.name}
          resume_if_exists: True
          resume_ignore_no_checkpoint: True
          create_checkpoint_callback: True
          checkpoint_callback_params:
            monitor: val_loss
            save_top_k: 10
            mode: min
            always_save_nemo: False
            save_nemo_on_train_end: False
            filename: 'megatron_gpt--{val_loss:.2f}-{step}-{consumed_samples}'
            model_parallel_size: ${multiply:${training.model.tensor_model_parallel_size}, ${training.model.pipeline_model_parallel_size}}
          log_step_timing: True
          step_timing_kwargs:
            sync_cuda: True
            buffer_size: 5


        model:
          # model parallelism
          micro_batch_size: 4
          global_batch_size: 2048
          tensor_model_parallel_size: 4
          pipeline_model_parallel_size: 1
          resume_from_checkpoint: null

          # model architecture
          encoder_seq_length: 2048
          max_position_embeddings: 2048
          num_layers: 44
          hidden_size: 6144
          ffn_hidden_size: ${multiply:4, ${.hidden_size}}
          num_attention_heads: 48
          init_method_std: 0.008165
          hidden_dropout: 0.1
          kv_channels: null
          apply_query_key_layer_scaling: True
          layernorm_epsilon: 1e-5
          make_vocab_size_divisible_by: 128
          pre_process: True
          post_process: True
          persist_layer_norm: True
          grad_div_ar_fusion: True
          gradient_as_bucket_view: True
          gradient_accumulation_fusion: True
          activations_checkpoint_granularity: selective
          activations_checkpoint_method: null
          activations_checkpoint_num_layers: null
          sequence_parallel: True

          tokenizer:
            library: 'megatron'
            type: 'GPT2BPETokenizer'
            model: null
            delimiter: null
            vocab_file: ${data_dir}/bpe/vocab.json
            merge_file: ${data_dir}/bpe/merges.txt

          # precision
          native_amp_init_scale: 4294967296
          native_amp_growth_interval: 1000
          hysteresis: 2
          fp32_residual_connection: False
          fp16_lm_cross_entropy: False

          # Megatron O2-style half-precision
          megatron_amp_O2: True
          grad_allreduce_chunk_size_mb: 125

          # miscellaneous
          seed: 1234
          use_cpu_initialization: False
          onnx_safe: False
          apex_transformer_log_level: 30

          optim:
            name: distributed_fused_adam
            lr: 1.3e-4
            weight_decay: 0.1
            betas:
            - 0.9
            - 0.95
            sched:
              name: CosineAnnealing
              warmup_steps: 115
              constant_steps: 12500
              min_lr: 1.3e-5

          nsys_profile:
            enabled: False
            trace: [nvtx,cuda]
            start_step: 10  # Global batch to start profiling
            end_step: 10 # Global batch to end profiling
            ranks: [0] # Global rank IDs to profile
            gen_shape: False # Generate model and kernel details including input shapes

          data:
            data_impl: mmap
            splits_string: "99990,8,2"
            seq_length: 2048
            skip_warmup: True
            num_workers: 2
            dataloader_type: single
            reset_position_ids: False
            reset_attention_mask: False
            eod_mask_loss: False
            index_mapping_dir: null
            data_prefix:
              - .0333
              - ${data_dir}/my-gpt3_00_text_document
              - .0333
              - ${data_dir}/my-gpt3_01_text_document
              - .0333
              - ${data_dir}/my-gpt3_02_text_document
              - .0333
              - ${data_dir}/my-gpt3_03_text_document
              - .0333
              - ${data_dir}/my-gpt3_04_text_document
              - .0333
              - ${data_dir}/my-gpt3_05_text_document
              - .0333
              - ${data_dir}/my-gpt3_06_text_document
              - .0333
              - ${data_dir}/my-gpt3_07_text_document
              - .0333
              - ${data_dir}/my-gpt3_08_text_document
              - .0333
              - ${data_dir}/my-gpt3_09_text_document
              - .0333
              - ${data_dir}/my-gpt3_10_text_document
              - .0333
              - ${data_dir}/my-gpt3_11_text_document
              - .0333
              - ${data_dir}/my-gpt3_12_text_document
              - .0333
              - ${data_dir}/my-gpt3_13_text_document
              - .0333
              - ${data_dir}/my-gpt3_14_text_document
              - .0333
              - ${data_dir}/my-gpt3_15_text_document
              - .0333
              - ${data_dir}/my-gpt3_16_text_document
              - .0333
              - ${data_dir}/my-gpt3_17_text_document
              - .0333
              - ${data_dir}/my-gpt3_18_text_document
              - .0333
              - ${data_dir}/my-gpt3_19_text_document
              - .0333
              - ${data_dir}/my-gpt3_20_text_document
              - .0333
              - ${data_dir}/my-gpt3_21_text_document
              - .0333
              - ${data_dir}/my-gpt3_22_text_document
              - .0333
              - ${data_dir}/my-gpt3_23_text_document
              - .0333
              - ${data_dir}/my-gpt3_24_text_document
              - .0333
              - ${data_dir}/my-gpt3_25_text_document
              - .0333
              - ${data_dir}/my-gpt3_26_text_document
              - .0333
              - ${data_dir}/my-gpt3_27_text_document
              - .0333
              - ${data_dir}/my-gpt3_28_text_document
              - .0334
              - ${data_dir}/my-gpt3_29_text_document
        """
        expected = OmegaConf.create(s)
        assert (
            expected == conf
        ), f"conf/training/gpt3/20b.yaml must be set to {expected} but it currently is {conf}."

    def test_training_config_40b(self):
        conf = OmegaConf.load("conf/training/gpt3/40b.yaml")
        s = """
        run:
          name: gpt3_40b
          results_dir: ${base_results_dir}/${.name}
          time_limit: "6-12:00:00"
          dependency: "singleton"

        trainer:
          num_nodes: 128
          devices: 8
          accelerator: gpu
          precision: bf16
          logger: False
          enable_checkpointing: False
          replace_sampler_ddp: False
          max_epochs: null
          max_steps: 75000
          max_time: "6:11:00:00"
          log_every_n_steps: 10
          val_check_interval: 2000
          limit_val_batches: 20
          limit_test_batches: 20
          accumulate_grad_batches: 1
          gradient_clip_val: 1.0

        exp_manager:
          explicit_log_dir: ${training.run.results_dir}/results
          exp_dir: null
          name: megatron_gpt
          create_wandb_logger: False
          wandb_logger_kwargs:
            project: nemo_gpt3
            name: ${training.run.name}
          resume_if_exists: True
          resume_ignore_no_checkpoint: True
          create_checkpoint_callback: True
          checkpoint_callback_params:
            monitor: val_loss
            save_top_k: 5
            mode: min
            always_save_nemo: False
            save_nemo_on_train_end: False
            filename: 'megatron_gpt--{val_loss:.2f}-{step}-{consumed_samples}'
            model_parallel_size: ${multiply:${training.model.tensor_model_parallel_size}, ${training.model.pipeline_model_parallel_size}}
          log_step_timing: True
          step_timing_kwargs:
            sync_cuda: True
            buffer_size: 5

        model:
          micro_batch_size: 2
          global_batch_size: 2048
          tensor_model_parallel_size: 4
          pipeline_model_parallel_size: 2
          resume_from_checkpoint: null

          # model architecture
          encoder_seq_length: 2048
          max_position_embeddings: 2048
          num_layers: 48
          hidden_size: 8192
          ffn_hidden_size: ${multiply:4, ${.hidden_size}}
          num_attention_heads: 64
          init_method_std: 0.007
          hidden_dropout: 0.1
          kv_channels: null
          apply_query_key_layer_scaling: True 
          layernorm_epsilon: 1e-5
          make_vocab_size_divisible_by: 128
          pre_process: True
          post_process: True
          persist_layer_norm: True
          grad_div_ar_fusion: True
          gradient_as_bucket_view: True
          gradient_accumulation_fusion: True
          activations_checkpoint_granularity: selective
          activations_checkpoint_method: null
          activations_checkpoint_num_layers: null
          sequence_parallel: True

          tokenizer:
            library: 'megatron'
            type: 'GPT2BPETokenizer'
            model: null
            delimiter: null
            vocab_file: ${data_dir}/bpe/vocab.json
            merge_file: ${data_dir}/bpe/merges.txt

          # precision
          native_amp_init_scale: 4294967296
          native_amp_growth_interval: 1000
          hysteresis: 2
          fp32_residual_connection: False
          fp16_lm_cross_entropy: False

          # Megatron O2-style half-precision
          megatron_amp_O2: True
          grad_allreduce_chunk_size_mb: 125

          # miscellaneous
          seed: 1234
          use_cpu_initialization: False
          onnx_safe: False
          apex_transformer_log_level: 30

          optim:
            name: distributed_fused_adam
            lr: 1.0e-4
            weight_decay: 0.1 
            betas: 
            - 0.9
            - 0.95
            sched:
              name: CosineAnnealing
              warmup_steps: 115
              constant_steps: 12500
              min_lr: 1.0e-5

          nsys_profile:
            enabled: False
            trace: [nvtx,cuda]
            start_step: 10  # Global batch to start profiling
            end_step: 10 # Global batch to end profiling
            ranks: [0] # Global rank IDs to profile
            gen_shape: False # Generate model and kernel details including input shapes

          data:
            data_impl: mmap
            splits_string: "99990,8,2"
            seq_length: 2048
            skip_warmup: True
            num_workers: 2
            dataloader_type: single
            reset_position_ids: False
            reset_attention_mask: False
            eod_mask_loss: False
            index_mapping_dir: null
            data_prefix:
              - .0333
              - ${data_dir}/my-gpt3_00_text_document
              - .0333
              - ${data_dir}/my-gpt3_01_text_document
              - .0333
              - ${data_dir}/my-gpt3_02_text_document
              - .0333
              - ${data_dir}/my-gpt3_03_text_document
              - .0333
              - ${data_dir}/my-gpt3_04_text_document
              - .0333
              - ${data_dir}/my-gpt3_05_text_document
              - .0333
              - ${data_dir}/my-gpt3_06_text_document
              - .0333
              - ${data_dir}/my-gpt3_07_text_document
              - .0333
              - ${data_dir}/my-gpt3_08_text_document
              - .0333
              - ${data_dir}/my-gpt3_09_text_document
              - .0333
              - ${data_dir}/my-gpt3_10_text_document
              - .0333
              - ${data_dir}/my-gpt3_11_text_document
              - .0333
              - ${data_dir}/my-gpt3_12_text_document
              - .0333
              - ${data_dir}/my-gpt3_13_text_document
              - .0333
              - ${data_dir}/my-gpt3_14_text_document
              - .0333
              - ${data_dir}/my-gpt3_15_text_document
              - .0333
              - ${data_dir}/my-gpt3_16_text_document
              - .0333
              - ${data_dir}/my-gpt3_17_text_document
              - .0333
              - ${data_dir}/my-gpt3_18_text_document
              - .0333
              - ${data_dir}/my-gpt3_19_text_document
              - .0333
              - ${data_dir}/my-gpt3_20_text_document
              - .0333
              - ${data_dir}/my-gpt3_21_text_document
              - .0333
              - ${data_dir}/my-gpt3_22_text_document
              - .0333
              - ${data_dir}/my-gpt3_23_text_document
              - .0333
              - ${data_dir}/my-gpt3_24_text_document
              - .0333
              - ${data_dir}/my-gpt3_25_text_document
              - .0333
              - ${data_dir}/my-gpt3_26_text_document
              - .0333
              - ${data_dir}/my-gpt3_27_text_document
              - .0333
              - ${data_dir}/my-gpt3_28_text_document
              - .0334
              - ${data_dir}/my-gpt3_29_text_document
                """
        expected = OmegaConf.create(s)
        assert (
            expected == conf
        ), f"conf/training/gpt3/40b.yaml must be set to {expected} but it currently is {conf}."

    def test_training_config_175b(self):
        conf = OmegaConf.load("conf/training/gpt3/175b.yaml")
        s = """
        run:
          name: gpt3_175b
          results_dir: ${base_results_dir}/${.name}
          time_limit: "35-00:00:00"
          dependency: "singleton"

        trainer:
          num_nodes: 128
          devices: 8
          accelerator: gpu
          precision: bf16
          logger: False
          enable_checkpointing: False
          replace_sampler_ddp: False
          max_epochs: null
          max_steps: 100000
          max_time: "34:23:00:00"
          log_every_n_steps: 10
          val_check_interval: 2000
          limit_val_batches: 20
          limit_test_batches: 20
          accumulate_grad_batches: 1
          gradient_clip_val: 1.0

        exp_manager:
          explicit_log_dir: ${training.run.results_dir}/results
          exp_dir: null
          name: megatron_gpt
          create_wandb_logger: False
          wandb_logger_kwargs:
            project: nemo_gpt3
            name: ${training.run.name}
          resume_if_exists: True
          resume_ignore_no_checkpoint: True
          create_checkpoint_callback: True
          checkpoint_callback_params:
            monitor: val_loss
            save_top_k: 5
            mode: min
            always_save_nemo: False
            save_nemo_on_train_end: False
            filename: 'megatron_gpt--{val_loss:.2f}-{step}-{consumed_samples}'
            model_parallel_size: ${multiply:${training.model.tensor_model_parallel_size}, ${training.model.pipeline_model_parallel_size}}
          log_step_timing: True
          step_timing_kwargs:
            sync_cuda: True
            buffer_size: 5

        model:
          micro_batch_size: 2
          global_batch_size: 2048
          tensor_model_parallel_size: 8
          pipeline_model_parallel_size: 8
          resume_from_checkpoint: null

          # model architecture
          encoder_seq_length: 2048
          max_position_embeddings: 2048
          num_layers: 96
          hidden_size: 12288
          ffn_hidden_size: ${multiply:4, ${.hidden_size}}
          num_attention_heads: 96
          init_method_std: 0.006
          hidden_dropout: 0.1
          kv_channels: null
          apply_query_key_layer_scaling: True
          layernorm_epsilon: 1e-5
          make_vocab_size_divisible_by: 128
          pre_process: True
          post_process: True
          persist_layer_norm: True
          grad_div_ar_fusion: True
          gradient_as_bucket_view: True
          gradient_accumulation_fusion: True
          activations_checkpoint_granularity: selective
          activations_checkpoint_method: null
          activations_checkpoint_num_layers: null
          sequence_parallel: True

          tokenizer:
            library: 'megatron'
            type: 'GPT2BPETokenizer'
            model: null
            delimiter: null
            vocab_file: ${data_dir}/bpe/vocab.json
            merge_file: ${data_dir}/bpe/merges.txt

          # precision
          native_amp_init_scale: 4294967296
          native_amp_growth_interval: 1000
          hysteresis: 2
          fp32_residual_connection: False
          fp16_lm_cross_entropy: False

          # Megatron O2-style half-precision
          megatron_amp_O2: True
          grad_allreduce_chunk_size_mb: 125

          # miscellaneous
          seed: 1234
          use_cpu_initialization: False
          onnx_safe: False
          apex_transformer_log_level: 30

          optim:
            name: distributed_fused_adam
            lr: 0.6e-4
            weight_decay: 0.1 
            betas: 
            - 0.9
            - 0.95
            sched:
              name: CosineAnnealing
              warmup_steps: 115
              constant_steps: 12500
              min_lr: 0.6e-5

          nsys_profile:
            enabled: False
            trace: [nvtx,cuda]
            start_step: 10  # Global batch to start profiling
            end_step: 10 # Global batch to end profiling
            ranks: [0] # Global rank IDs to profile
            gen_shape: False # Generate model and kernel details including input shapes

          data:
            data_impl: mmap
            splits_string: "99990,8,2"
            seq_length: 2048
            skip_warmup: True
            num_workers: 2
            dataloader_type: single
            reset_position_ids: False
            reset_attention_mask: False
            eod_mask_loss: False
            index_mapping_dir: null
            data_prefix:
              - .0333
              - ${data_dir}/my-gpt3_00_text_document
              - .0333
              - ${data_dir}/my-gpt3_01_text_document
              - .0333
              - ${data_dir}/my-gpt3_02_text_document
              - .0333
              - ${data_dir}/my-gpt3_03_text_document
              - .0333
              - ${data_dir}/my-gpt3_04_text_document
              - .0333
              - ${data_dir}/my-gpt3_05_text_document
              - .0333
              - ${data_dir}/my-gpt3_06_text_document
              - .0333
              - ${data_dir}/my-gpt3_07_text_document
              - .0333
              - ${data_dir}/my-gpt3_08_text_document
              - .0333
              - ${data_dir}/my-gpt3_09_text_document
              - .0333
              - ${data_dir}/my-gpt3_10_text_document
              - .0333
              - ${data_dir}/my-gpt3_11_text_document
              - .0333
              - ${data_dir}/my-gpt3_12_text_document
              - .0333
              - ${data_dir}/my-gpt3_13_text_document
              - .0333
              - ${data_dir}/my-gpt3_14_text_document
              - .0333
              - ${data_dir}/my-gpt3_15_text_document
              - .0333
              - ${data_dir}/my-gpt3_16_text_document
              - .0333
              - ${data_dir}/my-gpt3_17_text_document
              - .0333
              - ${data_dir}/my-gpt3_18_text_document
              - .0333
              - ${data_dir}/my-gpt3_19_text_document
              - .0333
              - ${data_dir}/my-gpt3_20_text_document
              - .0333
              - ${data_dir}/my-gpt3_21_text_document
              - .0333
              - ${data_dir}/my-gpt3_22_text_document
              - .0333
              - ${data_dir}/my-gpt3_23_text_document
              - .0333
              - ${data_dir}/my-gpt3_24_text_document
              - .0333
              - ${data_dir}/my-gpt3_25_text_document
              - .0333
              - ${data_dir}/my-gpt3_26_text_document
              - .0333
              - ${data_dir}/my-gpt3_27_text_document
              - .0333
              - ${data_dir}/my-gpt3_28_text_document
              - .0334
              - ${data_dir}/my-gpt3_29_text_document
        """
        expected = OmegaConf.create(s)
        assert (
            expected == conf
        ), f"conf/training/gpt3/175b.yaml must be set to {expected} but it currently is {conf}."