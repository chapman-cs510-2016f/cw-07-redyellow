#!/usr/bin/env python3

import cplane_np
import numpy as np
import pandas as pd
import csv
import json
import matplotlib.pyplot as plt

class JuliaPlane(cplane_np.ComplexPlaneNP):

	def set_f(self,c=-1.037 + 0.17j):
		'''
		Reset the transformation function f.
	     Refresh the plane as needed.
		'''
		self.f=cplane_np.julia(c)
		self.refresh()
		return 0

	def show(self,c=-1.037 + 0.17j):
		self.set_f(c)
		plt.imshow(self.plane, interpolation='bicubic', cmap='hot', origin='lower',extent=[self.xmin,self.xmax,self.ymin,self.ymax],label=c)
		plt.legend(loc='upper left')


	def toCSV(self,filename):
		myfile=open(filename, 'w')
		wr=csv.writer(myfile,delimiter='\n',quoting=csv.QUOTE_ALL)
		c=-1.037 + 0.17j
		self.set_f(c)
		Parameters=['xmin: %d, xmax: %d, xlen: %d, ymin: %d, ymax: %d, ylen: %d, c: %s' % (self.xmin, self.xmax, self.xlen, self.ymin, self.ymax, self.ylen, str(c))]
		wr.writerow(Parameters)
		wr.writerow(self.plane)
		myfile.close()
	
	def fromCSV(self, filename):
		'''
		open CSV file and read all the rows into a temporary dictionary
		'''
		myfile=open(filename, 'r')
		rd=csv.DictReader(myfile)  #http://howtodoinjava.com/python/python-read-write-csv-files/
		for row in rd:
			pr=row
		myfile.close()	
		'''
		get the value of each parameters
		'''
		self.xmin=int(pr['xmin'])
		self.xmax=int(pr['xmax'])
		self.xlen=int(pr['xlen'])
		self.ymin=int(pr['ymin'])
		self.ymax=int(pr['ymax'])
		self.ylen=int(pr['ylen'])
		c=complex(pr['c'])
		'''
		reset default fuction, and refresh the plane at the sametime.
		'''
		self.set_f(c)	
		return 0

	def toJson(self, filename):
		c=-1.037 + 0.17j
		self.set_f(c)
		plane=self.plane.tolist()
		Parameters=['xmin: %d, xmax: %d, xlen: %d, ymin: %d, ymax: %d, ylen: %d, c: %s' % (self.xmin, self.xmax, self.xlen, self.ymin, self.ymax, self.ylen,str(c))]
		with open(filename,'w')  as outfile:
			json.dump(Parameters, outfile,indent=4)
			json.dump(plane, outfile,indent=4)
		outfile.close()

	def fromJson(self,filename):
		'''
		Compare JSon with csv file:
		1. JSon is very good for key-value pares. In Json file, it defines the key and value in a directory, very easy to understand.  And it doesn't change the value's type. 
		2. CSV use string to read data from files. All values in CSV file will be changed as string automatically while reading. 
		3. Both CSV and JSon not support complex number. 
		

		open file and read all the rows into a temporary dictionary
		'''
		with open(filename,'r') as infile:
			pr=json.load(infile)
		infile.close()
		'''
		get the value of each parameters
		'''
		self.xmin=pr['xmin']
		self.xmax=pr['xmax']
		self.xlen=pr['xlen']
		self.ymin=pr['ymin']
		self.ymax=pr['ymax']
		self.ylen=pr['ylen']
		c=complex(pr['c'])

		'''
		reset default fuction, and refresh the plane at the sametime.
		'''
		self.set_f(c)
		return 0

def test_set_f_julia():
	'''
	Test all the points in the plane are positive integers.
	'''
	p1=JuliaPlane(-3,2,6,-3,2,3)
	p1.set_f()
	for r in np.arange(p1.ylen):
		for c in np.arange(p1.xlen):
			assert p1.plane[r][c] >= 0, 'It is not  a plane of positive integers' 
		

test_set_f_julia()
	
'''
p1=JuliaPlane(-3,2,6,-3,2,3)
p1.toCSV('plane.csv')
p1.fromCSV('plane1.csv')
print(p1.plane)
p1.toJson('plane.json')
p1.fromJson('plane1.json')
print(p1.plane)
		
'''		
