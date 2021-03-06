from Classes.FSDJumpEvent import FSDJumpEvent
from HelperFunctions.utils import get3dDistance, compareLists
from datetime import datetime

#TODO: delet
class factionStatusNotification:
    
    def __init__(self, notificationName, activeStateList = None, strictMatch: bool = True, minPopulation: int = 1, maxDistToSol = 250, minInfluence: float = 0.01, systemList = None):
        """Generates a faction Status notification for a program to listen for. Parameters are self-descriptive. !WILL ONLY CHECK IF A SINGLE FACTION HAS ALL THE LISTED STATES ACTIVE!"""
        # parameter setup
        self.notificationName = notificationName
        self.activeStateList = activeStateList
        self.strictMatch = strictMatch
        self.minPopulation = minPopulation
        self.maxDistToSol = maxDistToSol
        self.minInfluence = minInfluence
        self.systemList = systemList

        # output file setup
        #TODO: set up file tracking per faction status notification
        #TODO: look into async
        now = datetime.now()
        timeNowString = now.strftime("%H_%M_%S")
        self.fileName = f"{notificationName}_{timeNowString}.txt"
        f = open(self.fileName, "w+")
        f.write(f"{self.notificationName}\n  States: {self.activeStateList}\n  State Match Strictness: {self.strictMatch}\n  Min Pop': {self.minPopulation}\n  Max Dist' from Sol: {self.maxDistToSol}LY\n  Min Influence%: {self.minInfluence}:\n")
        f.close()


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

            for faction in event.factions:
                if not compareLists(faction.listStateNames('active'), self.activeStateList, self.strictMatch):
                    continue
                if faction.influenceDecimal > self.minInfluence or faction.controllingFlag:
                    return event
        
        return None
