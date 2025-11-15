set -e

script_dir="$(cd "$(dirname "$0")" && pwd)"

pushd "$script_dir/build/lua-"*

patch -p1 -i ../../build.patch

make \
  PLAT=mingw \
  CC="x86_64-w64-mingw32-gcc -std=gnu99" \
  AR="x86_64-w64-mingw32-ar rc" \
  RANLIB="x86_64-w64-mingw32-ranlib"

x86_64-w64-mingw32-strip --strip-unneeded src/lua.exe
cp src/lua.exe ../../lua-windows-x86_64.exe

popd
