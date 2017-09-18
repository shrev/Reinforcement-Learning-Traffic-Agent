import matplotlib.pyplot as plt
import numpy as np

wta = np.loadtxt("wta")
qla = np.loadtxt("qla")

x = range(1,1001)

'''
temp = 1000*[0]

for i in range(200,1000):
  temp[i] = i




wtan = wta -temp
'''

wtan = np.loadtxt("wta_exp4")
plt.plot(x,wta,'b')
plt.plot(x,wtan[0:1000],'r')
plt.xlabel("Simulation Step")
plt.ylabel("Waiting Time (ms)")
plt.show()



