import random


def generate_bad_adc_mock_values(max_voltage, num_of_samples):
    sigma = 0.05
    genera_var = []
    voltage = []
    genera_var.append((0, random.randint(0, 5) * sigma))
    voltage.append((0, 0))
    for a in range(1, num_of_samples):
        genera_var.append((a, (round(a + a*random.randint(-1, 5) *
                                     sigma/20)) * max_voltage/num_of_samples))
        voltage.append((a, a*max_voltage/num_of_samples))

    return (genera_var, voltage)
