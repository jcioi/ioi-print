import json
from urllib.parse import urljoin
from urllib.request import urlopen

from ioiprint.settings import contestant_data_url


def get_contestant_data(ip):
    url = contestant_data_url(ip)
    if url is None:
        return None
    return json.loads(urlopen(url).read().decode('utf-8'))
