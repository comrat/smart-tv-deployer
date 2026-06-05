#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import os
import shutil
import sys
from os import path
import subprocess
import re
import xml.etree.ElementTree as ET


def run_cmd(cmd, check=True):
	print(cmd)
	result = subprocess.run(cmd, shell=True)
	if check and result.returncode != 0:
		print(f"❌ Command failed: {cmd}")
		sys.exit(result.returncode)
	return result.returncode


def __pair_hook(pairs):
	obj = {}
	for k, v in pairs:
		if '.' in k:
			path = k.split('.')
			current = obj
			for p in path[:-1]:
				current = current.setdefault(p, {})
			current[path[-1]] = v
		obj[k] = v
	return obj


def parse_webos_appinfo(appinfo):
	data = None
	with open(appinfo) as f:
		data = json.load(f, object_pairs_hook = __pair_hook)
	if data is None:
		data = {}

	app_id = data.get('id', '')

	return app_id


def parse_manifest(manifest):
	data = None
	with open(manifest) as f:
		data = json.load(f, object_pairs_hook = __pair_hook)
	if data is None:
		data = {}

	title = 'app'
	version = '1.0.0'
	properties = data.get('properties', None)
	if properties:
		title = properties.get('title', 'app')
		version = properties.get('version', '1.0.0')
		android_build = properties.get('androidBuild', {})

	return title, version, android_build


def deploy_webos(title, version, tv, debug, build_only, app):
	print('Packaging...')
	app_folder = "build.webos/%s" %("" if not app else app[1:])
	os.system('$WEBOS_CLI_TV/ares-package %s -o %s' %(app_folder, app_folder))
	app_id = parse_webos_appinfo(app_folder + '/appinfo.json')
	print("Webos App ID:", app_id)
	app_file = '%s_%s_all.ipk' %(app_id, version)
	app_file_path = app_folder + app_file
	if build_only:
		print('IPK file bundled')
	else:
		print('Installing...')
		os.system('$WEBOS_CLI_TV/ares-install %s %s' %(app_file_path, ("-d %s" %tv) if tv else ''))
		os.system('$WEBOS_CLI_TV/ares-launch %s %s' %(app_id, ("-d %s" %tv) if tv else ''))
		if debug is True:
			os.system('$WEBOS_CLI_TV/ares-inspect %s %s' %(app_id, ("-d %s" %tv) if tv else ''))


def deploy_tizen(title, tv, profile, build_only, app):
	if tv is None:
		print('❌ Set target device name in --tv or -t flag')
		print('You can see available devices with command "sdb devices"')
		print('Don\'t forget to connect to desired device! For example this command connect to TV with 192.168.1.1 IP address: sdb connect 192.168.1.1:26101')
		sys.exit(1)

	tizen_installed = run_cmd('tizen version')
	if tizen_installed != 0:
		print('❌ "tizen" command not defined. If you\'ve installed tizen-cli already add it\'s "bin" directory to PATH. For example export PATH=\$PATH:/home/username/tizen-studio/tools/ide/bin')
		sys.exit(1)

	active_profile = "default"
	if profile is None:
		print('Use current active tizen profile...')
		command = 'tizen security-profiles list | awk \'NR > 2 && $2 == "O" { print $1; exit }\''
		output = subprocess.check_output(command, shell=True, text=True)
		active_profile = output.strip()
	print('Current active profile:', active_profile)

	app_folder = "build.tizen/%s" %("" if not app else app[1:])
	os.chdir('./' + app_folder)

	print('Packaging...')
	tizen_output = subprocess.check_output('tizen package -t wgt -s %s' %(active_profile), shell=True, text=True)
	output_file_match = re.search(r'Package File Location:\s*(.+\.wgt)', str(tizen_output))
	if output_file_match is None:
		print("❌ Can't find a wgt file")
		sys.exit(1)
	wgt_file = output_file_match.group(1)
	print('✅ Packaged file:', wgt_file)

	print('Installing...')
	run_cmd('tizen install -n %s -t %s' %(wgt_file, tv))
	print('✅ Installed')


	print('Launching...')
	tree = ET.parse('config.xml')
	root = tree.getroot()
	widget_id = root.get('id')
	ns = {'tizen': 'http://tizen.org/ns/widgets'}
	app = root.find('tizen:application', ns)
	print(f"Widget appID: {app}")

	if app is not None:
		app_id = app.get('id')
		package = app.get('package')
		print(f"Application ID: {app_id}")
		run_cmd(f'tizen run -p {app_id} -t {tv}')
		print('✅ Launched')
	else:
		print("❌ Failed to launch")


