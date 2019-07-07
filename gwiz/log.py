# log.py

import sys

def info(msg):
    print("-I- {}".format(msg))

def error(msg, code=1):
    print("-E- {}".format(msg))
    sys.exit(code)
