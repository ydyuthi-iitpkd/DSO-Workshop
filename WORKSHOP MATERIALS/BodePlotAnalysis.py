import pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt

rm = visa.ResourceManager()
list1 = rm.list_resources()

inst1 = rm.open_resource(list1[1])  #DSO
inst_sig = rm.open_resource(list1[0])   #Signal Generator


# Bode Plot Parameters  
f_start = 100 
f_stop = 10000
f_step = 500

#Create frequency array 
f_array = np.arange(f_start,f_stop+f_step,f_step)

#Signal Generator setup
inst_sig.write("SOUR1:FUNC:SHAP SIN")
inst_sig.write("SOUR1:VOLT:LEV:IMM:AMPL 3Vpp")
inst_sig.write("SOUR1:FREQ:MODE FIX")
inst_sig.write("OUTP1:STAT ON")

#Initialise output
dB = np.zeros_like(f_array,dtype=np.float16)

#Scaling for DSO
inst1.write(":CHAN1:OFFS 0V")
inst1.write(":CHAN2:OFFS 0V")
inst1.write(":CHAN1:SCAL 1V")
inst1.write(":CHAN2:SCAL 1V")

def set_freq(frequency, unit = "Hz"):
    query_string = "SOUR1:FREQ:FIX " + str(frequency) + unit
    inst_sig.write(query_string)

#Sweeping the frquency and measuring the output
for i in range(len(f_array)):
    set_freq(f_array[i])
    t = 2/(5*f_array[i])
    inst1.write(":TIM:SCAL "+str(t))
    time.sleep(0.5)
    inst1.write(":SING")
    x = float(inst1.query(":MEASure:VPP? CHANnel1"))
    y = float(inst1.query(":MEASure:VPP? CHANnel2"))
    dB[i] = 20*np.log10(y/x)

#Turn Off and Close
inst_sig.write("OUTP1:STAT OFF")
inst1.close()
inst_sig.close()


plt.plot(f_array,dB)
plt.semilogx()
plt.show()









