from hatchling.builders.hooks.plugin.interface import BuildHookInterface

import os
import platform
import subprocess
import shutil
import hashlib


class CustomBuildHook(BuildHookInterface):
    def run(self, workdir, *cmd_args):
        """Run command in specified working directory and exit on failure"""
        result = subprocess.run(cmd_args, cwd=workdir)
        if result.returncode != 0:
            print(f"Command finished with exit code: {result.returncode}")
            raise subprocess.CalledProcessError(result.returncode, cmd_args)

    def check_sha256(self, file_path, checksum_file):
        """Check file checksum from sha256 checksum file"""
        # Read the expected checksum from the checksum file
        with open(checksum_file, "r") as f:
            checksum_line = f.read().strip()
        # Parse the checksum and filename from the line
        # Format: "checksum *filename" or "checksum filename"
        parts = checksum_line.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid checksum file format: {checksum_line}")
        expected_checksum = parts[0]
        expected_filename = parts[1].lstrip("*")  # Remove leading '*' if present
        # Verify the filename matches
        actual_filename = os.path.basename(file_path)
        if expected_filename != actual_filename:
            raise ValueError(
                f"Filename mismatch: expected '{expected_filename}', got '{actual_filename}'"
            )
        # Calculate the actual checksum
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        actual_checksum = sha256_hash.hexdigest()
        # Compare checksums
        if actual_checksum != expected_checksum:
            raise ValueError(
                f"Checksum mismatch for {file_path}: expected {expected_checksum}, got {actual_checksum}"
            )
        print(f"Checksum verified: {file_path}")
        return True

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
        lua_src = f"lua-{lua_version}.tar.gz"
        lua_checksum = f"lua-{lua_version}.sha256"
        if current_os == "linux":
            print("Linux detected - building Lua from source...")
            # Change to lua directory
            os.chdir(lua_dir)
            # Download Lua source if it doesn't exist
            if not os.path.exists(lua_src):
                print(f"Downloading {lua_src}")
                self.run(
                    lua_dir,
                    "curl",
                    "-s",
                    "-L",
                    "-o",
                    lua_src,
                    f"https://www.lua.org/ftp/{lua_src}",
                )
            # Check checksum
            print(f"Checking {lua_src}")
            self.check_sha256(lua_src, lua_checksum)
            # Remove and recreate build directory
            build_dir = os.path.join(lua_dir, "build")
            # Use python native methods for removing and creating dirs below
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
            os.makedirs(build_dir, exist_ok=False)
            # Extract archive
            shutil.unpack_archive(lua_src, build_dir)
            # Change to extracted Lua source directory
            lua_build_dir = os.path.join(build_dir, f"lua-{lua_version}")
            os.chdir(lua_build_dir)
            # Apply patch
            print("Applying build patch...")
            patch_file = os.path.join(lua_dir, "build.patch")
            self.run(lua_build_dir, "patch", "-p1", "-i", patch_file)
            # Build Lua with optimization flags
            print("Building Lua...")
            self.run(
                lua_build_dir,
                "make",
                "PLAT=linux",
                "MYCFLAGS=-Os -fPIE -flto -fuse-linker-plugin -ffat-lto-objects",
                "MYLDFLAGS=-Os -pie -static -flto -fuse-linker-plugin -ffat-lto-objects -Wl,-z,relro,-z,now",
            )
            # Strip binary
            print("Stripping Lua binary...")
            lua_binary = os.path.join(lua_build_dir, "src", "lua")
            self.run(lua_build_dir, "strip", "--strip-unneeded", lua_binary)
            # Copy result
            print("Copying Lua binary...")
            dest_lua = os.path.join(lua_dir, "lua")
            shutil.copy2(lua_binary, dest_lua)
        elif current_os == "windows":
            print(
                f"Windows detected (architecture: {arch}) - selecting pre-built Lua binary..."
            )
            try:
                if arch in ["x86_64", "amd64"]:
                    source_binary = os.path.join(lua_dir, "lua-windows-x86_64")
                    target_binary = os.path.join(lua_dir, "lua.exe")
                elif arch in ["i686", "x86"]:
                    source_binary = os.path.join(lua_dir, "lua-windows-i686")
                    target_binary = os.path.join(lua_dir, "lua.exe")
                else:
                    print(
                        f"Warning: Unsupported Windows architecture '{arch}' - no Lua binary available"
                    )
                    return
                if os.path.exists(source_binary):
                    shutil.copy2(source_binary, target_binary)
                    print(f"Copied {source_binary} to {target_binary}")
                else:
                    print(f"Warning: Source binary not found at {source_binary}")
            except Exception as e:
                print(f"Error copying Lua binary: {e}")
        else:
            print(
                f"Warning: Unsupported operating system '{current_os}' - no Lua binary available"
            )
