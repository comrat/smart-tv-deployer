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



parser = argparse.ArgumentParser('smart-tv-deploy script')
parser.add_argument('--platform', '-p', help='target platform: webos|netcast|tizen|orsay|androidtv', dest='platform')
args = parser.parse_args()

manifest_path = '.manifest'
platform = args.platform
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
