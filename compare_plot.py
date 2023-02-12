import numpy as np
import matplotlib.pyplot as plt


x = []
y = []
file_name = "Text_Recognition_Queue_Delay_Time"
file_path = f"./simulation_report/logfiles/{file_name}.log"
with open(file_path, 'r') as f:
    next(f)
    for line in f:
        lines = [i for i in line.split()]
        x.append(float(lines[3])-600)
        y.append(float(lines[0]))

x_2 = []
y_2 = []

file_path = f"./simulation_report/logfiles/{file_name}_2.log"
with open(file_path, 'r') as f:
    next(f)
    for line in f:
        lines = [i for i in line.split()]
        x_2.append(float(lines[3]))
        y_2.append(float(lines[0]))

plt.title("Text Recognition Queue Delay Time Comparison")
# plt.xlabel('Simulation Time')
plt.ylabel('Queue Delay Time')
# plt.xticks(np.arange(min(x), max(x)+1, 20.0))
plt.plot(x, y, c = 'g')
plt.plot(x_2, y_2, c = 'm')
plt.xticks([])
plt.show()