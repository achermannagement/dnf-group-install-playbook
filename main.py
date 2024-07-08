import argparse
import subprocess

from dnf_group_info_parser import DnfGroupInfoParser
from ansible_playbook_emitter import AnsiblePlaybookEmitter

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("group_name", type=str, help="name of group to install")
    return parser.parse_args()

def main(args):
    process = subprocess.run(["dnf", "group", "info", args.group_name], capture_output=True) 
    dnf_parser = DnfGroupInfoParser()
    dnf_output = process.stdout.decode().split('\n')
    for dnf_line in list(filter(None, dnf_output)):
        dnf_parser.parse(dnf_line)
    breakpoint()

if __name__ == "__main__":
    args = parse_args()
    main(args)
