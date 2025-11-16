#!/bin/bash
set -e
script_dir="$( cd "$( dirname "$0" )" && pwd )"

if [[ ! -d "$script_dir/venv" ]]; then
  virtualenv "$script_dir/venv"
  "$script_dir/venv/bin/pip" --require-virtualenv install --upgrade pip build
fi

"$script_dir/venv/bin/python" "$@"
