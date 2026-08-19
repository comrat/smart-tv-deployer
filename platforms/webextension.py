from .base import BasePlatform
from utils.archive import zip_dir
import os

class WebExtensionPlatform(BasePlatform):
    platform = 'webextension'

    def package(self):
        print('Packaging Web Extension app...')
        output_zip = self.title + '_' + self.version + '.zip'
        platform_dir = f'build.webextension/{"" if not self.app else self.app[1:]}'
        os.rename(platform_dir, self.title)
        zip_dir(self.title, output_zip)
        os.rename(self.title, platform_dir)
        print(f'Now you can upload upload {output_zip} in your chrome or firefox browser')

    def deploy(self):
        self.package()
