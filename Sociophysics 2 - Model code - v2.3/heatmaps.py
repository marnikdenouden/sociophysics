import pygame
import math
import numpy as np
import settings
import random
import colors
from collections.abc import Callable
from agent import Agent
from display import Display, Section, Circle, Text
from interfaces import Vector
from forces import Forces
from environment import Wall
from matplotlib import colormaps
from control_buttons import Control, Button, Save

def setup():
    if __name__ == '__main__':
        # Pygame setup
        pygame.init()

        # Display the heatmaps that show the current force functions in display rotation,
        # With a specified amount of color steps that represent the range of force magnitudes.
        display_heatmaps(settings.HEATMAP_STEPS)

class NextButton(Button):
    '''Loops through the specified list by moving to the next item at each button click.'''
    def __init__(self, list:list, update:Callable, x: int, y: int, width: int, height: int):
        super().__init__('images/next_icon.png', x, y, width, height)
        self.list = list
        assert len(list) > 0
        self.index = 0
        self.update = update

    def click_action(self):
        self.index = (self.index + 1) % len(self.list)
        self.update()

    def get_color(self) -> tuple:
        return colors.BUTTON_BASE_COLOR

    def get_item(self):
        return self.list[self.index]

#region Heat map code to display in testing of forces.py
def display_heatmaps(colorsteps:int):
    """Display the various heatmaps that showcase the forces with a specified amount of color steps to show values with."""
    # Color mapping for the heatmaps
    colormap = colormaps["inferno"].resampled(colorsteps)

    # Define constants for force display
    SIZE = 100
    SIZING = (SIZE, SIZE)
    SCALED_SIZE = 5 * SIZE
    SCALED_SIZING = (SCALED_SIZE, SCALED_SIZE)
    LOOP_TIME = 5000 # Time in millis

    display = Display("Testing forces.py", (SCALED_SIZE, SCALED_SIZE + 40))

    display.surface.fill(colors.BACKGROUND_COLOR)
    Text("Generating heatmaps, please wait : )", 50, 0, 24).draw(display.surface)
    pygame.display.update()

    # Create the heatmap surfaces to display
    sight_agent_surface = pygame.transform.scale(get_sight_agent_surface(SIZING, colormap), SCALED_SIZING)
    sight_point_surface = pygame.transform.scale(get_sight_point_surface(SIZING, colormap), SCALED_SIZING)
    repulsion_surface = pygame.transform.scale(get_repulsion_surface(SIZING, colormap), SCALED_SIZING)
    avoidance_surface = pygame.transform.scale(get_avoidance_surface(SIZING, colormap), SCALED_SIZING)
    repulsion_and_avoidance_suface = pygame.transform.scale(get_repulsion_and_avoidance_surface(SIZING, colormap), SCALED_SIZING)
    avoidance_surface_multiple_agents = pygame.transform.scale(get_avoidance_surface_multiple_agents(SIZING, colormap), SCALED_SIZING)
    surfaces = [sight_agent_surface, sight_point_surface, repulsion_surface, avoidance_surface, repulsion_and_avoidance_suface, avoidance_surface_multiple_agents]

    def update_surface():
        display.add(Section(next_button.get_item(), 0, 40))
        control.saved = False
    next_button = NextButton(surfaces, update_surface, 0, 0, 40, 40)
    display.add(next_button)
    
    control = Control()
    control.Pause()
    display.add(Save(control, SCALED_SIZE - 40, 0, 40, 40))
    display.add(Text("Click for next heatmap", 50, 0, 24))
    display.add(Text("Click to save", SCALED_SIZE - 50 - Text("Click to save", 0, 0, 24).width, 0, 24))

    update_surface()
    while (display.active):
        display.update()
        control.check(display, lambda:next_button.get_item())
                
