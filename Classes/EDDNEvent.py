
def createEventFromJson(jsonData):
    """Gets the 'message' data structure from jsonData received by EDDN"""
    try:
        message = jsonData['message']
        return Event(message)
    except Exception as e:
        print("getMessageData() jsonData that does not contain the 'message' datastructure found:")
        print(e)
    return None

class Event:
    def __init__(self, message):
        self.timestamp = message.get('timestamp')
        self.eventType = message.get('event')
        if self.eventType == None:
            raise ValueError("Class 'Event': attempted to instantiate an Event Object using a message containing no Event. Check if the message has an event first.")