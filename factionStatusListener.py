import math
import csv
import re as regex
import datetime

def hasEvent(jsonData):
    """Checks if there is ANY entry of type 'event' in a json."""
    if jsonData['message'].get('event') == None:
        return False
    return True

def eventTypeCheck(jsonData, eventType):
    """Checks if the json's event is of a specified eventType."""
    if jsonData['message'].get('event') == eventType:
        return True
    return False

def systemPopulationCheck(jsonData, minPopulation):
    """Event: FSDJump. Checks if the system is higher than a specified value."""
    if jsonData['message'].get('Population') >= minPopulation:
        return True
    return False

def systemDistanceFromSol(jsonData):
    """Event: FSDJump. returns float value of the system's distance to Sol."""
    coordinates = jsonData['message'].get('StarPos')
    sqr = 0
    for i in coordinates:
        sqr += i*i
    return round(math.sqrt(sqr))

def systemIsInList(jsonData, systemList):
    """Checks the current system name against a system list."""
    system = jsonData['message'].get('StarSystem')
    if system in systemList:
        return True
    return False

def systemListFromCSV(fileName, sysNameColumn):
    """Takes the path of a CSV file and returns a list of system name strings given their column number (index is from zero)."""
    systemList = []
    rowCount = 0
    with open(fileName, newline='') as inputcsv:
        reader = csv.reader(inputcsv, delimiter=',', quotechar='"')
        for row in reader:
            systemList.append(row[sysNameColumn])
            rowCount += 1
    print("System entries = {0}".format(rowCount))
    return systemList

def systemFactionsInStates(jsonData, activeStatesList):
    """Iterates over each faction, returns either None or an array of faction data."""
    factions = jsonData['message'].get('Factions')
    fctnsInStates = []
    for faction in factions:
        result = factionInStates(faction, activeStatesList)
        if not result:
            continue
        fctnsInStates.append(result)
    if len(fctnsInStates) > 0:
        return fctnsInStates
    return None
        

def factionInStates(faction, activeStatesList):
    """Checks if a faction is in a given set of states, returns their details"""
    i = 0
    foundStates = []
    if faction.get('ActiveStates') == None:
        return False
    for state in faction.get('ActiveStates'):
        foundStates.append(state['State'])
        if state['State'] in activeStatesList:
            i+=1
    if i == len(activeStatesList):
        return True, faction['Name'], faction['Influence'], foundStates
    return False

def validateTimestamp(jsonData):
    """If timestamp of message is within 15 minutes of now, return True"""

    # Guard clause for events without timestamps
    if jsonData['message'].get('timestamp') == None:
        print("No timestamp was found!")
        return False

    eventTimestampString = jsonData['message'].get('timestamp')
    regexPattern = "(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2}:\d{2})."
    
    cleanTimestampArr = regex.split(regexPattern, eventTimestampString)
    dateTimeString = cleanTimestampArr[1] + " " + cleanTimestampArr[2] + ".000000"
    eventDate = datetime.datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S.%f')

    # Checks minutes passed since event recorded (all in UTC)
    # A more elegant solution would check if the data was recorded after the last tick
    delta_time = datetime.datetime.utcnow() - eventDate
    minutesPassed = delta_time.seconds / 60

    if minutesPassed < 15:
        return True
    #prints failed events 
    #print(minutesPassed)
    return False

class factionStatusNotification:
    
    def __init__(self, notificationName, activeStateList = None, population = 1, maxDistToSol = 250, systemList = None):
        """Generates a faction Status notification for a program to listen for. Parameters are self-descriptive. !WILL ONLY CHECK IF A SINGLE FACTION HAS ALL THE LISTED STATES ACTIVE!"""
        self.notificationName = notificationName
        self.activeStateList = activeStateList
        self.population = population
        self.maxDistToSol = maxDistToSol
        self.systemList = systemList
        self.result = None

    def assessFSDJumpEvent(self, jsonData):
        """Returns None if criteria aren't met, returns ValidFactions at [0] (see factionInStates) and the event's jsonData at [1]"""
        self.result = None

        #guard
        if not hasEvent(jsonData):
            return
        
        #guard
        if not eventTypeCheck(jsonData, "FSDJump"):
            return
        
        #guard
        if not systemPopulationCheck(jsonData, self.population):
            return
        
        #guard
        if systemDistanceFromSol(jsonData) > self.maxDistToSol:
            return

        #guard
        if not validateTimestamp(jsonData):
            return
        
        #optional param guard
        if self.systemList != None:
            if not systemIsInList(jsonData, self.systemList):
                return
        
        #optional param guard
        if self.activeStateList != None:
            validFactions = systemFactionsInStates(jsonData, self.activeStateList)

            # Guard clause
            if validFactions == None:
                return

            # return a HIT
            self.result = []
            self.result.append(validFactions)
            self.result.append(jsonData)
            return

        # default
        return
