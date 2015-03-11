#Tom Diehl 1-16-15
#Takes in 4 csv files with 3 columns formatted
#"mm-dd-yy hr:min:sec , bandwith , latency"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates 
import csv
import datetime

dt = datetime.datetime

#filenames to be read in
file0 = 'TOS_OTC_BG_Nov17_Dec9'         
file1 = 'TOS_OTC_BG_wired_Nov17_Dec9'
file2 = 'TOS_SSG_BG_Nov17_Dec9'
file3 = 'TOS_SSG_BG_wired_Nov21_Dec9'


#Class to hold a set of data
class DataClass:
		def __init__(self):
				self.data = []
				self.band = []           
				self.lat = []            
				self.dates = [] 


#Get data from file
def readIn(fileName):
	temp = DataClass()
	with open('%s.csv' % fileName) as csvfile:
		reader = csv.reader(csvfile)
		for elem in reader:
			temp.data.append(elem)
		csvfile.close()
	return temp
	
#Seperate data into individual list
def seperate(input):
    daTime = []     
    flatten = []
    n = 0
    
    for x in input.data:      
        for y in x:
            flatten.append(y)
    while n < len(flatten):         
        if n % 3 == 0:              #Date and time list
            daTime.append(flatten[n])
        elif n % 3 ==1:             #Bandwidth list
            input.band.append(flatten[n])
        else:                       #Latency list
            input.lat.append(flatten[n])
        n += 1
    for x in daTime:                #format datetime for plotting
        y = dt.strptime(x,"%Y-%m-%d %H:%M:%S")
        input.dates.append(matplotlib.dates.date2num(y))
    return input

#plotting function(position number, x-axis data, y-axis data,
#						filename,data type, units, y axis scale)
def iPlot(num,xaxi,yaxi,filename,types, units,scale):
#	plt.subplot(4,1,num)	
	if num == 1:	
		ax = plt.subplot(4,1,1)
	elif num== 2: 	
		ax = plt.subplot(4,1,2)
	elif num == 3:
		ax = plt.subplot(4,1,3)
	else:
		ax = plt.subplot(4,1,4)
	plt.plot_date(xaxi,yaxi,'-')
	plt.title(filename + "--%s" % types )
	plt.ylabel(" %s  %s " % (types,units))
	plt.ylim(0,scale)
	
	majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
	ax.xaxis.set_major_formatter(majorFormatter)
	



#select bandwidth, latency, or custom set plots
def plot(dataType):
	nameB = "Bandwidth"
	nameL = "Latency"
	unitsB = " (Mbps)"
	unitsL = "(ms)"
	scaleB = 60
	scaleL = 500

	if dataType == '1':
		iPlot(1,out0.dates,out0.lat,file0,nameL,unitsL,scaleL)
		iPlot(2,out1.dates,out1.lat,file1,nameL,unitsL,scaleL)
		iPlot(3,out2.dates,out2.lat,file2,nameL,unitsL,scaleL)
		iPlot(4,out3.dates,out3.lat,file3,nameL,unitsL,scaleL)

	elif dataType == '2':
		iPlot(1,out0.dates,out0.band,file0,nameB,unitsB,scaleB)
		iPlot(2,out1.dates,out1.band,file1,nameB,unitsB,scaleB)
		iPlot(3,out2.dates,out2.band,file2,nameB,unitsB,scaleB)
		iPlot(4,out3.dates,out3.band,file3,nameB,unitsB,scaleB)

	elif dataType =='3':
		iPlot(1,out0.dates,out0.lat,file0,nameL,unitsL,scaleL)
		iPlot(2,out0.dates,out0.band,file0,nameB,unitsB,scaleB)
		iPlot(3,out1.dates,out1.lat,file1,nameL,unitsL,scaleL)
		iPlot(4,out1.dates,out1.band,file1,nameB,unitsB,scaleB)

def main():
	global out0,out1,out2,out3

	print "Choose plot type"
	valid = ['1','2','3']

	while True:
		dataType = raw_input("1 = Latency\n2 = Bandwidth\n3 = Custom : ")
		if dataType in valid:
			break
		else:
			print('Please enter valid choice\n')
	print "Creating plots..."

	out0 = readIn(file0)
	out1 = readIn(file1)
	out2 = readIn(file2)
	out3 = readIn(file3)

	seperate(out0)
	seperate(out1)
	seperate(out2)
	seperate(out3)
	
	plot(dataType)

	plt.show()

main()
