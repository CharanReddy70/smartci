#!/usr/bin/env bash
set -euo pipefail
log_path=${1:?Provide the pytest log path}
work_dir=${MODEL_DIR:-${TMPDIR:-/tmp}/smartci-log-model}
mkdir -p "$work_dir"
python -m venv "$work_dir/venv"
"$work_dir/venv/bin/pip" install --quiet --only-binary=:all: \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu llama-cpp-python==0.3.18 >&2
model="$work_dir/model.gguf"
digest=1adf0b11065d8ad2e8123ea110d1ec956dab4ab038eab665614adba04b6c3370
if ! printf '%s  %s\n' "$digest" "$model" | sha256sum --check --status 2>/dev/null; then
  temp_model=$(mktemp "$work_dir/model.XXXXXX")
  trap 'rm -f "$temp_model"' EXIT
  curl --fail --location --silent --show-error --retry 2 \
    'https://huggingface.co/bartowski/Qwen2.5-1.5B-Instruct-GGUF/resolve/9eadc66189c7641e1ddd226b8267a9119b2ce2d4/Qwen2.5-1.5B-Instruct-Q4_K_M.gguf' \
    -o "$temp_model"
  printf '%s  %s\n' "$digest" "$temp_model" | sha256sum --check --status
  mv "$temp_model" "$model"
fi
"$work_dir/venv/bin/python" scripts/summarize_log.py --model "$model" "$log_path"
