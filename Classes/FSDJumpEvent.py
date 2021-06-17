from .EDDNEvent import *
from os import stat
#TODO this entire file and any other appropriate functions to be added

# def getIfFSDJumpEventObject(jsonData):
#     """Returns the a new FSDJumpEvent it is an FSDJump Event, otherwise returns None"""
#     message = getMessageData(jsonData)
#     if eventTypeCheck(message, "FSDJump"):
#         return FSDJumpEvent(message)
#     return None

# ----The following functions should all return a complete value for a well-formed FSDJump event's message, they will raise an exception otherwise----

class FSDJumpEvent(Event):
    """FSDJumpEvent class, an OOP approach, extends EDDNEvent"""
    def __init__(self, message):
        super().__init__
        # Jump data
        self.fuelUsed = message.get('FuelUsed')
        self.fuelLevel = message.get('FuelLevel')
        self.boostUsed = message.get('BoostUsed')

        # System data that's always present
        self.systemName = message.get('StarSystem')
        if self.systemName == None:
            # Backup data location
            self.systemName = message.get('SystemAddress')

        self.systemBody = message.get('Body')
        self.systemCoordinates = message.get('StarPos')
        self.systemPopulation = message.get('Population')
        self.systemSecurity = message.get('SystemSecurity')

        # only present/relevant in populated systems
        self.systemAllegiance = message.get('SystemAllegiance')
        self.systemEconomy = message.get('SystemEconomy')
        self.systemSecondEconomy = message.get('SystemSecondEconomy')
        self.systemGovernment = message.get('SystemGovernment')



        # Faction stuff, probably all needs revalidating due to data nesting
        self.controllingFaction = message.get('SystemFaction')
        self.factions = message.get('Factions')




        # Message Data
        self.messageData = message

# ----The following functions will return None if no entry is found, this is the inteded behaviour----

class Faction:
    # faction class which encapsulates all faction-pertinent data
    #TODO: this needs to be a generator
    def __init__(self, message, index):
        self.name = None
        self.controllingFlag = True if message['SystemFaction'].get('Name') == self.name else False



def getFactionActiveStates(faction):
    """Returns the state(s) of a Faction, may return None if none are found"""
    states = []
    statesRaw = faction.get('ActiveStates')
    if statesRaw == None:
        return None

    states = []
    for state in statesRaw:
        states.append(state['State'])

    return states