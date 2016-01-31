
# Author: Sean Ko 

# There may be additional python packages that may need to be downloaded
import sys
import serial
import io
import xlwt
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSlot
from PyQt4 import QtGui, QtCore
# Windows package only for opening file (Optional)
#from win32com.client import Dispatch

import time as realTime
import numpy as np
import pyqtgraph as pg

class GUI(QWidget):

	def __init__(self):
		# Boolean variable for if checkboxes were checked
		self.acc_x_checked = False
		self.acc_y_checked = False
		self.acc_z_checked = False

		self.gyro_x_checked = False
		self.gyro_y_checked = False
		self.gyro_z_checked = False

		# Initializing QWidget and GUI
		QWidget.__init__(self)

		self.resize(400, 400)
		self.move(300,300)
		self.setWindowTitle('Accelerometer-Gyro Data Collection')

		self.layout = QVBoxLayout()
		self.checkbox_layout = QHBoxLayout()

		self.filename_box = QLineEdit(self)
		self.filename_label = QLabel("Name your spreadsheet:", self)

		self.time_box = QLineEdit(self)
		self.time_label = QLabel("How long do you want to collect data for (in seconds)?", self)
		
		self.filename_label.move(20, 40)
		self.filename_box.move(170, 40)
		self.time_label.move(50, 110)
		self.time_box.move(135, 140)

		self.acc_checkboxes_title = QLabel("Which acclerometer dimensions do you want?", self)
		self.acc_x_check = QCheckBox("X-Dimension", self)
		self.acc_y_check = QCheckBox("Y-Dimension", self)
		self.acc_z_check = QCheckBox("Z-Dimension", self)

		self.gyro_checkboxes_title = QLabel("Which gyro sensor dimensions do you want?", self)
		self.gyro_x_check = QCheckBox("X-Dimension", self)
		self.gyro_y_check = QCheckBox("Y-Dimension", self)
		self.gyro_z_check = QCheckBox("Z-Dimension", self)

		self.acc_checkboxes_title.move(80,185)
		self.acc_x_check.move(20,220)
		self.acc_y_check.move(150,220)
		self.acc_z_check.move(280,220)

		self.gyro_checkboxes_title.move(80,265)
		self.gyro_x_check.move(20,300)
		self.gyro_y_check.move(150,300)
		self.gyro_z_check.move(280,300)

		# Checks the state of the checkboxes and updates them
		self.acc_x_check.stateChanged.connect(self.update_bools)
		self.acc_y_check.stateChanged.connect(self.update_bools)
		self.acc_z_check.stateChanged.connect(self.update_bools)

		self.gyro_x_check.stateChanged.connect(self.update_bools)
		self.gyro_y_check.stateChanged.connect(self.update_bools)
		self.gyro_z_check.stateChanged.connect(self.update_bools)

		# Button to start collecting data
		self.collect_button = QPushButton('Collect Data!', self)
		self.collect_button.move(150, 350)
		self.collect_button.clicked.connect(self.run_on_click)

		# Initializing pyqtgraph plots
		self.win = pg.GraphicsWindow()
		self.p1 = self.win.addPlot(1,1, title="Corrected X-Acceleration")
		self.p1.setYRange(-15,15)
		self.p2 = self.win.addPlot(2,1, title="Corrected X-Velocity")
		self.p2.setYRange(-3,3)
		self.p3 = self.win.addPlot(3,1, title="Z-Rotation")
		self.p3.setYRange(-300,300)

	# Connected function with the collect_button
	@pyqtSlot()
	def run_on_click(self):
		seconds = int(self.time_box.text())
		filename = self.filename_box.text()
		print("Collecting data...\n")
		self.data_collection(seconds, filename)

	# Connected function with the checkboxes
	@pyqtSlot()
	def update_bools(self):
		self.acc_x_checked = self.acc_x_check.isChecked()
		self.acc_y_checked = self.acc_y_check.isChecked()
		self.acc_z_checked = self.acc_z_check.isChecked()

		self.gyro_x_checked = self.gyro_x_check.isChecked()
		self.gyro_y_checked = self.gyro_y_check.isChecked()
		self.gyro_z_checked = self.gyro_z_check.isChecked()

	# Function called when the collect_button is clicked to
	# start collecting data
	def data_collection(self, time, filename):
		ser = serial.Serial('COM4', 9600)

		# Initializing excel sheet
		data = []
		wb = xlwt.Workbook()
		ws = wb.add_sheet('Test 1')
		style0 = xlwt.easyxf('font: bold on, underline single')

		# Writing the column titles of the excel sheet
		ws.write(0, 0, "Time (ms)", style0)
		n = 1

		if(self.acc_x_checked):
			ws.write(0, n, "X-acceleration", style0)
			n += 1
		if(self.acc_y_checked):
			ws.write(0, n, "Y-acceleration", style0)
			n += 1
		if(self.acc_z_checked):
			ws.write(0, n, "Z-acceleration", style0)
			n += 1
		ws.write(0,n, "Acceleration", style0)
		n += 1
		ws.write(0,n, "Corrected X-Acceleration", style0)
		n += 1
		
		if(self.acc_x_checked):
			ws.write(0, n, "X-velocity", style0)
			n += 1
		if(self.acc_y_checked):
			ws.write(0, n, "Y-velocity", style0)
			n += 1
		if(self.acc_z_checked):
			ws.write(0, n, "Z-velocity", style0)
			n += 1
		ws.write(0,n, "Velocity", style0)
		n += 1

		if(self.gyro_x_checked):
			ws.write(0, n, "X-rotation", style0)
			n += 1
		if(self.gyro_y_checked):
			ws.write(0, n, "Y-rotation", style0)
			n += 1
		if(self.gyro_z_checked):
			ws.write(0, n, "Z-rotation", style0)

		# Arrays initialized to collect data to be plotted
		xAccArr = []
		xVelArr = []
		zRotArr = []
		timeArr = []
		
		# Setting X-axis limits based on the user-inputted time
		self.p1.setXRange(0,time)
		self.p2.setXRange(0,time)
		self.p3.setXRange(0,time)

		curve1 = self.p1.plot()
		curve2 = self.p2.plot()
		curve3 = self.p3.plot()

		# Velocities calculated by continuous summation of the
		# instantaneous acceleration times time interval (0.05 sec here)
		Xvel = 0
		Yvel = 0
		Zvel = 0
		t = 0
		# Boolean to keep track of whether acceleration is positive (True)
		# or negative (False)
		positive_acc = None

		# Starting data collection loop
		for i in range(0, 20 * time):
			try:	
				# Reading each line from the Arduino serial port			 
				temp = [float(x) for x in ser.readline().split(" ")]
				#Writing time
				ws.write(i+1, 0, t)
				t = t + 0.05
				acc = 0
				vel = 0
				m = 1

				#Writing acceleration data
				if(self.acc_x_checked):
					ws.write(i+1, m, temp[0])
					acc = acc + (temp[0])**2
					m += 1
				if(self.acc_y_checked):
					ws.write(i+1, m, temp[1])
					acc = acc + (temp[1])**2
					m += 1
				if(self.acc_z_checked):
					ws.write(i+1, m, temp[2])
					acc = acc + (temp[2])**2
					m += 1
				ws.write(i+1, m, acc**(0.5))
				m += 1
				
				#Making X-acceleration correction and writing it
				temp[0] = temp[0]+0.35
				ws.write(i+1, m, temp[0])
				m += 1

				#Checking if corected X-Acceleration changed signs
				# #If changed, reset X-velocity to zero
				# if (positive_acc and temp[0]<0) or (not positive_acc and temp[0]>0):
				# 	Xvel = 0
				# 	positive_acc = not positive_acc
				# else:
				# 	Xvel = Xvel + temp[0] * 0.05
				
				#Initializing positive_rotation boolean
				if positive_acc == None:
					if temp[0] > 0:
						positive_acc = True
					elif temp[0] < 0:
						positive_acc = False

				#Writing calculated velocity data
				if(self.acc_x_checked):					
					ws.write(i+1, m, Xvel)
					Xvel = Xvel + temp[0] * 0.05
					vel = vel + Xvel**2
					m += 1 
				if(self.acc_y_checked):
					ws.write(i+1, m, Yvel)
					Yvel = Yvel + (temp[1]) * 0.05
					el = vel + Yvel**2
					m += 1
				if(self.acc_z_checked):
					ws.write(i+1, m, Zvel)
					Zvel = Zvel + (temp[2]) * 0.05
					el = vel + Zvel**2
					m += 1
				ws.write(i+1, m, vel**(0.5))
				m += 1

				#Writing Gyro Data
				if(self.gyro_x_checked):
					ws.write(i+1, m, temp[3])
					m += 1
				if(self.gyro_y_checked):
					ws.write(i+1, m, temp[4])
					m += 1
				if(self.gyro_z_checked):
					ws.write(i+1, m, temp[5])

				# Appending data points to the arrays
				timeArr.append(t)
				xAccArr.append(temp[0])
				xVelArr.append(Xvel)
				zRotArr.append(temp[5])

				# Updating the data of the plots to include the most recent data
				curve1.setData(timeArr,xAccArr)
				curve2.setData(timeArr,xVelArr)
				curve3.setData(timeArr,zRotArr)
				app.processEvents()
				
				realTime.sleep(0.05)

			# To catch some errors from the data being read from the Arduino
			except ValueError:
				print "Value Error on line " + str(i)
			except IndexError:
				print "Index Error on line" + str(i)

		print("Data collection complete")
		print("Opening file...")
		ser.close()
		print("Port closed.")

		# File will be saved in the same folder as this python script
		filename += ".xls"
		wb.save(filename)		

		# Opening the excel sheet requires the use of the win32com.client package
		# which is only available for windows
		# This step is optional as you can just open the file manually
		#xl = Dispatch("Excel.Application")
		#xl.Visible = True
		# Path of where to open the excel file (OPTIONAL)
		#wb = xl.Workbooks.Open(r"C:\\Users\\Sean Ko\\Dropbox (MIT)\\UROP\\Accelerometer-Gyro Data\\" + filename)

	def run(self):
		# Show the form
		self.show()
		# Run the application
		app.exec_()

# The main function
app = QApplication(sys.argv)
if __name__ == "__main__":
	gui = GUI()
	gui.run()