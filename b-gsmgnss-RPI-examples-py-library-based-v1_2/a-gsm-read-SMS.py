############################################################################################################################################
#a-gsm-read-SMS.py v1.01/24 March 2017 - a-gsmII/b-gsmgnss 2.105 send SMS utility / demo
#COPYRIGHT (c) 2017 Dragos Iosub / R&D Software Solutions srl
#
#You are legaly entitled to use this SOFTWARE ONLY IN CONJUNCTION WITH a-gsmII/b-gsmgnss DEVICES USAGE. Modifications, derivates and redistribution 
#of this software must include unmodified this COPYRIGHT NOTICE. You can redistribute this SOFTWARE and/or modify it under the terms 
#of this COPYRIGHT NOTICE. Any other usage may be permited only after written notice of Dragos Iosub / R&D Software Solutions srl.
#
#This SOFTWARE is distributed is provide "AS IS" in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied 
#warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#Dragos Iosub, Bucharest 2017.
#http://itbrainpower.net
############################################################################################################################################
#HEALTH AND SAFETY WARNING!!!!!!!!!!!!!!!!!!!!
#High power audio (around 870mW a-gsmII, 800mW b-gsmgnss)! You can damage your years! Use it with care when headset is connected.
#We recomend to use AT+CLVL=20 (as maximum value), audio setup command in order to limit the output power.
#
# WARNING: WIRING the gsm board with u-controllers/boards(RPi) must be made with boards UNPOWERED!!
#
# LEGAL DISCLAIMER:
# Incorrect or faulty wiring and/or connection can damage your RPi and/or your a-gsm board!
# Following directives are provided "AS IS" in the hope that it will be useful, but WITHOUT ANY WARRANTY!
# Do the wiring on your own risk! 
#
# References:
# https://itbrainpower.net/images/RaspberryPi_a-gsmII_b-gsmgnss_wiring.png
# https://itbrainpower.net/downloads#a-gsmII_documentation
# https://itbrainpower.net/downloads#b-gsmgnss_documentation
############################################################################################################################################
# this utility must be runned as root (just use: sudo python yourPythonFileName.py)


usePoweringControl = 1#change it to 0 if you do not want to control powerUP/powerDown the a-gsm board. In this case, please be sure the a-gsm board is powered UP(..see a-gsm_kickstart_v_x-yz.pdf) before run this utility   

#Do not change under following line! Insteed make one copy of the file and play with! 
#Hint: if you make changes of the code, before you run it run clear utility (erase the Python compiled *.pyc files)... 
############################################################################################################################################
# this utility must be runned as root (just use: sudo python yourPythonFileName.py)

import os
import serial
from time import sleep, time

from globalParVar import *
from agsm2_bgsmgnss_105_hw_control import *
from agsm_Serial_Lib import *
from agsm_Basic_Lib import *
from agsm_SMS_Lib import *

print "Light example - just list/read SMS"
sleep(1)

if not os.getuid() == 0:
    print("please use root privileges! try: \"sudo python yourPythonFileName.py\"")
    exit(0)

# set SERIAL/USB communication section start
# bellow chose value bw [SER] Serial /dev/ttyAMA0 or [USB] /dev/ttyUSB0
# if module USB port maps to other port as /dev/ttyUSB1, just edit the moduleName_Serial_lib.py...
serialCommunicationVia = SERIALCON      # OVERRIDE the default value loaded from globalParVar.py. here I use via SERIAL communication
setSerialCom(serialCommunicationVia)    # set the current communication option
startSerialCom()                        # open serial communication bw. RPi and a-gsm shield
# set SERIAL/USB communication section end

# set HARDWARE CONTROL setup & POWER ON section start        
if usePoweringControl==1:
    hwControlSetup()                    # setup the RPi I/O ports

sleep(2)#some delay...

if usePoweringControl==1:
    poweron()

sleep(1)
# set HARDWARE CONTROL setup & POWER ON section end        

# set MODEM STARTUP SETUP section start        
setupMODEM()
# set MODEM STARTUP SETUP section end


# MAIN PROGRAM section start        
print "list total and last SMS number"

res = listSMS()
if res==0:
	print "list SMS executed with succes"

noSMS = getnoSMS()                  #SMS stored count
totSMS = gettotSMS()                #total SMS capacity

print "total SMS locations: "+str(totSMS)
print "last SMS location: "+str(noSMS)
print ""

print "read/parse SMS stored @ location 1"
res = readSMS(1)                    #read SMS @ location 1
SMSmessage = getSMSmessage()        #retrieve the SMS message

print "SMS type: "+SMSmessage[0]
print "Sender no.: "+SMSmessage[1]
print "Date and time local: "+SMSmessage[2]+"  ...divide to 4 the last 2 digits to reach UTC standard offset(in hours). This is dependent on your NMO's behavior!"
print "Date and time UTC: "+ str(SMSmessage[2])[0:-3]
print "...and the message content:\r\n"+SMSmessage[3]
print ""
# MAIN PROGRAM section end        


# stop SERIAL COMMUNICATION section start        
stopSerialCom()                             # close modem communication
# stop SERIAL COMMUNICATION section end        

# HARDWARE CONTROL release & POWER OFF section start        
if usePoweringControl==1:
    poweroff()                              #shutdown modem

if usePoweringControl==1:
    hwControlRelease()                      # free GPIO
# HARDWARE CONTROL release & POWER OFF section end        

print("\r\n\r\nThat's all folks!\r\n")
