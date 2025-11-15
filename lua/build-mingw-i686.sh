set -e

script_dir="$(cd "$(dirname "$0")" && pwd)"

cd "$script_dir/build/lua-"*

patch -p1 -i ../../build.patch

make \
  PLAT=mingw \
  CC="i686-w64-mingw32-gcc -std=gnu99" \
  AR="i686-w64-mingw32-ar rc" \
  RANLIB="i686-w64-mingw32-ranlib" \
  MYCFLAGS="-Os -fPIE -flto -fuse-linker-plugin -ffat-lto-objects" \
  MYLDFLAGS="-Os -pie -static -flto -fuse-linker-plugin -ffat-lto-objects -Wl,-z,relro,-z,now"

i686-w64-mingw32-strip --strip-unneeded src/lua.exe
cp src/lua.exe ../../lua-windows-i686.exe
