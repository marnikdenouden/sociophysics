import pygame
import settings
from colors import *
from interfaces import Drawable
from display import Display, Text

# Constant RGB color values to easily change the palete and find colors.
def setup():
    if __name__ == '__main__':
        display = Display("Testing colors.py", (300, 400))
        legend = Legend()
        display.add(legend)

        while (display.active):
            display.update()

class Legend_Color:
    
    def __init__(self, label:str, color:tuple):
        self.label = label
        self.color = color

class Legend(Drawable):
    WIDTH = 100
    PADDING = 8
    TEXT_SIZE = 8

    def __init__(self, scale:float=2):
        self.scale = scale
        self.legend_colors = [Legend_Color("Base color", AGENT_BASE_COLOR), 
                       Legend_Color("Selected agent", AGENT_SELECTED_COLOR), 
                       Legend_Color("In danger area", AGENT_IN_DANGER_COLOR), 
                       Legend_Color("Known by selected", AGENT_KNOWN_COLOR), 
                       Legend_Color("Selected and in danger", AGENT_SELECTED_IN_DANGER_COLOR), 
                       Legend_Color("Known and in danger", AGENT_KNOWN_IN_DANGER_COLOR), 
                       Legend_Color("Target of selected", AGENT_TARGET_COLOR), 
                       Legend_Color("Waiting", AGENT_WAITING_COLOR)]
        
        self.padding = (int)(Legend.PADDING * self.scale)
        self.radius = (int)(settings.AGENT_RADIUS * self.scale)
        self.offset = self.padding + self.radius * 2

        self.x = 0
        self.y = 0

        self.width = (int)(Legend.WIDTH * self.scale)
        self.height = len(self.legend_colors) * (self.radius * 2 + self.padding) + self.padding

    def draw(self, surface:pygame.Surface):
        """Draws the legend to the specified surface."""
        pygame.draw.rect(surface, LEGEND_EDGE, pygame.Rect(self.x, self.y, 
            self.width, self.height), border_radius=(int)(self.radius * 1.4))
        pygame.draw.rect(surface, LEGEND_BACKGROUND, pygame.Rect(self.x + self.padding / 2, self.y + self.padding / 2, 
            self.width - self.padding, self.height - self.padding), border_radius=self.radius)
        
        for i in range(len(self.legend_colors)):
            # Keep in mind that the position starts in the top right.
            legend_color_x = self.x + self.padding + self.radius
            legend_text_x = legend_color_x + self.padding + self.radius
            legend_text_y = self.y + self.offset * i + self.padding
            legend_color_y = legend_text_y + self.radius

            pygame.draw.circle(surface, self.legend_colors[i].color, 
                               (legend_color_x, legend_color_y), self.radius)
            Text(self.legend_colors[i].label, legend_text_x, legend_text_y,
                 (int)(Legend.TEXT_SIZE * self.scale), False, LEGEND_TEXT, LEGEND_BACKGROUND).draw(surface)

setup()