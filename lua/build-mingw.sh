set -e

compiler="$1"
arch="$2"

[[ -z $compiler ]] && echo "compiler prefix must be provided"
[[ -z $arch ]] && echo "arch name must be provided"

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

cd "$script_dir/build/$lua_version"
patch -p1 -i "$script_dir/build.patch"
make \
  PLAT=mingw \
  CC="i686-w64-mingw32-gcc -std=gnu99" \
  AR="i686-w64-mingw32-ar rc" \
  RANLIB="i686-w64-mingw32-ranlib" \
  MYCFLAGS="-Os -fPIE -flto -fuse-linker-plugin -ffat-lto-objects" \
  MYLDFLAGS="-Os -pie -static -flto -fuse-linker-plugin -ffat-lto-objects"

i686-w64-mingw32-strip --strip-unneeded src/lua.exe
cp src/lua.exe ../../lua-windows-$arch
