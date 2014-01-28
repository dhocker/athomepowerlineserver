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
