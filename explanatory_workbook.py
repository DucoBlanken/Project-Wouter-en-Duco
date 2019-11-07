# The first part of the script generates a bunch of random traces, as couple of functions:

# +
import numpy as np

def trace_generator(N,base,step_size, noise_size,t_step_up,t_step_down):
    """ a single trace is generated based on your input
    
        Parameters
        ----------------
        N:          integer
                    number of data points
        base:       float
                    base line of trace
        step_size:  float
                    displacement of an individual step
        noise_size: float
                    size of the noise
        t_step_up:  numpy array 
                    containing time points of UPWARD steps
        t_step_down:numpy array 
                    containing time points of DOWNWARD steps
        
        Returns
        -----------------
        a trajectory x
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



def trace_simulator(N,base,step_size,noise_size,number_of_traces,max_number_of_steps):
    """ multiple traces are generated based on your input
    
        Parameters
        ----------------
        N:          integer
                    number of data points
        base:       float
                    base line of trace
        step_size:  float
                    displacement of an individual step
        noise_size: float
                    size of the noise
        number_of_traces: int
                    the number of traces to simulate
        max_number_of_steps: int
                    a random fraction of this number will be number of steps, both for up and down
        
        Returns
        -----------------
        x: a set of trajectories 
        t_step: for every trajectory, the exact time of the steps
        """
    t_step = []
    x = np.zeros((number_of_traces,len(N)))
    for i in range(number_of_traces):
        t_step_up = step_generator(N,int(np.random.rand(1)*max_number_of_steps))
        t_step_down= step_generator(N,int(np.random.rand(1)*max_number_of_steps))
        x[i,:] = trace_generator(N,base,step_size, noise_size,t_step_up,t_step_down)
    
    
        t_step.append(np.concatenate((t_step_up, t_step_down)))
    return x, t_step



# -

# We can use a little script to generate a set of these traces, like this:

# +
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
# -

# It takes a while, so let's not do that. Fortunately, we've saved the most important parts of the data. 
#
# x_data: an array with the traces 
#
# t_step_data: an array with where we added steps to our traces 

# Now we have a stepfinder. The goal is to find the steps in our traces, without any previous knowledge of the stuff used to generated the traces (like it is real data). We're going to test it's performance by comparing the outcome (found step times) to the input. 


