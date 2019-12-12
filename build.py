#!/usr/bin/env python

from __future__ import print_function

import sys
import json
import argparse
import os
from os import path

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
	return title, version


def deploy_webos(title, version, tv, debug, app):
	os.system('$WEBOS_CLI_TV/ares-package build.webos%s' %(app))
	if tv is not None:
		os.system('$WEBOS_CLI_TV/ares-install com.%s.app_%s_all.ipk -d %s' %(title, version, tv))
		os.system('$WEBOS_CLI_TV/ares-launch com.%s.app -d %s' %(title, tv))
		if debug is True:
			os.system('$WEBOS_CLI_TV/ares-inspect com.%s.app -d %s' %(title, tv))
	else:
		os.system('$WEBOS_CLI_TV/ares-install com.%s.app_%s_all.ipk' %(title, version))
		os.system('$WEBOS_CLI_TV/ares-launch com.%s.app' %(title))
		if debug is True:
			os.system('$WEBOS_CLI_TV/ares-inspect com.%s.app' %(title))


def deploy_tizen(title, tv, profile, app):
	if tv is None:
		print("Please set target device name in --tv or -t flag")
		print("You can see available devices with command 'sdb devices'")
		print("What's sdb? Smart Development Bridge - CLI tool used by Tizen (see https://developer.tizen.org/ko/development/tizen-studio/web-tools/running-and-testing-your-app/sdb?langredirect=1)")
		print("You can add symlink for sdb: sudo ln -s /home/username/tizen-studio/tools/sdb /usr/bin/sdb")
		print("Don't forget to connect to desired device! For example this command connect to TV with 192.168.1.1 IP address: sdb connect 192.168.1.1:26101")
		print("P.S. You need to type your IP address in developer mode on target TV")
		sys.exit(1)

	if profile is None:
		print("Please set profile in --tizen-profile or -tp flag")
		print("To install your app on TV your result .wgt file must be signed by your profile certificate")
		print("First of all you must generate certificate or add existed with tizen certificate manager mycert.p12 for example")
		print("After that provide path to tizen-studio profiles: tizen cli-config -g profiles.path='/home/username/tizen-workspace/.metadata/.plugins/org.tizen.common.sign/profiles.xml'")
		print("Then you need to add an security profile: tizen security-profiles add -n MyProfile -a /home/username/tizen-studio-data/keystore/author/mycert.p12 -p 1234")
		print("There '1234' is your certificate password")
		print("If you've done all this steps correctly you can now pass in --tizen-profile or -tp flag your profile name: 'MyProfile' in our example")
		sys.exit(1)

	tizen_installed = os.system("tizen version")
	if tizen_installed == 0:
		os.chdir("./build.tizen" + app)
		result_wgt = title + ".wgt"

		if path.exists(result_wgt):
			print("Remove previous WGT file...")
			os.system('rm %s' %(result_wgt))

		os.system('tizen package -t wgt -s %s' %(profile))
		os.system('tizen install -n %s -t %s' %(result_wgt, tv))
		print("If you see 'Failed to install Tizen application.' log up there don's worry, check 'My App' list on target device your app may be installed (see https://stackoverflow.com/a/42966767 for details)")
	else:
		print("'tizen' command not defined. If you've installed tizen-studio already export it's 'bin' directory to PATH. For example export PATH=\$PATH:/home/username/tizen-studio/tools/ide/bin")


def zip_dir(title, version, platform, app, withFolder):
	result_zip = title + "_" + version + ".zip"
	platform_folder = "build." + platform + app
	if path.exists(platform_folder):
		if not withFolder:
			os.chdir(platform_folder)
		if path.exists(result_zip):
			os.system('rm %s' %(result_zip))

		if withFolder:
			os.system('zip -r %s %s' %(result_zip, platform_folder))
		else:
			os.system('zip -r %s *' %(result_zip))
		return True
	else:
		return False


def deploy_orsay(title, version, app):
	result_zip = title + "_" + version + ".zip"
	if zip_dir(title, version, "orsay", app, True):
		print("Done")
		print("Now you can upload zip file on your server or unzip it on USB and insert it in your samsung smart TV")
	else:
		print("ERROR: Failed to deploy orsay")


def deploy_netcast(title, version, app):
	result_zip = title + "_" + version + ".zip"
	if zip_dir(title, version, "netcast", app, False):
		print("Done")
		print("Now you must add DRM subscription to your app, upload build.netcast/" + result_zip + " here 'http://developer.lge.com/apptest/retrieveApptestOSList.dev'")
	else:
		print("ERROR: Failed to deploy netcast")


