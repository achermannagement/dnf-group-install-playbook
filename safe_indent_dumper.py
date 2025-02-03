"""
We need to monkeypatch the YAML loader to indent blocks
this is mainly to satisfy ansible-lint and yamllint

see: https://github.com/yaml/pyyaml/issues/234
"""
import yaml

class SafeIndentDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

def safe_indent_dump(data, **kwargs):
    return yaml.dump(data, Dumper=SafeIndentDumper, default_flow_style=False, indent=2, **kwargs)
