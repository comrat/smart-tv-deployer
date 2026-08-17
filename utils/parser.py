import json
import xml.etree.ElementTree as ET


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
		android_build = properties.get('androidBuild', {})

	return title, version, android_build

def parse_webos_appinfo(appinfo):
	data = None
	with open(appinfo) as f:
		data = json.load(f, object_pairs_hook = __pair_hook)
	if data is None:
		data = {}

	app_id = data.get('id', '')
	return app_id

def parse_tizen_config(config):
	tree = ET.parse(config)
	root = tree.getroot()
	ns = {'tizen': 'http://tizen.org/ns/widgets'}
	return root.find('tizen:application', ns)

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