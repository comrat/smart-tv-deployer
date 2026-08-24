from .base import BasePlatform
from utils.cmd import run_cmd
from utils.parser import parse_webos_appinfo


class AndroidNativePlatform(BasePlatform):
    platform = 'androidnative'

    def package(self):
        print(f"Building...")  
        run_cmd(f'./qmlcore/platform/pure.femto/build-android-native.sh')
        print('✅ Building completed\n')

    def deploy(self):
        self.package()
        print(f"Install '{self.app}'...")  
        run_cmd(f'adb install -r ./build.pure.femto.{self.app}/app/app/build/outputs/apk/debug/app-debug.apk')
        print('✅ Install completed\n')
        # print(f"Launch '{app_id}'...")
        # print('✅ Launching completed\n')