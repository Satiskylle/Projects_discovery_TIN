import dwf
import time

import windows_api

from ctypes import *
import math
import sys
import ctypes

##############################################


class exit_cases():
    END_OF_PROGRAM = 0  # must be first xDDD
    NO_DEVICES_FOUND = 1
    UNDEFINED = 2

##############################################


test_waveform_ascending_and_descending = []
for i in range(4096):
    test_waveform_ascending_and_descending.append(i / 4096.0)
for i in range(4096, 0):
    test_waveform_ascending_and_descending.append(i / 4096.0)

##############################################


def print_dwf_version():
    print("DWF Version: " + dwf.FDwfGetVersion())


def dwf_check_num_of_devices():
    cdevices = dwf.DwfEnumeration()
    print("Number of devices: " + str(len(cdevices)))
    if len(cdevices) == 0:
        return False, str(len(cdevices))
    else:
        return True, str(len(cdevices))


def dwf_search_for_devices():
    result, num_of_devices_connected = dwf_check_num_of_devices()
    if result == False:
        exit_program(exit_cases.NO_DEVICES_FOUND)
    else:
        windows_api.windows_message(
            "Device found.", "Found " + num_of_devices_connected + " devices. Opening first", 0)


def dwf_open_first_device_as_analogout():
    print("Opening first device")
    # lol = cdll.LoadLibrary("dwf.dll")
    # hdwf = c_int()
    # lol.FDwfDeviceOpen(c_int(-1), byref(hdwf))
    dwf_aio = dwf.DwfAnalogIO()
    dwf_do = dwf.DwfDigitalOut(dwf_aio)
    dwf_di = dwf.DwfDigitalIn(dwf_do)
    dwf_ai = dwf.DwfAnalogIn(dwf_di)

    # enable positive supply
    dwf_aio.channelNodeSet(0, 0, True)
    # set voltage to 5 V
    dwf_aio.channelNodeSet(0, 1, 5.0)
    # set voltage to 3.3 V
    dwf_aio.channelNodeSet(1, 0, True)
    dwf_aio.channelNodeSet(1, 1, -3.3)
    dwf_aio.enableSet(True)

    # lol.FDwfDigitalSpiFrequencySet(hdwf, 10)

    print("LOL1")

    # lol.nodeEnableSet(0, lol.NODE.CARRIER, True)  # dodalem to
    # lol.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(1), c_double(3.3))
    # lol.FDwfAnalogIOEnableSet(hdwf, c_int(True))
    # lol.nodeOffsetSet(0, lol.NODE.CARRIER, 3.3)
    print("LOL2")

    time.sleep(20)
    print("END! ")
    # lol.FDwfAnalogIOEnableSet(hdwf, c_int(False))

    # dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

    # lol = cdll.dwf
    # hdwf = c_int()
    # lol.FDwfDeviceConfigOpen(c_int(-1), c_int(3), byref(hdwf))
    # lol.FDwfDigitalSpiFrequencySet(hdwf, 10)
    # dwf_dev = dwf.DwfDigitalOut()
    # dwf_ao = dwf.DwfAnalogOut(dwf_dev)

    # dwf_ao = "A"
    # dwf_dev = "B"

    # return dwf_ao, dwf_dev  # return dwf_ao, dwf_do


""" @brief This function generates waveform on channel @channel from @rgdSamples_custom_values
    @note  Use dwf_waveform_start to start generating waveform
    @param [in] dwf_ao - handle of dwf opened device (idxDevice)
    @param [in] channel - channel of the device for which waveform is configured
    @param [in] frequency - frequency of the pattern set in Hz
    @param [in] amplitude - amplitude of the signal in volts
    @param [in] rgdSamples_custom_values - samples which mades our waveform pattern
"""


def dwf_generate_custom_waveform(dwf_ao, channel, frequency, amplitude, rgdSamples_custom_values):
    dwf_ao.nodeEnableSet(channel, dwf_ao.NODE.CARRIER, True)
    dwf_ao.nodeFunctionSet(channel, dwf_ao.NODE.CARRIER, dwf_ao.FUNC.CUSTOM)
    # dwf_ao.nodeDataSet(channel, dwf_ao.NODE.CARRIER, rgdSamples_custom_values)
    dwf_ao.nodeOffsetSet(channel, dwf_ao.NODE.CARRIER,
                         rgdSamples_custom_values)
    dwf_ao.nodeFrequencySet(channel, dwf_ao.NODE.CARRIER, frequency)
    dwf_ao.nodeAmplitudeSet(channel, dwf_ao.NODE.CARRIER, amplitude)


