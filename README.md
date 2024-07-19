DNF Group Install Playbook
--------------------------

I was using [ansible](https://github.com/ansible/ansible) to automate my Fedora computer post-install setup and I was frustrated to find that the dnf module has poor support for installing package groups. Furthermore, I found dnf itself was misbehaving when it came to installing packages from the groups (specifically Multimedia). It refused to install any of the listed packages despite claiming it had installed the group.

Rather than pursue down the features I needed in these software, I thought it would be fairly simple to parse the dnf info from the group and output an ansible playbook which would download all packages present in the group. This is the result.

It consists of three components:

- Rudimentary parser of dnf group info output
- Emitting Ansible playbook compatible YAML based on dnf
- Command line tool that handles arguments and I/O

I then added a parser for basic system info that is used to print output file metadata in the comments of the playbook.
