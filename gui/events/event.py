class Event:
    def __init__(self, name: str):
        self.name = name


class EventDispatcher:
    listeners: dict[type[Event], list] = {}

    def call_event(ev: Event):
        if ev.__class__ in EventDispatcher.listeners:
            for listener in EventDispatcher.listeners[ev.__class__]:
                listener(ev)

    def add_listener(event: Event, func):
        if event in EventDispatcher.listeners:
            EventDispatcher.listeners[event].append(func)
        else:
            EventDispatcher.listeners[event] = [func]



def event_listener(func):
    """
    This is a function decorator which indicates that the associated function must be a listener for a specific event.

    Parameters
    ----------
    func: function
        The function that will listen to the event. The function must have a single parameter which must be annotated
        in order to identify the event which will trigger this function.
    
    Note
    ----
    The function must not be an object method and must contain 1 argument only.
    """
    ann = func.__annotations__
    EventDispatcher.add_listener(ann[list(ann.keys())[0]], func)
    def inner(*args, **kwargs):
        return func(args, kwargs)