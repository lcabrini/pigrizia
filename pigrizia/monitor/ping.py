# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import sys
import os
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import toml
import pingparsing
from pigrizia.config import config_dir
from .monitor import Monitor, NoTests

# TODO: read global configuration directory
config_file = sys.prefix + '/pigrizia/conf/monitor/ping.conf'

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

    count = 10
    workers = 20
    hosts = []
    networks = {}
    failures = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._config()

    def monitor(self):
        """
        Run this monitor. 
        """
        if len(self.networks) < 1:
            raise NoTests()

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [
                    (host, executor.submit(self._ping, host, self.count))
                    for host in self.hosts
                    ]
            for h, f in futures:
                res = f.result()
                if res is None:
                    self._add_failure(h, 'host_up', 'critical')
                else:
                    alarm_list = self._alarms_by_host(h)
                    for alarm in alarm_list:
                        para = alarm['parameter']
                        hostval = res[para]
                        paraval = alarm['threshold']
                        if hostval > paraval:
                            self._add_failure(h, para, alarm['severity'])
                                                    
        print("Alarms: {}".format(self.failures))
        # TODO: we should send these alarms someplace

    def _alarms_by_host(self, host):
        for network in self.networks:
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
            config = toml.load(config_file)
        except FileNotFoundError:
            # TODO: we need to do something here.
            return 1

        global_ = config['global']
        if 'count' in global_:
            self.count = global_['count']
        if 'workers' in global_:
            self.workers = global_['workers']

        self.networks = config['network']
        for nw in self.networks:
            self.hosts += nw['hosts']

    def _add_failure(self, host, test, severity):
        if not host in self.failures:
            self.failures[host] = []
        self.failures[host].append({
            'test': test,
            'severity': severity})

class PingConfigurator:
    """
    This class is used to configure a ping monitor on a host.
    """

    def __init__(self, host, **kwargs):
        pass
