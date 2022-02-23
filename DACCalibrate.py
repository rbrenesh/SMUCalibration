#uSMU calibration script
#Written by rbrenes 20220218

import serial
import numpy as np
from time import sleep
from scipy import stats

'''
DAC values must be ints, so I'm flooring the array. 
Could use np.arange, but this works fine for setting a small-ish set of numbers over a large range. Definitely fails over a smaller range since it can create duplicates
'''

dac_val = np.linspace(0,65536,num=100,dtype= int)

list_ports = False

if list_ports:
	import serial.tools.list_ports
	ports = serial.tools.list_ports.comports()

	for port, desc, hwid in sorted(ports):
        	print("{}: {} [{}]".format(port, desc, hwid))

#instance Serial and set baudrate and port
ser = serial.Serial()
ser.baudrate = 115200

#change port with whatever is the port that your device is at
ser.port = '/dev/cu.usbmodem2051395C4D521'
#ser.port = 'COM8'

#/dev/cu.usbmodem206A3083544E1

ser.open()

#Enable SMU output
ser.write(b'CH1:ENA')

#loop over dac values and read voltage from Keithley
for val in dac_val:
    #must turn string into bytes, hence the use of encode
	ser.write('DAC {:d}'.format(val).encode())
	# wait 50ms for value to settle
	sleep(0.05)

	#read voltage from Keithley

#disable SMU output
ser.write(b'CH1:DIS')

#calculate slope and intercept through a linear regression
res = stats.linregress(dac_val,volts)

print('Slope: {:.1f}; std dev {:.1f}:'.format(res.slope,res.slope_stderr))
print('Intercept: {:d}; std dev {:d}:'.format(res.intercept,res.intercept_stderr))

#write the calibration data to the SMU
ser.write('CAL:DAC {:.1f} {:d}'.format(res.slope,res.intercept).encode())
#reboot the SMU
ser.write(b'*RST')


#close connection to uSMU
ser.close()