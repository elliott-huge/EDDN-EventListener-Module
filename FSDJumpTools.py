from EDDNEventTools import eventTypeCheck, getMessage
from os import stat
#TODO this entire file and any other appropriate functions to be added

def checkGetFSDJumpEvent(jsonData):
    """Returns the event's message if it is an FSDJump Event, otherwise returns None"""
    message = getMessage(jsonData)
    if eventTypeCheck(message, "FSDJump"):
        return message
    return None

# The following functions all should return a complete value for a well-formed FSDJump event
# They will throw an exception if their data is not found
class FSDJumpEvent:
    def __init__(self, message):
        #TODO super() ??
        super(self, message).__
        self.systemName = message.get('StarSystem')


def getStarSystem(message):
    """Returns the star system name as a string"""
    system = message.get('StarSystem')
    if system != None:
        return system
    raise ValueError('getStarSystem(): No star system entry was found in the FSDJump events message')

def getSystemCoordinates(message):
    positionxyz = message.get('StarPos')
    if positionxyz != None:
        return positionxyz
    raise ValueError('getSystemCoordinates(), star position attribute was not found in the FSDJump events message')

def getSystemPopulation(message):
    population = message.get('Population')
    if population != None:
        return population
    raise ValueError('getSystemPopulation(), population attribute was not found in the FSDJump events message')

def getFactions(message):
    """Returns a list of Factions, may return None if none are found"""
    factions = message.get('Factions')
    return factions

def getFactionActiveStates(faction):
    """Returns the state(s) of a Faction"""
    states = []
    statesRaw = faction.get('ActiveStates')
    if statesRaw == None:
        return None

    states = []
    for state in statesRaw:
        states.append(state['State'])

    return states





