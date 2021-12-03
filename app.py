import time
import redis
from flask import Flask
import os, sys


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    output = os.popen("docker ps -a 2>&1").read()
    return 'Hello World! I have been seen {} times. test: {} \n'.format(count, output)
