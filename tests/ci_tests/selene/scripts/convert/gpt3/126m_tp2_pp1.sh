HYDRA_FULL_ERROR=1 python3 main.py \
    +ci_test=True \
    conversion=convert_gpt3 \
    run_data_preparation=False \
    run_training=False \
    run_conversion=True \
    run_finetuning=False \
    run_evaluation=False \
    bignlp_path=${GIT_CLONE_PATH} \
    data_dir=/lustre/fsw/joc/big_nlp/gpt3/prepare_dataset/the_pile/train \
    base_results_dir=${BASE_RESULTS_DIR} \
    "container='${BUILD_IMAGE_NAME_SRUN}'" \
    cluster.partition=${SLURM_PARTITION} \
    cluster.account=${SLURM_ACCOUNT} \
    cluster.gpus_per_task=null \
    cluster.gpus_per_node=null \
    cluster.job_name_prefix="${SLURM_ACCOUNT}-bignlp_ci:" \
    conversion.run.job_name=${RUN_NAME} \
    conversion.run.time_limit="30:00" \
    conversion.run.nodes=1 \
    conversion.run.model_train_name=gpt3_126m_tp2_pp1 \
    conversion.run.train_dir=${BASE_RESULTS_DIR}/train_gpt3_126m_tp2_pp1_1node_100steps \
    conversion.run.results_dir=${BASE_RESULTS_DIR}/${RUN_NAME} \
    conversion.run.output_path=${BASE_RESULTS_DIR}/${RUN_NAME} \
    conversion.model.tensor_model_parallel_size=2 \
    conversion.model.pipeline_model_parallel_size=1