def get_sight_agent_surface(sizing:tuple, colormap:colormaps) -> pygame.Surface:
    """Get the surface of the heatmap that showcases the sight value for an agent near a wall."""
    width = sizing[0]
    height = sizing[1]
    wall = Wall(round(0.3 * width), round(0.3 * height), round(0.4 * width), round(0.4 * height))
    forces = Forces([],[])

    # Create a random agent with:
    # x position between 0 and 0.3 times the sizing width
    # y position between 0.5 and 1 times the sizing height
    agent_x = 0.3 * width
    agent_y = 0.5 * height
    agent = Agent(0, [agent_x, agent_y])
    
    # Using a smaller surface for computating each pixel to later scale for visability
    surface = pygame.Surface(sizing)

    def get_sight_value(position:tuple) -> float:
        return forces.get_sight_value(agent, Vector.create(position))

    # Compute the matrix with the sight value for each position for the agent
    repulsion_matrix = compute_matrix(get_sight_value, sizing)
    draw_matrix(surface, repulsion_matrix, colormap)

    # Draw the surface
    #wall.draw(surface)
    agent.draw(surface)

    return surface

def get_sight_point_surface(sizing:tuple, colormap:colormaps) -> pygame.Surface:
    """Get the surface of the heatmap that showcases the sight value from a point to a wall."""
    width = sizing[0]
    height = sizing[1]
    wall = Wall(round(0.3 * width), round(0.3 * height), round(0.4 * width), round(0.4 * height))

    # Create a random point with:
    # x position between 0 and 0.3 times the sizing width
    # y position between 0.5 and 1 times the sizing height
    point_x = (random.random() * 0.3) * width
    point_y = (random.random() * 0.5 + 0.5) * height
    point = Vector.create((point_x, point_y))
    
    # Using a smaller surface for computating each pixel to later scale for visability
    surface = pygame.Surface(sizing)

    def get_sight_value(position:tuple) -> float:
        if wall.containsPoint(position):
            return 0.5 # Colored red in inferno colormap
        elif wall.blocks_line(point, position):
            return 0 # Colored black in inferno colormap
        else:
            return 1 # Colored yellow in infernor colormap

    # Compute the matrix with the wall and point the sight value for each position
    repulsion_matrix = compute_matrix(get_sight_value, sizing)
    draw_matrix(surface, repulsion_matrix, colormap)

    # Draw the surface
    #wall.draw(surface)
    Circle(point[0], point[1], 3).draw(surface)
    return surface
                
def get_repulsion_surface(sizing:tuple, colormap:colormaps) -> pygame.Surface:
    """Get the surface of the heatmap that showcases the repulsion force of a wall."""
    width = sizing[0]
    height = sizing[1]
    wall = Wall(round(0.3 * width), round(0.3 * height), round(0.4 * width), round(0.4 * height))
    forces = Forces([wall],[])
    # Using a smaller surface for computating each pixel to later scale for visability
    surface = pygame.Surface(sizing)

    def get_force_magnitude(position:tuple) -> float:
        return Vector.length(forces.get_repulsion_walls(position))

    # Compute the matrix with repulsion force magnitude for each position
    repulsion_matrix = compute_matrix(get_force_magnitude, sizing)
    draw_matrix(surface, repulsion_matrix, colormap)

    # Draw the map on top to show the object that acts the repulsion force
    wall.draw(surface)
    return surface

def get_avoidance_surface(sizing:tuple, colormap:colormaps) -> pygame.Surface:
    """Get the surface of the heatmap that showcases the avoidance force of another agent."""
    agent = Agent(0, (0.5 * sizing[0], 0.5 * sizing[1]))
    # Using a smaller surface for computating each pixel to later scale for visability
    surface = pygame.Surface(sizing)

    def get_force_magnitude(position:tuple) -> float:
        return Vector.length(Forces.get_repulsion_agent(agent, position))

    # Compute the matrix with repulsion force magnitude for each position
    avoidance_matrix = compute_matrix(get_force_magnitude, sizing)
    draw_matrix(surface, avoidance_matrix, colormap)

    # Draw the map on top to show the object that acts the repulsion force
    agent.draw(surface)
    return surface

