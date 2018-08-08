import os
import platform
import random
import string

from flask import Flask, request, jsonify

from ioiprint.settings import printer_for_contestant, printer_for_translation, \
    printer_for_mass
from ioiprint.modifier import make_cms_request_pdf, make_contestant_pdf, \
    make_translation_pdf
from ioiprint.contestant_data import get_contestant_data
from ioiprint.print import print_file
from ioiprint.utils import create_temp_directory, generate_print_id

app = Flask('ioiprint')

def _real_ip():
    return request.headers.get('X-Real-IP', request.remote_addr)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'OK'


@app.route('/mass', methods=['POST'])
def mass():
    temp_directory = create_temp_directory()
    original_pdf_path = os.path.join(temp_directory, 'original.pdf')
    request.files['pdf'].save(original_pdf_path)

    printer = request.form.get('printer', printer_for_mass())
    count = int(request.form['count'])
    for _ in range(count):
        print_file(original_pdf_path, printer, 'mass')
    return "OK"


@app.route('/translation', methods=['POST'])
def translation():
    temp_directory = create_temp_directory()
    original_pdf_path = os.path.join(temp_directory, 'original.pdf')
    request.files['pdf'].save(original_pdf_path)

    country_code = request.form['country_code']
    country_name = request.form['country_name']
    count = int(request.form['count'])
    final_pdf_path = make_translation_pdf(
        original_pdf_path,
        country_code,
        country_name,
        temp_directory
    )

    job_name = 'translation:%s'%country_code
    for _ in range(count):
        print_file(final_pdf_path, printer_for_translation(), job_name)
    return "OK"


@app.route('/cms_request', methods=['POST'])
def cms_request():
    temp_directory = create_temp_directory()

    request_message = request.form['request_message']
    contestant_data = get_contestant_data(_real_ip())

    request_pdf_path = make_cms_request_pdf(
        request_message,
        contestant_data['contestant_id'],
        contestant_data['contestant_name'],
        contestant_data['desk_id'],
        contestant_data['desk_image_url'],
        temp_directory
    )

    job_name = 'cms_request:%s'%contestant_data['contestant_id']
    print_file(request_pdf_path, printer_for_contestant(contestant_data['zone']), job_name)
    return "OK"


@app.route('/contestant', methods=['POST'])
def contestant():
    temp_directory = create_temp_directory()
    original_pdf_path = os.path.join(temp_directory, 'original.pdf')
    request.files['pdf'].save(original_pdf_path)

    contestant_data = get_contestant_data(_real_ip())
    print_id = generate_print_id()
    hostname = platform.uname().node

    final_pdf_path = make_contestant_pdf(
        original_pdf_path,
        contestant_data['contestant_id'],
        contestant_data['contestant_name'],
        contestant_data['contestant_country'],
        contestant_data['desk_id'],
        contestant_data['desk_image_url'],
        print_id,
        temp_directory
    )

    job_name = 'contestant:%s:%s'%(contestant_data['contestant_id'], print_id)
    print_file(final_pdf_path, printer_for_contestant(contestant_data['zone']), job_name)
    return "Queued as %s on %s"%(print_id, hostname)
