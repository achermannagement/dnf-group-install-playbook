import argparse
import pathlib
import subprocess

from dnf_group_info_parser import DnfGroupInfoParser
from ansible_playbook_emitter import AnsiblePlaybookEmitter

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("group_name", type=str, help="name of group to install")
    parser.add_argument("output_folder", type=pathlib.Path, help="output directory to ")
    return parser.parse_args()

def main(args):
    process = subprocess.run(["dnf", "group", "info", args.group_name], capture_output=True) 
    dnf_parser = DnfGroupInfoParser()
    dnf_output = process.stdout.decode().split('\n')
    for dnf_line in list(filter(None, dnf_output)):
        dnf_parser.parse(dnf_line)
    abe = AnsiblePlaybookEmitter(dnf_parser)
    # filename will just be based on group name
    output_folder = args.output_folder if args.output_folder.is_dir() else args.output_folder.parent
    path = output_folder.joinpath(f"{dnf_parser.group}_dnf_group.yaml")
    fh = open(path, 'w')
    fh.write(abe.emit())

if __name__ == "__main__":
    args = parse_args()
    main(args)
