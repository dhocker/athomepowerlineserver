#
# Timer program - represents the equivalent of a timer initiator
#
# The program is limited to turning a device on then off
#

#######################################################################
class TimerProgram:

  #######################################################################
  # Instance constructor
  def __init__(self, name, house_device_code, day_mask, on_time, off_time, security):
    self.name = name
    self.HouseDeviceCode = house_device_code
    self.DayMask = day_mask
    self.OnTime = on_time
    self.OffTime = off_time
    self.Security = security
  