import sys

import wx
import wx.lib.plot as plot

from AD_functions import *
from additional_functions import *


class MainFrame(wx.Frame):
    def __init__(self):

        window_wide = 1500
        window_hight = 800

        super().__init__(parent=None, title="ADC TESTER", size=(window_wide, window_hight))

        self.splitter = wx.SplitterWindow(self)
        self.left_Panel = wx.Panel(self.splitter, style=wx.SUNKEN_BORDER)
        self.right_Panel = wx.Panel(self.splitter, style=wx.SUNKEN_BORDER)

        self.splitter.SplitVertically(
            self.left_Panel, self.right_Panel, 0.2 * window_wide)

        my_box_sizer = wx.BoxSizer(wx.VERTICAL)
        my_box_sizer2 = wx.BoxSizer(wx.VERTICAL)

        self.plotter = plot.PlotCanvas(self.right_Panel)
        self.plotter.SetInitialSize(
            size=(0.8 * window_wide, 0.6 * window_hight))
        self.plotter.enableZoom = True

        my_box_sizer2.Add(self.plotter, 0, wx.ALL | wx.EXPAND, 5)

        btnDeviceSearch = wx.Button(self.left_Panel, label="Search for device")
        btnDeviceSearch.Bind(wx.EVT_BUTTON, self.on_press_search)
        my_box_sizer.Add(btnDeviceSearch, 0, wx.ALL | wx.LEFT | wx.EXPAND, 5)

        btnStartMeasurement = wx.Button(
            self.left_Panel, label="Start Measurement")
        btnStartMeasurement.Bind(wx.EVT_BUTTON, self.on_press_measurement)
        my_box_sizer.Add(btnStartMeasurement, 0,
                         wx.ALL | wx.LEFT | wx.EXPAND, 5)

        btnShowResults = wx.Button(self.left_Panel, label="Show Results")
        btnShowResults.Bind(wx.EVT_BUTTON, self.on_press_show_results)
        my_box_sizer.Add(btnShowResults, 0, wx.ALL | wx.LEFT | wx.EXPAND, 5)

        btnExit = wx.Button(self.left_Panel, label="Exit")
        btnExit.Bind(wx.EVT_BUTTON, self.on_press_exit)
        my_box_sizer.Add(btnExit, 0, wx.ALL | wx.LEFT | wx.EXPAND, 5)

        self.text_ctrl = wx.TextCtrl(self.right_Panel,
                                     size=(0.8 * window_wide,
                                           0.4 * window_hight),
                                     style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        my_box_sizer2.Add(self.text_ctrl, 0, wx.ALL | wx.CENTER | wx.EXPAND, 5)

        redir = RedirectText(self.text_ctrl)
        sys.stdout = redir

        self.left_Panel.SetSizer(my_box_sizer)
        self.right_Panel.SetSizer(my_box_sizer2)
        self.Show()

    def on_press_measurement(self, event):
        print("On press measurement")
        # idxDevice = dwf_open_first_device_as_analogout()

        # waveform_test_channel = 0
        # waveform_test_frequency = 0.1
        # waveform_test_amplitude = 1.0

        # dwf_generate_custom_waveform(dwf_ao, waveform_test_channel, waveform_test_frequency,
        #                            waveform_test_amplitude, test_waveform_ascending_and_descending)

        # test_adc(dwf_ao, waveform_test_channel, dwf_dio)
        # print("Signal generated for 10 seconds. Started")
        # time.sleep(10)
        # print("Done")
        # idxDevice.close()

    def on_press_search(self, event):
        print("On press search")
        dwf_search_for_devices()

    def on_press_show_results(self, event):

        print("Plotting ADC results")

        NUMB_OF_SAMPLES = 1000
        MAX_VOLTAGE = 5

        # ADC_data: list of generated data point tuples or list of collected results from AD
        # Ideal_Voltage_data: list of data points tuples for voltage
        (ADC_data, Ideal_Voltage_data) = generate_bad_adc_mock_values(
            MAX_VOLTAGE, NUMB_OF_SAMPLES)

        ADC = plot.PolyMarker(ADC_data, marker='circle',
                              size=0.5, colour='black')

        IdealVoltage = plot.PolyLine(Ideal_Voltage_data, width=1, colour='red')

        graph = plot.PlotGraphics(
            [ADC, IdealVoltage], 'Graph of ADC results', 'Samples', 'Voltage [V]')

        self.plotter.Draw(graph, xAxis=(0, NUMB_OF_SAMPLES),
                          yAxis=(0, MAX_VOLTAGE))

    def on_press_exit(self, event):
        print("On press exit")
        exit_program(exit_cases.END_OF_PROGRAM)


class RedirectText:
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
