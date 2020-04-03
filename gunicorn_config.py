# config.py 教程：https://www.jianshu.com/p/fecf15ad0c9a
import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

# debug = True
loglevel = 'debug'
bind = "0.0.0.0:5000"
pidfile = "log/gunicorn.pid"
accesslog = "log/access.log"
errorlog = "log/debug.log"
daemon = True

# 启动的进程数
workers = multiprocessing.cpu_count()*2+1
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'