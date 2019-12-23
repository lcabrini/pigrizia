# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
import toml

import logging
logger = logging.getLogger(__name__)

config_dir = os.getenv('HOME') + '/.pigrizia'
try:
    logger.debug("{} does not exist, creating it".format(config_dir))
    os.makedirs(config_dir, 0o700, exist_ok=True)
except FileExistsError:
    logger.info("{} already exists".format(config_dir))

def has_setting():
    pass

def read_config(config, key, value):
    pass

def write_config():
    pass
