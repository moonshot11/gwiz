# main.py

import argparse
import json
import requests

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("sites", required=True, choices=["github", "gitlab"])
    parser.add_argument("mode", required=True, choices=["upload", "export"])
    parser.add_argument("file", required=True)

    args = parse_args()
    return args

if __name__ == "__main__":
    setup_args()
    pass
