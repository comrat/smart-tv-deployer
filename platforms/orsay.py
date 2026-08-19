from .base import BasePlatform
from utils.archive import zip_dir
import os


class OrsayPlatform(BasePlatform):
    platform = 'orsay'

    def package(self):
        print('Packaging Samsung Orsay app...')
        output_zip = self.title + '_' + self.version + '.zip'
        platform_dir = f'build.orsay/{"" if not self.app else self.app[1:]}'
        os.rename(platform_dir, self.title)
        zip_dir(self.title, output_zip)
        os.rename(self.title, platform_dir)
        print('Now you can upload zip file on your app server or unzip it on the USB and plug in into your samsung Smart TV')

    def deploy(self):
        self.package()
