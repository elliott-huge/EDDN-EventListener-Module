from Classes.FSDJumpEvent import FSDJumpEvent
from HelperFunctions.miscTools import *

#TODO: delet
class factionStatusNotification:
    
    def __init__(self, notificationName, activeStateList = None, strictMatch: bool = True, minPopulation: int = 1, maxDistToSol = 250, systemList = None):
        """Generates a faction Status notification for a program to listen for. Parameters are self-descriptive. !WILL ONLY CHECK IF A SINGLE FACTION HAS ALL THE LISTED STATES ACTIVE!"""
        # parameter setup
        self.notificationName = notificationName
        self.activeStateList = activeStateList
        self.strictMatch = strictMatch
        self.minPopulation = minPopulation
        self.maxDistToSol = maxDistToSol
        self.systemList = systemList

    def assessFSDJumpEvent(self, event: FSDJumpEvent):
        """Checks and returns if the inputted event if it meets the notification's criteria."""
        
        #guard POPULATION
        if event.systemPopulation < self.minPopulation:
            return None
        
        #guard DISTANCE TO SOL
        if get3dDistance(event.systemCoordinates) > self.maxDistToSol:
            return None

        #guard against jumps older than an Hr
        if event.eventAgeSeconds > 3600:
            return None
        
        #optional guard against unlisted systems
        if self.systemList != None and event.systemName not in self.systemList:
            return None
        
        #optional guard against faction states
        #TODO: make into a function call that is reusable; a method of this class
        if self.activeStateList != None:
            factionCount = 0
            for faction in event.factions:
                factionCount+=1
                if compareTwoLists(faction.listStateNames('active'), self.activeStateList, self.strictMatch):
                    return event

        return None
