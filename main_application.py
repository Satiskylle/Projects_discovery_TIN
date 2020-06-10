import wx
from AD_functions import * 

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="ADC TESTER")
        panel = wx.Panel(self)
        
        my_box_sizer = wx.BoxSizer(wx.VERTICAL)

        btnDeviceSearch = wx.Button(panel, label="Search for device")
        btnDeviceSearch.Bind(wx.EVT_BUTTON, self.on_press_search)
        my_box_sizer.Add(btnDeviceSearch, 0, wx.ALL | wx.CENTER, 5)
        
        btnStartMeasurement = wx.Button(panel, label="Start Measurement")
        btnStartMeasurement.Bind(wx.EVT_BUTTON, self.on_press_measurement)
        my_box_sizer.Add(btnStartMeasurement, 0, wx.ALL | wx.CENTER, 5)

        btnExit = wx.Button(panel, label="Exit")
        btnExit.Bind(wx.EVT_BUTTON, self.on_press_exit)
        my_box_sizer.Add(btnExit, 0, wx.ALL | wx.CENTER, 5)

        #btnSetConfiguration = wx.Button(panel, label="Set Configuration")
        #btnSetConfiguration.Bind(wx.EVT_BUTTON, self.on_press)
        #my_box_sizer.Add(btnSetConfiguration, 0, wx.ALL | wx.CENTER, 5)
        
        self.text_ctrl = wx.TextCtrl(panel)
        my_box_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(my_box_sizer)
        self.Show()

    def on_press_measurement(self, event):
        idxDevice = dwf_open_first_device_as_analogout()
        
        waveform_test_channel = 0
        waveform_test_frequency = 0.1
        waveform_test_amplitude = 1.0
        
        #dwf_generate_custom_waveform(idxDevice, waveform_test_channel, waveform_test_frequency,
                        #waveform_test_amplitude, test_waveform_ascending_and_descending)

        test_adc(idxDevice, waveform_test_channel)
        print("Signal generated for 10 seconds. Started")
        time.sleep(10)
        print("Done")
        idxDevice.close()
            
    def on_press_search(self, event):
        dwf_search_for_devices()

    def on_press_exit(self, event):
        exit_program(exit_cases.END_OF_PROGRAM)
        
if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
