class Event:
    listeners: list = []

    def call(self):
        for listener in Event.listeners:
            listener()
    
    def addListener(func):
        Event.listeners.append(func)

