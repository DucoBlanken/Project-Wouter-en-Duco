import matplotlib.pyplot as plt
import numpy as np





def trace_generator(N,base,step_size, noise_size,t_step_up,t_step_down):
    """ traces are generated based on your input
        N: number of data points
        base: base line of trace
        step_size: displacement of an individual step
        noise_size: size of the noise
        t_step_up: numpy array containing time points of UPWARD steps
        t_step_down: numpy array containing time points of DOWNWARD steps
        """
    x_base = base
    x_noise = np.random.randn(len(N))*noise_size

    x_step=np.zeros((len(t_step_up)+len(t_step_down),len(N)))

    for i in range(0,len(t_step_up)):
        x_step[i,t_step_up[i]::] = step_size
    
    for i in range(0,len(t_step_down)):
        x_step[i+len(t_step_up),t_step_down[i]::] = -step_size
    
    
    x_step = np.sum(x_step, axis=0)
    return x_noise+x_base+x_step

def step_generator(N,number_of_steps):
    Q = np.floor(np.random.rand(number_of_steps)*len(N))
    return Q.astype('int')



N = np.linspace(0,1,100001)
base = 10000
step_size = 10
noise_size = 1
number_of_steps_up = 550
number_of_steps_down = 450
number_of_traces = 100


fig, (axes1, axes2) = plt.subplots(1,2)
x = np.zeros((number_of_traces,len(N)))
for i in range(number_of_traces):
    t_step_up = step_generator(N,number_of_steps_up)
    t_step_down= step_generator(N,number_of_steps_down)
    x[i,:] = trace_generator(N,base,step_size, noise_size,t_step_up,t_step_down)
    axes1.plot(N, x[i,:])
    axes1.set_ylim(9000, 12000)
    axes1.set_xlim(0, 1)
    
axes2.hist(np.mean(x,axis=1))


