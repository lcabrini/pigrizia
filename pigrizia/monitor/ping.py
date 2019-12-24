# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import toml
import pingparsing
from pigrizia.config import config_dir
from .monitor import Monitor

# TODO: read global configuration directory
config_file = '/usr/local/pigrizia/monitor/ping.conf'

class PingMonitor(Monitor):
    """
    This monitor pings hosts and reports the results. It compares these
    results with configurable thresholds. If any result is above its
    threshold value, an alarm is raised.

    This class is currently partially functional. It cannot yet do
    anything with alarms, because that part of the system is not yet
    implemented.

    Eventually there should also be a configurator for this monitor,
    so that the user does not have to touch the TOML file directly.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._config()

    def monitor(self):
        """
        Run this monitor. 
        """
        alarms = {}
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [
                    #(host, executor.submit(partial(self._ping, host,
                    #    self.count)))
                    (host, executor.submit(self._ping, host, self.count))
                    for host in self._hosts
                    ]
            for h, f in futures:
                res = f.result()
                if res is None:
                    if not h in alarms:
                        alarms[h] = []
                    alarms[h].append({ 
                        'alarm': 'down',
                        'severity': 'critical'})
                else:
                    alarm_list = self._alarms_by_host(h)
                    for alarm in alarm_list:
                        para = alarm['parameter']
                        hostval = res[para]
                        paraval = alarm['threshold']
                        if hostval > paraval:
                            if not h in alarms:
                                alarms[h] = []

                            alarms[h].append({ 
                                'alarm': para,
                                'severity': alarm['severity']})
                        
        print("Alarms: {}".format(alarms))
        # TODO: we should send these alarms someplace

    def _alarms_by_host(self, host):
        for network in self._networks:
            if host in network['hosts']:
                return network['alarm']
        return []

    def _ping(self, host, count):
        parsing = pingparsing.PingParsing()
        transmitter = pingparsing.PingTransmitter()
        transmitter.destination = host
        transmitter.count = count
        result = transmitter.ping()
        if result.returncode == 0:
            return parsing.parse(result).as_dict()
        else:
            return None

    def _config(self):
        try:
            config = toml.load('config_file')
        except FileNotFoundError:
            return 1

        glob = config['global']
        self.count = 10
        if 'count' in glob:
            self.count = glob['count']
        self.workers = 5
        if 'workers' in glob:
            self.workers = glob['workers']

        self._networks = config['network']
        self._hosts = []
        for nw in self._networks:
            self._hosts += nw['hosts']
