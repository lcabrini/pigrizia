# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from .service import Service

class MariaDB(Service):
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)

    def connect(self, **kwargs):
        pass

    def backup(self, **kwargs):
        pass
