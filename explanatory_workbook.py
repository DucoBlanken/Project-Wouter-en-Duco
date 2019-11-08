# ### Goal

# Our goal was to develop a stepfinder and test its performance on traces that we generate.

# ### Trace generation

# The first part of our project generates a bunch of random traces with discrete displacements we will refer to as steps. It is implemented as a couple of functions:

# %matplotlib inline

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

# If plotted, the traces look like this

# +
import matplotlib.pyplot as plt
import numpy as np

x = np.load('x_data.npy')
N = range(100001)
fig, (axes1, axes2) = plt.subplots(1,2)

for i in range(len(x)):
    axes1.plot(N, x[i,:])
axes1.set_title('Ten traces')
axes1.set_xlabel('Steps')
axes1.set_ylabel('Position x')

axes2.set_title('Zoom-in')
axes2.set_xlabel('Steps')
axes2.plot(range(0,1000),x[i,:1000])

# -

# ### Stepfinder

# Now we need a stepfinder. The goal is to find the steps in our traces, without any previous knowledge of the stuff used to generated the traces (like it is real data). We're going to test it's performance by comparing the outcome (found step times) to the input (set time steps). 

# The step finder compares for each data point the window left and right of this data point using a t-test. When a significant change in the mean position is found, a step is called. However, multiple steps will be called around a real step. Therefore, we select and retain only the first step of a train of consecutive steps and remove the rest. The step finder then returns a list of unique non-consecutive steps.

# +
from scipy import stats
from itertools import groupby, cycle 

def stepfinder(data, window = 10, alpha = 0.05):
    """Step finder using a sliding window t-test to find significant changes
    in mean position between the two windows. If a significant change is found,
    the position is stored in steps. This function returns a list of non-
    consecutive steps, selecting the first step from a consecutive train of
    steps.

    Parameters
    ----------
    data : array
        1D trajectory of a particle
    window : float
        Determines the number of points compared in the t-test
    alpha : float
        The value used to either accept or reject the null hypothesis in the 
        t-test: the means of the two windows do not differ significantly

    Returns
    -------
    An list of the positions where the null hypothesis was 
    rejected. From a consecutive train of steps, only the first step is 
    retained.
    """
    pass

    # Funtion to perform the data selection used in the t-test
    
    def apply_window(i):
        return (data[(i - window) : i], data[i : (i + window)])
    
    # Function to remove specific values from a list (the 0 entries from the
    #                                                 steps-list)
    
    def remove_values_from_list(the_list, val):
        return [value for value in the_list if value != val]
    
    # Check whether data set is large enough to be tested
    
    assert len(data) > 2 * window
    
    # Applying t-test to data points
    
    alpha = alpha/len(data)
    steps = list()
    for i in range(window + 1,len(data) - window):
        # determine if there is a significant change in mean position: if there
        # is, the position is saved in steps
        current_p_value = stats.ttest_ind(*apply_window(i))[1]
        if current_p_value < alpha:
            steps.append(i)
            
    # Check whether the step finder is not too sensitive
    
    assert len(steps) < len(data)/window
    
    # Make sure all directly consecutive steps are taken together
    
    for i in range(len(steps) - 1):
        if steps[i] == steps[i + 1] - 1:
            steps[i] = 0
    
    # Return the list of non-consecutive steps
    
    return remove_values_from_list(steps, 0)


# -

# ### Testing the performance of our stepfinder

# To determine the performance of our step finder, we wrote a function (determine_performance) that takes as input the found t_steps and the actual t_steps and determines the percentage of steps correctly identified, as well as the number of false positives. We permit an error of $\eta$, which is one timepoint by default.

