DOCUMENTATION = '''
    name: Etc_Hosts Inventory
    plugin_type: inventory
    author:
      - Eric McLeroy (@jmcleroy)
    short_description: Dynamic inventory plugin for a etc/hosts file.
    version_added: "n/a"
    extends_documentation_fragment:
      - constructed
    options:
        plugin:
            description: Token that ensures this is a source file for the plugin.
            required: True
            choices: ['ansible.network.etc_hosts']
        file_path:
            description:
                - The path to the etc/hosts file.
                - This can be either an absolute path, or relative to inventory file.
            required: True
    requirements:
        - python >= 2.7
'''
EXAMPLES = r'''
# example etc_hosts.yml file
---
plugin: ansible.network.etc_hosts
file_path: /etc/hosts
'''

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseFileInventoryPlugin, Constructable
from string import digits

import os
import re


class InventoryModule(BaseFileInventoryPlugin, Constructable):

    NAME = 'ansible.network.etc_hosts'

    def verify_file(self, path):
        super(InventoryModule, self).verify_file(path)
        return path.endswith(('etc_hosts.yml', 'etc_hosts.yaml'))

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)

        hosts_file_in = self.get_option('file_path')
        if os.path.isabs(hosts_file_in):
            hosts_file = hosts_file_in
        else:
            hosts_file = os.path.join(os.path.dirname(path), hosts_file_in)
        file=open(hosts_file, 'r')
        lines=file.readlines()
        for line in lines:
            group_name = line.split(' ')[1]
            group_name = re.split("\.|-", group_name)[1].rstrip('0123456789')
            self.inventory.add_group(group_name)
            host_name = self.inventory.add_host(line.split(' ')[1].strip(), group_name)
            self.inventory.set_variable(host_name, 'ansible_host' , line.split()[0])
        # Set variables for each host
#            self._set_composite_vars(self.get_option('compose'), self.inventory.get_host(host_name).get_vars(), host_name, self.get_option('strict'))
#            self._add_host_to_composed_groups(self.get_option('groups'), dict(), host_name, self.get_option('strict'))
#            self._add_host_to_keyed_groups(self.get_option('keyed_groups'), dict(), host_name, self.get_option('strict'))
