import re

"""
This is a simple parser for dnf group info output

Very rudimentary

The hope is to parse the different types of packages in the group

At the very least, it tracks what failed to parse as well
"""
class DnfGroupInfoParser:

    GROUP_RE = re.compile(r"Group: (\w+)")
    DESC_RE = re.compile(r"Description: (.*)")
    # assume each package type is a single word
    PKG_HEADER_RE = re.compile(r"(\w+) Packages:")

    # This parser assumes an order to dnf group info output
    def __init__(self):
        self.group = None
        self.description = None
        self.pkg_types = []
        self.curr_pkg_type = None
        self.pkg_lists = dict()
        self.in_pkgs = False
        self.unparsed = []

    def __repr__(self):
        return (
            f"DnfGroupInfoParser group={self.group}\n"
            f"description={self.description}"
        )

    # parses a single line from dnf group info
    def parse(self, dnf_line):
        cleaned = dnf_line.strip()
        if match := re.match(self.GROUP_RE, cleaned):
            self.group = match.group(1)
        elif match := re.match(self.DESC_RE, cleaned):
            self.description = match.group(1)
        elif match := re.match(self.PKG_HEADER_RE, cleaned):
            pkg_type = match.group(1)
            self.curr_pkg_type = pkg_type
            self.pkg_types.append(pkg_type)
            self.in_pkgs = True
            self.pkg_lists[pkg_type] = []
        elif self.in_pkgs:
            self.pkg_lists[self.curr_pkg_type].append(cleaned)
        else:
            self.unparsed.append(cleaned)
