import numpy as np
import matplotlib.pyplot as plt
from step_finder import stepfinder
from performance_analysis_functions import determine_performance
x = np.load('x_data.npy',allow_pickle=True)
t_step = np.load('t_step_data.npy',allow_pickle=True)


percentage_peaks_found = np.zeros(len(x))
false_positives = np.zeros(len(x))
 
for j in range(len(x)):
    t_step_found = stepfinder(x[j,:],window = 10, alpha =0.05)
    percentage_peaks_found[j], false_positives[j]  = determine_performance(t_step_found,t_step[j], etha  = 1)


#fig, axes = plt.subplots()
#axes.plot(x[0,:])
#axes.plot(t_step_found,x[0,t_step_found],'or')
#axes.set_xlim((0,1000))
#axes.set_ylim((9900,10100))


#print('percentage peaks found is',percentage_peaks_found, 'with', false_positives, 'false positives')
