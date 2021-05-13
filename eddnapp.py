import zlib
import zmq
import simplejson
import sys
import time
import math
## not mine
import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
## not mine

"""
 "  Configuration
"""
__relayEDDN             = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN           = 600000

## not mine
NUMBER_X: int = 300
NUMBER_Y: int = 300

CANVAS_WIDTH:  int = 300
CANVAS_HEIGHT: int = 300


## not mine

# check if log is of specified type
def eventTypeCheck(jsonData, type):
    if jsonData['message'].get('event') == type:
        return True
    return False

# check if system is at least of specified population
def systemPopulationCheck(jsonData, minPopulation):
    if jsonData['message'].get('Population') >= minPopulation:
        return True
    return False

# returns float value of distance to Sol
def systemDistanceFromSol(jsonData):
    coordinates = jsonData['message'].get('StarPos')
    sqr = 0
    for i in coordinates:
        sqr += i*i
    return round(math.sqrt(sqr))

def hasEvent(jsonData):
    if jsonData['message'].get('event') == None:
        return False
    return True

def eventIsExtant(event, eventDict):
    if event in eventDict.keys():
        return True
    return False

# pass eventDict as ref
def addToEventCounter(eventDict, jsonData):
    if hasEvent(jsonData) == False:
        return eventDict
    event = jsonData['message'].get('event')
    if eventIsExtant(event, eventDict):
        eventDict[event] += 1
        return eventDict
    eventDict[event] = 1
    return eventDict

def plotSystem(x, z, col, name):
    plt.scatter(x,z,color=col,s=3)
    plt.annotate(name, (x,z), color="white")


# is the system on the shortlist?
# TODO : make the shortlist lel
# is the faction major, booming, and under civil liberty
def main():
    context     = zmq.Context()
    subscriber  = context.socket(zmq.SUB)
    
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)

    eventCounter = {
        "Scan": 0,
        "FSDJump" : 0,
        "MarketUpdate": 0
    }

    nonEventCounter = 0
    i = 0

    fig = plt.figure()
    ax = plt.axes()
    ax.set_facecolor("black")
    ax.set(xlim=(-400, 400), ylim=(-400, 400))
    ax.set_title("1500 EDDN Jumps on 13/05/2021 around Sol")
    plt.xlabel("X  LY")
    plt.ylabel("Y  LY")
    plt.grid(color="white", lw=0.25, ls='--')

    plotSystem(55.72, 27.15, 'red', "Shinrarta Dezhra")
    plotSystem(-352.78, -346.34, 'blue', "Sothis")
    plotSystem(-303.41, -314.16, 'white', "Robigo")
    plotSystem(122.62, -47.28, 'orange', "Deciat")
    plotSystem(-348.66, -339.22, 'red', "Ceos")
    plotSystem(0.0, 0.0, 'green', "Sol")

    while True:
        try:
            subscriber.connect(__relayEDDN)
            while i <= 1500:
                sys.stdout.flush()
                __message   = subscriber.recv()
                if __message == False:
                    subscriber.disconnect(__relayEDDN)
                    break
                
                __message   = zlib.decompress(__message)
                __json      = simplejson.loads(__message)
                if hasEvent(__json) == False:
                    continue
                if eventTypeCheck(__json, "FSDJump") and systemDistanceFromSol(__json) < 565:
                    data = __json['message'].get('StarPos')
                    # remove y dimension
                    data.pop(1)

                    # check if location is within area of interest (TODO: write a function for this you git)
                    if data[0] < 400 and data[0] > -400 and data[1] < 400 and data[1] > -400:
                        plt.scatter(data[0], data[1], marker='o', color='cyan', alpha=0.15, s=1.2)
                        i += 1
                        if i > 1 and i % 100 == False:
                            print(str(i) + " Jumps Plotted")

            plt.savefig("flightmap.png", dpi=300)
            plt.show()
            plt.clf()
            wait = input()
        except zmq.ZMQError as e:
            print ('ZMQSocketException: ' + str(e))
            sys.stdout.flush()
            subscriber.disconnect(__relayEDDN)
            time.sleep(5)
            
        

if __name__ == '__main__':
    main()