def dwf_waveform_start(dwf_ao, channel):
    dwf_ao.configure(channel, True)


def dwf_waveform_stop(dwf_ao, channel):
    dwf_ao.configure(channel, False)


def test_adc(dwf_ao, channel):
    for offset in range(0, 4096):
        dwf_generate_custom_waveform(dwf_ao, channel, 0, 0, offset/4096)
        dwf_waveform_start(dwf_ao, channel)
        time.sleep(0.01)

# def dwf_get_value(dwf_ao, channel):
#    lolz


def exit_program(num_of_case):
    if num_of_case == int(exit_cases.NO_DEVICES_FOUND):
        windows_api.windows_message(
            "Error", "No connected device detected.", 0)
    elif num_of_case == exit_cases.END_OF_PROGRAM:
        windows_api.windows_message("Error", "Program ended.", 0)
    else:
        windows_api.windows_message("Error", "Unsupported error", 0)
    quit(-num_of_case)


##############################################
'''
print_dwf_version()

result, num_of_devices_connected = dwf_search_for_devices()
if result == False:
    exit_program(exit_cases.NO_DEVICES_FOUND)
else:
    windows_api.windows_message("Device found.", "Found " + num_of_devices_connected + " devices. Opening first")

idxDevice = dwf_open_first_device_as_analogout()

waveform_test_channel = 0
waveform_test_frequency = 1
waveform_test_amplitude = 1.0
dwf_generate_custom_waveform(idxDevice, waveform_test_channel, waveform_test_frequency,
                             waveform_test_amplitude, test_waveform_ascending_and_descending)
dwf_waveform_start(dwf_ao, waveform_test_channel)
print("Signal generated for 10 seconds. Started")
time.sleep(10)
print("Done")
idxDevice.close()

exit_program(exit_cases.END_OF_PROGRAM)
'''
# 3
# MCP3002 -- SERIAL COMMUNICATION FUNCTIONS


def dwf_configure_spi(hdwf, hz):
    hdwf.FDwfDigitalSpiFrequencySet(hdwf, hz)
   # hdwf.FDwf

# open device
# dwf_do = dwf.DwfDigitalOut()
# hzSys = dwf_do.internalClockInfo()

# SPI parameters
# CPOL = 0 # or 1
# CPHA = 0 # or 1
# hzFreq = 1e6
# cBits = 16
# rgdData = [0x12, 0x34]

# serialization time length
# dwf_do.runSet((cBits + 0.5) / hzFreq)

# DIO 2 Select
# dwf_do.enableSet(2, True)
# output high while DigitalOut not running
# dwf_do.idleSet(2, dwf_do.IDLE.HIGH)
# output constant low while running
# dwf_do.counterInitSet(2, False, 0)
# dwf_do.counterSet(2, 0, 0)

# DIO 1 Clock
# dwf_do.enableSet(1, True)
# set prescaler twice of SPI frequency
# dwf_do.dividerSet(1, int(hzSys / hzFreq / 2))
# 1 tick low, 1 tick high
# dwf_do.counterSet(1, 1, 1)
# start with low or high based on clock polarity
# dwf_do.counterInitSet(1, CPOL, 1)
# dwf_do.idleSet(1, dwf_do.IDLE.HIGH if CPOL else dwf_do.IDLE.LOW)

# DIO 0 Data
# dwf_do.enableSet(0, True)
# dwf_do.typeSet(0, dwf_do.TYPE.CUSTOM)
# for high active clock, hold the first bit for 1.5 periods
# dwf_do.dividerInitSet(0, int((1+0.5*CPHA)*hzSys/hzFreq))
# SPI frequency, bit frequency
# dwf_do.dividerSet(0, int(hzSys / hzFreq))
# data sent out LSB first
# dwf_do.dataSet(0, dwf.create_bitdata_stream(rgdData, 8))

# dwf_do.configure(True)
# print("Generating SPI signal")
# time.sleep(1)

# dwf_do.reset()
# dwf_do.close()
