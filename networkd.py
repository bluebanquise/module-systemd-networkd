#!/usr/bin/python
# -*- coding: utf-8 -*-

#from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
import re
import os


class NetworkdModuleError(Exception):
    pass

class Networkd(object):

    platform = 'Generic'
    distribution = None

    def __init__(self, module):
        self.module = module
        self.conn_name = module.params['conn_name']
        self.state = module.params['state']
        self.ifname = module.params['ifname']
        self.type = module.params['type']
        self.ip4 = module.params['ip4']
        self.method4 = module.params['method4']

    def generate_networks(self):
        network = []
        network.append("[Match]")
        if self.ifname is not None: 
            network.append("Name=" + self.ifname)
        network.append("[Network]")
        if self.method4 == "auto":
            network.append("DHCP=True")
        elif self.method4 == "manual":
            network.append("[Address]")
            network.append("Address=" + self.ip4)
        return network

def main():
    # Parsing argument file
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', required=True, choices=['absent', 'present']),
            conn_name=dict(type='str', required=True),
            ifname=dict(type='str'),
            type=dict(type='str',
                      choices=[
                          'bond',
                          'bond-slave',
                          'bridge',
                          'bridge-slave',
                          'dummy',
                          'ethernet',
                          'generic',
                          'gre',
                          'infiniband',
                          'ipip',
                          'sit',
                          'team',
                          'team-slave',
                          'vlan',
                          'vxlan',
                          'wifi',
                          'gsm',
                          'wireguard',
                          'vpn',
                      ]),
            ip4=dict(type='list', elements='str'),
            method4=dict(type='str', choices=['auto', 'link-local', 'manual', 'shared', 'disabled']),
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
            network = networkd.generate_networks()
            network_file = "/etc/systemd/network/" + networkd.conn_name +".network"
            if os.path.exists(network_file):
                with open("/etc/systemd/network/" + networkd.conn_name +".network") as f:
                    network_lines = f.readlines()
                changed = 0
                for i in range(0,len(network),1):
                    if network[i] != network_lines[i]:
                        changed = 1
            else:
                changed = 1
            f = open(network_file, "w")
            for it in network:
                f.write(it + "\n")
            f.close()
                  
    except NetworkdModuleError as e:
        module.fail_json(name=networkd.conn_name, msg=str(e))

    if changed == 0:
        result['changed'] = False
    else:
        result['changed'] = True
    
    result['stdout'] = "COUCOU LES AMICHES"

    module.exit_json(**result)


if __name__ == '__main__':
    main()

