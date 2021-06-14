from EDDNEventTools import *
from os import stat
#TODO this entire file and any other appropriate functions to be added

def getIfFSDJumpEventMessage(jsonData):
    """Returns the event's message if it is an FSDJump Event, otherwise returns None"""
    message = getMessageData(jsonData)
    if eventTypeCheck(message, "FSDJump"):
        return message
    return None

def getIfFSDJumpEventObject(jsonData):
    """Returns the a new FSDJumpEvent it is an FSDJump Event, otherwise returns None"""
    message = getMessageData(jsonData)
    if eventTypeCheck(message, "FSDJump"):
        return FSDJumpEvent(message)
    return None

# ----The following functions should all return a complete value for a well-formed FSDJump event's message, they will raise an exception otherwise----

def getStarSystem(message):
    """Takes FSDJump event message, returns the star system name as a string"""
    system = message.get('StarSystem')
    if system != None:
        return system
    raise ValueError('getStarSystem(): No star system entry was found in the FSDJump events message')

def getSystemCoordinates(message):
    """Takes FSDJump event message, returns a star system's coordinates as a list"""
    positionxyz = message.get('StarPos')
    if positionxyz != None:
        return positionxyz
    raise ValueError('getSystemCoordinates(), star position attribute was not found in the FSDJump events message')

def getSystemPopulation(message):
    """Takes FSDJump event message, returns the population of that system"""
    population = message.get('Population')
    if population != None:
        return population
    raise ValueError('getSystemPopulation(), population attribute was not found in the FSDJump events message')

class FSDJumpEvent(Event):
    """FSDJump Event class, for those preferring an OOP approach"""
    def __init__(self, message):
        super().__init__
        self.systemName = getStarSystem(message)
        self.systemCoordinates = getSystemCoordinates(message)
        self.systemPopulation = getSystemPopulation(message)
        self.messageData = message

# ----The following functions will return None if no entry is found, this is the inteded behaviour----

def getIfFactions(message):
    """Takes FSDJump event message, returns a list of Factions, may return None if none are found"""
    factions = message.get('Factions')
    return factions

def getIfFactionActiveStates(faction):
    """Returns the state(s) of a Faction, may return None if none are found"""
    states = []
    statesRaw = faction.get('ActiveStates')
    if statesRaw == None:
        return None

    states = []
    for state in statesRaw:
        states.append(state['State'])

    return states