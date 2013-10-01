#!/usr/bin/python
# This python script demonstrates the use of sampling to estimate the
# execution time of software.

#Import is similar to "include" in Java and in C.
import threading
import time
import math
from numpy.random import exponential

def app(state,scale,stop,log=True):
    """ App is the program that we want to profile.
    state: the current state of the program (can be 1,2 or 3)
    scale: The number of iterations in each state is a multiple of scale
    log: a flag that controls whether or not the program generates 
         a detailed log.
    """
    print "App Started"
    initial_time=time.time();   # record the time the program started
    last_time=initial_time      # last_time and now are variables used
                                # to store the time a section of the
                                # program is executed
    Total1=0; Total2=0; Total3=0;
    # app loop ###############################################################
    while not stop.is_set():
        state[0]=1;  # set state to 1
        if log: print_state(state, initial_time, 'switch to state 1')
        for j in range(scale*3): # this is the loop that consumes most
                                 # of the time in the state, it is
                                 # execute scale*3 times
            a=math.log(j+1)      # an arbitrary command that is
                                 # executed in the loop
        now=time.time(); 
        Total1 += now-last_time; # add to Total1 the sufference
                                 # between the time at the start of
                                 # state 1 and the time at the end of
                                 # state 1.
        last_time=now

        # The two following section are similar to the first one, the
        # difference is only in the state number and in the number of
        # times that the loop is executed.
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
    End of profiled segment ##########################################################
    
    # print out a summary of what happened using the exact measures Total1, Total2, Total3
    print 'app stopped after ',time.time()-initial_time, 'seconds'
    print 'Total1=%5.2f, Total2=%5.2f, Total3=%5.2f' % (Total1,Total2,Total3)
    Sum_Total=Total1+Total2+Total3
    print 'Sum Total=',Sum_Total
    print 'Frac1=%5.2f, Frac2=%5.2f, Frac3=%5.2f' % (Total1/Sum_Total,Total2/Sum_Total,Total3/Sum_Total)

def print_state(state, initial, message):
    print "%6.4f: state=%1d \t%s" % (time.time()-initial,state[0],message)


####### Main part of the script ###########
if __name__=='__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Demonstration of sampling method ')

    parser.add_argument('-s','--sample_step', type=float, default='0.01',
                        help='the expected time between consecutive samples')
    parser.add_argument('-n','--n',type=int, default=100,
                        help='number os samples')
    parser.add_argument('-i','--Iteration_Length', type=int, default='100',
                        help='Length of each inner loop in app')
    parser.add_argument('-l','--log',action='store_true',default=False,
                        help='Log loops and samples as they occur (if False, only summary is printed)')

    args = vars(parser.parse_args())
    print args
    # log=True and sample_step=0.001 generates very biased results.
    # log=True and sample_step=0.01 also generates biased results
    # log=False and sample_step=0.01 is good.
    log=args['log']
    sample_step=args['sample_step']
    Iteration_Length=args['Iteration_Length']
    n=args['n']

    state=[0]
    # Create a parallel thread running the app
    try:   # the following thread-related command are surrounded by a "try" to catch any problems.
        stop = threading.Event()
        stop.clear()
        t = threading.Thread(target=app, args = (state,Iteration_Length,stop), kwargs={'log':log})
        t.start()
    except:
        print "Error: unable to start thread"

    timer=time.time()    
    count=[0]*4            # this defines a list of length 4 [0,0,0,0]
    # Sampling loop   ########################################################################
    for i in range(n):          # n is the number of samples
        if log:
            ntime=time.time()
            delta=ntime - timer
            timer=ntime
            print '-------- state=%1d, sample_step= %5.3f time since last=%5.3f' % (state[0],sample_step,delta)
            
        count[state[0]] += 1 # increment the count corresponding to the current state of app()
        time.sleep(exponential(sample_step))   # sleep for a random length of time (exponentially distributed)
    ##########################################################################################

    stop.set()      # send event to thread to cause it to terminate.
    time.sleep(0.5) # make sure that the app() thread terminated.

    # print the results of the sampling. 
    print count[1:]
    sum=float(count[1]+count[2]+count[3])
    print '\t'.join(['%1d: %5.3f' %(i,count[i]/sum) for i in range(1,4)])

