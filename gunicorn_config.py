import os

from multiprocessing import cpu_count

# gunicorn -c gunicorn_config.py wsgi:wsgi

safety_net = 1
pool_size = RDS_POOL_SIZE = int(os.getenv('RDS_POOL_SIZE')) if os.getenv('RDS_POOL_SIZE') else 1
pool_size += safety_net
RDS_POOL_SIZE += safety_net

if not ((pool_size - safety_net) > 0):
    raise Exception('Threads has to be higher that 0.')

bind = '0.0.0.0:' + os.getenv('PORT', '8080')
# workers = (cpu_count() * 2) + 1
workers = 1
threads = pool_size - safety_net
worker_class = 'gthread'
proc_name = "gunicorn"
default_proc_name = "gunicorn"
timeout = 60
accesslog = '-'
errorlog = '-'
loglevel = 'debug'
capture_output = True
