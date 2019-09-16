#!/usr/bin/env python


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import scipy.interpolate
import matplotlib.cm as cm

import csv

data = csv.reader(open('output2panel.csv', 'rb'), delimiter = ',')

mydata = np.genfromtxt('output2panel.csv', delimiter = ',')

xs = []
ys = []
zs = []

for row in data:
 xs.append(float(row[1]))
 ys.append(float(row[0]))
 zs.append(float(row[2]))


##xys = zip(xs, ys)

#z = zip(xys, zs)

X = np.array(xs)
Y = np.array(ys)
Z = np.array(zs)

xi, yi = np.linspace(X.min(), X.max(), np.sqrt(len(zs))), np.linspace(Y.min(), Y.max(), np.sqrt(len(zs)))

#lev = np.arange(0.30, 0.45, 0.05)

zi = scipy.interpolate.griddata((X, Y), Z, (xi[None,:], yi[:, None]), method = 'cubic')

#lev = [.30, .35, .40, .45]

CS = plt.contour(xi, yi, zi)
plt.clabel(CS, inline = 1,  fontsize=10)

plt.show()