def deploy_extension(title, version, app):
	result_zip = title + "_" + version + ".zip"
	if zip_dir(title, version, "webextension", app, False):
		print("Done")
		print("Now you can upload upload build.webextension/" + result_zip + " in your chrome or firefox browser")
	else:
		print("ERROR: Failed to deploy web extension")


def deploy_electron(app, electronjs_os):
	platform_folder = "./build.electronjs" + app
	if electronjs_os == "windows":
		print("Make windows build...")
		os.system('rm -rf ./electron_win')
		os.system('mkdir ./electron_win')
		os.system('cp -r ./smart-tv-deployer/dist/electronjs/windows/* ./electron_win/.')
		os.system('cp -r %s ./electron_win/resources/app' %(platform_folder))
	else:
		os.system('cd %s' %(platform_folder))
		os.system('npm install')
		os.system('npm start')


def deploy_android(platform, title, release, app):
	platform_folder = "./build." + platform + app
	os.system('cd %s' %(platform_folder))
	os.chdir(platform_folder)

	if path.exists(title):
		print("Clean...")
		os.system('rm -rf %s' %(title))

	print("Run build.py...")
	app_folder = title if not app else app[1:]
	if release:
		os.system('./build.py --app %s --title %s --release' %(app_folder, app_folder))
	else:
		os.system('./build.py --app %s --title %s' %(app_folder, app_folder))

	print("Install via adb...")
	os.system('adb install -r ./%s/platforms/android/build/outputs/apk/debug/android-debug.apk' %(title))


parser = argparse.ArgumentParser('smart-tv-deploy script')
parser.add_argument('--minify', '-m', action='store_true', help='force minify step', dest='minify', default=False)
parser.add_argument('--jobs', '-j', help='run N jobs in parallel', dest='jobs', default=1, nargs='?')
parser.add_argument('--platform', '-p', help='target platform: webos|netcast|tizen|orsay|androidtv', dest='platform')
parser.add_argument('--os', '-os', help='target electronjs OS', dest='electronjs_os')
parser.add_argument('--tizen-profile', '-tp', help='tizen studio profile path', dest='tizen_profile')
parser.add_argument('--tv', '-t', help='TV name', dest='tv')
parser.add_argument('--release', '-r', help='build release apk for android platform', dest='release', default=False)
parser.add_argument('--debug', '-d', help='start debugging afer building', dest='debug', default=False)
parser.add_argument('--app', '-a', help='target application if there is more than one apps in project', dest='app')
parser.add_argument('--base-url', '-b', help='base URL value if you need to get qml.app.js file remotely', dest='baseurl')
args = parser.parse_args()

manifest_path = '.manifest'
tizen_profile = args.tizen_profile
electronjs_os = args.electronjs_os
platform = args.platform
tv = args.tv
release = args.release
debug = args.debug
jobs = args.jobs
minify = args.minify
app = args.app
baseurl = args.baseurl

if platform is None:
	print("Provide platform name: ./smart-tv-deployer.py -p <PLATFORM_NAME>")
	sys.exit(1)

if path.exists(manifest_path):
	manifest_title, version = parse_manifest(manifest_path)
	title = manifest_title
	if args.app is not None:
		title = args.app
	app_dir = "/" + args.app if args.app is not None else ""
	print("Manifest parsed, title:", title, "version", version)
	print("Build project...")
	os.system('./qmlcore/build %s -p %s -j %s %s %s' %("-m" if minify else "", platform, jobs, "-s baseurl " + baseurl if baseurl is not None else "", app if app is not None else ""))

	if platform == "webos":
		print("============== WEBOS DEPLOYMENT ==============")
		deploy_webos(manifest_title, version, tv, debug, app_dir)
	elif platform == "tizen":
		print("============== TIZEN DEPLOYMENT ==============")
		deploy_tizen(title, tv, tizen_profile, app_dir)
	elif platform == "netcast":
		print("============== NETCAST DEPLOYMENT ==============")
		deploy_netcast(title, version, app_dir)
	elif platform == "orsay":
		print("============== ORSAY DEPLOYMENT ==============")
		deploy_orsay(title, version, app_dir)
	elif platform == "androidtv":
		print("============== ANDROIDTV DEPLOYMENT ==============")
		deploy_android("androidtv", title, release, app_dir)
	elif platform == "android":
		print("============== ANDROID DEPLOYMENT ==============")
		deploy_android("android", title, release, app_dir)
	elif platform == "webextension":
		print("============== WEB EXTENSION DEPLOYMENT ==============")
		deploy_extension(title, version, app_dir)
	elif platform == "electronjs":
		print("============== ELECTRON.JS DEPLOYMENT ==============")
		deploy_electron(app_dir, electronjs_os)
	else:
		print("Unknown platform:", platform)
else:
	print(".manifest file not found")
