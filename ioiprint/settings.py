import json
import os

PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_PATH = os.path.join(PATH, 'static')
TEMPLATES_PATH = os.path.join(PATH, 'template')

if 'IOIPRINT_CONFIG' in os.environ:
    with open(os.environ['IOIPRINT_CONFIG']) as f:
        SETTINGS = json.load(f)
else:
    SETTINGS = {}

if 'CONTESTANT_MAX_PAGES' in os.environ:
    SETTINGS['contestant_max_pages'] = int(os.environ['CONTESTANT_MAX_PAGES'])
if 'CONTESTANT_PRINTER_MAP' in os.environ:
    SETTINGS['contestant_printer_map'] = json.loads(os.environ['PRINTERS_FOR_ZONES'])
if 'CONTESTANT_PRINTER' in os.environ:
    SETTINGS['contestant_printer'] = os.envion['CONTESTANT_PRINTER']
if 'TRANSLATION_PRINTER' in os.environ:
    SETTINGS['translation_printer'] = os.envion['TRANSLATION_PRINTER']
if 'DEFAULT_PRINTER' in os.environ:
    SETTINGS['default_printer'] = os.envion['DEFAULT_PRINTER']
if 'NETADMIN_URL' in os.environ:
    SETTINGS['netadmin_url'] = os.envion['NETADMIN_URL']
if 'CUPS_ADDRESS' in os.environ:
    SETTINGS['cups_address'] = os.environ['CUPS_ADDRESS']
if 'UPLOAD_DIRECTORY' in os.environ:
    SETTINGS['upload_directory'] = os.environ['UPLOAD_DIRECTORY']

MAX_NUM_OF_PAGES_FOR_CONTESTANTS = SETTINGS.get('contestant_max_pages')

NET_ADMIN_URL = SETTINGS.get('netadmin_url')
CONTESTANT_DATA_URL = '{url}/api/nodes/ip/{{ip}}/'.format(url=NET_ADMIN_URL)

PDF_UPLOAD_PATH = SETTINGS.get('upload_directory')
CUPS_SERVER_ADDRESS = SETTINGS.get('cups_address')

def printer_for_contestant(zone):
    if 'contestant_printer_map' in SETTINGS:
        return SETTINGS['contestant_printer_map'][zone]
    if 'contestant_printer' in 'SETTINGS':
        return SETTINGS['contestant_printer']
    return SETTINGS['default_printer']

def printer_for_translation():
    if 'translation_printer' in 'SETTINGS':
        return SETTINGS['translation_printer']
    return SETTINGS['default_printer']

def printer_for_mass():
    return SETTINGS['default_printer']
