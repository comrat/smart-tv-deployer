#!/usr/bin/env python

from __future__ import print_function

import sys
from os import path

from utils.cmd import run_cmd
from utils.parser import parse_manifest
from platforms.netcast import NetCastPlatform
from platforms.tizen import TizenPlatform
from platforms.webos import WebOSPlatform
from platforms.orsay import OrsayPlatform
# from platforms.android import AndroidDeployer, AndroidNativeDeployer
# from platforms.ios import iOSDeployer
# from platforms.electronjs import ElectronJSDeployer
# from platforms.webextension import WebExtensionDeployer


class SmartTVDeployer:    
    PLATFORM_DEPLOYERS = {
        'webos': WebOSPlatform,
        'tizen': TizenPlatform,
        'netcast': NetCastPlatform,
        'orsay': OrsayPlatform,
        # 'webextension': WebExtensionPlatform,
        # 'android': AndroidDeployer,
        # 'androidtv': AndroidDeployer,
        # 'androidnative': AndroidNativeDeployer,
        # 'ios': iOSDeployer,
        # 'electronjs': ElectronJSDeployer,
        # 'vidaa': None,  # Специальный случай
    }

    def __init__(self, args):
        self.args = args
        self.manifest_path = '.manifest'
        self.title = None
        self.version = None
        self.android_build = None

    def load_manifest(self):
        if not path.exists(self.manifest_path):
            print('❌ .manifest file not found')
            sys.exit(1)

        print(f'Manifest parsing...')
        self.title, self.version, self.android_build = parse_manifest(self.manifest_path)

        if self.args.app:
            self.title = self.args.app

        print(f'Title: {self.title}')
        print(f'Version: {self.version}')
        print(f'✅ Manifest parsed\n')

    def build_project(self):
        print('Build project...')
        params = self._build_params()
        minify_arg = '-m' if self.args.minify else ''
        app_arg = self.args.app if self.args.app else ''

        cmd = (
            f'./qmlcore/build {minify_arg} '
            f'-p {self.args.platform} '
            f'-j {self.args.jobs} '
            f'{params} '
            f'{app_arg}'
        )

        run_cmd(cmd)
        print('✅ Build completed\n')

    def deploy(self):
        platform = self.args.platform

        print(f'Deploy {platform.lower()} project...')

        if platform == 'vidaa':
            app_dir = f'/{self.args.app}' if self.args.app else ''
            print(f'✅ VIDAA build is in build.vidaa{app_dir}:')
            return

        if platform not in self.PLATFORM_DEPLOYERS:
            print(f'❌ Unknown platform: {platform}')
            sys.exit(1)

        deployer_class = self.PLATFORM_DEPLOYERS.get(platform)
        if deployer_class is None:
            print(f'❌ Platform {platform} not yet implemented')
            sys.exit(1)

        deployer = self._create_deployer(deployer_class, platform)

        try:
            deployer.deploy()
            print(f'✅ {platform} deployment completed successfully')
        except Exception as e:
            print(f'❌ {platform} deployment failed: {str(e)}')
            sys.exit(1)

    def run(self):
        try:
            self.load_manifest()
            self.build_project()
            self.deploy()
        except KeyboardInterrupt:
            print('\n\n⚠️ Deployment interrupted by user')
            sys.exit(1)
        except Exception as e:
            print(f'\n❌ Error: {str(e)}')
            sys.exit(1)

    def _create_deployer(self, deployer_class, platform):
        common_kwargs = {
            'title': self.title,
            'version': self.version,
            'app': self.args.app,
        }
        if platform == 'webos':
            return deployer_class(
                tv=self.args.tv,
                debug=self.args.debug,
                # build_only=self.args.buildonly,
                **common_kwargs
            )
        elif platform == 'tizen':
            return deployer_class(
                tv=self.args.tv,
                profile=self.args.tizen_profile,
                # build_only=self.args.buildonly,
                **common_kwargs
            )
        elif platform in ['android', 'androidtv']:
            return deployer_class(
                platform=platform,
                release=self.args.release,
                # build_only=self.args.buildonly,
                android_build=self.android_build,
                **common_kwargs
            )
        elif platform == 'androidnative':
            return deployer_class(
                release=self.args.release,
                **common_kwargs
            )
        elif platform == 'ios':
            return deployer_class(**common_kwargs)
        elif platform == 'electronjs':
            return deployer_class(
                electronjs_os=self.args.electronjs_os,
                **common_kwargs
            )
        elif platform in ['netcast', 'orsay', 'webextension']:
            return deployer_class(**common_kwargs)
        else:
            raise ValueError(f'Unknown platform: {platform}')

    def _build_params(self):
        params = []

        if self.args.baseurl:
            params.append(f'-s baseurl {self.args.baseurl}')

        if self.args.properties:
            for name, value in self.args.properties:
                params.append(f'-s {name} {value}')

        if self.args.width and self.args.height:
            params.append(f'-s resolutionWidth {self.args.width}')
            params.append(f'-s resolutionHeight {self.args.height}')

        if self.args.release:
            params.append('-r')

        return ' '.join(params)