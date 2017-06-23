import csv
import numpy as np
import matplotlib.pyplot as plt
 
data = np.genfromtxt('../data/data.txt', dtype = str, delimiter='	')
data = np.transpose(data)
len = len(data[0])
price = 5
p = data[24][1:]
for i in range(len-1):
	if p[i] == 'VL':
		p[i] = 1
	elif p[i] == 'L':
		p[i] = 2
	elif p[i] == 'M':
		p[i] = 3
	elif p[i] == 'H':
		p[i] = 4
	else:
		p[i] = 5
p = np.array(p, dtype = int)
p = (p-np.mean(p))/np.std(p)
 
s = data[22][1:]
s = np.array(s, dtype = float)
s = np.array(s, dtype = int)
s = (s-np.mean(s))/np.std(s)
 
X = (np.vstack((p,s)))
print(np.cov(X))