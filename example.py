#!/usr/bin/env python3

import os
import sys
from py_lua_helper import PyLuaHelper

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

print("example.py says: creating PyLuaHelper instance")

# Create PyLuaHelper instance with same parameters as example.bash
cfg = PyLuaHelper(
    lua_config_script=os.path.join(script_dir, "example.cfg.lua"),
    export_vars=["config.sub", "config.paths", "config.empty", "wrong.table", "empty"],
    pre_script=os.path.join(script_dir, "example.pre.lua"),
    post_script=os.path.join(script_dir, "example.post.lua"),
    work_dir=script_dir,
    result_name="cfg",
    export_list_name="cfg_list"
)

print("example.py says: PyLuaHelper complete")
print(f"example.py says: my own cmdline params={sys.argv[1:]}")
print("")
print("example.py says: names of all global variables exported from lua script:")
print(cfg.keys())
print("")

# Check variable availability
print("example.py says: check for config.empty variable availability is ", end="")
try:
    if "config.empty" in cfg:
        print("passed, but should fail !!!")
    else:
        print("failed, as expected")
except Exception:
    print("failed, as expected")

print("example.py says: check for wrong.table variable availability is ", end="")
try:
    if "wrong.table" in cfg:
        print("passed, but should fail !!!")
    else:
        print("failed, as expected")
except Exception:
    print("failed, as expected")

print("example.py says: check for empty variable availability is ", end="")
try:
    if "empty" in cfg:
        print("passed, but should fail !!!")
    else:
        print("failed, as expected")
except Exception:
    print("failed, as expected")

print("example.py says: check for config.value variable availability is ", end="")
try:
    if "config.value" in cfg:
        print("passed, but should fail !!!")
    else:
        print("failed, as expected")
except Exception:
    print("failed, as expected")

print("example.py says: check for config.sub.string variable availability is ", end="")
try:
    if "config.sub.string" in cfg:
        print("passed, as expected")
    else:
        print("failed, but should pass !!!")
except Exception:
    print("failed, but should pass !!!")

print("example.py says: check for config.sub variable availability is ", end="")
try:
    if "config.sub" in cfg:
        print("passed, as expected")
    else:
        print("failed, but should pass !!!")
except Exception:
    print("failed, but should pass !!!")

print(f"example.py says: config.value is not selected for export, so cfg['config.value'] = {cfg.get('config.value', 'NOT_FOUND')}")
print(f"example.py says: config.empty is not found in lua config file, so cfg['config.empty'] = {cfg.get('config.empty', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.paths.tempdir'] = {cfg.get('config.paths.tempdir', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.paths.workdir'] = {cfg.get('config.paths.workdir', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.paths.dynpath'] = {cfg.get('config.paths.dynpath', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.paths.tempdir_raw'] = {cfg.get('config.paths.tempdir_raw', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.paths.workdir_raw'] = {cfg.get('config.paths.workdir_raw', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.paths.dynpath_raw'] = {cfg.get('config.paths.dynpath_raw', 'NOT_FOUND')}")
print(f"example.py says: (should be empty, because it is a container) cfg['config.sub'] = {cfg.get('config.sub', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.lua_v1'] = {cfg.get('config.sub.lua_v1', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.lua_v2'] = {cfg.get('config.sub.lua_v2', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.lua_v3'] = {cfg.get('config.sub.lua_v3', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.lua_num'] = {cfg.get('config.sub.lua_num', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.number1'] = {cfg.get('config.sub.number1', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.string'] = {cfg.get('config.sub.string', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.problematic_string'] = {cfg.get('config.sub.problematic_string', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.non_latin_string'] = {cfg.get('config.sub.non_latin_string', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.sub.message'] = {cfg.get('config.sub.sub.message', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.sub.message2'] = {cfg.get('config.sub.sub.message2', 'NOT_FOUND')}")
print(f"example.py says: cfg['config.sub.multiline_string'] = {cfg.get('config.sub.multiline_string', 'NOT_FOUND')}")

# Test table operations
print(f"example.py says: table start for config.sub: {cfg.get_table_start('config.sub')}")
print(f"example.py says: table end for config.sub: {cfg.get_table_end('config.sub')}")
