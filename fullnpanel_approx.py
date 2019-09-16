#!/usr/bin/env python



import numpy as np
import scipy as scy
import bisect as bis
import numpy as np
import sys
import pandas as pd
import heapq as hp


##################################### DESCRIPTION ####################################

#This is a program designed to find clusters of efficiency in multi-junction non-current matching solar panels using the measured 
#solar spectrum and generated combinations of photo cells with band gaps in descending order of value

#Input includes the max and min energy thresholds for each band in a solar panel

#The output of script is a file containing each bandgaps for each cell in descending order in the stack and the calculated efficiency.

#constants are electron charge (eperc), the speed of light (c), Planck's constant (h)

#nmet is a list of wavelengths of solar radiation in nanometers, photflux the density of photons at that wavelength, and photnrg the energy at that wavelength

#gap_combos takes generated length N combinations of band_gaps in descending order (I.E. [3,2,1] is permissible but not [2,3,1])

#contains each element from gap_combos with the calculated efficiency of energy conversion added at the end.


##################################### USER INPUT #####################################

#input format- list of tuples
#each tuple represents a different band in the panel
#first value of tuple is the max energy accepted by band
#second value of tuple is the minimum energy accepted by band
bands_ranges_input = [(4, 1.5), (3, .7), (2, 0.5)]

#the energy spacing we want to use for our analysis
#e.g.- if set to 0.1, then the efficiency will be calculated for every in range using 0.1 unit incraments
brand_voltage_spacing = 0.05

#The variable top_values will specify how many of the highest efficiency combinations are printed

top_values_input = 20

########################################################################################



#using the user input, we will construct the band ranges array
band_ranges_general=[]
for i in range(len(bands_ranges_input)):
    band_ranges_general.append(np.arange(bands_ranges_input[i][0], bands_ranges_input[i][1], -1*brand_voltage_spacing))
 

eperc = 1.602*10**-19

c = 2.996*10**8

h = 6.626*10**-34

hep = h/eperc

thermlim = 0.687

nmet = []

photflux = []

photnrg = []

Nlist = []

gap_combos = []

import csv

#file containing a table of wavelengths of solar radiation in nanometers, 
with open('nanometers.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
                for i in row:
                        nmet.append(float(i))

#This os the energy of the photons at a given wavelength
import csv
with open('phoenergyev.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
                for i in row:
                        photnrg.append(float(i))
#This is the number of photons at a given wavelength
import csv
with open('phoflux.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
                for i in row:
                        photflux.append(float(i))

#The data is brought from CSV files and changed to arrays

enar = np.asarray(photnrg)
nmar = np.asarray(nmet)
flar = np.asarray(photflux)


#Allowed ranges for band gaps in each cell are determined, these are samples for testing band_ranges_general

band_ranges_4 = [np.arange(4, 1.9, -0.1), np.arange(3, .9, -0.1), np.arange(2.5, .9, -0.1), np.arange(2, .4, -0.1)]

band_ranges_3 = [np.arange(4, 2, -0.05), np.arange(3.5, 1, -0.05), np.arange(3, 0.5, -0.05)]


def interp(w,t):

#This interpolates and estimates the photon density at a point between two of the measured points of photon density 
#per unit wavelength
#INPUT w (integer) w is the wavelength between 
#INPUT t (integer) this is the index of the first wavelength entry in the measured list longer than the wavelength associated with the bandgap
#OUTPUT (integer) Trapezoidal numerical integration is so assuming photon density changes linearly between two measured wavelengths
#this gives a height to a new trapezoid or an estimation of photon density at a non measured point. Here "m" is the slope "b" the "intercept"
#for a line forllowing form y = mx + b

 m = (flar[t] - flar[t - 1])/(nmar[t] - nmar[t - 1])

 b = flar[t] - m*nmar[t]
 return m*w + b

#aflist will take a list of tuples and makes new combinations 

def aflist(x, k):
    emp = []
    for y in gap_combos:
        for z in k[x]:
            if y[x - 1] > z:
                emp.append(y + [z])
    del gap_combos[:]
    for g in emp:
        gap_combos.append(g)

#This makes an initial list of tuples then calls aflist to make the full list of band gap combinations

def make_all(m):
    i = 0
    while i < len(m):
        if i == 0:
            for v in m[0]:
                gap_combos.append([v])
        else:
            aflist(i, m)
        i += 1
        pass

#Calc_pow calculates the power output from the combination of band gaps using numerical integration to find the 
#number of photons that cause an electron to be ejected from a panel and multiplying it by the gap voltage.
#The calculated power is in watts but is converted to a percentage of power converted for the output.
#thermlim is the theoretical thermodynamic limit for power converted based on the carnot cycle


def calc_pow(n):
    i = 0
    pwr = 0
    while i < len(n):
        if i == 0:
            wvlen = ((hep*c)/n[0])*10**9
            in1 = bis.bisect(nmar, wvlen)
            nsl1 = nmar[0:in1 - 1]
            fsl1 = flar[0:in1 - 1]
            pwr +=  thermlim*0.9*(((wvlen - nmar[in1 - 1])*(interp(wvlen, in1) + flar[in1 - 1])/2) + np.trapz(fsl1, nsl1))*n[0]*eperc* .9
        else:
            wvlent = ((hep*c)/n[i - 1])*10**9
            wvlenb = ((hep*c)/n[i])*10**9
            in1 = bis.bisect(nmar, wvlent)
            in2 = bis.bisect(nmar, wvlenb)
            nsl2 = nmar[in1:in2 -1]
            fsl2 = flar[in1:in2 -1]
            addin = ((nmar[in1] - wvlent)*(flar[in1] + interp(wvlent, in1)/2)) + (wvlenb - nmar[in2 - 1])*((interp(wvlenb, in2) + flar[in2])/2)
                #print len(nsl2), len(fsl2)
            pwr +=  thermlim*0.9*(addin + np.trapz(fsl2, nsl2))*n[i]*eperc* .9
        i += 1
        #print pwr/977.67, i, i - 1
    Nlist.append(n + [pwr/977.67])

##977.67 is the approximate total power of solar radiation incident on one square meter division in the above function normalizes the power to a percent.



#make_all(band_ranges_3)

#calc_pow(gap_combos[10])




def all_calc(g):
    make_all(g)
    for u in gap_combos:
        calc_pow(u)


def find_top(x):
	listo = zip(*x)
	s = pd.Series(listo[len(listo)-1])
	topn = s.nlargest(top_values_input)
	print topn

def graphs():
 	if len(bands_ranges_input) == 2:
 		import contour_plot
 	elif len(bands_ranges_input) == 3:
 		import threedscatter
 	else:
 		return "Too large to graph."


all_calc(band_ranges_general)

find_top(Nlist)

graphs()

#This is the output with the band gap combinations and corresponding efficiencies. It can be read in Microsoft excel or libre calc
with open("output" + str(len(bands_ranges_input)) + "panel.csv", "wb") as csvfile:
 writer = csv.writer(csvfile, delimiter=',')
 writer.writerows(Nlist)##

 