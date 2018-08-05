import json
from urllib.parse import urljoin
from urllib.request import urlopen

from ioiprint.settings import contestant_data_url


def get_contestant_data(ip):
    url = contestant_data_url(ip)
    data = json.loads(urlopen(url).read().decode('utf-8'))
    return {
        'contestant_id': data['contestant']['id'],
        'contestant_name': data['contestant']['name'],
        'contestant_country': data['contestant']['country'],
        'zone': data['desk']['zone'],
        'desk_id': data['desk']['id'],
        'desk_image_url': urljoin(url, data['desk']['map']),
    }
