import subprocess

from ioiprint import CUPS_SERVER_ADDRESS


def print_file(file_path, printer, job_name=None):
    args = ['-H', CUPS_SERVER_ADDRESS, '-P', printer]
    if job_name is not None:
        args.extend(['-J', job_name])

    subprocess.run(['lpr', *args, file_path], check=True)
