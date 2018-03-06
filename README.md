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
./smart-tv-deployer.py -p TARGET_PLATFORM
```
```TARGET_PLATFORM``` - platform you wont to deploy possible possible values are webos|netcast|tizen|orsay|androidtv
# Platform specific deployment
Each platform has some features during deploy
### LG WebOS
To install app on WebOS Smart TV you need to install [WebOS SDK](http://webostv.developer.lge.com/sdk/download/download-sdk/) (at least CLI).
Than you must enable developer mode on your TV for details see [this link](http://webostv.developer.lge.com/develop/app-test/).

After configuring TV run the script:
```
./smart-tv-deployer.py -p webos -t tvName
```
```tvName``` - name of TV which you've set in ``` ares-setup-device ```
### LG NetCast
Run the script:
```
./smart-tv-deployer.py -p netcast
```
After deploying all files will be archived in zip file in ```build.netcast/<title>_<version>.zip``` where

* ```title``` - is app title from ```.manifest``` if it wasn't declared it will be called ```app``` by default
* ```version``` - app version from the manifest or ```1.0.0``` if it wasn't defined

Follow this steps to install your app zip file on your TV:
* subscribe app zip file on [corresponded LG site](http://developer.lge.com/apptest/retrieveApptestOSList.dev)
* download subscribed archive and unzip it on USB storage in special directory (you should create it first) ```./lgapps/installed/```
* stick USB storage in your Smart TV and open "My Apps" there and find your app in USB part, for more details see [this guide](http://webostv.developer.lge.com/download_file/view_inline/3513/)

### Samsung Tizen
TODO: add description
### Samsung Orsay
Run the script:
```
./smart-tv-deployer.py -p orsay
```
After deploying all files will be archived in zip file in ```build.orsay/<title>_<version>.zip``` where

* ```title``` - is app title from ```.manifest``` if it wasn't declared it will be called ```app``` by default
* ```version``` - app version from the manifest or ```1.0.0``` if it wasn't defined

To run the app on your SmartTV just unzip archive in USB storage and stick it in your TV and open your app in 'My Apps'
### AndroidTV
TODO: add description
