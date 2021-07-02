import zlib
import zmq
import simplejson
import sys
import time
from Classes.factionStatusNotification import factionStatusNotification
from Classes.FSDJumpEvent import createFSDJumpEvent
from Classes.EDDNEvent import createMessageFromJson
from HelperFunctions.miscTools import systemListFromCSV

__relayEDDN             = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN           = 600000

#boomAlert = factionStatusNotification("BoomSystemFactions Alert", ["Boom"], False, 1000000, 100)
candidateList = systemListFromCSV("Data\candidateSystems pop 500k.csv", 0)
Alert = factionStatusNotification("Gold / Silver Alert", ["InfrastructureFailure"], False, 30000000, 250, 0.25, candidateList)
#iFAlert = factionStatusNotification("Gold / Silver Alert", ["InfrastructureFailure"], False, 5000000, 220)
fName = "goldRushSystems.txt"
f = open(fName, "a")
f.write(f"{Alert.notificationName}:\n")
f.close()

hitSystems = []
hitSystemNames = []

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

                message = createMessageFromJson(__json)
                fsdEvent = createFSDJumpEvent(message)

                if fsdEvent != None:
                    hit = Alert.assessFSDJumpEvent(fsdEvent)
                    if hit != None and hit.systemName not in hitSystemNames:
                        print(f"System: {hit.systemName}, System Population: {hit.systemPopulation}, Controlling Faction: {hit.controllingFactionName}")
                        hitSystems.append(hit)
                        hitSystemNames.append(hit.systemName)
                        f = open(fName, "a")
                        f.write(f"{hit.systemName}, Population: {hit.systemPopulation}\n")
                        for faction in hit.factions:
                            states = faction.listStateNames("active")
                            isControlling = ", is the Controlling Faction!" if faction.controllingFlag else ""
                            f.write(f"      {faction.name}, States: {states}, Influence: {faction.influenceDecimal}{isControlling}\n")
                        f.close()

                        

                # if a.result != None:
                #     print("System '{0}' has been pinged by {1}:".format(a.result[1]['message'].get('StarSystem'), a.notificationName))
                #     for faction in a.result[0]:
                #         print("Faction: '{0}', of Influence: '{1}', is in States: '{2}'".format(faction[1], faction[2], faction[3]))
                #     i+=1


            
            wait = input()
        except zmq.ZMQError as e:
            print ('ZMQSocketException: ' + str(e))
            sys.stdout.flush()
            subscriber.disconnect(__relayEDDN)
            time.sleep(5)
            
        

if __name__ == '__main__':
    main()
