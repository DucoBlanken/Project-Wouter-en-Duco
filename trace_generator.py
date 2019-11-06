import matplotlib.pyplot as plt
import numpy as np

N = np.linspace(0,1,1001)
base = 10
t_step_up = np.array([500,600])
t_step_down= np.array([300,700])
step_size = 10
noise_size = 3


x_base = base
x_noise = np.random.rand(len(N))*noise_size

x_step=np.zeros((len(t_step_up)+len(t_step_down),len(N)))

for i in range(0,len(t_step_up)):
    x_step[i,t_step_up[i]::] = step_size
    
for i in range(0,len(t_step_down)):
    x_step[i+len(t_step_up),t_step_down[i]::] = -step_size
    
    
x_step = np.sum(x_step, axis=0)






fig, axes = plt.subplots()
axes.plot(N, x_noise+x_base+x_step,'ok')
axes.set_ylim(0, 50)

