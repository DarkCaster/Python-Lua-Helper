set -e

script_dir="$(cd "$(dirname "$0")" && pwd)"

arch="$1"
[[ -z $arch ]] && arch=$(arch)

cd "$script_dir/build/lua-"*

patch -p1 -i ../../build.patch

make \
  PLAT=linux \
  MYCFLAGS="-fPIC" \
  MYLDFLAGS="-static -fPIC"

strip --strip-unneeded src/lua
cp src/lua ../../lua-linux-$arch
