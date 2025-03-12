import os
import json
from multiprocessing import cpu_count

# gunicorn -c gunicorn_config.py wsgi:app

safety_net = 1
pool_size = RDS_POOL_SIZE = int(os.getenv('RDS_POOL_SIZE')) if os.getenv('RDS_POOL_SIZE') else 1
pool_size += safety_net
RDS_POOL_SIZE += safety_net

if not ((pool_size - safety_net) > 0):
    raise Exception('Threads has to be higher that 0.')

bind = '0.0.0.0:' + os.getenv('PORT', '8080')
workers = (cpu_count() * 2) + 1
threads = pool_size - safety_net
worker_class = 'gthread'
proc_name = "gunicorn"
# default_proc_name = "gunicorn"
timeout = 60
# accesslog = '-'
# errorlog = '-'
loglevel = 'debug'
capture_output = True
accesslog_var = os.getenv("ACCESS_LOG", "-")
use_accesslog = accesslog_var or None
accesslog = use_accesslog
errorlog_var = os.getenv("ERROR_LOG", "-")
use_errorlog = errorlog_var or None
errorlog = use_errorlog

log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "timeout": timeout,
    "errorlog": errorlog,
    "accesslog": accesslog,
    # Additional, non-gunicorn variables
}
print(json.dumps(log_data))