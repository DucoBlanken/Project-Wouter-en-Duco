from scipy import stats
from itertools import groupby, cycle 
        
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
            
    def remove_values_from_list(the_list, val):
        return [value for value in the_list if value != val]
    
    for i in range(len(steps) - 1):
        if steps[i] == steps[i + 1] - 1:
            steps[i] = 0
    
    return remove_values_from_list(steps, 0)
