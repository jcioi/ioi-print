import redis
from ioiprint.settings import REDIS_HOST, REDIS_PORT

print_count_prefix = 'print_count:'
print_count_prefixes_by_job = {
    'contestant': print_count_prefix + 'contestant:',
    'translation': print_count_prefix + 'translation:',
    'staff_call': print_count_prefix + 'staff_call:'
}
db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def countup_print(job_name):
    try:
        key = print_count_prefix + job_name
        db.incr(key)
    except redis.exceptions.ConnectionError as e:
        pass

def get_metrics():
    counter = {}
    try:
        for job_name, prefix in print_count_prefixes_by_job.items():
            keys = db.keys(prefix + '*')
            counter[job_name] = {}
            for key in keys:
                job_value = key.decode('utf-8')[len(prefix):]
                counter[job_name][job_value] = db.get(key).decode('utf-8')
    except redis.exceptions.ConnectionError as e:
        pass
    return counter