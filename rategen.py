import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import random
from scipy.stats import invweibull
from scipy.stats import burr
from random import randint


secondsInHour = 60.0*60.0
c = 5.8
x = np.linspace(invweibull.ppf(0.01, c),invweibull.ppf(0.99,c),720)
arr = invweibull.pdf(x, c)
q = arr*10
q = np.round(q)
q = q.astype(int)

c = 5.9
d = 1.4
x = np.linspace(burr.ppf(0.01, c,d),burr.ppf(0.99,c,d),900)
arr = burr.pdf(x, c,d)
b = arr*10
b = np.round(b)
b = b.astype(int)





edges = ['D1 D4', 'D1  D3', 'D7  D5', 'D7 D2', 'D8 D5', 'D8 D2', 'D6 D3', 'D6 D4', 'D7  D4', 'D8 D3', 'D6 D5', 'D1 D2']

	
with open('rl.invw.rou.xml', 'w') as routes:
		routes.write("""<?xml version="1.0"?>""" + '\n' + '\n')
		routes.write("""<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">""" + '\n')
		routes.write('\n')
		routes.write("""<vType id="type1" color="255,105,180"/>""" + '\n')
		routes.write("""<vType id="type0" color="0,255,255"/>""" + '\n')
		routes.write('\n')	
		for i in range(12):
			routes.write("""<route id=\"""" + str(i) + """\"""" + """ edges=\"""" + edges[i] + """\"/> """ + '\n')
		routes.write('\n')
		idCounter = 0
		rval=0
                ival=0
                lrc =-1
                tc=-1
                ic =0
		for i in range(3600):
                        if((i%4!=0)and(i%5!=0)):
                        	continue
                        if(i%5==0):
				rval = randint(0,7)
                                lrc = lrc+1
                                ival = q   
                                ic = lrc                            
                        if(i%4==0):
				rval = randint(8,11)
                                tc = tc+1
				ival = b  
                                ic = tc
			for y in range(ival[ic]):
				if (idCounter%2==1):
					color = """ color=\"255,105,180\""""
					vType = """\" type=\"type1"""
				else:
					color = """ color=\"0,255,255\""""
					vType = """\" type=\"type0"""
				routes.write("""<vehicle id=\"""" + str(idCounter) + """\" depart=\"""" + str(i) + """\" route=\"""" + str(rval) + vType + """\"/>""" + '\n')
	 			idCounter += 1
		routes.write("""</routes>""")	  
  




