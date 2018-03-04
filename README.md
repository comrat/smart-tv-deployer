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
Place script in your PureQML project root (or use symbol link). Just run script:
```
./smart-tv-deployer.py -p TARGET_PLATFORM
```
<i>TARGET_PLATFORM</i> - platform you wont to deploy possible possible values are webos|netcast|tizen|orsay|androidtv
# Platform specific deployment
Each platform has some features during deploy
### LG WebOS
To install app on WebOS Smart TV you need to install [WebOS SDK](http://webostv.developer.lge.com/sdk/download/download-sdk/) (at least CLI).
Than you must enable developer mode on your TV for details see [this link](http://webostv.developer.lge.com/develop/app-test/).

After configuring TV run the script:
```
./smart-tv-deployer.py -p webos -t tvName
```
<i>tvName</i> - name of TV which you've set in ``` ares-setup-device ```
### LG NetCast
TODO: add description
### Samsung Tizen
TODO: add description
### Samsung Orsay
TODO: add description
### AndroidTV
TODO: add description
