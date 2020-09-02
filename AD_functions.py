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
        print("No devices found, please check if you connected Analog Discovery properly")
    else:
        print("Device found.", "Found " +
              num_of_devices_connected + " devices. Opening first")


def dwf_open_first_device():
    print("Opening first device")
    dwf_aio = dwf.DwfAnalogIO()
    dwf_do = dwf.DwfDigitalOut(dwf_aio)
    dwf_di = dwf.DwfDigitalIn(dwf_do)
    dwf_ao = dwf.DwfAnalogOut(dwf_di)
    dwf_dio = dwf.DwfDigitalIO(dwf_ao)

    # enable positive supply 5 V
    dwf_aio.channelNodeSet(0, 0, True)
    dwf_aio.channelNodeSet(0, 1, 5.0)
    dwf_aio.enableSet(True)

    return dwf_dio, dwf_aio, dwf_do, dwf_di, dwf_ao


def dwf_close_device(dwf_dio, dwf_aio, dwf_do, dwf_di, dwf_ao):
    print("Closing devices")
    dwf_aio.close()
    dwf_do.close()
    dwf_di.close()
    dwf_ao.close()
    dwf_dio.close()


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


def test_adc(dwf_ao, channel, dwf_dio):
    for offset in range(0, 4096):
        dwf_generate_custom_waveform(dwf_ao, channel, 0, 0, offset/4096)
        dwf_waveform_start(dwf_ao, channel)
        time.sleep(0.001)


def exit_program(num_of_case):
    if num_of_case == int(exit_cases.NO_DEVICES_FOUND):
        windows_api.windows_message(
            "Error", "No connected device detected.", 0)
    elif num_of_case == exit_cases.END_OF_PROGRAM:
        windows_api.windows_message("Error", "Program ended.", 0)
    else:
        windows_api.windows_message("Error", "Unsupported error", 0)
    quit(-num_of_case)


# SPI


def spi_send_data(dwf_do, dwf_di, dwf_dio):
    # SPI parameters
    CPOL = 0  # or 1
    CPHA = 0  # or 1
    hzSys = dwf_do.internalClockInfo()
    hzFreq = 1e6
    cBits = 2
    rgdData = [0x02]

# serialization time length
    dwf_do.runSet((cBits + 0.5) / hzFreq)

# DIO 2 Select
    dwf_do.enableSet(2, True)
    # output high while DigitalOut not running
    dwf_do.idleSet(2, dwf_do.IDLE.HIGH)
    # output constant low while running
    dwf_do.counterInitSet(2, False, 0)
    dwf_do.counterSet(2, 0, 0)

# DIO 1 Clock
    dwf_do.enableSet(1, True)
    # set prescaler twice of SPI frequency
    dwf_do.dividerSet(1, int(hzSys / hzFreq / 2))
    # 1 tick low, 1 tick high
    dwf_do.counterSet(1, 1, 1)
    # start with low or high based on clock polarity
    dwf_do.counterInitSet(1, CPOL, 1)
    dwf_do.idleSet(1, dwf_do.IDLE.HIGH if CPOL else dwf_do.IDLE.LOW)

    # DIO 3 Data
    dwf_do.enableSet(3, True)
    dwf_do.typeSet(3, dwf_do.TYPE.CUSTOM)
    # for high active clock, hold the first bit for 1.5 periods
    dwf_do.dividerInitSet(3, int((1+0.5*CPHA)*hzSys/hzFreq))
    # SPI frequency, bit frequency
    dwf_do.dividerSet(3, int(hzSys / hzFreq))
    # data sent out LSB first
    dwf_do.dataSet(3, dwf.create_bitdata_stream(rgdData, 2))

    # # acquisition
    # dwf_di.dividerSet(1)
    # # 16bit per sample format
    # dwf_di.sampleFormatSet(16)
    # # set number of sample to acquire
    # N_SAMPLES = 10000
    # dwf_di.bufferSizeSet(N_SAMPLES)

    # begin acquisition and send data
    dwf_do.configure(True)
    # dwf_di.configure(False, True)
    print("Acquisition started, waiting to finish...")

    # dwf_do.configure(True)
    # print("Generated SPI signal \ sent spi data")

    # while True:
    #     sts = dwf_di.status(True)
    #     print("STS VAL: " + str(sts))
    #     if sts == dwf_di.STATE.DONE:
    #         break
    #     time.sleep(1)
    # endofacquisition
    # for v in range(0, 1000):
    #    get_data_from_io_pins(dwf_dio)
    #    time.sleep(0.001)

    print("Acquisition finished")

    # get samples, byte size
    # rgwSamples = dwf_di.statusData(N_SAMPLES)

    # dwf_do.reset()
    # dwf_di.reset()

    # print(rgwSamples)
    # return rgwSamples


def get_data_from_io_pins(dwf_dio):
    dwf_dio.status()
    dwRead = dwf_dio.inputStatus()
    # remove 0b on front, 32 digits
    print("Digital IO: " + bin(dwRead)[2:].zfill(32))
