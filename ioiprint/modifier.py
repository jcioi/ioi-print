import os
import subprocess
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ioiprint.settings import MAX_NUM_OF_PAGES_FOR_CONTESTANTS, STATIC_PATH, \
    TEMPLATES_PATH
from ioiprint.utils import html_to_pdf

JINJA_ENV = Environment(
    loader=FileSystemLoader(TEMPLATES_PATH),
    autoescape=select_autoescape(['html'])
)

def _formatted_time():
    return datetime.now().strftime('%a, %H:%M:%S')

def _get_num_of_pages(pdf_file_path):
    return int(subprocess.check_output(['qpdf', '--show-npages', pdf_file_path]).strip())

def make_translation_pdf(pdf_file_path, country_code, country_name,
                         temp_directory):
    time = _formatted_time()
    num_pages = _get_num_of_pages(pdf_file_path)

    first_page_template = JINJA_ENV.get_template('translation.html.jinja2')
    first_page_html = first_page_template.render(
        static_path=STATIC_PATH,
        country_code=country_code,
        country_name=country_name,
        num_pages=num_pages,
        time=time,
    )
    first_page_pdf = html_to_pdf(first_page_html, 'first', temp_directory)

    final_pdf_path = os.path.join(temp_directory, 'final.pdf')
    subprocess.run(
        [
            'qpdf',
            '--empty',
            '--pages',
            first_page_pdf,
            pdf_file_path,
            '--',
            final_pdf_path  # output
        ],
        check=True
    )
    return final_pdf_path


def make_contestant_pdf(pdf_file_path, contestant, desk,  print_id, temp_directory):
    time = _formatted_time()
    num_pages = _get_num_of_pages(pdf_file_path)
    original_num_pages = None

    if num_pages > MAX_NUM_OF_PAGES_FOR_CONTESTANTS:
        original_num_pages = num_pages
        num_pages = MAX_NUM_OF_PAGES_FOR_CONTESTANTS

    first_page_template = JINJA_ENV.get_template('first.html.jinja2')
    first_page_html = first_page_template.render(
        static_path=STATIC_PATH,
        contestant=contestant,
        desk=desk,
        num_pages=num_pages,
        original_num_pages=original_num_pages,
        time=time,
        print_id=print_id,
    )
    first_page_pdf = html_to_pdf(first_page_html, 'first', temp_directory)

    last_page_template = JINJA_ENV.get_template('last.html.jinja2')
    last_page_html = last_page_template.render(
        static_path=STATIC_PATH,
        contestant=contestant,
        desk=desk,
        num_pages=num_pages,
        original_num_pages=original_num_pages,
        time=time,
        print_id=print_id,
    )
    last_page_pdf = html_to_pdf(last_page_html, 'last', temp_directory)

    final_pdf_path = os.path.join(temp_directory, 'final.pdf')
    subprocess.run(
        [
            'qpdf',
            '--empty',
            '--pages',
            first_page_pdf,
            pdf_file_path, '1-%d' % num_pages,
            last_page_pdf,
            '--',
            final_pdf_path  # output
        ],
        check=True
    )
    return final_pdf_path


def make_staff_call_pdf(message, contestant, desk, temp_directory):
    time = _formatted_time()

    template = JINJA_ENV.get_template('staff_call.html.jinja2')
    html = template.render(
        static_path=STATIC_PATH,
        message=message,
        contestant=contestant,
        desk=desk,
        time=time,
    )
    return html_to_pdf(html, 'staff_call', temp_directory)

def make_password_pdf(title, users, temp_directory):
    template = JINJA_ENV.get_template('password.html.jinja2')
    html = template.render(
        static_path=STATIC_PATH,
        title=title,
        users=users,
    )
    return html_to_pdf(html, 'password', temp_directory)
