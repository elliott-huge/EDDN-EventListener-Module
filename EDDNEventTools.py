
def getMessageData(jsonData):
    """Gets the 'message' data structure from jsonData received by EDDN"""
    try:
        message = jsonData['message']
    except Exception as e:
        print("getMessageData() jsonData that does not contain the 'message' datastructure found:")
        print(e)
    return message

def getIfEventType(message):
    """Returns the message's 'event' type from the inputted json, will return None if none is found"""
    event = message.get('event')

    return event

def ifEventTypeCheck(message, eventType):
    """Checks if the json's event is of a specified eventType (string value eg: "FSDJump")."""
    receivedEventType = getIfEventType(message)
    # Guard agains messages without an 
    if receivedEventType == None:
        return False

    if receivedEventType == eventType:
        return True
    return False

def getTimeStamp(message):
    timeStamp = message.get('timestamp')
    if timeStamp == None:
        raise ValueError("getTimeStamp(): Message did not contain a timestamp, timstamp could not be obtained")
    return timeStamp

class Event:
    def __init__(self, message):
        self.timestamp = getTimeStamp(message)
        self.eventType = getIfEventType(message)
        if self.eventType == None:
            raise ValueError("Class 'Event': attempted to instantiate an Event Object using a message containing no Event. Check if the message has an event first.")