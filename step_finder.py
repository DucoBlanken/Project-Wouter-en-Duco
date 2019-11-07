from scipy import stats
import numpy as np
        
def simple_test_data(size = 100):
    data = np.array(range(size))
    return data

def stepfinder(data, window = 10, alpha = 0.05):
    """Step finder using a sliding window t-test to find significant changes
    in mean position between the two windows. If a significant change is found,
    the position is stored in steps.

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
    An array called 'steps' of the positions where the null hypothesis was 
    rejected
    """
    pass

    # A simple step finder
    
    def apply_window(i):
        return (data[(i - window) : i], data[i : (i + window)])
    
    
    # Check whether data set is large enough to be tested
    assert len(data) > 2 * window
    
    alpha = alpha/len(data)
    #steps = np.zeros(len(data))
    steps = list()
    for i in range(window + 1,len(data) - window):
        # determine if there is a significant change in mean position: if there
        # is, the position is saved in steps
        if stats.ttest_ind(*apply_window(i))[1] < 0.05:
            #steps[i] = i
            steps.append(i)

   # steps = steps[steps != 0]
    assert len(steps) < len(data)/10
    return steps

