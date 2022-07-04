#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
import re


class NetworkdModuleError(Exception):
    pass


class Networkd(object):

    platform = 'Generic'
    distribution = None

    def __init__(self, module):
        self.module = module
        self.conn_name = module.params['conn_name']
        self.state = module.params['state']


def main():
    # Parsing argument file
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', required=True, choices=['absent', 'present']),
            conn_name=dict(type='str', required=True),
        ),
        mutually_exclusive=[],
        required_if=[],
        supports_check_mode=True,
    )
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')

    networkd = Networkd(module)

    (rc, out, err) = (None, '', '')
    result = {'conn_name': networkd.conn_name, 'state': networkd.state}

    # check for issues
    if networkd.conn_name is None:
        networkd.module.fail_json(msg="Please specify a name for the connection")

    try:
        if networkd.state == 'absent':
            print("COUCOU Absent")
        elif networkd.state == 'present':
            print("COUCOU Present")
    except NetworkdModuleError as e:
        module.fail_json(name=networkd.conn_name, msg=str(e))

    if rc is None:
        result['changed'] = False
    else:
        result['changed'] = True
    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err

    module.exit_json(**result)


if __name__ == '__main__':
    main()

