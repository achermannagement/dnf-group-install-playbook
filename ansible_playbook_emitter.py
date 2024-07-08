"""
Simple emitter for dnf group info into ansible playbook

No I/O, just string is emitted
"""
import yaml

class AnsiblePlaybookEmitter:

    DEFAULT_PREAMBLE = {'hosts':'localhost', 'become':'yes', 'become_method': 'sudo'}

    DEFAULT_POSTAMBLE = {} #FIXME

    def __init__(self, dnf_parser, preamble=None, start_indent=None):
        self._preamble = preamble if preamble else self.DEFAULT_PREAMBLE
        self._indent = start_indent if start_indent else 1
        self._dnf_parser = dnf_parser

    def emit(self):
        results = []
        results.append(self.DEFAULT_PREAMBLE)
        results[0]['tasks'] = []

        # using list comprehension for flattening the dict_value lists
        all_pkgs = [x for xs in self._dnf_parser.pkg_lists.values() for x in xs]

        for pkg_name in all_pkgs:
            results[0]['tasks'].append(
                    {'name': f'install {pkg_name}',
                     'package': {'name': pkg_name, 'state': 'present'}})

        return yaml.dump(results)
