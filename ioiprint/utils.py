import os
import subprocess
import tempfile
import urllib.request

import pdfkit
from xvfbwrapper import Xvfb


def create_temp_directory():
    return tempfile.mkdtemp('ioiprint-')


def html_to_pdf(html, name, temp_directory):
    html_file_path = os.path.join(temp_directory, '%s.html' % name)
    with open(html_file_path, 'wb') as html_file:
        html_file.write(html.encode('utf-8'))
    pdf_file_path = os.path.join(temp_directory, '%s.pdf' % name)
    with Xvfb():
        pdfkit.from_file(html_file_path, pdf_file_path)
    return pdf_file_path
