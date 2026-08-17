#!/usr/bin/env python
import subprocess
import sys


def run_cmd(cmd, check=True):
	print(cmd)
	result = subprocess.run(cmd, shell=True)
	if check and result.returncode != 0:
		print(f"❌ Command failed: {cmd}")
		sys.exit(result.returncode)
	return result.returncode