import numpy as np
from step_finder import stepfinder

x = np.load('x_data.npy',allow_pickle=True)
t_step = np.load('t_step_data.npy',allow_pickle=True)


t_step_found = stepfinder(x[0,:],window = 10, alpha = 0.05)


fig, axes = plt.subplots()
axes.plot(x[0,:])
axes.plot(t_step_found,x[0,t_step_found],'or')
axes.set_xlim((0,1000))
axes.set_ylim((9900,10100))


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

accuracy = np.zeros(len(t_step[0]))
for j in range(len(t_step[0])):
    accuracy[j] = abs(find_nearest(t_step_found,t_step[0][j])-t_step[0][j])