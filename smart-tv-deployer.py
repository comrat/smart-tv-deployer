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




parser = argparse.ArgumentParser('smart-tv-deploy script')
parser.add_argument('--platform', '-p', help='target platform: webos|netcast|tizen|orsay|androidtv', dest='platform')
parser.add_argument('--tv', '-t', help='TV name', dest='tv')
args = parser.parse_args()

manifest_path = '.manifest'
platform = args.platform
tv = args.tv

if platform is None:
    print "Provide platform name: ./smart-tv-deployer.py -p <PLATFORM_NAME>"
    sys.exit(1)

if path.exists(manifest_path):
    title, version = parse_manifest(manifest_path)
    print "Manifest parsed, title:", title, "version", version
    print "Build project..."
    os.system('./qmlcore/build -m -p %s' %(platform))

    if platform == "webos":
        print "============== WEBOS DEPLOYMENT =============="
        deploy_webos(title, version, tv)
    elif platform == "tizen":
        print "============== TIZEN DEPLOYMENT =============="
    elif platform == "netcast":
        print "============== NETCAST DEPLOYMENT =============="
    elif platform == "orsay":
        print "============== ORSAY DEPLOYMENT =============="
    elif platform == "androidtv":
        print "============== ANDROIDTV DEPLOYMENT =============="
    else:
        print "Unknown platform:", platform
else:
    print ".manifest file not found"
