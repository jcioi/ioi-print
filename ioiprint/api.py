import os
import random
import string

from flask import Flask, request, jsonify

from ioiprint.settings import printer_for_contestant, printer_for_translation, \
    printer_for_mass
from ioiprint.modifier import make_cms_request_pdf, make_contestant_pdf, \
    make_translation_pdf
from ioiprint.contestant_data import get_contestant_data
from ioiprint.print import print_file
from ioiprint.utils import create_temp_directory

app = Flask('ioiprint')

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
    ip = request.form['ip']
    contestant_data = get_contestant_data(ip)
    desk_image_url = contestant_data['desk_image_url']

    request_pdf_path = make_cms_request_pdf(
        request_message,
        contestant_data['contestant_id'],
        contestant_data['contestant_name'],
        contestant_data['desk_id'],
        desk_image_url,
        temp_directory
    )

    job_name = 'cms_request:%s'%contestant_data['contestatnt_id']
    print_file(request_pdf_path, printer_for_contestant(contestant_data['zone']), job_name)
    return "OK"


@app.route('/contestant', methods=['POST'])
def contestant():
    temp_directory = create_temp_directory()
    original_pdf_path = os.path.join(temp_directory, 'original.pdf')
    request.files['pdf'].save(original_pdf_path)

    ip = request.form['ip']
    cups_job_id = request.form['cups_job_id']
    contestant_data = get_contestant_data(ip)
    desk_image_url = contestant_data['desk_image_url']

    final_pdf_path = make_contestant_pdf(
        original_pdf_path,
        contestant_data['contestant_id'],
        contestant_data['contestant_name'],
        contestant_data['contestant_country'],
        contestant_data['desk_id'],
        desk_image_url,
        cups_job_id,
        temp_directory
    )

    job_name = 'contestant:%s:%s'%(contestant_data['contestant_id'], cups_job_id)
    print_file(final_pdf_path, printer_for_contestant(contestant_data['zone']), job_name)
    return "OK"
