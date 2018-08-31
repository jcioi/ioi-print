import subprocess

from ioiprint.settings import CUPS_SERVER_ADDRESS
from ioiprint.metrics import countup_print

JOB_PRIORITY_DEFAULT=1
JOB_PRIORITY_HIGH=50

def print_file(file_path, printer, job_name=None, job_priority=JOB_PRIORITY_DEFAULT):
    countup_print(job_name)

    args = ['-H', CUPS_SERVER_ADDRESS, '-P', printer]
    if job_name is not None:
        args.extend(['-J', job_name])
    args.extend(['-o', 'job-priority={}'.format(job_priority)])

    subprocess.run(['lpr', *args, file_path], check=True)
