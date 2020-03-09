# smart-tv-deployer
Python script to deploy
[pureqml](https://github.com/pureqml/qmlcore) apps on SmartTV. You can also run Bash version of the script

# Supported platforms
* LG WebOS
* LG NetCast
* Samsung Tizen
* Samsung Orsay
* AndroidTV

# Quick start
Place script in your PureQML project root (or use symbol link). Your project must contain the ```.manifest``` file. Run the script:
```
./build.py -p TARGET_PLATFORM -j JOBS_COUNT -m
```
```TARGET_PLATFORM``` - platform you wont to deploy possible values are webos|netcast|tizen|orsay|androidtv
```JOBS_COUNT``` - optional flag `j` declares jobs count, to increase speed of the `qmlcore/build` script
```-m``` - flag to minify build
# Platform specific deployment
Each platform has some features during deploy
### LG WebOS
To install app on WebOS Smart TV you need to install [WebOS SDK](http://webostv.developer.lge.com/sdk/download/download-sdk/) (at least CLI).
Than you must enable developer mode on your TV for details see [this link](http://webostv.developer.lge.com/develop/app-test/).

After configuring TV run the script:
```
./build.py -p webos -t tvName
```
```tvName``` - name of TV which you've set in ``` ares-setup-device ```
### LG NetCast
Run the script:
```
./build.py -p netcast
```
After deploying all files will be archived in zip file in ```build.netcast/<title>_<version>.zip``` where

* ```title``` - is app title from ```.manifest``` if it wasn't declared it will be called ```app``` by default
* ```version``` - app version from the manifest or ```1.0.0``` if it wasn't defined

Follow this steps to install your app zip file on your TV:
* subscribe app zip file on [corresponded LG site](http://developer.lge.com/apptest/retrieveApptestOSList.dev)
* download subscribed archive and unzip it on USB storage in special directory (you should create it first) ```./lgapps/installed/```
* stick USB storage in your Smart TV and open "My Apps" there and find your app in USB part, for more details see [this guide](http://webostv.developer.lge.com/download_file/view_inline/3513/)

### Samsung Tizen
To deploy tuzen projects you need [Tizen Studio](https://developer.tizen.org/ko/development/tizen-studio/download?langredirect=1) to install.
Then you must generate certificate or add existed with [tizen certificate manager](https://developer.tizen.org/ko/development/visual-studio-tools-tizen/tools/certificate-manager?langredirect=1).
After that configure path to tizen-studio profiles:

```tizen cli-config -g profiles.path='/home/username/tizen-workspace/.metadata/.plugins/org.tizen.common.sign/profiles.xml'```


To deploy your app on TV you need to connect to it first via [sdb](https://developer.tizen.org/ko/development/tizen-studio/web-tools/running-and-testing-your-app/sdb?langredirect=1). For example if your TV IP address is ```192.168.1.1``` the considered command will be ```sdb connect 192.168.1.1:26101```

Now you must figure out your TV name. You can get it from available devices list via command:```sdb devices```

Then you need to add an security profile:
```
tizen security-profiles add -n MyProfile -a /home/username/tizen-studio-data/keystore/author/mycert.p12 -p 1234"
```

There ```1234``` is your certificate password"
If you've done all this steps correctly you can now pass in ```--tizen-profile``` or ```-tp``` flag your profile name: ```MyProfile``` in our example

Finally we can build our project:

```
./build.py -p tizen --tizen-profile <PROFILE> --tv <TV_NAME>
```
Where
* ```PROFILE``` - is profile name like ```MyProfile``` in example below
* ```TV_NAME``` - TV name from ```sdb devices```

### Samsung Orsay
Run the script:
```
./build.py -p orsay
```
After deploying all files will be archived in zip file in ```<title>_<version>.zip``` where

* ```title``` - is app title from ```.manifest``` if it wasn't declared it will be called ```app``` by default
* ```version``` - app version from the manifest or ```1.0.0``` if it wasn't defined

To run the app on your SmartTV just unzip archive in USB storage and stick it in your TV and open your app in 'My Apps'

### AndroidTV
To build android projects you need to install [cordova](https://cordova.apache.org/) first. Then run the script:
```
./build.py -p androidtv
```
The result apk will be located in path: ```./build.androidtv/<your_app_title>/platforms/android/build/outputs/apk/debug/android-debug.apk``` where
* ```your_app_title``` - your app title from ```.manifest``` file

### iOS
To build iOS projects you need to install [cordova](https://cordova.apache.org/) first. Then run the script:
```
./build.py -p ios
```

### Electron.JS
To build electron.js project you need ```npm``` installed and run this script with this flags:
```
./build.py -p electronjs
```
The result app will be in ```./build.electronjs``` directory and it will be builded and run with ```npm```.
To build app for target OS (Linux, MacOS or Windows) follow correspnded steps below:

##### 1. Windows
To build windows runnable exe file run command with this parameters:
```
./build.py -p electronjs -os windows
```
The result `electron_win` app directory will be created to run result app call `app.exe` there

##### 2. MacOS
To create MacOS executable file run this command:
```
./build.py -p electronjs -os macos
```
The result `electron_macos` app directory will be created. Executable file location is `electron_macos/Electron.app/Contents/MacOS/Electron`
