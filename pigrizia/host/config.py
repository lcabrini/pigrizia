# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
import toml

from pigrizia.config import config_dir
host_config = '/'.join((config_dir, 'hosts.conf'))

def get_host_config(host):
    try:
        hosts = toml.load(host_config)
    except FileNotFoundError:
        return {}

    if host in hosts:
        return hosts[host]
    else:
        return {}

def set_host_config(host, config):
    try:
        hosts = toml.load(host_config)
    except FileNotFoundError:
        hosts = {}

    hosts[host] = config
    with open(host_config, 'w') as f:
        toml.dump(hosts, f)
