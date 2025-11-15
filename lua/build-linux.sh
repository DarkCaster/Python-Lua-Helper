set -e

script_dir="$(cd "$(dirname "$0")" && pwd)"
arch=$(arch)

cd "$script_dir/build/lua-"*

patch -p1 -i ../../build.patch

#  CC="x86_64-linux-gnu-gcc -std=gnu99" \
#  AR="x86_64-linux-gnu-ar rcu" \
#  RANLIB="x86_64-linux-gnu-ranlib" \

make \
  PLAT=linux \
  MYCFLAGS="-fPIC" \
  MYLDFLAGS="-static -fPIC"

x86_64-linux-gnu-strip --strip-unneeded src/lua
cp src/lua ../../lua-linux-$arch
