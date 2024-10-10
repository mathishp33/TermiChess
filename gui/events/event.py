class Event:
    listeners: list = []

    def call(self):
        for listener in Event.listeners:
            if type(listener) == list:
                listener[0](listener[1])
            else:
                listener()
    
    def addListener(func, mself = None):
        Event.listeners.append(func) if mself == None else Event.listeners.append([func, mself])

