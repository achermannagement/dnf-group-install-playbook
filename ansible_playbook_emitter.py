"""
Simple emitter for dnf group info into ansible playbook

No I/O, just string is emitted

FIXME: use yaml instead of raw text
"""
class AnsiblePlaybookEmitter:

    INDENT_SIZE = 2
    INDENT = " " * INDENT_SIZE

    DEFAULT_PREAMBLE = """
- hosts: localhost
  become: yes
  become_method: sudo
  tasks:
"""

    DEFAULT_POSTAMBLE = """

"""

    INSTALL_TASK = """
- name: install {pkg_name}
  package:
    name: {pkg_name}
    state: present
"""

    def __init__(self, dnf_parser, preamble=None, start_indent=None):
        self._preamble = preamble if preamble else self.DEFAULT_PREAMBLE
        self._indent = start_indent if start_indent else 1
        self._dnf_parser = dnf_parser

    def emit(self):
        results = ""
        results += self._preamble
        results += "\n"
        for pkg_name in self._dnf_parser.pkg_lists.values():
            results += self.INDENT * self._indent
            results += self.INSTALL_TASK.format(pkg_name=pkg_name)
        results += self.DEFAULT_POSTAMBLE
        return results
