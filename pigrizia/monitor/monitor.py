# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from datetime import datetime

class NoTests(Exception):
    """
    This error is raised if a monitor is run without any tests defined.
    """
    pass

class NotStarted(Exception):
    """
    This error is raised if the start_time property is accessed on a 
    monitor that has not yet started.
    """
    pass

class NotDone(Exception):
    """
    This error is raised if the end_time propery is access on a monitor
    that has not yet ended.
    """
    pass

class Configurator:
    """
    Base class for monitor configurators (which is a very dumb name, by
    the way).
    """
    def __init__(self, config_file, **kwargs):
        self._config_file = config_file

        if 'host' in kwargs:
            self.host = kwargs['host']
        else:
            self.host = get_host()
        self._config = self.configure()

    def configure(self):
        """
        Reads in the configuration for this host. 
        """
        try:
            f = self.host.read_file(self._config_file)
            config = toml.loads(f)
        except FileNotFoundError:
            # TODO: we need to do something here.
            return 1
        return config

class Monitor:
    """
    Base class for monitors.
    """

    def __init__(self, **kwargs):
        self._start_time = None
        self._end_time = None

    @property
    def start_time(self):
        """
        Gets the date/time this monitor was started.

        :getter: the date and time this monitor started
        :type: datetime.datetime
        :raises NotStarted: if this monitor hasn't been started yet
        """
        if self._start_time is not None:
            return self._start_time
        else:
            raise NotStarted()

    @property
    def end_time(self):
        """
        Gets the date/time this monitor was ended.

        :getter: the date and time this monitor ended
        :type: datetime.datetime
        :raises NotDone: if this monitor is still running
        """
        if self._end_time is not None:
            return self._end_time
        else:
            raise NotDone

    @property
    def duration(self):
        """
        Gets the time the monitor took to complete.

        :getter: the time the monitor took to complete
        :type: datetime.timedelta
        :raises NotDone: if the monitor has not completed
        """
        try:
            return self.end_time - self.start_time
        except:
            raise NotDone()

    def start(self):
        """
        Starts this monitor.
        """
        self._start_time = datetime.now()
        self._monitor()
        self._end_time = datetime.now()

    def severity(self, value, thresholds):
        """
        Compares a value against a set of severities and returns the
        highest severity the value is greater than.

        :param int/float value: the value to be tested
        :param list thresholds: the severity levels
        :returns: the hightest severity
        :rtype: str
        """
        levels = ('Notice', 'Warning', 'Critical')
        severity = None
        for index, threshold in enumerate(thresholds):
            if value < threshold:
                return severity
            else:
                severity = levels[index]
        return severity
