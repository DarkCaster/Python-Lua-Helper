from hatchling.builders.hooks.plugin.interface import BuildHookInterface

import os
import platform
import subprocess
import sys
import shutil


class CustomBuildHook(BuildHookInterface):
    def run(self, workdir, *cmd_args):
        """Run command in specified working directory and exit on failure"""
        result = subprocess.run(cmd_args, cwd=workdir)
        if result.returncode != 0:
            print(f"Command finished with exit code: {result.returncode}")
            raise subprocess.CalledProcessError(result.returncode, cmd_args)

    def initialize(self, version, build_data):
        build_data["pure_python"] = False
        build_data["infer_tag"] = True
        # Get needed params
        current_os = platform.system().lower()
        arch = platform.machine().lower()
        print(f"OS: {current_os}, arch: {arch}")
        lua_dir = os.path.join(os.path.dirname(__file__), "lua")
        # Build lua for linux
        lua_version = "5.4.8"
        lua_src=f"lua-{lua_version}.tar.gz"
        lua_checksum=f"lua-{lua_version}.sha256"
        if current_os == "linux":
            print("Linux detected - building Lua from source...")
            # Change to lua directory
            os.chdir(lua_dir)
            # Download Lua source if it doesn't exist
            if not os.path.exists(lua_src):
                print(f"downloading {lua_src}")
                self.run(lua_dir, "curl", "-s", "-L", "-o", lua_src, f"https://www.lua.org/ftp/{lua_src}")
            # Check checksum
            print(f"checking {lua_src}")
            self.run(lua_dir, "sha256sum", "-c", lua_checksum)
            # Remove and recreate build directory
            build_dir = os.path.join(lua_dir, "build")
            #use python native methods for removing and creating dirs below
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
            os.makedirs(build_dir, exist_ok=False)
            #extract archive
            shutil.unpack_archive(lua_src, build_dir)
