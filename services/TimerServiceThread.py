#
# TimerService thread
#

import threading
import time
import datetime

# The timer service thread periodically examines the list of timer programs.
# When a timer event expires, it transmits the appropriate X10 function.
class TimerServiceThread(threading.Thread):

  # Constructor
  def __init__(self, thread_id, name):
    threading.Thread.__init__(self)
    self.thread_id = thread_id
    self.name = name
    self.terminate_signal = False

  # Called by threading on the new thread
  def run(self):
    # print "Timer service running"

    # Line up timing to the minute
    time_count = datetime.datetime.now().second
    # Check the terminate signal every second
    while not self.terminate_signal:
      time.sleep(1.0)
      time_count += 1
      # Every minute run the program checks
      if time_count >= 60:
        # Maintain top of the minute alignment
        time_count = datetime.datetime.now().second
        # run checks
        print datetime.datetime.now()

  # Terminate the timer service thread
  def Terminate(self):
    self.terminate_signal = True
    # wait for service thread to exit - could be a while
    print "Waiting for timer service to stop...this could take a few seconds"
    self.join()
    print "Timer service stopped"