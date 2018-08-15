import json
from urllib.parse import urljoin
from urllib.request import urlopen

from ioiprint.settings import contestant_data_url


def get_contestant_data(ip):
    url = contestant_data_url(ip)
    if url is not None:
        data = json.loads(urlopen(url).read().decode('utf-8'))
        return {
            'contestant_id': data['contestant']['id'],
            'contestant_name': data['contestant']['name'],
            'contestant_remark': data['contestant']['remark'],
            'contestant_country': data['contestant']['country'],
            'zone': data['desk']['zone'],
            'desk_id': data['desk']['id'],
            'desk_image_url': urljoin(url, data['desk']['map']),
        }
    else:
        return {
            'contestant_id': 'IOI-1',
            'contestant_name': 'IOI Contestant',
            'contestant_remark': 'Some notes here...',
            'contestant_country': 'IOI',
            'zone': 'X',
            'desk_id': 'X-42',
            'desk_image_url': 'file:///dev/null',
        }
