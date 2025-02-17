"""
Simple emitter for dnf group info into ansible playbook

No I/O, just string is emitted
"""
from safe_indent_dumper import safe_indent_dump

import yaml
from datetime import datetime
import time

class AnsiblePlaybookEmitter:

    PREAMBLE_COMMENTS = """\
---

# This file was generated by dnf-group-install-playbook
# https://github.com/achermannagement/dnf-group-install-playbook
# at {} {}
# for Fedora: {} dnf: {}
"""

    DEFAULT_PREAMBLE = {'hosts':'localhost', 'become': True, 'become_method': 'ansible.builtin.sudo'}

    def __init__(self, dnf_parser, sys_parser, preamble=None):
        self.preamble_comments = self.PREAMBLE_COMMENTS.format(datetime.now().astimezone(), time.tzname[0], sys_parser.fedora_version, sys_parser.dnf_version)
        if preamble:
            self._preamble = {
                'name': f'Install {dnf_parser.group} dnf group',
                **preamble
            }
        else:
            self._preamble = {
                'name': f'Install {dnf_parser.group} dnf group',
                **self.DEFAULT_PREAMBLE
            }
        self._dnf_parser = dnf_parser

    def emit(self):
        results = []
        results.append(self._preamble)
        results[0]['tasks'] = []

        # using list comprehension for flattening the dict_value lists
        all_pkgs = [x for xs in self._dnf_parser.pkg_lists.values() for x in xs]

        for pkg_name in all_pkgs:
            results[0]['tasks'].append(
                    {'name': f'Install {pkg_name}',
                     'ansible.builtin.package':
                     {'name': pkg_name,
                      'state': 'present'}
                     })

        return safe_indent_dump(results, sort_keys=False)
