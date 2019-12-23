# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
import toml

from pigrizia.config import config_dir
hosts_config = '/'.join((config_dir, 'hosts.conf'))

class HostConfig:
    _label = None
    _config = {}

    def __init__(self, addr=None):
        self.label = get_label_by_addr(addr)
        self._config = get_host_config(self.label)
        if not 'addr' in self._config:
            self.addr = addr

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if value != self.label:
            hosts = _read_hosts_file()
            if value is not None:
                hosts[value] = hosts.pop(self.label, self._config)
            else:
                hosts.pop(self.label)
            self._label = value
            _write_hosts_file(hosts)

    @property
    def addr(self):
        return self._config['addr']

    @addr.setter
    def addr(self, value):
        self._config['addr'] = value
        self._update()

    def _update(self):
        hosts = _read_hosts_file()
        if self.label is not None:
            hosts[self.label] = self._config
            _write_hosts_file(hosts)

def get_host_config(label):
    hosts = _read_hosts_file()
    if label in hosts:
        return hosts[label]
    else:
        return {}

def get_label_by_addr(addr):
    if addr is None:
        return None
    hosts = _read_hosts_file()
    for label, config in hosts.items():
        if 'addr' in config and config['addr'] == addr:
            return label
    return None

def _read_hosts_file():
    try:
        return toml.load(hosts_config)
    except FileNotFoundError:
        return {}

def _write_hosts_file(hosts):
    with open(hosts_config, 'w') as f:
        toml.dump(hosts, f)
