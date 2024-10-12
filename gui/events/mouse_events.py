from gui.events.event import *

class MouseEvent(Event):
    def __init__(self, name: str, mouseX: int, mouseY: int, mouseButton: int) -> None:
        super().__init__(name)
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.mouseButton = mouseButton
        

class MouseClickEvent(MouseEvent):
    def __init__(self, mouseX: int, mouseY: int, mouseButton: int) -> None:
        super().__init__("MouseClickEvent", mouseX, mouseY, mouseButton)

class MouseReleaseEvent(MouseEvent):
    def __init__(self, mouseX: int, mouseY: int, mouseButton: int) -> None:
        super().__init__("MouseReleaseEvent", mouseX, mouseY, mouseButton)

class MouseDragEvent(MouseEvent):
    def __init__(self, piece: int, mouseX: int, mouseY: int, mouseButton: int) -> None:
        super().__init__("MouseDragEvent", mouseX, mouseY, mouseButton)
        self.piece = piece