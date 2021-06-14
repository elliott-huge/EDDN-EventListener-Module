import FSDJumpTools
import csv
#from miscTools import *
import miscTools
import EDDNEventTools
import re as regex
import datetime





def systemPopulationCheck(jsonData, minPopulation):
    """Event: FSDJump. Checks if the system is higher than a specified value."""
    if FSDJumpTools.getSystemPopulation(jsonData) >= minPopulation:
        return True
    return False

def checkSystemDistanceSol(jsonData, maxDistance):
    """Event: FSDJump. returns float value of the system's distance to Sol."""
    coordinates = FSDJumpTools.getSystemCoordinates(jsonData)
    distance = miscTools.get3dDistance(coordinates)
    return (distance < maxDistance)

def systemIsInList(jsonData, systemList):
    """Checks the current system name against a system list."""
    system = FSDJumpTools.getStarSystem(jsonData)
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

def compareActiveSystemFactionStates(jsonData, givenStates):
    """Iterates over each faction, returns True or False if any factions are in the desired state(s)"""
    factionsList = FSDJumpTools.getFactions(jsonData)
    for faction in factionsList:
        if compareActiveFactionStates(faction, givenStates):
            return True
    
    return False



def compareActiveFactionStates(faction, givenStates):
    """Checks if a faction is in a given set of states, returns their details"""
    activeStates = FSDJumpTools.getFactionActiveStates(faction)

    if activeStates == None:
        return False
    
    i = 0
    for state in activeStates:
        if state in givenStates:
            i+=1
    
    if i == len(givenStates):
        return True
    
    return False

def compareEventAge(jsonData, maxAgeMinutes):
    """If timestamp of message is within 15 minutes of now, return True"""

    # Guard clause for events without timestamps (erroneous data)
    eventTimestampString = FSDJumpTools.getTimeStamp(jsonData)
    if eventTimestampString == None:
        return False
    
    regexPattern = "(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2}:\d{2})."
    
    cleanTimestampArr = regex.split(regexPattern, eventTimestampString)
    dateTimeString = cleanTimestampArr[1] + " " + cleanTimestampArr[2] + ".000000"
    eventDate = datetime.datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S.%f')

    # Checks minutes passed since event recorded (all in UTC)
    delta_time = datetime.datetime.utcnow() - eventDate
    minutesPassed = delta_time.seconds / 60

    if minutesPassed < maxAgeMinutes:
        return True

    return False

class factionStatusNotification:
    
    def __init__(self, notificationName, activeStateList = None, population = 1, maxDistToSol = 250, systemList = None):
        """Generates a faction Status notification for a program to listen for. Parameters are self-descriptive. !WILL ONLY CHECK IF A SINGLE FACTION HAS ALL THE LISTED STATES ACTIVE!"""
        # parameter setup
        self.notificationName = notificationName
        self.activeStateList = activeStateList
        self.population = population
        self.maxDistToSol = maxDistToSol
        self.systemList = systemList

        
        self.validResultFlag = False
        self.resultDataDump = None
        self.resultSystem = None
        self.resultFactions = None

    def assessFSDJumpEvent(self, jsonData):
        """Returns None if criteria aren't met, returns ValidFactions at [0] (see factionInStates) and the event's jsonData at [1]"""
        self.validResultFlag = False
        self.resultDataDump = None
        self.resultSystem = None
        self.resultFactions = None

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
        if checkSystemDistanceSol(jsonData, self.maxDistToSol):
            return

        #guard
        if not compareEventAge(jsonData, 30):
            return
        
        #optional param guard
        if self.systemList != None:
            if not systemIsInList(jsonData, self.systemList):
                return
        
        #optional param guard
        if self.activeStateList != None and compareActiveFactionStates(jsonData, self.activeStateList):
            


            # return a HIT (???)
            #TODO make into a function
            self.validResultFlag = True
            self.resultDataDump = jsonData
            self.resultSystem = FSDJumpTools.getStarSystem(jsonData)
            #TODO make getValidFactions(1,2)
            self.resultFactions = miscTools.getValidFactions(jsonData, self.activeStateList)
            return

        # default (???)
        #TODO make into a function
        self.validResultFlag = True
        self.resultDataDump = jsonData
        self.resultSystem = FSDJumpTools.getStarSystem(jsonData)

        return
