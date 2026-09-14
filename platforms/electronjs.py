
from .base import BasePlatform
from utils.cmd import run_cmd
import os
import shutil


class ElectronJSPlatform(BasePlatform):
    platform = 'electronjs'

    def __init__(self, electronjs_os=None, **kwargs):
        super().__init__(**kwargs)
        self.electronjs_os = electronjs_os

    def package(self):
        app_folder = self.get_app_folder()
        print('Building ElectronJS app...', self.electronjs_os)

        if self.electronjs_os == 'windows':
            print('Windows app building...')
            if os.path.exists('./electron_win'):
                shutil.rmtree('./electron_win')
            run_cmd(f'mkdir ./electron_win')
            run_cmd(f'cp -r ./smart-tv-deployer/dist/electronjs/windows/* ./electron_win/.')
            run_cmd(f'cp -r {app_folder} ./electron_win/resources/app')
        elif self.electronjs_os == "macos":
            print('Make MacOS build...')
            shutil.rmtree('./electron_macos')
            run_cmd(f'mkdir ./electron_macos')
            run_cmd(f'unzip ./smart-tv-deployer/dist/electronjs/macos/Electron.app.zip -d ./electron_macos/.')
            run_cmd(f'cp -r {app_folder} ./electron_macos/Electron.app/Contents/Resources/app')
        else:
            print('Build nodejs')
            os.chdir(app_folder)
            run_cmd('npm install')
            run_cmd('npm start')


    def deploy(self):
        self.package()
