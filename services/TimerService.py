#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Timer service
#

import threading
import TimerServiceThread

# This class should be used as a singleton
class TimerService:

  def __init__(self):
    self.timer_thread = None

  def Start(self):
    self.timer_thread = TimerServiceThread.TimerServiceThread(1, "TimerServiceThread")
    self.timer_thread.start()

  def Stop(self):
    if self.timer_thread is not None:
      self.timer_thread.Terminate()
