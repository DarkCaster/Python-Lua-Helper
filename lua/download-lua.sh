#!/bin/bash

set -e

script_dir="$(cd "$(dirname "$0")" && pwd)"
lua_version="5.4.8"
lua_src="lua-$lua_version.tar.gz"
lua_checksum="lua-$lua_version.sha256"

cd "$script_dir"

[[ ! -e "$lua_src" ]] && echo "downloading $lua_src" && curl -s -L -o "$script_dir/$lua_src" "https://www.lua.org/ftp/$lua_src"
echo "checking $lua_src" && sha256sum -c "$lua_checksum"

rm -rf "$script_dir/build"
mkdir -p "$script_dir/build"

cd "$script_dir/build"
tar xf "$script_dir/$lua_src"
