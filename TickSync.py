#!/usr/bin/env python
#rqueiroz@gsd.uwaterloo.ca
# ---------------------------------------------
# TickSync
# Syncronize simulation loop based on a given frequency (frame-rate).
# Higher rate allows smoother trajectories and more precise metrics and collisions,
# but requires more processing capabilities. Can't avoid drift if hardware is slow.
# --------------------------------------------

import datetime
import time

class TickSync():
    def __init__(self, rate = 30, realtime = True, block = False, verbose = False, label = ""):
        #config
        self.timeout = None
        self.tick_rate = rate
        self.expected_tick_duration = 1.0/rate
        self.realtime = realtime
        self.block = block
        self.verbose = verbose
        self.label = label
        #global
        self._sim_start_clock = None        #clock time when sim started (first tick) [clock] 
        self.tick_count = 0
        self.sim_time = 0.0                 #Total simulation time since start() [s]
        #per tick
        self._tick_start_clock = None       #sim time when tick started [s] 
        self.delta_time = 0.0               #diff since previous tick [s] (aka frame time) 
        self.drift = 0.0                    #diff between expected tick time and actual time caused by lag
    
    def set_timeout(self,timeout):
        self.timeout = timeout
    
    def print(self,msg):
        if (self.verbose):
            print(msg)

    def tick(self):
        now = datetime.datetime.now()
        #First Tick
        if (self.tick_count==0): 
            #First Tick is special:
            self._sim_start_clock = now
            self.delta_time = 0.0
            self._tick_start_clock = now
            #Update globals
            self.tick_count+=1
            self.sim_time = 0.0
            self.print('{:05.2f}s {} Tick {:3}# START'.
                    format(self.sim_time,self.label,self.tick_count))
            return True
        else:
            #Can tick? Preliminary numbers:
            diff_tick = (now - self._tick_start_clock).total_seconds()                #diff from previous tick
            drift =  diff_tick - self.expected_tick_duration                        #diff from expected time
            if (drift<0):
                #Too fast. Need to chill.
                if (self.block):
                    time.sleep(-drift)      #blocks diff if negative drift
                    #self.print('sleep {:.3}'.format(drift))
                else:
                    #self.print('skip {:.3}'.format(drift))
                    return False            #return false to skip
        #Can proceed tick: on time or late (drift):
        now = datetime.datetime.now()    #update after wake up
        self.delta_time = (now - self._tick_start_clock).total_seconds()         #diff from previous tick
        self.drift = self.delta_time - self.expected_tick_duration        #diff from expected time
        self._tick_start_clock = now
        #Update globals
        self.sim_time = (now - self._sim_start_clock).total_seconds()
        self.tick_count+=1
        #Check timeout
        if (self.timeout):
            if (self.sim_time>=self.timeout):
                self.print('{} TIMEOUT: {:.3}s'.format(self.label,self.sim_time))
                return False

        self.print('{:05.2f}s {} Tick {:3}# +{:.3f} e{:.3f} d{:.3f} '.
                    format(self.sim_time,self.label,self.tick_count, self.delta_time, self.expected_tick_duration, self.drift))
        return True


   