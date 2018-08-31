import redis

print_count_prefix = 'print_count:'
db = redis.Redis(host='redis', port=6379)

def countup_print(job_name):
  key = print_count_prefix + job_name
  db.incr(key)