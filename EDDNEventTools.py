def getMessage(jsonData):
    message = jsonData['message']
    return message

def getEventType(message):
    """Returns the message's 'event' type from the inputted json."""
    event = message.get('event')
    return event

def eventTypeCheck(message, eventType):
    """Checks if the json's event is of a specified eventType (string value eg: "FSDJump")."""
    if getEventType(message) == eventType:
        return True
    return False

def getTimeStamp(message):
    timeStamp = message.get('timestamp')
    #if timeStamp != None:
    #    return timeStamp
    
    return timeStamp

class Event:
    def __init__(self, message):
        self.timestamp = getTimeStamp(message)
        self.eventType = getEventType(message)