from gui.events.event import *

class MouseEvent(Event):
    def __init__(self, mouseX: int, mouseY: int, mouseButton: int) -> None:
        super().__init__()
        self.mouseX = mouseX
        self.mouseY = mouseY

class ClickEvent(MouseEvent):
    def __init__(self, mouseX: int, mouseY: int, mouseButton: int) -> None:
        super().__init__(mouseX, mouseY, mouseButton)
        self.button = mouseButton

class ReleaseEvent(MouseEvent):
    def __init__(self, mouseX: int, mouseY: int, mouseButton: int) -> None:
        super().__init__(mouseX, mouseY, mouseButton)

class DragEvent(MouseEvent):
    def __init__(self, piece: int, mouseX: int, mouseY: int, mouseButton: int) -> None:
        super().__init__(mouseX, mouseY, mouseButton)
        self.piece = piece