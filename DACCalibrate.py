#uSMU calibration script
#Written by rbrenes 20220218

import serial
import numpy as np
from time import sleep
from scipy import stats


#DAC values must be ints, so I'm flooring the array. Could use np.arange, but this works fine for setting a small-ish set of numbers over a large range
dac_val = np.floor(np.linspace(0,65536,num=100))

#instance Serial and set baudrate and port
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM8'


ser.open()

#Enable SMU output
ser.write('CH1:ENA')

#loop over dac values and read voltage from Keithley
for val in dac_val:
	ser.write('DAC {:d}'.format(val))
	# wait 50ms for value to settle
	sleep(0.05)

	#read voltage from Keithley

#disable SMU output
ser.write('CH1:DIS')

#calculate slope and intercept through a linear regression
res = stats.linregress(dac_val,volts)

print('Slope: {:.1f}; std dev {:.1f}:'.format(res.slope,res.slope_stderr))
print('Intercept: {:d}; std dev {:d}:'.format(res.intercept,res.intercept_stderr))

#write the calibration data to the SMU
ser.write('CAL:DAC {:.1f} {:d}'.format(res.slope,res.intercept))
#reboot the SMU
ser.write('*RST')


#close connection to uSMU
ser.close()