DNF Group Install Playbook
--------------------------

I was using [ansible](https://github.com/ansible/ansible) to automate my Fedora computer post-install setup and I was frustrated to find that the dnf module has poor support for installing package groups. Furthermore, I found dnf itself was misbehaving when it came to installing packages from the groups (specifically Multimedia). It refused to install any of the listed packages despite claiming it had installed the group.

This may be related to the fact that the dnf modules for ansible do not expose the underlying options to the dnf subprocess that specifies if packages other than the essential packages in the group are to be installed. Here is a related [issue](https://github.com/ansible/ansible/issues/67187)

Rather than chase up this issue on ansible directly, I thought it would be fairly simple to parse the dnf info from the group and output an ansible playbook which would download all packages present in the group regardless of the "package type".

It consists of three components:

- Rudimentary parser of dnf group info output
- Emitting Ansible playbook compatible YAML based on dnf
- Command line tool that handles arguments and I/O

I then added a parser for basic system info that is used to print output file metadata in the comments of the playbook.
