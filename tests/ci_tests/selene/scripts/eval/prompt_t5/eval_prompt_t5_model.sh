params=()
if [[ "$TEST_TASK" = "squad_real" ]]; then
  params+=(container_mounts=[/lustre/fsw/joc/big_nlp/bignlp_ci_resources:/lustre/fsw/joc/big_nlp/bignlp_ci_resources,/lustre/fsw/joc/yuya/bignlp/bignlp-scripts_gpt3/data:/lustre/fsw/joc/yuya/bignlp/bignlp-scripts_gpt3/data])
fi

HYDRA_FULL_ERROR=1 BIGNLP_CI=1 python3 main.py \
    evaluation=${RUN_MODEL}/squad \
    stages=["evaluation"] \
    bignlp_path=${GIT_CLONE_PATH} \
    data_dir=${BASE_RESULTS_DIR}/data \
    base_results_dir=${BASE_RESULTS_DIR} \
    "container='${BUILD_IMAGE_NAME_SRUN}'" \
    cluster.partition=${SLURM_PARTITION} \
    cluster.account=${SLURM_ACCOUNT} \
    cluster.gpus_per_task=null \
    cluster.gpus_per_node=null \
    cluster.job_name_prefix="${SLURM_ACCOUNT}-bignlp_ci:" \
    evaluation.run.name=${RUN_NAME} \
    evaluation.run.time_limit=${TIME_LIMIT} \
    evaluation.run.model_train_name=${RUN_NAME} \
    evaluation.run.results_dir=${BASE_RESULTS_DIR}/${RUN_NAME} \
    evaluation.virtual_prompt_model_file=${BASE_RESULTS_DIR}/${PROMPT_LEARN_MODEL_DIR}/results/megatron_t5_prompt.nemo \
    evaluation.pretrained_language_model_file=${BASE_RESULTS_DIR}/${CONVERT_MODEL_DIR}/results/megatron_t5.nemo \
    evaluation.tensor_model_parallel_size=${TP_SIZE} \
    evaluation.pipeline_model_parallel_size=${PP_SIZE} \
    "${params[@]}" ${ADDITIONAL_PARAMS}