# +
import numpy as np
def find_nearest(array, value):
    """ finds nearest point in an array to a certain value
    
    Parameters
    ----------
    array: an array
    value: a value
    
    Output
    ---------
    the closest point
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def determine_accuracy(t_step_found,t_step):
    """ For every actual step, see how close the closest found step is
    
     Parameters
    ----------
    t_step_found: the steps as found by the stepfinder
    t_step: the actual steps, knowledge from simulation

    
    Output
    ---------
    an array with the distance to the nearest found step for every actual step
    """
    accuracy = np.zeros(len(t_step_found))
    for j in range(len(t_step_found)):
        accuracy[j] = abs(find_nearest(t_step,t_step_found[j])-t_step_found[j])
    return  accuracy

def determine_performance(t_step_found,t_step, etha  = 1):
    """ determines some performance parameters for the peak finder
    
         Parameters
    ----------
    t_step_found: the steps as found by the stepfinder
    t_step: the actual steps, knowledge from simulation
    etha: permitted error to still be an accurate peak find, default 1

    
    Output
    ---------
    percentage_peaks_found: percentage of the peaks in t_peaks that is correctly identified in t_peak_founds
    false positives: peaks found that are not peaks
    """
    accuracy = determine_accuracy(t_step_found,t_step)
    percentage_peaks_found  = sum(accuracy<=etha)/len(t_step)*100
    false_positives = sum(accuracy>etha)
    return percentage_peaks_found, false_positives 


# -

# Applying this function on a set of 100 traces generated with the trace generator and analysed with the stepfinder yields the following results. (Since this script takes very long, we will load results generated yesterday.) Over 90% of the peaks in this kind of data can be identified accurately, with a low number of false positives.

# +
import numpy as np
import matplotlib.pyplot as plt

percentage_peaks_found = np.loadtxt('percentage_peaks_found.txt')
fig, (axes1, axes2) = plt.subplots(1,2)
axes1.hist(percentage_peaks_found)
axes1.set_xlim([0,100])
axes1.set_xlabel('Percentage of peaks found (%)')
axes1.set_ylabel('Counts')

false_positives = np.loadtxt('false_positives.txt')
axes2.hist(false_positives)
axes2.set_xlim([0,10])
axes2.set_xlabel('Number of false positives')
axes2.set_ylabel('Counts')
# -

# ### Challenging the stepfinder: traces with more noise

# Finally, we challenge the stepfinder by feeding it a set of increasingly noisy traces. Since we made all those functions before, this can be executed in only a couple lines of code:

# +
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


# +
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib widget

noise_size= np.arange(0,8,0.5)

mean_percentage_found = np.loadtxt('mean_percentage_found.txt')
std_percentage_found = np.loadtxt('std_percentage_found.txt')

mean_false_positives = np.loadtxt('mean_false_positives.txt')
std_false_positives = np.loadtxt('std_false_positives.txt')

fig, (axes1, axes2) = plt.subplots(1,2)
axes1.set_xlabel('Noise size')
axes1.set_ylabel('Percentage of peaks found')
axes1.errorbar(noise_size,mean_percentage_found,std_percentage_found)


axes2.set_xlabel('Noise size')
axes2.set_ylabel('False positives')
axes2.errorbar(noise_size,mean_false_positives,std_false_positives)

# +
import numpy as np
import matplotlib.pyplot as plt

from trace_generator_functions import trace_generator
N = np.linspace(0, 1, 1001)

base = 100
step_size = 10
number_of_traces = 1
t_step_up = [200, 500, 800]
t_step_down = [400, 900]
fig, (axes1, axes2,axes3) = plt.subplots(1,3)
noise_size  =1
x = trace_generator(N,base,step_size, noise_size,t_step_up,t_step_down)
axes1.plot(N,x)
axes1.set_ylim([80,140])
axes1.set_title("noise size  = 1")

noise_size  =2.5
x = trace_generator(N,base,step_size, noise_size,t_step_up,t_step_down)
axes2.plot(N,x)
axes2.set_ylim([80,140])
axes2.set_title("noise size  = 2.5")
noise_size  =5
x = trace_generator(N,base,step_size, noise_size,t_step_up,t_step_down)
axes3.plot(N,x)
axes3.set_ylim([80,140])
axes3.set_title("noise size  = 5")
# -




