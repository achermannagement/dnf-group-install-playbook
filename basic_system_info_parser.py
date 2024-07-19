import re

"""
This is a simple parser for basic system information

Particularly, fedora version and dnf version
"""
class BasicSystemInfoParser:

    DNF_VERSION_REGEX = re.compile(r"")

    def __init__(self):
        self.dnf_version = None
        self.fedora_version = None

    def __repr__(self):
        return (
            f"dnf version={self.dnf_version}\n"
            f"fedora version={self.fedora_version}"
        )

    # just return kernel version for now
    def parse_fedora(self, uname_output):
        self.fedora_version = uname_output.strip()

    # just take the first line for now
    def parse_dnf_version(self, dnf_output):
        self.dnf_version = dnf_output.split('\n')[0].strip()
