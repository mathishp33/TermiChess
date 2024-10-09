class Event:
    listeners: list[function] = []

    def call():
        for listener in Event.listeners:
            listener()
    
    def addListener(func: function):
        Event.listeners.append(func)

