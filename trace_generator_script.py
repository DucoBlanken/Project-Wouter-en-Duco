import matplotlib.pyplot as plt
import numpy as np
from trace_generator_functions import trace_simulator

N = np.linspace(0,1,100001)
base = 10000
step_size = 10
noise_size = 1
max_number_of_steps =1000
number_of_traces = 10


x, t_step = trace_simulator(N,base,step_size,noise_size,number_of_traces,max_number_of_steps)


for i in range(0,number_of_traces):
    plt.plot(N,x[i,:])
    
np.save('x_data', x)
np.save('t_step_data', t_step)





