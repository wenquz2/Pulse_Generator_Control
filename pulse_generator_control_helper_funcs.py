import time

'''
Helper function to obtain the "wait" and "delay" parameters for pulses in single shot modes
parameters:
@T0: internal clock cycle
@t_interval: time interval till certain pulse is to be turned on
return: cycles_waited: how many cycles to wait until starting pulse
        delay: delay as a parameter to be passed into the pulse generator
'''

def GetWaitandDelay(T0, t_interval):
    cycles_waited = int (t_interval // T0)
    delay = t_interval - T0 * cycles_waited
    return (cycles_waited, delay)


'''
Helper function to set the modes of the pulse generators channels to values that are fit for the experiment
parameters:
@T0: internal clock cycle
@t_interval: time interval till certain pulse is to be turned on
return: cycles_waited: how many cycles to wait until starting pulse
        delay: delay as a parameter to be passed into the pulse generator
'''

def SetModesDefault(instrument):
    #setting the single shot channels
    for i in range(8):
        command = ":PULSe{}:CMODe {}".format(i + 1, "SINGle")
        instrument.write(command)

    #setting the channels (E, F) to burst mode
    for i in range(5, 7, 1):
        command = ":PULSe{}:CMODe {}".format(i, "DCYCle")
        instrument.write(command)


'''
Helper function to switch the pulse generator on and then turn off automatically after the duration of the test has expired. 
parameters:
@instrument: the instrument of interest
@duration: the duration of running, if empty then will default to 10000 seconds runtime
'''

def Run(instrument, duration = 10000):
        start = time.time()
        instrument.write(":PULSe0:STATe 1")
        while(True):
                if time.time() - start > duration:
                        instrument.write(":PULSe0:STATe 0")
                        break