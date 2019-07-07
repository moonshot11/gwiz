# main.py

import argparse
import json
import requests

from gwiz import log

def setup_args():
    parser = argparse.ArgumentParser()

    subs = parser.add_subparsers(dest="action", title="Actions")

    sub_upload = subs.add_parser("upload", help="Upload data to site")
    sub_export = subs.add_parser("export", help="Download data to local file")
    sub_clrlabels = subs.add_parser("clear_labels", help="Clear labels on site")

    for sub in (sub_upload, sub_export):
        sub.add_argument("--file", required=True)
    for sub in (sub_upload, sub_export, sub_clrlabels):
        sub.add_argument("--site", required=True, choices=["github", "gitlab"])

    args = parser.parse_args()

    if args.action is None:
        log.error("Must provide action: see usage (-h)")
    return args

if __name__ == "__main__":
    args = setup_args()
    print(args.action)
