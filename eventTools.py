from os import stat

#TODO this entire file and any other appropriate functions to be added

def getStarSystem(jsonData):
    """Returns the star system name as a string"""
    system = jsonData['message'].get('StarSystem')
    if system != None:
        return system
    #throw exception?
    print("StarSystem data not found in jsonData (eventTools: getStarSystem)")
    return "None"

def getTimeStamp(jsonData):
    timeStamp = jsonData['message'].get('timestamp')
    if timeStamp != None:
        return timeStamp
    
    return timeStamp

def getFactions(jsonData):
    factions = jsonData['message'].get('Factions')
    return factions

def getFactionActiveStates(faction):
    states = None
    statesRaw = faction.get('ActiveStates')
    if statesRaw == None:
        return states

    states = []
    for state in statesRaw:
        states.append(state['State'])

    return states