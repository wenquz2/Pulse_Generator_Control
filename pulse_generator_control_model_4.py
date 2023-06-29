#Fourth version of the pulse generator control - designed for breadboard LED testing.
#features gating the E and F channels, which employs duty cycles 

#Connecting to pulse generator
import pyvisa
import numpy as np
import time
from pulse_generator_control_helper_funcs import GetWaitandDelay, SetModesDefault, Run



rm = pyvisa.ResourceManager()
pulse_generator = rm.open_resource('ASRL3::INSTR')
pulse_generator.baud_rate = 115200
print(pulse_generator.query('*IDN?')) #verify the connection

scale = 0

#define t0
t0 = 1 * 10 ** scale #20e-3


#set the modes to default values using helper funtion
SetModesDefault(pulse_generator)

#enable gate?
pulse_generator.write("PULSe0:GATe:MODe CHOUtputinh")

#set all the parameters(To be updated)
Ta = 2.5 * 10 ** scale
Tac = 2.5 * 10 ** scale
Tab = 150 * 10 ** scale #150e-3
Tc = 65 * 10 ** scale   #65e-3
Td = 50 * 10 ** scale   #50e-3
duration = 400 * 10 ** scale



#set the internal clock cycle of the pulse generator
command_t0 = ":PULSe0:PERiod {}".format(t0)
pulse_generator.write(command_t0)

#channel A programming (mode:ss)
'''
parameters: 
@Ta: the width of the pulse on the A channel
@Tac: the time interval between the end of C and the start of A
@T_waited_A: time to wait before pulse A could be generatored, since the beginning of the program.
@cycles_waited_A
@delayA: the time delay before pulse A could be created, after waiting

'''
#Ta = 2.5e-3
#Tac = 2.5e-3
T_waited_A = Tac + Tc
cycles_waited_A = GetWaitandDelay(t0, T_waited_A)[0]
delayA = GetWaitandDelay(t0, T_waited_A)[1]



command_A_1 = ":PULSe1:DELay {}".format(delayA)
print(Ta)
command_A_2 = ":PULSe1:WIDth {}".format(Ta)
command_A_3 = ":PULSe1:WCOunter {}".format(cycles_waited_A)

pulse_generator.write(command_A_1)
pulse_generator.write(command_A_2)
pulse_generator.write(command_A_3)

#channel B programming (mode: ss)
'''
parameters: 
@Tab: the time interval between the end of pulse A and the beginning of pulse B
@Tb: the width of pulse B
@T_waited_B: time to wait before B pulse could be generatored
@cycles_waited_B: number of clock cycles to wait
@delayB: delay before pulse B could be generated
'''

#Tab = 0.15 #150e-3
Tb = Ta 
T_waited_B = T_waited_A + Ta + Tab
cycles_waited_B = GetWaitandDelay(t0, T_waited_B)[0]
delayB = GetWaitandDelay(t0, T_waited_B)[1]

command_B_1 = ":PULSe2:WIDth {}".format(Tb)
command_B_2 = ":PULSe2:DELay {}".format(delayB)
command_B_3 = ":PULSe2:WCOunter {}".format(cycles_waited_B)

pulse_generator.write(command_B_1)
pulse_generator.write(command_B_2)
pulse_generator.write(command_B_3)

#combine the output of A and B so that their pulses. A = A + B
pulse_generator.write(":PULSe1:MUX 3") # 3 = (00000011) binary

#channel C programming (mode: ss)
'''
parameters: 
@Tc: the width of pulse c

'''

#Tc = 0.065 #65e-3
command_C_1 =  ":PULSe3:WIDth {}".format(Tc)
pulse_generator.write(command_C_1)

#channel D programming (mode: ss)
'''
parameters: 
@Td: the width of pulse d
@Twaited_D: 
@cycles_waited_D: number of clock cycles to wait
@delayD: delay before pulse D could be generated

'''
#Td = 0.05      #50e-3
T_waited_D = T_waited_B + Ta 
cycles_waited_D = GetWaitandDelay(t0, T_waited_D)[0]
delayD = GetWaitandDelay(t0, T_waited_D)[1]

command_D_1 = ":PULSe4:WIDth {}".format(Td)
command_D_2 = ":PULSe4:DELay {}".format(delayD)
command_D_3 = ":PULSe4:WCOunter {}".format(cycles_waited_D)

pulse_generator.write(command_D_1)
pulse_generator.write(command_D_2)
pulse_generator.write(command_D_3)

#channel E programming (mode: burst)
'''
parameters: 
@Te: the width of E bursts, which is half of t0
@cycles_waited_E: number of clock cycles to wait
@delayE: delay before pulse D could be generated
@n_burst: number of bursts to generate
'''

Te =  t0
cycles_waited_E = 0
delayE = 0
n_burst = int(Td // t0)

command_E_1 = ":PULSe5:WIDth {}".format(Te)
command_E_2 = ":PULSe5:DELay {}".format(delayE)
command_E_3 = ":PULSe5:WCOunter {}".format(cycles_waited_E)

pulse_generator.write(command_E_1)
pulse_generator.write(command_E_2)
pulse_generator.write(command_E_3)
pulse_generator.write(":PULSe5:PCOunter 1")
pulse_generator.write(":PULSe5:OCOunter 1")
pulse_generator.write(":PULSe5:CGATe HIGH")

#channel F programming (mode: burst)
'''
parameters: 
@Tf: the width of E bursts, which is half of t0
@Twaited_f: 
@cycles_waited_F: number of clock cycles to wait
@delayF: delay before pulse D could be generated
@n_burst: number of bursts to generate
'''

Tf = t0
cycles_waited_F = 1
delayF = 0

command_F_1 = ":PULSe6:WIDth {}".format(Tf)
command_F_2 = ":PULSe6:DELay {}".format(delayF)
command_F_3 = ":PULSe6:WCOunter {}".format(cycles_waited_F)

pulse_generator.write(command_F_1)
pulse_generator.write(command_F_2)
pulse_generator.write(command_F_3)
pulse_generator.write(":PULSe6:PCOunter 1")
pulse_generator.write(":PULSe6:OCOunter 1")
pulse_generator.write(":PULSe6:CGATe HIGH")


#channel G : outputting the same waveform as C (G = C)
#pulse_generator.write(":PULSe7:MUX 4") # 4 = (00000100) binary

#channel H: outputting C + D
pulse_generator.write(":PULSe8:MUX 12") # 12 = (00001100) binary


#switch the pulse generator on and test for a duration(if needed)
#Run(pulse_generator, duration)