def zip_dir(title, version, platform, app, withFolder):
	result_zip = title + '_' + version + '.zip'
	platform_folder = 'build.' + platform + app
	if path.exists(platform_folder):
		if not withFolder:
			os.chdir(platform_folder)
		if path.exists(result_zip):
			os.remove(result_zip)

		if withFolder:
			os.system('zip -r %s %s' %(result_zip, platform_folder))
		else:
			os.system('zip -r %s *' %(result_zip))
		return True
	else:
		return False


def deploy_orsay(title, version, app):
	result_zip = title + '_' + version + '.zip'
	if zip_dir(title, version, 'orsay', app, True):
		print('Done')
		print('Now you can upload zip file on your server or unzip it on USB and insert it in your samsung smart TV')
	else:
		print('ERROR: Failed to deploy orsay')


def deploy_netcast(title, version, app):
	result_zip = title + '_' + version + '.zip'
	if zip_dir(title, version, 'netcast', app, False):
		print('Done')
		print('Now you must add DRM subscription to your app, upload build.netcast/' + result_zip + ' here "http://developer.lge.com/apptest/retrieveApptestOSList.dev"')
	else:
		print('ERROR: Failed to deploy netcast')


def deploy_extension(title, version, app):
	result_zip = title + '_' + version + '.zip'
	if zip_dir(title, version, 'webextension', app, False):
		print('Done')
		print('Now you can upload upload build.webextension/' + result_zip + ' in your chrome or firefox browser')
	else:
		print('ERROR: Failed to deploy web extension')


def deploy_electron(app, electronjs_os):
	platform_folder = './build.electronjs' + app
	if electronjs_os == 'windows':
		print('Make windows build...')
		shutil.rmtree('./electron_win')
		os.system('mkdir ./electron_win')
		os.system('cp -r ./smart-tv-deployer/dist/electronjs/windows/* ./electron_win/.')
		os.system('cp -r %s ./electron_win/resources/app' %(platform_folder))
	if electronjs_os == "macos":
		print('Make MacOS build...')
		shutil.rmtree('./electron_macos')
		os.system('mkdir ./electron_macos')
		os.system('unzip ./smart-tv-deployer/dist/electronjs/macos/Electron.app.zip -d ./electron_macos/.')
		os.system('cp -r %s ./electron_macos/Electron.app/Contents/Resources/app' %(platform_folder))
	else:
		os.chdir(platform_folder)
		os.system('npm install')
		os.system('npm start')


def deploy_android(platform, title, release, build_only, app, android_build):
	platform_folder = './build.' + platform + app
	os.system('cd %s' %(platform_folder))
	os.chdir(platform_folder)

	if path.exists(title):
		print('Clean...')
		shutil.rmtree(title)

	print('Run build.py...')
	app_folder = title if not app else app[1:]
	release_arg = '--release' if release else ''
	os.system('./build.py --app %s --title %s %s' %(app_folder, app_folder, release_arg))
	build_type = 'release' if release else 'debug'
	output_path = '%s/platforms/android/app/build/outputs/' %title
	apk_file_path = '%s/apk/%s/app-%s.apk' %(output_path, build_type, build_type)
	aab_file_path = '%s/bundle/%s/app-%s.aab' %(output_path, build_type, build_type)
	if path.exists(apk_file_path):
		if build_only:
			print('Building apk file...')
			os.system('cp %s ./%s.apk' %(apk_file_path, app_folder))
		else:
			print('Install via adb...')
			os.system('adb install -r %s' %apk_file_path)
	elif path.exists(aab_file_path):
		if build_only:
			print('Building aab file...')
			os.system('cp %s ./%s.aab' %(aab_file_path, app_folder))
		else:
			print('Install via adb...')
			print('Installing aab files via adb is not supported yet. Please use apk file or upload aab to Google Play Console.')
	else:
		print('No .(apk|aab) file at path %s' %output_path)

def deploy_android_native(title, release, app):
	os.system('./qmlcore/platform/pure.femto/build-android-native.sh')
	os.system('adb install ./build.pure.femto.%s/app/app/build/outputs/apk/debug/app-debug.apk' %(app))


