import pygame
import time
import math
import colors
from interfaces import Drawable, Clickable, JsonObject

def setup():
    if __name__ == '__main__':
        ### Code to test this file. ###
        
        # Pygame setup
        pygame.init()

        # Test creating a display with screen title
        display = Display("Testing display.py")
        display.update()
        time.sleep(1)

        # Test adding a basic rectangle to the display
        display.add(Rectangle(30, 40, 60, 20, (255, 0, 0)))               
        display.update()
        time.sleep(1)
        
        # Test adding text to the display
        display.add(Text("Click the 2nd circle", 140, 60))               
        display.update()
        time.sleep(1)
        
        # Test adding a basic circle to the display
        display.add(Circle(80, 110, 10, (0, 255, 0)))
        display.update()
        time.sleep(1)
        
        # Test adding a clickable circle to the display
        display.add(RainbowButton(90, 170, 16))

        # Keeps the window running, until update returns False
        while (display.active):
            display.update()

class Display:
    background_color = colors.BACKGROUND_COLOR

    def __init__(self, title : str, size : tuple = (400, 400)):
        icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption(f"{title} - Group 2 [Sociophysics 2023]")

        self.surface = pygame.display.set_mode(size)
        self.drawables = []
        self.clickables = []
        self.active = True

    def update(self):     
        self.__draw__()
        self.check()
        
    def check(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    self.active = False
                case pygame.MOUSEBUTTONDOWN:
                    if (event.button == 1): # Only activate for left click (1) and not for scroll wheel (2) or right click (3)
                        self.__click__(event.pos)

    def __draw__(self):
        self.surface.fill(Display.background_color)
        for i in range(len(self.drawables)):
            self.drawables[i].draw(self.surface)
        pygame.display.update()

    def __click__(self, position:tuple[float, float]):
        for i in range(len(self.clickables)):
            self.clickables[i].click(position)

    def add(self, drawable: Drawable):
        self.drawables.append(drawable)
        if (isinstance(drawable, Clickable)):
            self.clickables.append(drawable)

    def draw_pixel(self, position:tuple[float, float], color:tuple):
        self.surface.set_at(position, color)

class Rectangle(Drawable, JsonObject):

    def __init__(self, x:int, y:int, width:int, height:int, color=colors.SHAPE_BASE_COLOR, border_radius:int=0):
        # Rectangle variables used for display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.border_radius = border_radius

    def draw(self, surface : pygame.Surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height), border_radius=self.border_radius)  

    def containsPoint(self, position:tuple[float, float]) -> bool:
        '''Checks if the position is contained in or on the edge of the rectangle.'''
        horizontal = self.x <= position[0] <= self.x + self.width 
        vertical = self.y <= position[1] <= self.y + self.height
        return horizontal and vertical
    
    def save_dictionary(self) -> dict:
        rectangle = {
            "x" :self.x,
            "y" :self.y,
            "width" :self.width,
            "height" :self.height,
        }
        return rectangle
    
    def load_object(dictornary:dict):
        x = dictornary.get("x")
        y = dictornary.get("y")
        width = dictornary.get("width")
        height = dictornary.get("height")
        return Rectangle(x, y, width, height)

class Circle(Drawable, JsonObject):

    def __init__(self, x:int, y:int, radius=5, color=colors.SHAPE_BASE_COLOR):
        # Circle variables used for display
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface : pygame.Surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def containsPoint(self, position:tuple[float, float]) -> bool:
        '''Checks if the position is contained in or on the edge of the circle.'''
        return math.dist((self.x, self.y), position) <= self.radius
    
    def save_dictionary(self) -> dict:
        circle = {
            "x" :self.x,
            "y" :self.y,
            "radius" :self.radius,
        }
        return circle
    
    def load_object(dictornary:dict):
        x = dictornary.get("x")
        y = dictornary.get("y")
        radius = dictornary.get("radius")
        return Circle(x, y, radius)

class Text(Drawable):
    font_initialized = False
    
    def __init__(self, text:str, x:int, y:int, textSize:int=32, center_position:bool=False, 
                 color:tuple=colors.TEXT_COLOR, background_color:tuple=colors.BACKGROUND_COLOR):
        # Text variables used for display
        self.text = text
        self.x = x
        self.y = y
        font = Text.__load_font__(textSize)
        self.color = color
        self.background_color = background_color
    
        # Create the text rectangle that can be displayed
        self.textSurface = font.render(text, True, color, background_color)
        self.textRect = self.textSurface.get_rect()
        self.width = self.textSurface.get_width()
        self.height = self.textSurface.get_height()

        if center_position:
            self.x -= self.width / 2
            self.y -= self.height / 2

    def __load_font__(textSize:int) -> pygame.font.Font:
        if (not Text.font_initialized):
            # Initialize the font to use for text display
            pygame.font.init()
        return pygame.font.Font('OpenSans_condensed-Regular.ttf', textSize)

    def draw(self, surface : pygame.Surface):
        surface.blit(self.textSurface, (self.x, self.y), self.textRect)

class Section(Drawable):
    def __init__(self, surface:pygame.Surface, x:int, y:int):
        # Image variables used for display
        self.surface = surface
        self.x = x
        self.y = y
        self.width = surface.get_width()
        self.height = surface.get_height()

    def draw(self, surface : pygame.Surface):
        surface.blit(self.surface, (self.x, self.y))

class Image(Section):
    def __init__(self, image_file:str, x: int, y: int):
        super().__init__(pygame.image.load(image_file), x, y)

class RainbowButton(Drawable, Clickable):
    def __init__(self, x:int, y:int, radius:int):
        # Raindbow button variables used for display
        self.circle = Circle(x, y, radius)

    def draw(self, surface : pygame.Surface):
        self.circle.draw(surface)

    def click(self, position:tuple[float, float]):
        if self.circle.containsPoint(position):
            self.circle.color = colors.get_random_color()

setup()