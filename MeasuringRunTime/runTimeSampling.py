#!/usr/bin/python
# This python script demonstrates the use of sampling to estimate the execution time of software.

import threading
import time
import math
from numpy.random import exponential

# Define a function for the thread

def print_state(state, initial, message):
    print "%6.4f: state=%1d \t%s" % (time.time()-initial,state[0],message)

def app(state,scale,stop,log=True):
    print "App Started"
    initial_time=time.time();
    last_time=initial_time
    Total1=0; Total2=0; Total3=0;
    while not stop.is_set():
        state[0]=1; 
        if log: print_state(state, initial_time, 'switch to state 1')
        for j in range(scale*3):
            a=math.log(j+1)
        now=time.time(); Total1 += now-last_time; last_time=now

        state[0]=2;  
        if log: print_state(state, initial_time, 'switch to state 2')
        for j in range(scale*5):
            a=math.log(j+1)
        now=time.time(); Total2 += now-last_time; last_time=now

        state[0]=3;  
        if log: print_state(state, initial_time, 'switch to state 3')
        for j in range(scale*2):
            a=math.log(j+1)
        now=time.time(); Total3 += now-last_time; last_time=now
    
    print 'app stopped after ',time.time()-initial_time, 'seconds'
    print 'Total1=%5.2f, Total2=%5.2f, Total3=%5.2f' % (Total1,Total2,Total3)
    Sum_Total=Total1+Total2+Total3
    print 'Sum Total=',Sum_Total
    print 'Frac1=%5.2f, Frac2=%5.2f, Frac3=%5.2f' % (Total1/Sum_Total,Total2/Sum_Total,Total3/Sum_Total)

if __name__=='__main__':
    # log=True and sample_step=0.001 generates very biased results.
    # log=True and sample_step=0.01 also generates biased results
    # log=False and sample_step=0.01 is good.
    log=False
    sample_step=0.01
    n=1000    # number of samples

    state=[0]
    # Create a parallel thread running the app
    try:
        stop = threading.Event()
        stop.clear()
        t = threading.Thread(target=app, args = (state,100,stop), kwargs={'log':log})
        t.start()
    except:
        print "Error: unable to start thread"

    timer=time.time()    
    count=[0]*4
    for i in range(n):
        if log:
            ntime=time.time()
            delta=ntime - timer
            timer=ntime
            print '-------- state=%1d, sample_step= %5.3f time since last=%5.3f' % (state[0],sample_step,delta)
            
        count[state[0]] += 1
        time.sleep(exponential(sample_step))

    stop.set()     # send event to thread to cause it to terminate.
    time.sleep(0.5)

    print count[1:]
    sum=float(count[1]+count[2]+count[3])
    print '\t'.join(['%1d: %5.3f' %(i,count[i]/sum) for i in range(1,4)])

