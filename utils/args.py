import argparse
import sys


def get_args():
    parser = argparse.ArgumentParser('smart-tv-deploy script')
    parser.add_argument('--minify', '-m', help='force minify step', action='store_true', dest='minify')
    parser.add_argument('--jobs', '-j', help='run N jobs in parallel', dest='jobs', default=1, nargs='?')
    parser.add_argument('--platform', '-p', help='target platform: webos|netcast|tizen|orsay|androidtv', dest='platform')
    parser.add_argument('--os', '-os', help='target electronjs OS', dest='electronjs_os')
    parser.add_argument('--tizen-profile', '-tp', help='tizen studio profile path', dest='tizen_profile')
    parser.add_argument('--tv', '-t', help='TV name', dest='tv')
    parser.add_argument('--release', '-r', help='generate release code (no logs)', action='store_true', dest='release')
    # parser.add_argument('--build-only', '-B', help='generate apk file (without deploy)', default=False, action='store_true', dest='buildonly')
    parser.add_argument('--debug', '-d', help='start debugging after building', dest='debug', default=False)
    parser.add_argument('--app', '-a', help='target application if there is more than one apps in project', dest='app')
    parser.add_argument('--base-url', '-b', help='base URL value if you need to get qml.app.js file remotely', dest='baseurl')
    parser.add_argument('--width', '-w', help='app width (1280 by default)', dest='width')
    parser.add_argument('--height', '-he', help='app height (720 by default)', dest='height')
    parser.add_argument('--set-property', '-sp', dest='properties', action='append', help = 'sets manifest property name value', nargs=2)
    return parser.parse_args()

def validate_args(args):
    tizen_profile = args.tizen_profile
    electronjs_os = args.electronjs_os
    platform = args.platform
    tv = args.tv
    release = args.release
    # build_only = args.buildonly
    debug = args.debug
    jobs = args.jobs
    minify = args.minify
    app = args.app
    baseurl = args.baseurl
    width = args.width
    height = args.height

    if platform is None:
        print(f"❌ Platform not found. Provide the platform name with -p flag")
        sys.exit(1)

    #TODO: check electronjs target OS for the electron js
