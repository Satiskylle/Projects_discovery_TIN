import sys
import wx

import matplotlib
import matplotlib.pyplot as plt

from AD_functions import *


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="ADC TESTER", size=(1500, 1000))

        self.splitter = wx.SplitterWindow(self)
        self.left_Panel = wx.Panel(self.splitter, style=wx.SUNKEN_BORDER)
        self.right_Panel = wx.Panel(self.splitter, style=wx.SUNKEN_BORDER)

        self.splitter.SplitVertically(self.left_Panel, self.right_Panel, 500)

        # panel = wx.Panel(self)

        my_box_sizer = wx.BoxSizer(wx.VERTICAL)

        btnDeviceSearch = wx.Button(self.left_Panel, label="Search for device")
        btnDeviceSearch.Bind(wx.EVT_BUTTON, self.on_press_search)
        my_box_sizer.Add(btnDeviceSearch, 0, wx.ALL | wx.CENTER, 5)

        btnStartMeasurement = wx.Button(
            self.left_Panel, label="Start Measurement")
        btnStartMeasurement.Bind(wx.EVT_BUTTON, self.on_press_measurement)
        my_box_sizer.Add(btnStartMeasurement, 0, wx.ALL | wx.CENTER, 5)

        btnExit = wx.Button(self.left_Panel, label="Exit")
        btnExit.Bind(wx.EVT_BUTTON, self.on_press_exit)
        my_box_sizer.Add(btnExit, 0, wx.ALL | wx.CENTER, 5)

        # btnSetConfiguration = wx.Button(panel, label="Set Configuration")
        # btnSetConfiguration.Bind(wx.EVT_BUTTON, self.on_press)
        # my_box_sizer.Add(btnSetConfiguration, 0, wx.ALL | wx.CENTER, 5)

        self.text_ctrl = wx.TextCtrl(self.right_Panel,
                                     size=(400, 200),
                                     style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        my_box_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.CENTER, 5)

        redir = RedirectText(self.text_ctrl)
        sys.stdout = redir

        self.left_Panel.SetSizer(my_box_sizer)
        self.Show()

    def on_press_measurement(self, event):
        print("On press measurement")
        # idxDevice, hdwf = dwf_open_first_device_as_analogout()
        # idxDevice, hdwf =
        dwf_dio, dwf_aio, dwf_do, dwf_di, dwf_ao = dwf_open_first_device()
        self.to_plot = spi_send_data(dwf_do, dwf_di, dwf_dio)

        # dwf_configure_spi(hdwf, 10)

        waveform_test_channel = 0
        waveform_test_frequency = 0.1
        waveform_test_amplitude = 1.0

        # dwf_generate_custom_waveform(dwf_ao, waveform_test_channel, waveform_test_frequency,
        #                            waveform_test_amplitude, test_waveform_ascending_and_descending)

        test_adc(dwf_ao, waveform_test_channel, dwf_dio)
        # print("Signal generated for 10 seconds. Started")
        # time.sleep(10)
        # print("Done")
        # idxDevice.close()

        dwf_close_device()

    def on_press_search(self, event):
        self.plot_results()
        # dwf_search_for_devices()
        # dwf_open_first_device_as_analogout()

    def on_press_exit(self, event):
        print("On press exit")
        # exit_program(exit_cases.END_OF_PROGRAM)

        # def print_in_monitor(self):
        #     wx.Printer(data="Hell
    def plot_results(self):
        # x = [*range(0, 4096)]
        # y = [*range(0, 4096)]

        plt.plot(self.to_plot)  # x, y)  # self.to_plot)
        plt.show()


class RedirectText:
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
