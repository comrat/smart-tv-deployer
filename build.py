#!/usr/bin/env python2.7

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


def deploy_webos(app, version, tv):
	os.system('$WEBOS_CLI_TV/ares-package build.webos')
	if tv is not None:
		os.system('$WEBOS_CLI_TV/ares-install com.%s.app_%s_all.ipk -d %s' %(app, version, tv))
		os.system('$WEBOS_CLI_TV/ares-launch com.%s.app -d %s' %(app, tv))
	else:
		os.system('$WEBOS_CLI_TV/ares-install com.%s.app_%s_all.ipk' %(app, version))
		os.system('$WEBOS_CLI_TV/ares-launch com.%s.app' %(app))


def deploy_tizen(app, version, tv, profile):
	if tv is None:
		print "Please set target device name in --tv or -t flag"
		print "You can see available devices with command 'sdb devices'"
		print "What's sdb? Smart Development Bridge - CLI tool used by Tizen (see https://developer.tizen.org/ko/development/tizen-studio/web-tools/running-and-testing-your-app/sdb?langredirect=1)"
		print "You can add symlink for sdb: sudo ln -s /home/username/tizen-studio/tools/sdb /usr/bin/sdb"
		print "Don't forget to connect to desired device! For example this command connect to TV with 192.168.1.1 IP address: sdb connect 192.168.1.1:26101"
		print "P.S. You need to type your IP address in developer mode on target TV"
		sys.exit(1)

	if profile is None:
		print "Please set profile in --tizen-profile or -tp flag"
		print "To install your app on TV your result .wgt file must be signed by your profile certificate"
		print "First of all you must generate certificate or add existed with tizen certificate manager"
		print "After that provide path to tizen-studio profiles: tizen cli-config -g profiles.path='/home/username/tizen-workspace/.metadata/.plugins/org.tizen.common.sign/profiles.xml'"
		sys.exit(1)

	tizen_installed = os.system("tizen version")
	if tizen_installed == 0:
		os.chdir("./build.tizen")
		result_wgt = app + "_" + version + ".wgt"

		if path.exists(result_wgt):
			print "Remove previous WGT file..."
			os.system('rm %s' %(result_wgt))

		os.system('tizen package -t wgt -s %s' %(profile))
		os.system('tizen install -n %s -t %s' %(result_wgt, tv))
		print "If you see 'Failed to install Tizen application.' log up there don's worry, check 'My App' list on target device your app may be installed (see https://stackoverflow.com/a/42966767 for details)"
	else:
		print "'tizen' command not defined. If you've installed tizen-studio already export it's 'bin' directory to PATH. For example export PATH=\$PATH:/home/username/tizen-studio/tools/ide/bin"


def zip_dir(app, version, platform):
	result_zip = app + "_" + version + ".zip"
	platform_folder = "build." + platform
	if path.exists(platform_folder):
		os.chdir(platform_folder)
		if path.exists(result_zip):
			os.system('rm %s' %(result_zip))
		os.system('zip -r %s *' %(result_zip))
		return True
	else:
		return False


def deploy_orsay(app, version):
	result_zip = app + "_" + version + ".zip"
	if zip_dir(app, version, "orsay"):
		print "Done"
		print "Now you can upload zip file on your server or unzip it on USB and insert it in your samsung smart TV"
	else:
		print "ERROR: Failed to deploy orsay"


def deploy_netcast(app, version):
	result_zip = app + "_" + version + ".zip"
	if zip_dir(app, version, "netcast"):
		print "Done"
		print "Now you must add DRM subscription to your app, upload build.netcast/" + result_zip + " here 'http://developer.lge.com/apptest/retrieveApptestOSList.dev'"
	else:
		print "ERROR: Failed to deploy netcast"


def deploy_android(platform, app, release):
	platform_folder = "./build." + platform
	os.system('cd %s' %(platform_folder))
	os.chdir(platform_folder)

	if path.exists(app):
		print "Clean..."
		os.system('rm -rf %s' %(app))

	print "Run build.py..."
	if release:
		os.system('./build.py --app %s --title %s --release' %(app, app))
	else:
		os.system('./build.py --app %s --title %s' %(app, app))

	print "Install via adb..."
	os.system('adb install -r ./%s/platforms/android/build/outputs/apk/debug/android-debug.apk' %(app))


parser = argparse.ArgumentParser('smart-tv-deploy script')
parser.add_argument('--jobs', '-j', help='run N jobs in parallel', dest='jobs', default=1, nargs='?')
parser.add_argument('--platform', '-p', help='target platform: webos|netcast|tizen|orsay|androidtv', dest='platform')
parser.add_argument('--tizen-profile', '-tp', help='tizen studio profile path', dest='tizen_profile')
parser.add_argument('--tv', '-t', help='TV name', dest='tv')
parser.add_argument('--release', '-r', help='build release apk for android platform', dest='release', default=False)
args = parser.parse_args()

manifest_path = '.manifest'
tizen_profile = args.tizen_profile
platform = args.platform
tv = args.tv
release = args.release
jobs = args.jobs

if platform is None:
	print "Provide platform name: ./smart-tv-deployer.py -p <PLATFORM_NAME>"
	sys.exit(1)

if path.exists(manifest_path):
	title, version = parse_manifest(manifest_path)
	print "Manifest parsed, title:", title, "version", version
	print "Build project..."
	os.system('./qmlcore/build -m -p %s -j %s' %(platform, jobs))

	if platform == "webos":
		print "============== WEBOS DEPLOYMENT =============="
		deploy_webos(title, version, tv)
	elif platform == "tizen":
		print "============== TIZEN DEPLOYMENT =============="
		deploy_tizen(title, version, tv, tizen_profile)
	elif platform == "netcast":
		print "============== NETCAST DEPLOYMENT =============="
		deploy_netcast(title, version)
	elif platform == "orsay":
		print "============== ORSAY DEPLOYMENT =============="
		deploy_orsay(title, version)
	elif platform == "androidtv":
		print "============== ANDROIDTV DEPLOYMENT =============="
		deploy_android("androidtv", title, release)
	elif platform == "android":
		print "============== ANDROID DEPLOYMENT =============="
		deploy_android("android", title, release)
	else:
		print "Unknown platform:", platform
else:
	print ".manifest file not found"
