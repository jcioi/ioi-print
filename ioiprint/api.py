import os
import platform
import random
import string

from flask import Flask, request, jsonify

import ioiprint.settings as settings
import ioiprint.modifier as modifier
from ioiprint.print import print_file, JOB_PRIORITY_HIGH
from ioiprint.contestant_data import get_contestant_data
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

    printer = request.form.get('printer', settings.printer_for_mass())
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
    cover_page = int(request.form['cover_page']) > 0
    count = int(request.form['count'])

    if cover_page:
        final_pdf_path = modifier.make_translation_pdf(
            original_pdf_path,
            country_code,
            country_name,
            temp_directory
        )
    else:
        final_pdf_path = original_pdf_path

    job_name = 'translation:%s'%country_code
    for _ in range(count):
        print_file(final_pdf_path, settings.printer_for_translation(), job_name)
    return "OK"


@app.route('/staff_call', methods=['POST'])
def staff_call():
    req_data = request.get_json()
    message = req_data['message']
    contestant = req_data['contestant']
    contestant_id = req_data['contestant']['id']
    desk = req_data['desk']
    desk_zone = req_data['desk'].get('zone')

    temp_directory = create_temp_directory()
    pdf_path = modifier.make_staff_call_pdf(
        message=message,
        contestant=contestant,
        desk=desk,
        temp_directory=temp_directory,
    )

    job_name = 'staff_call:%s'%contestant_id
    print_file(pdf_path, settings.printer_for_contestant(desk_zone),
               job_name, job_priority=JOB_PRIORITY_HIGH)
    return jsonify({'status': 'OK'})


@app.route('/contestant', methods=['POST'])
def contestant():
    temp_directory = create_temp_directory()
    original_pdf_path = os.path.join(temp_directory, 'original.pdf')
    request.files['pdf'].save(original_pdf_path)

    contestant_data = get_contestant_data(_real_ip())
    print_id = generate_print_id()
    hostname = platform.uname().node

    final_pdf_path = modifier.make_contestant_pdf(
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
    metric_name = 'contestant:%s'%(contestant_data['contestant_id'])
    print_file(
        file_path=final_pdf_path,
        printer=settings.printer_for_contestant(contestant_data['zone']),
        job_name=job_name,
        metric_name=metric_name
    )
    return "Queued as %s on %s"%(print_id, hostname)

@app.route('/password', methods=['POST'])
def password():
    req_data = request.get_json()
    title = req_data['title']
    users = req_data['users']

    temp_directory = create_temp_directory()
    pdf_path = modifier.make_password_pdf(
        title=title,
        users=users,
        temp_directory=temp_directory,
    )

    job_name = 'password'
    print_file(pdf_path, settings.printer_for_mass(), job_name)
    return jsonify({'status': 'OK'})

@app.route('/metrics', methods=['GET'])
def metrics():
    return 'OK'