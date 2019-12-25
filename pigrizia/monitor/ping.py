# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

"""
This module implements a simple ping monitor, that is a monitor that sends
ICMP packets to hosts and then reports any failures. 

Configuration File
------------------

A ping configuration is a TOML file. If you don't want to, you should not
have to touch a configuration file directly, since the configurator class
allows you to make all the modifications you need to the configuration 
file. However, there is nothing stopping you from editing the file
directly.

The following is an example of ``ping.conf``

.. code-block :: toml

    [global]
    ping_count = 10
    workers = 5

    [[network]]
    label = 'lan'
    hosts = ['192.168.0.1', '192.168.0.10']

        [[network.test]]
        parameter = 'packet_loss_rate'
        threshold = 1.0
        severity = 'warn'

    [[network]]
    label = 'remote'
    hosts = ['8.8.8.8']

        [[network.test]]
        parameter = 'rtt_max'
        threshold = 350
        severity = 'notice'

The first section is **global**. At the current time, there is not much
here. You can set the number of packets that pings should send. You
can also set the maximum number of worker threads.

After this, there should be one or more **network** sections. Each one of
these should have a label and a list of hosts to be pinged. As well as
one or more **tests** to be performed.

The network section allows you to group hosts from which you expect
similar results. It is of course fully acceptable to just put all the
hosts in a single network section.

Each test consists of three things: the **parameter** to be checked, the
**threshold** value which indicates the point at which the test fails and
finally the **severity**, that is how serious a failure in this test should
be considered.
"""

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
    This class is used to configure a ping monitor on a host. The host
    is specified with the *host* keyword argument. If no host is given,
    the configurator will configure the ping monitor on the local machine.
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
        Get or set the number of ICMP packets to be sent.
        """
        return self.config['global']['ping_count']

    @ping_count.setter
    def ping_count(self, count):
        self.config['global']['ping_count'] = count

    @property
    def workers(self):
        """
        Get or set the number of worker threads that will be created. Each
        thread pings one host, so the more workers that are created, the
        more ping jobs will run at the same time.
        """
        return self.config['global']['workers']

    @workers.setter
    def workers(self, workers):
        self.config['global']['workers'] = workers

    @property
    def networks(self):
        """
        Returns a list of the labels of each network.
        """
        return [network['label'] for network in self.config['network']]

    @property
    def hosts(self):
        """
        Returns a list of all the hosts, across all the networks.
        """
        hosts = []
        for network in self.config['network']:
            hosts += network['hosts']
        return hosts

    @property
    def test_count(self):
        """
        Returns the total number of tests to be performed across all
        networks.
        """
        count = 0
        for network in self.config['network']:
            count += len(network['test'])
        return count
    
    def host_network(self, host):
        """
        Returns the label of the network that the given host belongs to.
        """
        for network in self.config['network']:
            if host in network['hosts']:
                return network['label']
        return None
    
    def network_tests(self, label):
        """
        Returns the tests to be performed on the given network.
        """
        for network in self.config['network']:
            if network['label'] == label:
                return network['test']
        return None

    def host_tests(self, host):
        """
        Returns the tests to be performed on the given host.
        """
        network = self.host_network(host)
        return self.network_tests(network)

    def configure(self):
        """
        Reads in the configuration for this host. 
        """
        try:
            f = self.host.read_file(config_file)
            config = toml.loads(f)
        except FileNotFoundError:
            # TODO: we need to do something here.
            return 1
        return config

    def update(self):
        """
        Updates the configuration for this host.
        """
        pass

class PingMonitor(Monitor):
    """
    This is the monitor class which performs the actual ping jobs, 
    compares the results to acceptible values and sends notifications
    if the tests do not meet the expected results.

    The class uses the configuration provided by the the 
    :class:`.PingConfigurator` class.


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
