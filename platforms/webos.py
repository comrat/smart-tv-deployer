from .base import BasePlatform
from utils.cmd import run_cmd
from utils.parser import parse_webos_appinfo


class WebOSPlatform(BasePlatform):
    platform = 'webos'

    def package(self):
        print('Packaging LG WebOS app...')
        app_folder = self.get_app_folder()
        run_cmd(f'$WEBOS_CLI_TV/ares-package {app_folder} -o {app_folder}')
        print('✅ Packaging completed\n') # TODO: display result ipk file location
        return self._get_app_id_and_file(app_folder)

    def deploy(self):
        app_id, app_file_path = self.package()
        print(f"Install '{app_id}'...")  
        self._install(app_file_path, app_id)
        print('✅ Install completed\n')
        print(f"Launch '{app_id}'...")
        self._launch(app_id)
        print('✅ Launching completed\n')

    def _get_app_id_and_file(self, app_folder):
        app_id = parse_webos_appinfo(app_folder + '/appinfo.json')
        app_file = f'{app_id}_{self.version}_all.ipk'
        return app_id, f'{app_folder}/{app_file}'

    def _install(self, app_file_path, app_id):
        device = f'-d {self.tv}' if self.tv else ''
        run_cmd(f'$WEBOS_CLI_TV/ares-install {app_file_path} {device}')

    def _launch(self, app_id):
        device = f'-d {self.tv}' if self.tv else ''
        run_cmd(f'$WEBOS_CLI_TV/ares-launch {app_id} {device}')
        # if self.debug: TODO: add debug mode
