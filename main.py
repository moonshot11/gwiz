# main.py

import argparse
import json
import requests

from gwiz import github
from gwiz import gitlab
from gwiz import log

site2cls = {"github" : github.Github, "gitlab" : gitlab.Gitlab}

def setup_args():
    parser = argparse.ArgumentParser()

    subs = parser.add_subparsers(dest="action", title="Actions")

    sub_upload = subs.add_parser("upload", help="Upload data to site")
    sub_export = subs.add_parser("backup", help="Download data to local file")
    sub_clrlabels = subs.add_parser("clear", help="Clear online info")

    for sub in (sub_upload, sub_export):
        sub.add_argument("--file", "-f", required=True)
    for sub in (sub_upload, sub_export, sub_clrlabels):
        sub.add_argument("--site", "-s", required=True, choices=["github", "gitlab"])
        sub.add_argument("--user", "-u", required=True)
        sub.add_argument("--proj", "-p", required=True)
        sub.add_argument("--labels-only", action="store_true")
        sub.add_argument("--issues-only", action="store_true")

    args = parser.parse_args()

    if args.action is None:
        log.error("Must provide action: see usage (-h)")
    if args.labels_only and args.issues_only:
        log.error("Can only provide one of --labels-only and --issues-only")

    if args.labels_only:
        args.only = "labels"
    elif args.issues_only:
        args.only = "issues"
    else:
        args.only = None

    return args

if __name__ == "__main__":
    args = setup_args()
    Cls = site2cls[args.site]
    session = Cls(args.user, args.proj)

    if args.action == "backup":
        session.write_json(args.file, args.only)
    elif args.action == "upload":
        session.apply_json(args.file, args.only)
    elif args.action == "clear":
        choice = input("\nDelete ALL labels? Type 'delete' to confirm: ")
        if choice == "delete":
            session.delete_all(args.only)
