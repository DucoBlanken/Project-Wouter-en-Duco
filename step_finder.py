from scipy import stats
import numpy as np
        
def simple_test_data(size = 100):
    data = np.array(range(size))
    return data

def stepfinder(data, window = 10, alpha = 0.05):
    

    # A simple step finder
    
    # For each data point, a t-test is conducted comparing a set points before and
    # after the tested data point
    

    steps = np.zeros(len(data) - 2 * window)
    for i in range(1,len(steps)):
        if stats.ttest_ind(data[(i - window) : i], data[i : (i + window)])[1] < 0.05:
            steps[i] = i + window

    steps = steps[steps != 0]
    return steps

