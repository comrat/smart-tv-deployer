#!/usr/bin/env python2.7

import json
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


manifest_path = '.manifest'
if path.exists(manifest_path):
    title, version = parse_manifest(manifest_path)
    print "Manifest parsed, title:", title, "version", version
else:
    print ".manifest file not found"
