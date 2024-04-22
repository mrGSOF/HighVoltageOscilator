#!/usr/bin/env python
"""
Script to build an High Voltage Oscillator object and configure it.
To customize the environment, you will need to change the parameters
in the "PARAMETER BLOCK" in the __main__ section

By: Guy Soffer
Date: 21/Sep/2022
"""

#Basic modules to load
import time
import ArduHV_osci as OSCI

def close():
    ardu.OpenClosePort(0)
    print('COM port is closed')

def Help():
    print("osci.setFreq_khz(f) #< Set the output frequency (1 to 15 Khz)")
    print("osci.setVoltage(b)  #< Set the output voltage {45 is 40Vp-p; 70 is 200Vp-p @5Khz}")
    print("osci.getVoltage()   #< Read the output voltage")
    print("osci.setVoltage(45)")
    print("osci.setFreq_khz(5)")

if __name__ == "__main__":
    #\/\/\/ CHANGE THESE PARAMETERS \/\/\/
    port = "COM12"       #<--Change to the correct COM-Port to access the Arduino
    baudRate = 115200*2  #<--Leave as is
    #/\/\/\   PARAMETERS BLOCK END  /\/\/\
    
    print('Using port %s at %d'%(port, baudRate))
    osci = OSCI.ArduHV_Osci( COM=port, baud=baudRate )

    print('Discovering the High Voltage Oscilator on port %s'%(port))
    if osci.OpenClosePort(1):
        print('HVO is ON-LINE.')
    else:
        print('HVO is not responding.')

    osci.cfg()
    Help()
