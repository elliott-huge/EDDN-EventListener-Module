import FSDJumpEventTools
import csv
#from miscTools import *
import miscTools
import EDDNEventTools
import re as regex
import datetime





def systemPopulationCheck(message, minPopulation):
    """Event: FSDJump. Checks if the system is higher than a specified value."""
    if FSDJumpEventTools.getSystemPopulation(message) >= minPopulation:
        return True
    return False

def checkSystemDistanceSol(message, maxDistance):
    """Event: FSDJump. returns float value of the system's distance to Sol."""
    coordinates = FSDJumpEventTools.getSystemCoordinates(message)
    distance = miscTools.get3dDistance(coordinates)
    return (distance < maxDistance)

def systemIsInList(message, systemList):
    """Checks the current system name against a system list."""
    system = FSDJumpEventTools.getStarSystem(message)
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

def compareActiveFactionState(faction, seekState):
    """Checks if a single faction is in a single given state"""
    activeStates = FSDJumpEventTools.getFactionActiveStates(faction)

    # Has no active states
    if activeStates == None:
        return False
    
    # Has a match
    for state in activeStates:
        if state == seekState:
            return True

    # Has active states, none match the seek state
    return False

def compareActiveFactionStates(faction, givenStates, strictFlag = False):
    """Checks if a faction is in all of the given state(s), strictFlag=True to allows exact matches only"""
    i = 0
    stateRequirement = givenStates.len()
    for seekState in givenStates:
        if compareActiveFactionState(faction, seekState):
            i+=1
    if i == stateRequirement or i >= stateRequirement and not strictFlag:
        return True
    
    return False


def compareActiveSystemStates(message, givenStates, strictFlag = False):
    """Checks if any of the system's factions are in all of the desired state(s), strictFlag=True to allows exact matches only"""
    factionsList = FSDJumpEventTools.getIfFactions(message)
    if factionsList == None:
        # System has no factions... is this intended behaviour?
        return False

    for faction in factionsList:
        if compareActiveFactionStates(faction, givenStates, strictFlag):
            return True
    # Has factions, match not found
    return False




#TODO: refactor and break into EDDNEventTools / miscTools
def compareEventAge(jsonData, maxAgeMinutes):
    """If timestamp of message is within 15 minutes of now, return True"""

    # Guard clause for events without timestamps (erroneous data)
    eventTimestampString = FSDJumpEventTools.getTimeStamp(jsonData)
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


#TODO: delet
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
            self.resultSystem = FSDJumpEventTools.getStarSystem(jsonData)
            #TODO make getValidFactions(1,2)
            self.resultFactions = miscTools.getValidFactions(jsonData, self.activeStateList)
            return

        # default (???)
        #TODO make into a function
        self.validResultFlag = True
        self.resultDataDump = jsonData
        self.resultSystem = FSDJumpEventTools.getStarSystem(jsonData)

        return
