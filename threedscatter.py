#!/usr/bin/env python


from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import scipy.interpolate
import matplotlib.cm as cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import pandas as pd

#This data is taken from the outful of fullnpanel_approx

full_data=pd.read_csv('output3panel.csv', header=None, names=['top_panel', 'middle_panel', 'lower_panel', 'efficiency'])

#This was used to filter data given certain efficiencies.

filtered_data= full_data[(full_data['efficiency']>=0.43)] #&& (full_data['middle_pannel']==2.4)]



nconsidered = full_data.nlargest(50000, 'efficiency')





nconsidered.to_csv('maxima from spanels.csv')





xi = nconsidered['top_panel']
yi = nconsidered['middle_panel']
zi = nconsidered['lower_panel']
ei = nconsidered['efficiency']


fig = plt.figure()

ax = fig.add_subplot(111,projection='3d')


colmap = cm.ScalarMappable(cmap=cm.hsv)
colmap.set_array(ei)




yg = ax.scatter(xi, yi, zi, c=cm.hsv(ei/max(ei)), marker='o')
cb = fig.colorbar(colmap)

ax.set_xlabel('Top Panel (eV)')
ax.set_ylabel('Middle Panel (eV)')
ax.set_zlabel('Lower Panel (eV)')


plt.show()


