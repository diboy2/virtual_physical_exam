import numpy as np
import matplotlib.pyplot as plt


x = []
y = []
file_path = "Text_Recognition_Utilization.log"
with open(file_path, 'r') as f:
    next(f)
    for line in f:
        lines = [i for i in line.split()]
        x.append(float(lines[3]))
        y.append(float(lines[0]))

plt.title("Text Recognition Utilization")
plt.xlabel('Simulation Time')
plt.ylabel('Busy or Idle')
plt.yticks(y)
plt.xticks(np.arange(min(x), max(x)+1, 20.0))
plt.plot(x, y, c = 'b', drawstyle='steps-pre')

plt.show()