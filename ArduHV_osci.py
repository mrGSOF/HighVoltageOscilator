#!/usr/bin/env python

"""
    This file is part of GSOF_ArduBridge.

    GSOF_ArduBridge is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GSOF_ArduBridge is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GSOF_ArduBridge.  If not, see <https://www.gnu.org/licenses/>.

Class to access the Arduino-Bridge digital inputs and outputs.
This class is using the BridgeSerial class object to communicate over serial
with the GSOF-Arduino-Bridge firmware.
The packet has a binary byte based structure
byte0 - 'F' to set the oscilator frequency
byte1 - frequency in Khz (0 - off, 1-30 - on (binary-value)
"""

__version__ = "1.0.0"

__author__ = "Guy Soffer"
__copyright__ = "Copyright 2022"
__credits__ = []
__license__ = "GPL-3.0-or-later"
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Production"

import time, math
from GSOF_ArduBridge import ArduBridge
from GSOF_ArduBridge import CON_prn

class ArduHV_Osci(ArduBridge.ArduBridge):
    def __init__(self, COM, baud):
        super().__init__( COM=COM, baud=baud )
        self.osci = ArduOsci(bridge=self.comm)
        self.negV_ctPin = 5
        self.posV_ctPin = 6
        self.posV_adcPin = 0
        self.zeroV_adcPin = 1
        self.cur_adcPin = 2
        self.p5V_adcPin = 3
        self.Vin_adcPin = 4
        self.temp_adcPin = 5
        self._hv_bias = 100
        self._hv_gain = 0.5

    def cfg(self):
        self.gpio.pinMode(self.posV_ctPin, self.gpio.OUTPUT, 0)
        self.gpio.pinMode(self.negV_ctPin, self.gpio.OUTPUT, 0)

    def setFreq_khz(self, khz) -> int:
        """ Set the oscillator's output frequency (Khz) """
        ok_to_set = True
        if khz > 10:
            Vout = self.getVoltage()
            if Vout > 245:
                ok_to_set = False
        if ok_to_set:
            return self.osci.setFreq_khz(khz)
        print("Voltage is too high for the requested frequency")
        return 0
        
    def setVoltage(self, posV, negV=None) -> None:
        """ Set the oscillator's peak positive and negative output voltages """
        posV = abs(posV)
        if negV == None:
            negV = posV
        negV = abs(negV)
        self.an.analogWrite(self.posV_ctPin, posV)
        self.an.analogWrite(self.negV_ctPin, negV)

    def getVoltage(self) -> list:
        """ Returns the oscillator's peak positive and negative output voltages """
        posRaw =  self.an.analogRead(self.posV_adcPin)
        zeroRaw = self.an.analogRead(self.zeroV_adcPin)
        peakV = (posRaw -self._hv_bias)*self._hv_gain
        print( "%1.1fVpk-pk"%(2*peakV) )
        return 2*peakV #(posRaw, zeroRaw)




class ArduOsci():
    OFF = 0
    def __init__(self, bridge=False, v=False):
        self.v = v
        self.comm = bridge
        self.RES = {1:"OK", 0:"ERR" , -1:"ERR"}
        self.DIR = {1:"IN", 0:"OUT",   2:"SERVO"}

    def setFreq_khz(self, khz) -> int:
        """ Send the command to set the output frequency (Khz) """
        vDat = [ord('F'), khz]
        self.comm.send(vDat)
        reply = self.comm.receive(1)

        if khz == self.OFF:
            khz = "OFF"
        else:
            khz = str(khz)
        CON_prn.printf("OSCI: %s Khz - %s", par=(khz, self.RES[reply[0]]), v=self.v)
        return reply[0]
