# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

"""

"""

import sys
import subprocess
import humanfriendly
from .monitor import Configurator, Monitor

config_file = sys.prefix + '/pigrizia/conf/monitor/system.conf'

class SystemConfigurator(Configurator):
    """

    """
    
    def __init__(self, **kwargs):
        super().__init__(config_file, **kwargs)

    def diskfree(self, mount_point):
        """

        """
        #print(self._config)
        df = self._config['diskfree']
        return [d for d in df if d['mount_point'] == mount_point]

class SystemMonitor(Monitor):
    """

    """
    
    def __init__(self, **kwargs):
        self.config = SystemConfigurator()
        self.failures = []

    def _monitor(self):
        for line in subprocess.getoutput("LANG=en df -h").splitlines()[1:]:
            details = line.split()
            mount_point = details[-1]
            #print(mount_point)
            for test in self.config.diskfree(mount_point):
                #size = float(details[1]) * 1000
                size = humanfriendly.parse_size(details[1])
                param = test['parameter']
                thresholds = self.get_thresholds(test['thresholds'])
                if param == 'free':
                    # Instead of free we check used, with inverted
                    # threshold values.
                    #val = float(details[3]) * 1000
                    val = humanfriendly.parse_size(details[3])
                    #thresholds = [size - t for t in thresholds]
                    #print("VAL is {}".format(val))
                    #print("THRESHOLDS: {}".format(thresholds))
                elif param == 'used':
                    #val = float(details[2]) * 1000
                    val = humanfriendly.parse_size(details[2])
                elif param == 'used_percent':
                    val = float(details[4].replace("%", ""))
                else:
                    # TODO: what to do here?
                    pass
 
                sev = self.severity(val, thresholds)
                print("{}: {}".format(mount_point, sev))

    def get_thresholds(self, thresholds):
        ret = []
        for t in thresholds:
            try:
                ret.append(humanfriendly.parse_size(t))
            except TypeError:
                ret.append(t)
        return ret

