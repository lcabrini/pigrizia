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
