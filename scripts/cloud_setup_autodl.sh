#!/usr/bin/env bash
set -euo pipefail

echo "== ChartMind-VL AutoDL environment check =="
python --version

echo "== CUDA check =="
python - <<'PY'
import torch

print("torch:", torch.__version__)
print("cuda available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("device:", torch.cuda.get_device_name(0))
    total_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"total memory: {total_gb:.2f} GB")
PY

echo "== Install Python dependencies =="
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "== Suggested cache environment =="
echo 'export HF_HOME="${PWD}/.cache/huggingface"'
echo 'export TRANSFORMERS_CACHE="${PWD}/.cache/huggingface/transformers"'
echo 'export HF_DATASETS_CACHE="${PWD}/.cache/huggingface/datasets"'
