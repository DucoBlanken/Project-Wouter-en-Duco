import matplotlib.pyplot as plt
import numpy as np
from trace_generator_functions import step_generator, trace_generator

N = np.linspace(0,1,100001)
base = 10000
step_size = 10
noise_size = 1
# number_of_steps_up = int(np.random.rand(1)*1000)
# number_of_steps_down = int(np.random.rand(1)*1000)
number_of_traces = 10


fig, axes1 = plt.subplots()
x = np.zeros((number_of_traces,len(N)))
for i in range(number_of_traces):
    t_step_up = step_generator(N,int(np.random.rand(1)*1000))
    t_step_down= step_generator(N,int(np.random.rand(1)*1000))
    x[i,:] = trace_generator(N,base,step_size, noise_size,t_step_up,t_step_down)
    
    axes1.plot(N, x[i,:])
    axes1.set_xlim(0, 1)
    axes1.set_xlabel('time (a.u.)')
    axes1.set_ylabel('x (a.u.)')
    
    t_step= np.concatenate((t_step_up, t_step_down))
    print(len(t_step))
np.savetxt('x_data.dat', x)




t_step = np.concatenate((t_step_up, t_step_down))
print(len(t_step))







