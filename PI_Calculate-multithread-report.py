# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:32:23 2015

@author: lucien
"""
debug = False
# use this later (((x + 1)/2)%2)*2-1 to get sign (1,-1,1,-1...)
import Queue
import threading

def sgn(theNumb):
    if theNumb>0:
        return 1
    elif theNumb<0:
        return -1
    else:
        return 0
        
def calculatePiSet(testRange,theQueue):
    piReturnValue=0.
    for ii in testRange:
        ii=(ii*2)+1
        piReturnValue=piReturnValue+ 4*(((((ii + 1)/2)%2)*2-1)*1./ii)
        if debug:
            print(str((((ii + 1)/2)%2)*2-1) + " * 4/" + str(ii))
    theQueue.put(piReturnValue)
    if debug:
        print("placing: " + str(piReturnValue))
    #return piReturnValue
        
    

if __name__ == '__main__':
    # USER SET
    threadCount = 20
    calculateTimes = 100

    
    rangeOffset=0
    finalPi=0    
    while True:
        calculateTimes = calculateTimes + (threadCount-(calculateTimes % threadCount))%threadCount
        calculateThreadAmount = int(calculateTimes/threadCount)
        
        if debug:
            
            print(calculateTimes)
        
        q = Queue.Queue()
        
        '''for ii in range(calculateTimes):
            thePi = thePi + 4.* 1./ ((ii*2)+1) * ((-1)**ii)'''
            
        herpDerp=0
        for ii in range(threadCount):
            if debug:
                print("=====  ii = "+str(ii))
                
            low = ii * calculateThreadAmount + rangeOffset
            high = (ii+1) * calculateThreadAmount + rangeOffset
            if debug:
                print("low: "+str(low))
                print("High: "+str(high))
                print("range: "+ str(range(low,high)) +"\n")
                
            #calculatePiSet(range(low,high),q)
            t = threading.Thread(target=calculatePiSet, args = (range(low,high),q))
            t.daemon = True
            t.start()
        
        t.join()
        if debug:
            print("=======assembling=======")
        while not q.empty():
            finalPi=finalPi+q.get()
            if debug:
                print("Pi: "+str(finalPi))
            q.task_done()
            
        print("Final PI: " + str(finalPi))
        rangeOffset=high
        
        #print(thePi)