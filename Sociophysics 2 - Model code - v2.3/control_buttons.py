import pygame
import colors
from collections.abc import Callable
from interfaces import Drawable, Clickable
from display import Rectangle, Image, Display

class Button(Clickable, Drawable):
    PADDING = 8

    def __init__(self, icon_file:str, x:int, y:int, width:int, height:int):
        self.edge = Rectangle(x, y, width, height, colors.BUTTON_EDGE_COLOR, 8)
        width = width - Button.PADDING
        height = height - Button.PADDING
        x += (int)(Button.PADDING / 2)
        y += (int)(Button.PADDING / 2)
        self.rectangle = Rectangle(x, y, width, height, colors.BUTTON_ACTIVE_COLOR, 4)
        self.image = Image(icon_file, x, y)

        # Center image based on self.image.width and self.image.height
        if self.image.width < width:
            self.image.x = x + (int)(width - self.image.width) / 2

        if self.image.height < height:
            self.image.y = y + (int)(height - self.image.height) / 2

    def click(self, position:tuple):
        if self.rectangle.containsPoint(position):
            self.click_action()

    def click_action(self):
        pass

    def get_color(self) -> tuple:
        pass

    def draw(self, surface : pygame.Surface):
        self.rectangle.color = self.get_color()
        self.edge.draw(surface)
        self.rectangle.draw(surface)
        self.image.draw(surface)

class Control():
    def __init__(self):
        self.paused = False
        self.save = False
        self.saved = False

    def check(self, display:Display, get_surface:Callable[[], pygame.Surface]=None):
        if get_surface == None:
            get_surface = lambda:display.surface
        while(self.paused and display.active):
            display.update()
            if self.save and not self.saved:
                print("Saving screenshot")
                pygame.image.save(get_surface(), "images/screenshot.png")   
                self.save = False
                self.saved = True
        self.saved = False

    def Play(self):
        self.paused = False

    def Pause(self):
        self.paused = True

    def Save(self):
        self.save = True

class Play(Button):
    def __init__(self, control:Control, x:int, y:int, width:int, height:int):
        super(Play, self).__init__('images/play_icon.png', x, y, width, height)
        self.control = control

    def click_action(self):
        self.control.Play()
        
    def get_color(self) -> tuple:
        return colors.get_button_color(self.control.paused)

class Pause(Button):
    def __init__(self, control:Control, x:int, y:int, width:int, height:int):
        super(Pause, self).__init__('images/pause_icon.png', x, y, width, height)
        self.control = control

    def click_action(self):
        self.control.Pause()
        
    def get_color(self) -> tuple:
        return colors.get_button_color(not self.control.paused)

class Save(Button):
    def __init__(self, control:Control, x:int, y:int, width:int, height:int):
        super(Save, self).__init__('images/download_icon.png', x, y, width, height)
        self.control = control

    def click_action(self):
        self.control.Save()
        
    def get_color(self) -> tuple:
        return colors.get_button_color(self.control.paused and not self.control.saved)