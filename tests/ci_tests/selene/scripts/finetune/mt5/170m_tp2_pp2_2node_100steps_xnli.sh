HYDRA_FULL_ERROR=1 python3 main.py \
    +ci_test=True \
    finetuning=mt5/xnli \
    run_data_preparation=False \
    run_training=False \
    run_conversion=False \
    run_finetuning=True \
    run_evaluation=False \
    bignlp_path=${GIT_CLONE_PATH} \
    data_dir=${BASE_RESULTS_DIR}/data \
    base_results_dir=${BASE_RESULTS_DIR} \
    "container='${BUILD_IMAGE_NAME_SRUN}'" \
    cluster.partition=${SLURM_PARTITION} \
    cluster.account=${SLURM_ACCOUNT} \
    cluster.gpus_per_task=null \
    cluster.gpus_per_node=null \
    cluster.job_name_prefix="${SLURM_ACCOUNT}-bignlp_ci:" \
    finetuning.run.time_limit="40:00" \
    finetuning.run.results_dir=${BASE_RESULTS_DIR}/${RUN_NAME} \
    finetuning.trainer.num_nodes=2 \
    finetuning.trainer.max_steps=100 \
    finetuning.trainer.log_every_n_steps=1 \
    finetuning.trainer.val_check_interval=20 \
    finetuning.model.restore_from_path=${BASE_RESULTS_DIR}/convert_mt5_170m_tp2_pp2/megatron_mt5.nemo \
    finetuning.model.tensor_model_parallel_size=2 \
    finetuning.model.pipeline_model_parallel_size=2 \
    finetuning.model.data.train_ds.micro_batch_size=32 \
    finetuning.model.data.validation_ds.micro_batch_size=32 \
    finetuning.model.data.test_ds.micro_batch_size=32