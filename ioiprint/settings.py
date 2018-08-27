import json
import os

PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_PATH = os.path.join(PATH, 'static')
TEMPLATES_PATH = os.path.join(PATH, 'template')

if 'IOIPRINT_CONFIG' in os.environ:
    config = os.environ['IOIPRINT_CONFIG']
    if config.startswith('{'):
        SETTINGS = json.loads(config)
    else:
        with open(config) as f:
            SETTINGS = json.load(f)
else:
    SETTINGS = {}

MAX_NUM_OF_PAGES_FOR_CONTESTANTS = SETTINGS.get('contestant_max_pages')
CUPS_SERVER_ADDRESS = SETTINGS.get('cups_server')

def printer_for_contestant(zone):
    if zone is not None and 'contestant_printer_map' in SETTINGS:
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

def contestant_data_url(ip):
    if 'netadmin_url' in SETTINGS:
        return '{base}/api/nodes/ip/{ip}/'.format(base=SETTINGS['netadmin_url'], ip=ip)
    else:
        return None
