import argparse
import pathlib
import subprocess

from dnf_group_info_parser import DnfGroupInfoParser
from ansible_playbook_emitter import AnsiblePlaybookEmitter
from basic_system_info_parser import BasicSystemInfoParser

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
    dnf_proc = subprocess.run(["dnf", "--version"], capture_output=True)
    # unfortunately need to rely on kernel release
    uname_proc = subprocess.run(["uname", "-r"], capture_output=True)
    bsip = BasicSystemInfoParser()
    bsip.parse_fedora(uname_proc.stdout.decode())
    bsip.parse_dnf_version(dnf_proc.stdout.decode())
    abe = AnsiblePlaybookEmitter(dnf_parser, bsip)
    # filename will just be based on group name
    output_folder = args.output_folder if args.output_folder.is_dir() else args.output_folder.parent
    path = output_folder.joinpath(f"{dnf_parser.group}_dnf_group.yaml")
    fh = open(path, 'w')
    fh.write(abe.preamble_comments)
    fh.write(abe.emit())

if __name__ == "__main__":
    args = parse_args()
    main(args)
