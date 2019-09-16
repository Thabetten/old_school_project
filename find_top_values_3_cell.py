#!/usr/bin/env python


from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import scipy.interpolate
import matplotlib.cm as cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import pandas as pd

full_data=pd.read_csv('outputnpanel.csv', header=None, names=['p1', 'p2', 'p3', 'efficiency'])

filtered_data= full_data[(full_data['efficiency']>=0.43)] #&& (full_data['']==2.4)]

#print(filtered_data['efficiency'])


topn = full_data.nlargest(150, 'efficiency')


print topn


#import csv

#with open("output3panelmaxes.csv", "wb") as csvfile:
# writer = csv.writer(csvfile, delimiter=',')
# writer.writerows(triplelist)


topn.to_csv('maxima from spanels.csv')



#print len(topn)