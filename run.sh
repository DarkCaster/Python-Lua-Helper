#!/bin/bash
set -e

script_dir="$(cd "$(dirname "$0")" && pwd)"
venv_dir="$script_dir/venv"

if [[ ! -d "$venv_dir" ]]; then
  python -m venv "$venv_dir"
  "$venv_dir/bin/python" -m pip --require-virtualenv install --upgrade pip build
fi

"$venv_dir/bin/python" "$@"
