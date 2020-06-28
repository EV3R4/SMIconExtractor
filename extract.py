from argparse import ArgumentParser
import cv2
from json import loads
from json.decoder import JSONDecodeError
from os.path import isfile
import re
from shutil import copyfile
from sys import exit
from xml.sax import make_parser, handler

# ArgumentParser
ap = ArgumentParser()
ap.add_argument('-c', '--config', required=False, help='Path to the config file', default='config.json')
ap.add_argument('-n', '--name', required=False, help='Name of the icon')
ap.add_argument('-u', '--uuid', required=False, help='UUID of the icon (replaces -n)')
ap.add_argument('-m', '--map', required=False, help='Map to extract from (default survival)', default='survival')
ap.add_argument('-g', '--gender', required=False, help='Gender (for customization)', default='')
args = ap.parse_args()

CONFIG_FORMAT = {
    'files': str,
    'language': str
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

MAPS = {
    'data': '/Data/Gui/IconMap',
    'customization': '/Data/Gui/CustomizationIconMap',
    'tool': '/Data/Gui/ToolIconMap',
    'survival': '/Survival/Gui/IconMapSurvival'
}
FOLDERS = {
    'data': '/Data',
    'customization': '/Data',
    'tool': '/Data',
    'survival': '/Survival'
}
DESCRIPTIONFILES = {
    'data': '/Gui/Language/' + config['language'] + '/InventoryItemDescriptions.json',
    'customization': '/Gui/Language/' + config['language'] + '/CustomizationDescriptions.json',
    'tool': '/Gui/Language/' + config['language'] + '/InventoryItemDescriptions.json',
    'survival': '/Gui/Language/' + config['language'] + '/inventoryDescriptions.json'
}
if not args.map in MAPS:
    print('Map "' + args.map + '" does not exist!')
    exit(1)

if args.uuid:
    name = args.uuid
    iconuuid = args.uuid
elif args.name:
    name = args.name
    with open(config['files'] + FOLDERS[args.map] + DESCRIPTIONFILES[args.map], 'r') as f:
        descriptions = loads(re.sub('//.+', '', f.read()))
        for uuid in descriptions:
            value = descriptions[uuid]
            if value['title'] == args.name:
                iconuuid = uuid

    try:
        iconuuid
    except NameError:
        print('Could not find icon!')
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
            if lastuuid == iconuuid or lastuuid == iconuuid + '_' + args.gender:
                targetx = int(x)
                targety = int(y)

xmlparser = make_parser()
xmlparser.setContentHandler(IconHandler())
xmlparser.parse(config['files'] + MAPS[args.map] + '.xml')

img = cv2.imread(config['files'] + MAPS[args.map] + '.png', cv2.IMREAD_UNCHANGED)
imgname = name

if len(args.gender) > 0:
    imgname += '_' + args.gender

origname = imgname
imgname = re.sub(':', '', imgname)

if imgname != origname:
    print('Original name was: "' + origname + '"')
    print('Modified name is:  "' + imgname + '"')

cv2.imwrite(imgname + '.png', img[targety:targety+96, targetx:targetx+96])

print('Finished!')
