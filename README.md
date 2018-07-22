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
./build.py -p TARGET_PLATFORM -j JOBS_COUNT
```
```TARGET_PLATFORM``` - platform you wont to deploy possible values are webos|netcast|tizen|orsay|androidtv
```JOBS_COUNT``` - optional flag `j` declares jobs count, to increase speed of the `qmlcore/build` script
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

Finally we can build our project:

```
./build.py -p tizen --tizen-profile <PROFILE_PATH> --tv <TV_NAME>
```
Where
* ```PROFILE_PATH``` - is path to the to the tizen profile
* ```TV_NAME``` - TV name from ```sdb devices```

### Samsung Orsay
Run the script:
```
./build.py -p orsay
```
After deploying all files will be archived in zip file in ```build.orsay/<title>_<version>.zip``` where

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
