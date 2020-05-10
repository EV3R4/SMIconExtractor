from argparse import ArgumentParser
import cv2
from json import loads
from json.decoder import JSONDecodeError
from os.path import isfile
from shutil import copyfile
from sys import exit
from xml.sax import make_parser, handler

# ArgumentParser
ap = ArgumentParser()
ap.add_argument('-c', '--config', required=False, help='Path to the config file', default='config.json')
ap.add_argument('-n', '--name', required=False, help='Name of the item')
ap.add_argument('-u', '--uuid', required=False, help='UUID of the item (replaces -n)')
args = ap.parse_args()

CONFIG_FORMAT = {
    'iconmappng': str,
    'iconmapxml': str,
    'descriptions': str
}
def load_config():
    global config
    if not isfile(args.config):
        print('Error: Could not find "' + args.config + '"')
        exit(1)
    try:
        with open(args.config, 'r') as f:
            config = loads(f.read())
    except JSONDecodeError:
        print('Error: Config is malformed')
        exit(1)
    
    # Validation
    contains = []
    for key, value in config.items():
        try:
            if type(value) is not CONFIG_FORMAT[key]:
                print('Error: Config value "' + key + '" needs to be of type ' + CONFIG_FORMAT[key].__name__)
                exit(1)
            else:
                contains.append(key)
        except KeyError:
            print('Warning: Config contains unknown value "' + key + '"')
    for key in CONFIG_FORMAT:
        if not key in config:
            print('Error: Config is missing "' + key + '"')
            exit(1)
load_config()

if args.uuid:
    name = args.uuid
    iconuuid = args.uuid
elif args.name:
    name = args.name
    with open(config['descriptions'], 'r') as f:
        descriptions = loads(f.read())
        for uuid in descriptions:
            value = descriptions[uuid]
            if value['title'] == args.name:
                iconuuid = uuid

    try:
        iconuuid
    except NameError:
        print('Could not find part!')
        exit(1)
else:
    print('Error: You need to define -n or -u')
    exit(1)

targetx = 0
targety = 0
class IconHandler(handler.ContentHandler):
    lastuuid = ''
    def startElement(self, elementname, attrs):
        global targetx, targety, lastuuid
        if elementname == 'Index':
            lastuuid = attrs['name']
        elif elementname == 'Frame':
            x, y = attrs['point'].split(' ')
            if lastuuid == iconuuid:
                targetx = int(x)
                targety = int(y)

xmlparser = make_parser()
xmlparser.setContentHandler(IconHandler())
xmlparser.parse(config['iconmapxml'])

img = cv2.imread(config['iconmappng'], cv2.IMREAD_UNCHANGED)
cv2.imwrite(name + '.png', img[targety:targety+96, targetx:targetx+96])

print('Finished!')
