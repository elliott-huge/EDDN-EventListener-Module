import zlib
import zmq
import simplejson
import sys
import time
import requests
from factionStatusListener import *

__relayEDDN             = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN           = 600000
#factionStatusNotification("BoomSystemFactions Alert", ["Boom"], 1000000, 100, systemListFromCSV('candidateSystems pop 500k.csv', 0))
a = factionStatusNotification("BoomSystemFactions Alert", ["Boom"], 1000000, 100)
#b = requests.get('https://elitebgs.app/api/ebgs/v5/stations?system=gateway&type=orbis&count=0', allow_redirects=True)
#print(b)
#wait = input()
def main():
    context     = zmq.Context()
    subscriber  = context.socket(zmq.SUB)
    
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)

    i = 0
    while True:
        try:
            subscriber.connect(__relayEDDN)
            #iterator so you dont go ham
            while i < 10:
                sys.stdout.flush()
                __message   = subscriber.recv()
                if __message == False:
                    subscriber.disconnect(__relayEDDN)
                    break
                __message   = zlib.decompress(__message)
                __json      = simplejson.loads(__message)

                a.assessFSDJumpEvent(__json)

                if a.result != None:
                    print("System '{0}' has been pinged by {1}:".format(a.result[1]['message'].get('StarSystem'), a.notificationName))
                    for faction in a.result[0]:
                        print("Faction: '{0}', of Influence: '{1}', is in States: '{2}'".format(faction[1], faction[2], faction[3]))
                    i+=1


            wait = input()
        except zmq.ZMQError as e:
            print ('ZMQSocketException: ' + str(e))
            sys.stdout.flush()
            subscriber.disconnect(__relayEDDN)
            time.sleep(5)
            
        

if __name__ == '__main__':
    main()
