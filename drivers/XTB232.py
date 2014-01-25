#
# XTB232/CM11A controller driver
#
# References: 
#   http://jvde.us/info/CM11A_protocol.txt
#   http://jvde.us//xtb/XTB-232_description.htm
#

import X10ControllerInterface
import Configuration
import serial
import datetime
import array

class XTB232(X10ControllerInterface.X10ControllerInterface):
  
  # XTB232/CM11A constants. See protocol spec for these values.
  InterfaceAck = 0x00
  InterfaceReady = 0x55
  InterfacePoll = 0x5A
  InterfaceTimeRequest = 0xA5 
  SelectFunction = 0x04
  
  # Device functions
  AllUnitsOff = 0
  AllLightsOn = 1
  On = 2
  Off = 3
  Dim = 4
  Bright = 5
  AllLightsOff = 6
  StatusRequest = 15
  
  # Function header constants
  HdrFunction = 0x02;
  HdrAlwaysOne = 0x04;  
    
  #************************************************************************
  def __init__(self):
    X10ControllerInterface.X10ControllerInterface.__init__(self)
    
  #************************************************************************
  # Open the device
  def Open(self):
    self.InitializeController()
    
  #************************************************************************
  # Close the device
  def Close(self):
    self.port.close()

  #************************************************************************
  # Turn a device on
  # house_device_code = Ex. 'A1'
  # dim_amount 0 <= v <= 22
  def DeviceOn(self, house_device_code, dim_amount):
    self.ExecuteFunction(house_device_code, dim_amount, XTB232.On)
    
  #************************************************************************
  def SelectAddress(self, house_device_code):
    SelectCommand = array.array('B', [0x04, 0])

    HouseBinary = XTB232.GetHouseCode(house_device_code[0:1])
    DeviceBinary = XTB232.GetDeviceCode(house_device_code[1:])

    SelectCommand[0] = XTB232.SelectFunction;
    SelectCommand[1] = ((HouseBinary << 4) + DeviceBinary)
    
    return self.SendCommand(SelectCommand)        
    
  #************************************************************************
  # Common function for sending a complete function to the controller.
  # The device function code is treated as a data value.
  def ExecuteFunction(self, house_device_code, dim_amount, device_function):
    self.SelectAddress(house_device_code)
    
    Xfunction = array.array('B', [0, 0])

    Xfunction[0] = ((dim_amount << 3) + XTB232.HdrAlwaysOne + XTB232.HdrFunction)
    HouseBinary = XTB232.GetHouseCode(house_device_code[0:1])
    Xfunction[1] = (HouseBinary << 4) + device_function
    
    return self.SendCommand(Xfunction)        
    
  #************************************************************************
  # Return a datetime type
  def GetTime(self):
    pass        
    
  #************************************************************************
  # TODO Consider defining this as SetCurrentTime taking no parameters.
  # Set the controller time to the current, local time.
  def SetTime(self, time_value):
    pass  

  #************************************************************************
  def InitializeController(self):
    print "Initializing XTB232 controller..."
    # Open the COM port
    self.com_port = Configuration.Configuration.ComPort()
    try:
      self.port = serial.Serial(self.com_port, baudrate=4800, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2)
      print "XTB232 controller on COM port:", self.com_port
    except Exception as ex:
      print "Unable to open COM port:", self.com_port
      print str(ex)
      return
      
    # Handshake with controller. Usually the controller wants
    # the current time.
    response = self.port.read(1)
    if response == XTB232.InterfaceTimeRequest:
      print "Setting interface time"
      self.SendTime(datetime.datetime.now())
    else:
      print "During initialization, no interface time request was received from controller"
      
  #************************************************************************
  # Send a time value to the controller. Usually the time is the current time.
  # time_value should be a datetime.
  # Note that the XTB232 ignores the time value. But, this is kept for CM11A compatibility.
  # See section 8 of the spec.
  def SendTime(self, time_value):
    #The set time command is 7 bytes long
    TimeData = array.array('B', [0,0,0,0,0,0,0])
    
    TimeData[0] = 0x9B;
    # Seconds
    TimeData[1] = (time_value.second & 0xFF);
    # Minutes 0-119
    TimeData[2] = (((time_value.hour * 60) + time_value.Minute) % 120);
    # Hours / 2
    TimeData[3] = (time_value.hour / 2);
    # Day of year bits 0-7
    TimeData[4] = (time_value.timetuple().tm_yday & 0xFF);
    # Day of week
    TimeData[5] = XTB232.GetDayOfWeek(time_value);
    # Day of year bit 8
    TimeData[5] |= ((time_value.timetuple().tm_yday >> 1) & 0x80);
    # Monitored house code
    TimeData[6] = ((XTB232.GetHouseCode("A") << 4) & 0xF0);
    # bits 0-3 are left 0

    return self.SendCommand(TimeData);

  #************************************************************************
  #
  # Send a multi-byte command to the interface
  #
  # PC                               Interface
  #--------------------              --------------------------
  # Bytes of command     ->
  #                      <-          Checksum
  # 0x00 commit          ->
  #                      <-          Interface ready 
  #
  #************************************************************************
  def SendCommand(self, cmd):
    success = False
    expected_checksum = XTB232.CalculateChecksum(cmd)
    
    good_checksum = False
    retry_count = 0
    
    print "Sending command:", cmd
    
    while (not good_checksum) and (retry_count < 3):
      # Send the command bytes
      self.port.write(cmd)
      # Read the response - it should be the actual checksum from the controller
      response = self.port.read(1)
      # Does the expected checksum match the actual checksum?
      if expected_checksum == response:
        # Send commit byte
        self.port.write([XTB232.InterfaceAck])
        # Wait for interface ready signal
        for i in range(0,10):
          response = self.port.read()
          if response == XTB232.InterfaceReady:
            break
        if response == XTB232.InterfaceReady:
          success = True
        else:
          print "Expected interface ready signal, but none received"
          success = False
      else:
        retry_count += 1
        
      return success
    
  #************************************************************************
  # Calculate the simple checksum of an iterable list of bytes  
  @staticmethod
  def CalculateChecksum(data):
    checksum = 0
    for b in data:
      checksum += b
    return checksum & 0xFF