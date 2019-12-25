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
from pigrizia.host import get_host
from .monitor import Monitor, NoTests

# TODO: read global configuration directory
config_file = sys.prefix + '/pigrizia/conf/monitor/ping.conf'

class PingConfigurator:
    """
    This class is used to configure a ping monitor on a host.
    """

    def __init__(self, **kwargs):
        if 'host' in kwargs:
            self.host = kwargs['host']
        else:
            self.host = get_host()
        self.config = self.configure()

    @property
    def ping_count(self):
        """

        """
        return self.config['global']['ping_count']

    @ping_count.setter
    def ping_count(self, count):
        self.config['global']['ping_count'] = count

    @property
    def workers(self):
        """

        """
        return self.config['global']['workers']

    @workers.setter
    def workers(self, workers):
        self.config['global']['workers'] = workers

    @property
    def networks(self):
        """

        """
        return [network['label'] for network in self.config['network']]

    @property
    def hosts(self):
        """

        """
        hosts = []
        for network in self.config['network']:
            hosts += network['hosts']
        return hosts

    @property
    def test_count(self):
        count = 0
        for network in self.config['network']:
            count += len(network['test'])
        return count
    
    def host_network(self, host):
        """

        """
        for network in self.config['network']:
            if host in network['hosts']:
                return network['label']
        return None
    
    def network_tests(self, label):
        """

        """
        for network in self.config['network']:
            if network['label'] == label:
                return network['test']
        return None

    def host_tests(self, host):
        """

        """
        network = self.host_network(host)
        return self.network_tests(network)

    def configure(self):
        """
        
        """
        try:
            f = self.host.read_file(config_file)
            config = toml.loads(f)
        except FileNotFoundError:
            # TODO: we need to do something here.
            return 1
        return config

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

    failures = []
    config = PingConfigurator()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def monitor(self):
        """
        Run this monitor. 
        """
        if self.config.test_count < 1:
            raise NoTests()

        workers = self.config.workers
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for host, future in self._make_futures(executor):
                result = future.result()
                if result is None:
                    self.failures.append((host, {'parameter': 'host_up'}))
                else:
                    for test in self.config.host_tests(host):
                        if not self.passed(result, test):
                            self.failures.append((host, test))
                                                    
        print("Failed tests: {}".format(self.failures))
        # TODO: we should send these alarms someplace

    def passed(self, result, test):
        """

        """
        parameter = test['parameter']
        result_value = result[parameter]
        test_value = test['threshold']
        return result_value < test_value


    def _tests_by_host(self, host):
        for network in self.networks:
            if host in network['hosts']:
                return network['test']
        return []

    def _host_has_test(self, host, test):
        for network in self.networks:
            if host in network['hosts']:
                return test in network['test']['parameter']

    def _get_test_for_host(self, host, test):
        for network in self.networks:
            if host in network['hosts']:
                pass
                
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

    def _add_failure(self, host, test, threshold, severity):
        if not host in self.failures:
            self.failures[host] = []
        self.failures[host].append({
            'test': test,
            'threshold': threshold,
            'severity': severity,})

    def _make_futures(self, executor):
        ping_count = self.config.ping_count
        return [
            (host, executor.submit(self._ping, host, ping_count))
            for host in self.config.hosts
            ]


