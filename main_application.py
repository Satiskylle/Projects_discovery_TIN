import sys

import wx
import wx.lib.plot as plot

from AD_functions import *
from additional_functions import *


class MainFrame(wx.Frame):

    MAX_VOLTAGE = 5
    ADC_RESOLUTION = 10

    WINDOW_WIDE = 1500
    WINDOW_HIGHT = 800

    def __init__(self):

        super().__init__(parent=None, title="ADC TESTER",
                         size=(self.WINDOW_WIDE, self.WINDOW_HIGHT))

        # Splitting Window to LEFT and RIGHT panel
        self.splitter = wx.SplitterWindow(self)
        self.left_Panel = wx.Panel(self.splitter, style=wx.SUNKEN_BORDER)
        self.right_Panel = wx.Panel(self.splitter, style=wx.SUNKEN_BORDER)

        self.splitter.SplitVertically(
            self.left_Panel, self.right_Panel, 0.2 * self.WINDOW_WIDE)

        # Plotting settings and enabling
        self.plotter = plot.PlotCanvas(self.right_Panel)
        self.plotter.SetInitialSize(
            size=(0.8 * self.WINDOW_WIDE, 0.6 * self.WINDOW_HIGHT))
        self.plotter.enableZoom = True

        # BUTTONS
        btnDeviceSearch = wx.Button(self.left_Panel, label="SEARCH FOR DEVICE")
        btnDeviceSearch.Bind(wx.EVT_BUTTON, self.on_press_search)

        btnStartMeasurement = wx.Button(
            self.left_Panel, label="START MEASUREMENT")
        btnStartMeasurement.Bind(wx.EVT_BUTTON, self.on_press_measurement)

        btnShowResults = wx.Button(self.left_Panel, label="SHOW RESULTS")
        btnShowResults.Bind(wx.EVT_BUTTON, self.on_press_show_results)

        btnExit = wx.Button(self.left_Panel, label="EXIT")
        btnExit.Bind(wx.EVT_BUTTON, self.on_press_exit)

        btnSet = wx.Button(self.left_Panel, label="SET VALUES")
        btnSet.Bind(wx.EVT_BUTTON, self.on_press_set_values)

        # Info output
        self.text_ctrl = wx.TextCtrl(self.right_Panel,
                                     size=(0.8 * self.WINDOW_WIDE,
                                           0.4 * self.WINDOW_HIGHT),
                                     style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        redir = RedirectText(self.text_ctrl)
        sys.stdout = redir

        # Entry controls
        entryVoltageLabel = wx.StaticText(
            self.left_Panel, -1, 'Tested Max Voltage')

        self.textEntryVoltage = wx.TextCtrl(
            self.left_Panel, style=wx.LEFT | wx.EXPAND | wx.TE_PROCESS_ENTER, value="5")
        self.textEntryVoltage.SetEditable(True)

        entryResolutionLabel = wx.StaticText(
            self.left_Panel, -1, 'ADC Resolution')

        self.textResolution = wx.TextCtrl(
            self.left_Panel, style=wx.LEFT | wx.EXPAND | wx.TE_PROCESS_ENTER, value="10")
        self.textResolution.SetEditable(True)

        # Panels arrangement
        # LEFT
        my_box_sizer = wx.BoxSizer(wx.VERTICAL)

        my_box_sizer.Add(btnDeviceSearch, 0, wx.ALL | wx.LEFT | wx.EXPAND, 8)
        my_box_sizer.Add(btnStartMeasurement, 0,
                         wx.ALL | wx.LEFT | wx.EXPAND, 8)
        my_box_sizer.Add(btnShowResults, 0, wx.ALL | wx.LEFT | wx.EXPAND, 8)
        my_box_sizer.Add(btnExit, 0, wx.ALL | wx.LEFT | wx.EXPAND, 8)

        my_box_sizer.AddSpacer(30)

        my_box_sizer.Add(entryVoltageLabel, 0, wx.ALL | wx.LEFT | wx.EXPAND, 2)
        my_box_sizer.Add(self.textEntryVoltage, 0, wx.ALL | wx.LEFT, 5)

        my_box_sizer.AddSpacer(10)

        my_box_sizer.Add(entryResolutionLabel, 0,
                         wx.ALL | wx.LEFT | wx.EXPAND, 2)
        my_box_sizer.Add(self.textResolution, 0, wx.ALL | wx.LEFT, 5)

        my_box_sizer.Add(btnSet, 0, wx.ALL | wx.LEFT | wx.EXPAND, 5)

        self.left_Panel.SetSizer(my_box_sizer)

        # RIGHT
        my_box_sizer2 = wx.BoxSizer(wx.VERTICAL)

        my_box_sizer2.Add(self.plotter, 0, wx.ALL | wx.EXPAND, 8)
        my_box_sizer2.Add(self.text_ctrl, 0, wx.ALL |
                          wx.CENTER | wx.EXPAND, 5)

        self.right_Panel.SetSizer(my_box_sizer2)

        self.Show()

    def on_press_set_values(self, event):
        self.MAX_VOLTAGE = float(self.textEntryVoltage.GetLineText(0))
        self.ADC_RESOLUTION = int(self.textResolution.GetLineText(0))

        print("Test Max Voltage set to " + str(self.MAX_VOLTAGE))
        print("ADC resolution set to " + str(self.ADC_RESOLUTION))

    def on_press_measurement(self, event):
        print("Starting measurement procedure")
        # idxDevice, hdwf = dwf_open_first_device_as_analogout()
        dwf_dio, dwf_aio, dwf_do, dwf_di, dwf_ao = dwf_open_first_device()
        #self.to_plot = spi_send_data(dwf_do, dwf_di, dwf_dio)

        # dwf_configure_spi(hdwf, 10)

        waveform_test_channel = 0
        #waveform_test_frequency = 0.1
        #waveform_test_amplitude = 1.0

        # dwf_generate_custom_waveform(dwf_ao, waveform_test_channel, waveform_test_frequency,
        #                            waveform_test_amplitude, test_waveform_ascending_and_descending)

        print("Testing ADC")
        test_adc(dwf_ao, waveform_test_channel, dwf_dio)
        # print("Signal generated for 10 seconds. Started")
        # time.sleep(10)
        # print("Done")
        # idxDevice.close()

        dwf_close_device(dwf_dio, dwf_aio, dwf_do, dwf_di, dwf_ao)

        print("Measurement procedure ended. You can check the results by clicking 'SHOW RESULTS'")

    def on_press_search(self, event):
        print("Searching for devices ... ")
        dwf_search_for_devices()

    def on_press_show_results(self, event):
        print("Plotted ADC results")

        # ADC_data: list of generated data point tuples or list of collected results from AD
        (NUMB_OF_SAMPLES, ADC_data) = generate_quasi_adc_signal(
            self.MAX_VOLTAGE, 5000, self.ADC_RESOLUTION, 15000)

        # Ideal_Voltage_data: list of data points tuples for voltage
        Ideal_Voltage_data = generate_ideal_voltage_data(
            self.MAX_VOLTAGE, NUMB_OF_SAMPLES)

        ADC = plot.PolyMarker(ADC_data, marker='circle',
                              size=0.5, colour='black', legend="ADC data")

        IdealVoltage = plot.PolyLine(
            Ideal_Voltage_data, width=1, colour='red', legend="Ideal Voltage")

        graph = plot.PlotGraphics(
            [ADC, IdealVoltage], 'Graph of ADC results', 'Samples', 'Voltage [V]')

        self.plotter.Draw(graph, xAxis=(0, NUMB_OF_SAMPLES),
                          yAxis=(0, self.MAX_VOLTAGE))

    def on_press_exit(self, event):
        print("Exiting program")
        quit()


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
