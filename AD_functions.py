import dwf
import time

import windows_api

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
    return dwf.DwfAnalogOut()


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
        time.sleep(0.01)


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
