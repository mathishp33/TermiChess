from gui.events.event import *

class KeyboardEvent(Event):
    def __init__(self, name: str, key: int) -> None:
        super().__init__(name)
        self.key = key
        

class KeyPressEvent(KeyboardEvent):
    def __init__(self, key: int) -> None:
        super().__init__("KeyPressEvent", key)

class KeyReleaseEvent(KeyboardEvent):
    def __init__(self, key: int) -> None:
        super().__init__("KeyReleaseEvent", key)