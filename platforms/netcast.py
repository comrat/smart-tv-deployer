from .base import BasePlatform
from utils.cmd import run_cmd
from utils.archive import zip_dir
import os

class NetCastPlatform(BasePlatform):
    platform = 'netcast'

    def package(self):
        print('Packaging LG NetCast app...')
        output_zip = self.title + '_' + self.version + '.zip'
        platform_dir = f'build.netcast/{"" if not self.app else self.app[1:]}'
        os.chdir(platform_dir)
        zip_dir("*", f'../{output_zip}')
        print(f'⚠️ Now you must add DRM subscription to your app, upload build.netcast here "http://developer.lge.com/apptest/retrieveApptestOSList.dev"\n')

    def deploy(self):
        self.package()
