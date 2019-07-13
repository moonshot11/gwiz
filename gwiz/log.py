# log.py

import sys

def info(msg, **kwargs):
    print("-I- {}".format(msg), flush=True, **kwargs)

def error(msg, code=1):
    print("-E- {}".format(msg))
    sys.exit(code)

def resp(msg):
    print("-R- {}".format(msg))
