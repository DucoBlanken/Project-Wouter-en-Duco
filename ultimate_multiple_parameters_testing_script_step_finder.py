from trace_generator_functions import trace_simulator
from step_finder import stepfinder
from performance_analysis_functions import determine_performance
import numpy as np

N = np.linspace(0, 1, 100001)
base = 10000
step_size = 10
number_of_traces = 5
max_number_of_steps = 1000
mean_percentage_found = []
std_percentage_found = []
mean_false_positives = []
std_false_positives =[]

for noise_size in np.arange(0, 8, 0.5):
    x, t_step = trace_simulator(N,base,step_size,noise_size,number_of_traces,max_number_of_steps)
    percentage_peaks_found = np.zeros(number_of_traces)
    false_positives = np.zeros(number_of_traces)
    for j in range(number_of_traces):
        t_step_found = stepfinder(x[j,:])
        percentage_peaks_found[j], false_positives[j] = determine_performance(t_step_found,t_step[j], etha  = 1)
     
    mean_percentage_found.append(np.mean(percentage_peaks_found))
    std_percentage_found.append(np.std(percentage_peaks_found))
    mean_false_positives.append(np.mean(false_positives))
    std_false_positives.append(np.std(false_positives))
