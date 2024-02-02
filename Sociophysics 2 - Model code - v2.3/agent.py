import pygame
import numpy as np
import math
import colors
import settings
from display import Drawable, Display, Circle
from platform_environment import InDangerZone
from interfaces import Vector, Clickable

def setup():
    if __name__ == '__main__':
        ### Code to test this file. ###
        # Pygame setup
        pygame.init()

        clock = pygame.time.Clock()

        # Create a display to showcase the current agent class functionality
        display = Display("Testing agent.py")

        # Add an agent that will move from the specified position with the specified velocity
        agent = Agent(1, (30, 20), (12, 8))
        display.add(agent)
        
        # Update the agent and display
        while (display.active):
            agent.step(np.array([0, 0]), 0.1)
            display.update()
            clock.tick(20)

class Agent(Drawable, Clickable):
    memory_updates = 0

    def __init__(self, ID:int, position:list[float, float], dangerzone_awareness:bool=True, velocity:list=[settings.START_VELOCITY_X, settings.START_VELOCITY_Y], mass:float=1, 
                 color:tuple=colors.AGENT_BASE_COLOR, target:list[float, float] = None):
        self.ID = ID
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = settings.AGENT_MASS
        if target:
            self.target = np.array(target)
            has_target = True
        else:
            self.target = np.array(position) + np.array([50, 0])
            has_target = True
        self.has_target = has_target
        self.color = color
        self.memory = np.zeros(settings.MAX_AGENTS + 5)
        self.in_danger_zone = False
        self.selected = False
        self.waiting = False
        self.dangerzone_awareness = dangerzone_awareness
        self.aware_move_path = True
        self.last_target_time = 10 #For updating the target due to low velocity, this is a buffer so it does not happen at the start

    def step(self, force:np.ndarray, dt:float):
        self.update_velocity(force, dt)
        self.position += self.velocity * dt
        self.last_target_time -= settings.STEP_SIZE

    def update_velocity(self, force:np.ndarray, dt:float):
        self.velocity += force/self.mass * dt

    def reached_target(self) -> bool:
        return Circle(self.target[0], self.target[1], 
                      settings.TARGET_REACHED_RADIUS).containsPoint(Vector.extract(self.position))

    # Gets the distance vector for a specified position.
    def get_distance_vector(self, position):
        # Create the vector from the distance of the point to the agent
        distance = position - self.position
        return distance

    def add_to_memory(self, agent:'Agent'):
        self.memory[agent.ID] = settings.AGENT_FORGET_TIME

    def update_memory(agent_list:list['Agent']):
        Agent.memory_updates += 1
        #print(f"Number of memory updates: {Agent.memory_updates}")
        for person in agent_list:
            for agent in agent_list:
                    if person.memory[agent.ID] > 0:
                        person.memory[agent.ID] -= settings.STEP_SIZE
                    elif person.memory[agent.ID] < 0:
                        person.memory[agent.ID] = 0

    def update_oversteps(agent_list:list['Agent']):
        new_oversteps = 0
        for agent in agent_list:
            if InDangerZone((agent.position[0], agent.position[1])):
                new_oversteps += settings.STEP_SIZE
                agent.in_danger_zone = True
            else:
                agent.in_danger_zone = False
        return new_oversteps
    
    def update_color(self):
        self.color = colors.get_agent_color(self.selected, self.in_danger_zone, self.is_known_by_selected(), self.waiting)

    def draw(self, surface : pygame.Surface):
        self.update_color()
        pygame.draw.circle(surface, self.color, self.position, settings.AGENT_RADIUS)
        if (self.selected and settings.DISPLAY_TARGET):
            pygame.draw.circle(surface, colors.AGENT_TARGET_COLOR, self.target, settings.TARGET_RADIUS)

    def get_known_crowd(self, agent_list:list['Agent']) -> list['Agent']:
        known_crowd = list['Agent']()
        for agent in agent_list:
            if self.knows_agent(agent):
                known_crowd.append(agent)
        return known_crowd
    
    def knows_agent(self, agent:'Agent') -> bool:
        return self.memory[agent.ID] > 0

    def is_known_by_selected(self) -> bool:
        return selectedAgent.knows_agent(self)
        
    def click(self, position:tuple[float, float]):
        if Circle(self.position[0], self.position[1], settings.AGENT_RADIUS + 5).containsPoint(position):
            select_agent(self)

# Set the selected agent to a not used agent by default.
selectedAgent = Agent(-1, np.array([0, 0]), True)
def select_agent(agent:Agent):
    global selectedAgent
    selectedAgent.selected = False
    selectedAgent = agent
    selectedAgent.selected = True

setup()