def deploy_ios(title, app):
	platform_folder = './build.ios' + app
	os.chdir(platform_folder)

	if path.exists(title):
		print('Clean...')
		shutil.rmtree(title)

	print('Run build.py...')
	app_folder = title if not app else app[1:]
	os.system('../qmlcore/platform/ios/build.py --app %s --title %s' %(app_folder, app_folder))


parser = argparse.ArgumentParser('smart-tv-deploy script')
parser.add_argument('--minify', '-m', help='force minify step', action='store_true', dest='minify')
parser.add_argument('--jobs', '-j', help='run N jobs in parallel', dest='jobs', default=1, nargs='?')
parser.add_argument('--platform', '-p', help='target platform: webos|netcast|tizen|orsay|androidtv', dest='platform')
parser.add_argument('--os', '-os', help='target electronjs OS', dest='electronjs_os')
parser.add_argument('--tizen-profile', '-tp', help='tizen studio profile path', dest='tizen_profile')
parser.add_argument('--tv', '-t', help='TV name', dest='tv')
parser.add_argument('--release', '-r', help='generate release code (no logs)', action='store_true', dest='release')
parser.add_argument('--build-only', '-B', help='generate apk file (without deploy)', default=False, action='store_true', dest='buildonly')
parser.add_argument('--debug', '-d', help='start debugging after building', dest='debug', default=False)
parser.add_argument('--app', '-a', help='target application if there is more than one apps in project', dest='app')
parser.add_argument('--base-url', '-b', help='base URL value if you need to get qml.app.js file remotely', dest='baseurl')
parser.add_argument('--width', '-w', help='app width (1280 by default)', dest='width')
parser.add_argument('--height', '-he', help='app height (720 by default)', dest='height')
parser.add_argument('--set-property', '-sp', dest='properties', action='append', help = 'sets manifest property name value', nargs=2)
args = parser.parse_args()

manifest_path = '.manifest'
tizen_profile = args.tizen_profile
electronjs_os = args.electronjs_os
platform = args.platform
tv = args.tv
release = args.release
build_only = args.buildonly
debug = args.debug
jobs = args.jobs
minify = args.minify
app = args.app
baseurl = args.baseurl
width = args.width
height = args.height

if platform is None:
	print('Provide platform name: ./smart-tv-deployer.py -p <PLATFORM_NAME>')
	sys.exit(1)

if path.exists(manifest_path):
	manifest_title, version, android_build = parse_manifest(manifest_path)

	title = manifest_title
	if args.app is not None:
		title = args.app
	app_dir = '/' + args.app if args.app is not None else ''
	print('Manifest parsed, title:', title, 'version', version)
	print('Build project...')
	params = '-s baseurl ' + baseurl if baseurl is not None else ''

	if args.properties:
		for name, value in args.properties:
			params += ' -s ' + name + ' ' + value

	if width and height:
		params = ' -s resolutionWidth ' + width + ' -s resolutionHeight ' + height

	if release:
		params += ' -r '

	os.system('./qmlcore/build %s -p %s -j %s %s %s' %('-m' if minify else '', platform, jobs, params, app if app is not None else ''))
	print('============== ' + platform.upper() + ' DEPLOYMENT ==============')

	if platform == 'webos':
		deploy_webos(title, version, tv, debug, build_only, app_dir)
	elif platform == 'tizen':
		deploy_tizen(title, tv, tizen_profile, build_only, app_dir)
	elif platform == 'netcast':
		deploy_netcast(title, version, app_dir)
	elif platform == 'orsay':
		deploy_orsay(title, version, app_dir)
	elif platform == 'androidtv':
		deploy_android('androidtv', title, release, build_only, app_dir, android_build)
	elif platform == 'android':
		deploy_android('android', title, release, build_only, app_dir, android_build)
	elif platform == 'androidnative':
		deploy_android_native(title, release, app_dir)
	elif platform == 'ios':
		deploy_ios(title, app_dir)
	elif platform == 'webextension':
		deploy_extension(title, version, app_dir)
	elif platform == 'electronjs':
		deploy_electron(app_dir, electronjs_os)
	elif platform == 'vidaa':
		print('VIDAA build is in build.vidaa%s:' %app_dir)
	else:
		print('Unknown platform:', platform)
else:
	print('.manifest file not found')
