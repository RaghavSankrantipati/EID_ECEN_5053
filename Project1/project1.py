# Author: Sai Raghavendra Sankrantipati
# File: project1.py
# Description: In this project DHT 22 sensor is interfaced to RPi3
#  				A UI is developed using PyQt4 which has options for
#				refreshing sensor values, setting alarm for high limit of 
#				temperature, plotting past 100 samples and averaging these samples

import threading
import sys
from PyQt4 import QtGui
import Adafruit_DHT
import time
import matplotlib.pyplot as plt

# list to store 100 samples of temperature
array = [None] * 100

#DHT library has the generic function for all DHT sensors
# 22 is the input for DHT 22 sensor
DHT_22 = 22
#GPIO Pin of RPi3
GPIO_PIN = 4

#This is the UI class which has a widget in which push buttons, Labels, progessing bar is present
#Input QtGui.QWidget
#Output A QT UI widget
class MyWidget(QtGui.QWidget):
    
    def __init__(self):
        super(MyWidget, self).__init__()
        self.initUI()
        
    def initUI(self):
        #Widget initialisation
        self.setGeometry(500, 500, 400, 350)
        self.setWindowTitle('Temperature and Humidity')     
        
		#Refresh button initialisation
        self.btn = QtGui.QPushButton('Refresh', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 210)    
        self.btn.clicked.connect(self.signalRefresh)

		#Set Alarm button initialisation
        self.btn = QtGui.QPushButton('Set Alarm', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(250, 210)    
        self.btn.clicked.connect(self.setAlarm)

		#Plot button initialisation
        self.btn = QtGui.QPushButton('Plot', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 270)    
        self.btn.clicked.connect(self.plot)
        
		#Average Temperature button initialisation
        self.btn = QtGui.QPushButton('Avg Temp', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(250, 270)    
        self.btn.clicked.connect(self.average)

        self.lbl = QtGui.QLabel('Temperature:', self)
        self.lbl.move(50, 30)
	
	#progress bar of temperature initialisation 
	self.progress1 = QtGui.QProgressBar(self)
	self.progress1.setGeometry(50, 60, 300, 20)
	                
        self.lbl = QtGui.QLabel('Humidity:', self)
        self.lbl.move(50, 100)	
	
	#progress bar of humidity initialisation 
	self.progress2 = QtGui.QProgressBar(self)
	self.progress2.setGeometry(50, 130, 300, 20)
	      
        
	self.lbl1 = QtGui.QLabel('',self)
        self.lbl1.move(50, 170) 
 
	self.lbl2 =  QtGui.QLabel('', self)
	self.lbl2.move(240, 310)
 
	self.lbl3 =  QtGui.QLabel('', self)
	self.lbl3.move(80, 310)
	
	self.alarm_temp = 100

        self.show()
		
#In this function Time and sensor readings are updated on UI and has error handling
#self(widget created) is passed as input
    def signalRefresh(self): 
	self.lbl1.setText(time.ctime())
        self.lbl1.move(50, 170)  
	self.lbl1.adjustSize()	

	humidity = 20
	temperature = 20

	humidity, temperature = Adafruit_DHT.read_retry(DHT_22, GPIO_PIN)

	if temperature > self.alarm_temp:
            QtGui.QMessageBox.warning(self, "Message", "Temperature is above the limit")

	if humidity is not None and temperature is not None:
	    self.temp = 0
		
            while self.temp < temperature:
                self.temp+=0.0001
                self.progress1.setValue(self.temp)

            self.hum = 0
		
            while self.hum < humidity:
                self.hum+=0.0001
                self.progress2.setValue(self.hum)

        else:
            print('Failed to get reading. Try again!')
       	    QtGui.QMessageBox.warning(self, "Message", "unable to read from sensor")

			
#In this function average of all the samples is calculated and displayed
    def average(self):
	i = 0 
	sum = 0
	while(i<100):
		#checking for null value to estimate the end of array
		if array[i] is None:
			break
		sum += array[i]
		i+=1
	sum = str(float(sum)/i)
	print sum

	self.lbl2.setText(sum) 
	self.lbl2.adjustSize()	

	self.lbl3.setText('Average Temperature:')
	self.lbl3.adjustSize()	
     
#in this function high limit of alarming tempeature is recorded using user input(InputDialog)
    def setAlarm(self):
	alarm, ok = QtGui.QInputDialog.getText(self, 'alarm temperature', ' Enter Upper Limit:')
	if ok:
		self.alarm_temp = int(alarm)

#This is a basic plotting function using matplotlib
    def plot(self):
	plt.plot(array, 'r')
	plt.xlabel('Samples')
	plt.ylabel('Temperature in centigrade')
	plt.title('Plot of last 100 tempeatures')
	plt.show()

#DESCRIPTION: fetch() is used to fetch temperature data and updates the global array of temperature values
#An array of 100 elements is used to store tempeature values
#This array is updated every 5 seconds usind threads
#if array is not full append value to items
#if array is full each value is tranferred its previous one and 100th element is updated with sensor data
# Input: It doesn't have any input but uses global array
# Output: It updates global array

def fetch():	
	humidity, temperature = Adafruit_DHT.read_retry(DHT_22, GPIO_PIN)
	threading.Timer(1.0, fetch).start()	
	#if array is not full add data at the nth place
	if array[99] is None:
		i = 0
		while(i<100):			
			if array[i] is None:
				array[i] =  temperature
				break
			i+=1
	else:
	#if array is full add data at the end
		i = 0
		while (i<99):
			#transfer a element to its previous element
			array[i] = array[i+1]
			i+=1
		array[99] = temperature
	print array
                
				
def main():
    app = QtGui.QApplication(sys.argv)	
    fetch()
    w = MyWidget()    
    app.exec_()

if __name__ == '__main__':
    main()
	
	
#Adafruit_DHT.read_retry() is implemented from Github Adafruit_DHT library
# URL: https://github.com/adafruit/DHT-sensor-library

#https://www.tutorialspoint.com/pyqt/
#http://zetcode.com/gui/pyqt4/
#https://github.com/snazrul1/PyRevolution/tree/master/PyQt4
#The above links are used for learning PyQt4 

#https://pythonspot.com/en/threading/ 
#The above link is used for learning threads in Python



