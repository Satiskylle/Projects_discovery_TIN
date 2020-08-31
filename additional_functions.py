import random


class RedirectText:
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)


def generate_ideal_voltage_data(max_voltage, num_of_samples):
    voltage = []
    voltage.append((0, 0))
    for a in range(1, num_of_samples):
        voltage.append((a, a*max_voltage/num_of_samples))

    return (voltage)


def generate_quasi_adc_signal(max_voltage, adc_frequency, adc_resolution, sampling_freq):
    '''
    @brief Generates signal simmiliar as adc's while sampled
    @param [in] max_voltage - reference voltage for ads (Vmax - may be vsupply)
    @param [in] adc_frequency - frequency how fast adc can sample values
    @param [in] adc_resolution - resolution of adc
    @param [out] num_of_samples - returned number of data
    @param [in] sampling_freq - frequency of sampling adc return value
    '''
    y_sigma = 0.05
    x_offset = 0  # offset in number of samples
    gain_distortion = 0  # add gain distortion (not linear gain)
    chance_for_lost_step = 0.05  # chance for step lost. Minimal value is 0.001

    data_need_to_be_copied = (int)(sampling_freq / adc_frequency)
    proper_gain_value_each_step = max_voltage/(2**adc_resolution)
    num_of_samples = round(
        (max_voltage / proper_gain_value_each_step * data_need_to_be_copied) + 0.5)
    table = [None] * num_of_samples
    for a in range(-1, x_offset):
        table[a+1] = y_sigma * random.randint(0, 1)

    for i in range(x_offset, num_of_samples, data_need_to_be_copied):
        if random.randint(0, 1000) < (chance_for_lost_step*1000):
            i = i-data_need_to_be_copied

        for q in range(0, data_need_to_be_copied):
            proper_value = proper_gain_value_each_step * \
                (i - x_offset) * (gain_distortion + 1) / data_need_to_be_copied

            # protect from overvoltage return
            if proper_value > max_voltage:
                proper_value = max_voltage - proper_gain_value_each_step

            table[i+q] = proper_value

    # change values to list of tuples for graph
    output_data = []
    sample_nb = 0
    for t in table:
        output_data.append((sample_nb, t))
        sample_nb += 1

    return(num_of_samples, output_data)
