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
# XTB232/CM11A controller driver
#
# References: 
#   http://jvde.us/info/CM11A_protocol.txt
#   http://jvde.us//xtb/XTB-232_description.htm
#
# Complete list of CM11A functions from protocol spec
# Function                  Binary Value
# All Units Off             0000
# All Lights On             0001
# On                        0010
# Off                       0011
# Dim                       0100
# Bright                    0101
# All Lights Off            0110
# Extended Code             0111
# Hail Request              1000
# Hail Acknowledge          1001
# Pre-set Dim (1)           1010
# Pre-set Dim (2)           1011
# Extended Data Transfer    1100
# Status On                 1101
# Status Off                1110
# Status Request            1111
#

import drivers.X10ControllerInterface as X10ControllerInterface
import Configuration
import serial
import datetime
import array
import logging
import binascii
import time

logger = logging.getLogger("server")


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
    HdrFunction = 0x02
    HdrAlwaysOne = 0x04

    # Error codes
    ChecksumTimeout = 1
    InterfaceReadyTimeout = 2
    AckNotReceived = 3
    PortNotAvailable = 4
    AccessException = 5
    ChecksumError = 6

    # ************************************************************************
    def __init__(self):
        X10ControllerInterface.X10ControllerInterface.__init__(self)

    # ************************************************************************
    # Open the device
    def Open(self):
        self.InitializeController()

    # ************************************************************************
    # Close the device
    def Close(self):
        if self.port is not None:
            self.port.close()

    # ************************************************************************
    # Turn a device on
    # house_device_code = Ex. 'A1'
    # dim_amount as a percent 0 <= v <= 100
    def DeviceOn(self, house_device_code, dim_amount):
        self.ClearLastError()

        # The XTB-232 does not seem to perform the dim action as part of the on action.
        # Therefore, we do an on and a conditional dim (if dim > 0)
        result = self.ExecuteFunction(house_device_code, self.ConvertDimPercent(dim_amount), XTB232.On)
        if result and (dim_amount > 0):
            result = self.ExecuteFunction(house_device_code, self.ConvertDimPercent(dim_amount), XTB232.Dim)
        return result

    # ************************************************************************
    # Turn a device off
    # house_device_code = Ex. 'A1'
    # dim_amount 0 <= v <= 100
    def DeviceOff(self, house_device_code, dim_amount):
        self.ClearLastError()
        return self.ExecuteFunction(house_device_code, self.ConvertDimPercent(dim_amount), XTB232.Off)

    # ************************************************************************
    # Dim a lamp module
    # house_device_code = Ex. 'A1'
    # dim_amount as a percent 0 <= v <= 100
    def DeviceDim(self, house_device_code, dim_amount):
        self.ClearLastError()
        return self.ExecuteFunction(house_device_code, self.ConvertDimPercent(dim_amount), XTB232.Dim)

    # ************************************************************************
    # Bright(en) a lamp module
    # house_device_code = Ex. 'A1'
    # bright_amount as a percent 0 <= v <= 100
    def DeviceBright(self, house_device_code, bright_amount):
        self.ClearLastError()
        return self.ExecuteFunction(house_device_code, self.ConvertDimPercent(bright_amount), XTB232.Bright)

    # ************************************************************************
    # Turn all units off (for a given house code)
    # house_code = "A"..."P"
    def DeviceAllUnitsOff(self, house_code):
        self.ClearLastError()
        return self.SendStandardCommand(house_code, 0, XTB232.AllUnitsOff)

    # ************************************************************************
    # Turn all lights off
    # house_code = "A"..."P"
    def DeviceAllLightsOff(self, house_code):
        self.ClearLastError()
        return self.SendStandardCommand(house_code, 0, XTB232.AllLightsOff)

    # ************************************************************************
    # Turn all lights on
    # house_code = "A"..."P"
    def DeviceAllLightsOn(self, house_code):
        self.ClearLastError()
        return self.SendStandardCommand(house_code, 0, XTB232.AllLightsOn)

    # ************************************************************************
    def SelectAddress(self, house_device_code):
        SelectCommand = bytearray(2)  # array.array('B', [0x04, 0])

        HouseBinary = XTB232.GetHouseCode(house_device_code[0:1])
        DeviceBinary = XTB232.GetDeviceCode(house_device_code[1:])

        SelectCommand[0] = XTB232.SelectFunction
        SelectCommand[1] = ((HouseBinary << 4) + DeviceBinary)

        logger.info(X10ControllerInterface.X10ControllerInterface.FormatStandardTransmission(SelectCommand))

        return self.SendCommand(SelectCommand)

        # ************************************************************************

    # Common function for sending a complete function to the controller.
    # The device function code is treated as a data value.
    def ExecuteFunction(self, house_device_code, dim_amount, device_function):
        logger.debug("Executing function: %s",
                     X10ControllerInterface.X10ControllerInterface.GetFunctionName(device_function))
        # First part of two step sequence. Select the specific device that is the command target.
        if not self.SelectAddress(house_device_code):
            logger.error("SelectAddress failed")
            return False

        # Second part, send the command for all devices selected for the house code.
        return self.SendStandardCommand(house_device_code[0:1], dim_amount, device_function)

    # ************************************************************************
    def SendStandardCommand(self, house_code, dim_amount, device_function):
        # Second part, send the command for all devices selected for the house code.
        Xfunction = bytearray(2)  # array.array('B', [0, 0])

        Xfunction[0] = ((dim_amount << 3) + XTB232.HdrAlwaysOne + XTB232.HdrFunction)
        HouseBinary = XTB232.GetHouseCode(house_code)
        Xfunction[1] = (HouseBinary << 4) + device_function

        logger.info(X10ControllerInterface.X10ControllerInterface.FormatStandardTransmission(Xfunction))

        return self.SendCommand(Xfunction)

    # ************************************************************************
    # Return a datetime type
    def GetTime(self):
        self.ClearLastError()
        # TODO implement
        pass

    # ************************************************************************
    # Return controller status
    def GetStatus(self):
        self.ClearLastError()
        # TODO implement
        pass

        # ************************************************************************

    # TODO Consider defining this as SetCurrentTime taking no parameters.
    # Set the controller time to the current, local time.
    def SetTime(self, time_value):
        self.ClearLastError()
        # TODO implement
        pass

    # ************************************************************************
    def ConvertDimPercent(self, dimPercent):
        """
        Convert a percent value in the range 0-100 into device dim units 0-22
        """
        return int(round(float(dimPercent) / 100.0 * 22))

    # ************************************************************************
    def InitializeController(self):
        logger.info("Initializing XTB232 controller...")
        # Open the COM port
        self.com_port = Configuration.Configuration.ComPort()
        try:
            # self.port = serial.Serial(self.com_port, baudrate=4800, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2)
            self.port = serial.Serial(self.com_port, 4800, timeout=2)
            logger.info("XTB232 controller on COM port: %s", self.com_port)
        except Exception as ex:
            self.port = None
            logger.error("Unable to open COM port: %s", self.com_port)
            logger.error(str(ex))
            return

        # Handshake with controller. Usually the controller wants
        # the current time.
        self.ResetController()

    # ************************************************************************
    def ResetController(self, interface_response=None):
        logger.info("Resetting controller to a known state")
        # Handshake with controller. Usually the controller wants
        # the current time.
        if interface_response is None:
            response = self.ReadSerialByte()
        else:
            response = interface_response

        reset_complete = False
        while not reset_complete:
            if (response is not None) and (response != 0):
                logger.info("ResetController byte received: %x", response)
                # Does the controller want the time?
                if response == XTB232.InterfaceTimeRequest:
                    logger.info("ResetController received InterfaceTimeRequest. Setting interface time now.")
                    self.SetInterfaceTime(datetime.datetime.now())
                    time.sleep(0.2)
                    response = self.ReadSerialByte()
                    logger.info("ResetController response from SetInterfaceTime was %x", response)
                    # Regardless of the response, we'll send and ACK
                    self.SendAck()
                # Is this an interface ready signal?
                elif response == XTB232.InterfaceReady:
                    logger.info("ResetController received interface ready")
                    # response = self.ReadSerialByte()
                    reset_complete = True
                else:
                    logger.info("ResetController unexpected byte %x", response)
                    # Read another byte from the controller and hope for something better
                    response = self.ReadSerialByte()
            else:
                # If the controller did not provide another byte, give up.
                # Empirically, the XTB-232 seems to be in sync when this happens.
                logger.info("ResetController received None or 0")
                reset_complete = True

        logger.info("ResetController arrived at a known state")

    # ************************************************************************
    def SetInterfaceTime(self, time_value):
        """
        Send a time value to the controller. Usually the time is the current time.
        time_value should be a datetime.
        Note that the XTB232 ignores the time value. But, this is kept for CM11A compatibility.
        See section 8 of the spec.
        NOTE: This method CANNOT call another method that would result in recursion.
        Specifically, that means it cannot call SendCommand.
        """
        self.ClearLastError()

        # The set time command is 7 bytes long
        TimeData = self.CreateSetTimeCommand(time_value)

        # Send the time to the controller
        self.port.write(TimeData)
        logger.info("Sending empty set time command: %s", binascii.hexlify(TimeData))

        # Ordinarily, the controller responds to a command with a checksum.
        # However, by observation the XTB-232 never seems to return a valid checksum.
        # Therefore, we don't bother to read the checksum. We let the caller
        # handle the response from the controller.

    # ************************************************************************
    def CreateSetTimeCommand(self, time_value):
        # The set time command is 7 bytes long
        # TimeData = bytearray(7)  # array.array('B', [0,0,0,0,0,0,0])
        TimeData = bytearray(7)

        TimeData[0] = 0x9B
        for i in range(1, len(TimeData)):
            TimeData[i] = 0

        """
        # Seconds
        TimeData[1] = (time_value.second & 0xFF)
        # Minutes 0-119
        TimeData[2] = (((time_value.hour * 60) + time_value.minute) % 120)
        # Hours / 2
        TimeData[3] = (time_value.hour / 2)
        # Day of year bits 0-7
        TimeData[4] = (time_value.timetuple().tm_yday & 0xFF)
        # Day of week
        TimeData[5] = XTB232.GetDayOfWeek(time_value)
        # Day of year bit 8
        TimeData[5] |= ((time_value.timetuple().tm_yday >> 1) & 0x80)
        # Monitored house code
        TimeData[6] = ((XTB232.GetHouseCode("A") << 4) & 0xF0)
        # bits 0-3 are left 0
        """

        return TimeData

    # ************************************************************************
    # Send a time value to the controller. Usually the time is the current time.
    # time_value should be a datetime.
    # Note that the XTB232 ignores the time value. But, this is kept for CM11A compatibility.
    # See section 8 of the spec.
    def SendTime(self, time_value):
        self.ClearLastError()

        # The set time command is 7 bytes long
        TimeData = self.CreateSetTimeCommand(time_value)

        return self.SendCommand(TimeData)

    # ************************************************************************
    def SendAck(self):
        ack = bytearray(1)
        ack[0] = XTB232.InterfaceAck
        self.port.write(ack)
        logger.info("Sent ACK.")

    # ************************************************************************
    #
    # Send a multi-byte command to the interface
    #
    # PC                               Interface
    # --------------------              --------------------------
    # Bytes of command     ->
    #                      <-          Checksum
    # 0x00 commit          ->
    #                      <-          Interface ready
    #
    # ************************************************************************
    def SendCommand(self, cmd):
        expected_checksum = XTB232.CalculateChecksum(cmd)

        good_checksum = False
        retry_count = 0

        # There are only three ways out of this loop
        # 1. We successfully send time
        # 2. We fail to read any more data from the serial port
        # 3. We exhaust the retry count
        while (not good_checksum) and (retry_count < 3):
            # TODO This is OK for now, but it would be better if we had
            # decent formatting on the cmd string.
            logger.info("Sending command: %s", binascii.hexlify(cmd))
            # Send the command bytes
            self.port.write(cmd)
            # Read the response - it should be the actual checksum from the controller
            response = self.ReadSerialByte()
            # Does the expected checksum match the actual checksum?
            if expected_checksum == response:
                good_checksum = True
                logger.info("Good checksum received")
                # Send commit byte (must be an array type)
                self.SendAck()
                # Wait for interface ready signal. The retry time is arbitrary.
                start_time = datetime.datetime.now()
                elapsed_time = datetime.timedelta()
                max_elapsed_time = datetime.timedelta(seconds=2)
                while elapsed_time < max_elapsed_time:
                    response = self.ReadSerialByte()
                    if response == XTB232.InterfaceReady:
                        break
                # If we got an interface ready signal, the command was successfully transmitted.
                if response == XTB232.InterfaceReady:
                    self.LastErrorCode = XTB232.Success
                    self.LastError = ""
                    logger.info("Interface ready received")
                    # Command successful
                    return True
                else:
                    self.LastErrorCode = XTB232.InterfaceReadyTimeout
                    self.LastError = "Expected interface ready signal, but received {0}".format(
                        response if not None else "None")
                    logger.warn(self.LastError)
                    # At this point, we have received a good checksum and sent the ACK (committed the command).
                    # However, we did not receive an interface ready. It's 50-50 as to whether everything
                    # is OK. We'll assume it is.
                    return True
            elif response == XTB232.InterfaceReady:
                # Here's a guess. We expected a checksum, but we receive 0x55 instead.
                # Looks like we got an interface ready, so we'll move on.
                self.LastErrorCode = XTB232.Success
                self.LastError = "SendCommand expected a checksum, but has received an interface ready"
                logger.warn(self.LastError)
                return True
            elif response == XTB232.InterfaceTimeRequest:
                # We received an interface timer request. This likely means that the
                # power line controller was reset and is now waiting for the current time.
                # We'll reset the controller and retry the command.
                logger.info("Expected checksum, but received an InterfaceTimeRequest. Resetting controller.")
                self.ResetController(response)
                retry_count += 1
            elif (response == '') or (response is None):
                self.LastErrorCode = XTB232.ChecksumTimeout
                self.LastError = "Timeout waiting for checksum from controller"
                logger.error(self.LastError)
                return False
            else:
                logger.error("Checksum error. Exp: %x Act: %x", expected_checksum, response)
                self.LastErrorCode = XTB232.ChecksumError
                self.LastError = "Expected checksum {0}, but received {1}".format(expected_checksum,
                                                                                  response if not None else "None")
                retry_count += 1

        # If we have fallen to here, the command transmission failed.
        self.LastErrorCode = XTB232.ChecksumError
        self.LastError = "Checksum error attempting to transmit command"
        return False

    # ************************************************************************
    # Calculate the simple checksum of an iterable list of bytes
    @staticmethod
    def CalculateChecksum(data):
        checksum = 0
        for b in data:
            checksum += b
            checksum &= 0xFF
        return checksum

    # ************************************************************************
    def ReadSerialByte(self):
        """
        Read a byte from the serial port
        Returns an integer
        """
        b = self.port.read(1)
        logger.info("ReadSerialByte: 0x%X", ord(b) if len(b) > 0 else 0)
        if len(b) == 1:
            return ord(b)
        return None
