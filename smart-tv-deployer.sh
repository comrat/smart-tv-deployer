#! /bin/bash

function deploy_webos() {
	cd $WEBOS_CLI_TV
	./ares-package $1
	echo $1
	if [ "$#" -ge 1 ]; then
		./ares-install com.$1.app_1.0.0_all.ipk -d $2
		./ares-launch com.$1.app -d $2
	else
		./ares-install com.$1.app_1.0.0_all.ipk
		./ares-launch com.$1.app
	fi
}

function cd_and_zip_dir() {
	DIR=$1
	PLATFORM=$2
	if [ -d "$DIR" ]; then
		cd $DIR
		if [ -e "$PLATFORM.zip" ]; then
			rm $PLATFORM.zip
		fi
		zip -r $PLATFORM.zip *
		retval=0
	else
		retval=1
	fi
	return $retval
}

./qmlcore/build -p $2 -m

if [ "$2" == "webos" ]; then
	if [ -z ${WEBOS_CLI_TV+x} ]; then
		echo "WEBOS_CLI_TV is unset. Probably webOS SDK wasn't installed"
		exit 1
	fi

	echo "============== WEBOS DEPLOYMENT =============="
	echo "Update deploy directory..."
	rm -rf "$WEBOS_CLI_TV/$1"
	cp -r ./build.webos "$WEBOS_CLI_TV/$1"
	echo "Build and run package..."

	if [ "$#" -ge 1 ]; then
		deploy_webos $1 $3
	else
		deploy_webos $1
	fi
fi

if [ "$2" == "tizen" ]; then
	if [ "$#" -le 1 ]; then
		echo "Please set target device name in second argument"
		echo "You can see available devices with command 'sdb devices'"
		echo "What's sdb? Smart Development Bridge - CLI tool used by Tizen (see https://developer.tizen.org/ko/development/tizen-studio/web-tools/running-and-testing-your-app/sdb?langredirect=1)"
		echo "You can add symlink for sdb: sudo ln -s /home/username/tizen-studio/tools/sdb /usr/bin/sdb"
		echo "Don't forget to connect to desired device! For example this command connect to TV with 192.168.1.1 IP address: sdb connect 192.168.1.1:26101"
		echo "P.S. You need to type your IP address in developer mode on target TV"
		exit 1
	fi

	if [ "$#" -le 2 ]; then
		echo "Please set profile name as third argument"
		echo "To install your app on TV your result .wgt file must be signed by your profile certificate"
		echo "First of all you must generate certificate or add existed with tizen certificate manager"
		echo "After that provide path to tizen-studio profiles: tizen cli-config -g profiles.path='/home/username/tizen-workspace/.metadata/.plugins/org.tizen.common.sign/profiles.xml'"
		exit 1
	fi

	echo "============== TIZEN DEPLOYMENT =============="
	command -v tizen >/dev/null 2>&1 || { echo "'tizen' command not defined. If you've installed tizen-studio already export it's 'bin' directory to PATH. For example export PATH=\$PATH:/home/username/tizen-studio/tools/ide/bin" >&2; exit 1; }

	cd ./build.tizen
	rm *.wgt
	tizen package -t wgt -s $4
	tizen install -n *.wgt -t $3

	echo "If you see 'Failed to install Tizen application.' log up there don's worry, check 'My App' list on target device your app may be installed (see https://stackoverflow.com/a/42966767)"
fi

if [ "$2" == "androidtv" ]; then
	echo "============== ANDROID DEPLOYMENT =============="
	cd ./build.androidtv
	echo "Clean..."
	rm -rf ./$1
	echo "Run build.py..."

	if [ "$3" == "release" ]; then
		echo "Release"
		./custom_build.py --app $1 --title $1
	else
		echo "Debug"
		./custom_build.py --app $1 --title $1 --debug
	fi
	echo "Install via adb..."
	adb install -r ./$1/platforms/android/build/outputs/apk/debug/android-debug.apk
fi

if [ "$2" == "netcast" ]; then
	echo "============== NETCAST DEPLOYMENT =============="
	cd_and_zip_dir ./build.netcast $1
	retval=$?
	if [ $retval == 0 ]; then
		echo "Done"
		echo "Now you must add DRM subscription to your app, upload build.netcast/$1.zip here 'http://developer.lge.com/apptest/retrieveApptestOSList.dev'"
	else
		echo "ERROR: Failed to deploy netcast"
	fi
fi

if [ "$2" == "orsay" ]; then
	echo "============== ORSAY DEPLOYMENT =============="
	cd_and_zip_dir ./build.netcast $1
	retval=$?
	if [ $retval == 0 ]; then
		echo "Done"
		echo "Now you can upload zip file on your server or unzip it on USB and insert it in your samsung smart TV"
	else
		echo "ERROR: Failed to deploy orsay"
	fi
fi
