import matplotlib.pyplot as plt
import numpy as np

print('hello world')

x = np.linspace(0, 2 * np.pi, 101)
y = np.sin(x)

fig, axes = plt.subplots()
axes.plot(x, y,'ok')