def get_repulsion_and_avoidance_surface(sizing:tuple, colormap:colormaps):
    """Get the surface heatmap that showcases the repulsion of a wall combined with the avoidance of agents"""
    width = sizing[0]
    height = sizing[1]
    wall = Wall(round(0.3 * width), round(0.3 * height), round(0.4 * width), round(0.4 * height))

    agent = Agent(0, (0.1 * sizing[0], 0.5 * sizing[1]))

    forces = Forces([wall],[])
    # Using a smaller surface for computating each pixel to later scale for visability
    surface = pygame.Surface(sizing)

    def get_force_magnitude(position:tuple) -> float:
        return Vector.length(Forces.get_repulsion_agent(agent, position) + forces.get_repulsion_walls(position))
    
    # Compute the matrix with repulsion force magnitude for each position
    repulsion_and_avoidance_matrix = compute_matrix(get_force_magnitude, sizing)
    draw_matrix(surface, repulsion_and_avoidance_matrix, colormap)

    # Draw the map on top to show the object that acts the repulsion force
    agent.draw(surface)
    wall.draw(surface)
    return surface

def get_avoidance_surface_multiple_agents(sizing:tuple, colormap:colormaps) -> pygame.Surface:
    """Get the surface of the heatmap that showcases the avoidance force of another agent."""
    global agent_list 
    agent_list = [Agent(0, (0.3 * sizing[0], 0.5 * sizing[1]))]
    for _ in range(2):
        agent = Agent(0, (random.random() * sizing[0], random.random() * sizing[1]))
        agent_list.append(agent)

    # Using a smaller surface for computating each pixel to later scale for visability
    surface = pygame.Surface(sizing)

    def get_force_magnitude(position:tuple) -> float:
        force = np.array([0.0, 0.0])
        for agent in agent_list:
            force += Forces.get_repulsion_agent(agent, position)
        return Vector.length(force)

    # Compute the matrix with repulsion force magnitude for each position
    avoidance_matrix = compute_matrix(get_force_magnitude, sizing)
    draw_matrix(surface, avoidance_matrix, colormap)

    # Draw the map on top to show the object that acts the repulsion force
    for agent in agent_list:
        agent.draw(surface)
    return surface

def display_scaled_surface(surface:pygame.Surface, title:str, SCALED_SIZING) -> Display:
    """Display the specified surface on a new display with the specified title and scaled sizing."""
    # Create the display for the surface
    display = Display(title, SCALED_SIZING)

    # Scale the surface so each pixel is clearly visable
    pygame.transform.scale(surface, SCALED_SIZING, display.surface)
    pygame.display.update()
    return display

def compute_matrix(get_value, sizing:tuple) -> np.ndarray:
    """Compute the matrix of given 2 dimensional sizing with the specified get value function."""
    # Initialize an array for the values
    array = []
    for x in range(sizing[0]):
        array.append([])
        for y in range(sizing[1]):
            # For each position get the value and insert it
            position = (x, y)
            value = get_value(position)
            array[x].append(value)

    # Convert the array to np array
    return np.array(array)

def draw_matrix(surface:pygame.Surface, matrix_2d:np.ndarray, colormap:colormaps):
    """Draw a 2 dimensional matrix of np array type on the specified surface. \n
    Each matrix value will have a pixel value from the colormap,
      as mapped from the minimum to the maximum matrix value."""
    assert len(matrix_2d.shape) == 2

    # Convert the array to np array for min and max value computation
    min_val = np.min(matrix_2d)
    max_val = np.max(matrix_2d)

    if min_val == max_val:
        surface.fill(colormap(0.5))
        return

    # Transform values to range from 0 to 1, so they are suitable for color mapping
    heatmap_matrix = (matrix_2d - min_val) / (max_val - min_val)

    # For each point we convert the adjusted maginitude value to a heatmap pixel color on the surface
    for x in range(matrix_2d.shape[0]):
        for y in range(matrix_2d.shape[1]):
            position = (x, y)
            value = heatmap_matrix[x][y]
            color_values = colormap(value)
            color = (255 * color_values[0], 255 * color_values[1], 255 * color_values[2])
            surface.set_at(position, color)
#endregion
            
setup()