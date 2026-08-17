from .base import BasePlatform
from utils.cmd import run_cmd
from utils.parser import parse_tizen_config
import os
import re
import subprocess
import sys


class TizenPlatform(BasePlatform):
    platform = 'tizen'

    def package(self):
        print('Packaging Samsung Tizen app...')
        tizen_installed = run_cmd('tizen version')
        if tizen_installed != 0:
            print('❌ "tizen" command not defined. If you\'ve installed tizen-cli already add it\'s "bin" directory to PATH. For example export PATH=\$PATH:/home/username/tizen-studio/tools/ide/bin')
            sys.exit(1)

        active_profile = "default"
        if self.profile is None:
            print('Use current active tizen profile...')
            command = 'tizen security-profiles list | awk \'NR > 2 && $2 == "O" { print $1; exit }\''
            output = subprocess.check_output(command, shell=True, text=True)
            active_profile = output.strip()
        print(f'Use profile: {active_profile}')

        app_folder = "build.tizen/%s" %("" if not self.app else self.app[1:])
        os.chdir('./' + app_folder)

        print('Packaging...')
        tizen_output = subprocess.check_output(f'tizen package -t wgt -s {active_profile}', shell=True, text=True)
        output_file_match = re.search(r'Package File Location:\s*(.+\.wgt)', str(tizen_output))
        if output_file_match is None:
            print("❌ Can't find a wgt file")
            sys.exit(1)
        wgt_file = output_file_match.group(1)
        print(f'✅ Packaged file: {wgt_file}\n')
        return wgt_file

    def deploy(self):
        wgt_file = self.package()
        print(f"Install '{wgt_file}'...")  
        run_cmd(f'tizen install -n %s -t %s' %(wgt_file, self.tv))
        print('✅ Installed\n')
        print(f'Launching...')
        app = parse_tizen_config('config.xml')

        if app is not None:
            app_id = app.get('id')
            print(f"appID: {app_id}")
            print(f"Application ID: {app_id}")
            run_cmd(f'tizen run -p {app_id} -t {self.tv}')
            print('✅ Launching completed\n')
        else:
            print("❌ Failed to launch")