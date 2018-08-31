import redis

print_count_prefix = 'print_count:'
print_count_prefixes_by_job = {
  'contestant': print_count_prefix + 'contestant:',
  'translation': print_count_prefix + 'translation:',
  'staff_call': print_count_prefix + 'staff_call:'
}
db = redis.Redis(host='redis', port=6379)

def countup_print(job_name):
  key = print_count_prefix + job_name
  db.incr(key)

def get_metrics():
  counter = {}
  for job_name, prefix in print_count_prefixes_by_job.items():
    keys = db.keys(prefix + '*')
    counter[job_name] = {}
    for key in keys:
      job_value = key.decode('utf-8')[len(prefix):]
      counter[job_name][job_value] = db.get(key).decode('utf-8')
  return counter