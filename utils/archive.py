import os
import sys
from os import path
from utils.cmd import run_cmd


def zip_dir(input_dir, output_zip):
	if path.exists(input_dir) or input_dir == "*":
		if path.exists(output_zip):
			os.remove(output_zip)

		run_cmd(f'zip -r {output_zip} {input_dir}')
	else:
		print("❌ input directory '{input_dir}' doesn't exist")
		sys.exit(1)
