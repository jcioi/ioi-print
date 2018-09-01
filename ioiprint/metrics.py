import json

from ioiprint.settings import METRICS_STORE_FILE

print_count_prefix = 'print_count:'
print_count_prefixes_by_job_type = {
    'contestant': print_count_prefix + 'contestant:',
    'translation': print_count_prefix + 'translation:',
    'staff_call': print_count_prefix + 'staff_call:'
}

def load_metrics():
    try:
        metrics_file = open(METRICS_STORE_FILE)
        metrics = json.load(metrics_file)
    except FileNotFoundError as e:
        metrics = None
    except json.decoder.JSONDecodeError as e:
        metrics = None
    if metrics is None:
        metrics = {}
    return metrics

def countup_print(job_name):
    metrics = load_metrics()
    key = print_count_prefix + job_name
    if key not in metrics:
        metrics[key] = 0
    metrics[key] += 1
    json.dump(metrics, open(METRICS_STORE_FILE, 'w+'))

def search_job_type_from_key(key):
    for job_type , prefix in print_count_prefixes_by_job_type.items():
        if key.startswith(prefix):
            return job_type
    return None

def get_job_value_from_key(job_type, key):
    prefix = print_count_prefixes_by_job_type[job_type]
    job_value = key[len(prefix):]
    return job_value

def get_metrics():
    counter = {}
    metrics = load_metrics()
    for key, count in metrics.items():
        job_type = search_job_type_from_key(key)
        if job_type not in counter:
            counter[job_type] = {}
        job_value = get_job_value_from_key(job_type, key)
        counter[job_type][job_value] = count
    return counter
