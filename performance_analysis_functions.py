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
    
