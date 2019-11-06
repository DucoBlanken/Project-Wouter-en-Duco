import matplotlib.pyplot as plt
import numpy as np
from trace_generator_functions import step_generator, trace_generator

N = np.linspace(0,1,100001)
base = 10000
step_size = 10
noise_size = 1
number_of_steps_up = 550
number_of_steps_down = 450
number_of_traces = 1


fig, axes1 = plt.subplots()
x = np.zeros((number_of_traces,len(N)))
for i in range(number_of_traces):
    t_step_up = step_generator(N,number_of_steps_up)
    t_step_down= step_generator(N,number_of_steps_down)
    x[i,:] = trace_generator(N,base,step_size, noise_size,t_step_up,t_step_down)
    
    axes1.plot(N, x[i,:])
    
axes1.set_ylim(9000, 12000)
axes1.set_xlim(0, 1)
axes1.set_xlabel('time (a.u.)')
axes1.set_ylabel('x (a.u.)')

