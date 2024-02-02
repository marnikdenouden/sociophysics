import random
import pygame
from agent import Agent
import settings
from display import Display
from environment import SpawningCircle, SpawningRectangle

Last_ID = 0

def setup():
    if __name__ == '__main__':
        # Pygame setup
        pygame.init()
            
        clock = pygame.time.Clock()

        # Create a display to showcase the current agent class functionality
        display = Display("Testing spawning.py")

        # Creating spawning areas to show, note that the first and last have a heigher spawning weight, which are colored gray
        spawning_areas = []
        spawning_areas.append(SpawningRectangle(110, 20, 150, 60, 4, (128, 128, 128)))
        spawning_areas.append(SpawningRectangle(70, 120, 30, 80, 1))
        spawning_areas.append(SpawningRectangle(230, 190, 70, 130, 1))
        spawning_areas.append(SpawningCircle(300, 120, 20, 1))
        spawning_areas.append(SpawningCircle(130, 340, 30, 4, (128, 128, 128)))
        # Note that the weight is per shape, for uniform distribution over area set the weight to be the area of the shape.

        for spawning_area in spawning_areas:
            display.add(spawning_area)
        
        # A spawner can be created for a list of spawning area objects
        spawner = Spawner(spawning_areas)

        agent_list = []

        while(display.active):
            # spawner.spawn or spawner.spawn_agent return the spawned agent, which can then be added to the display
            for agent in spawner.spawn(30, 0.01):
                display.add(agent)
                agent_list.append(agent)
                
            # Display with a limited frame rate to not rush through the spawning
            display.update()
            clock.tick(20)

class Spawner:
    def __init__(self, spawning_areas:list):
        self.spawning_areas = spawning_areas
        self.weights = []
        for spawning_area in spawning_areas:
            self.weights.append(spawning_area.weight)

    # Spawn a single agent in a weighted selected spawning area
    def spawn_agent(self, Agent_ID) -> Agent:
        spawning_area = random.choices(self.spawning_areas, self.weights)[0]
        return Agent(Agent_ID, spawning_area.get_spawn_position(), dangerzone_awareness=random.random() < settings.dangerzone_awareness)
    
    # Spawn binominal number of agents in the spawning areas for the specified attempts and probability
    def spawn(self, attempts:int, probability:int) -> list[Agent]:
        global Last_ID
        new_agents = []
        for i in range(random.binomialvariate(attempts, probability)):
            Last_ID += 1
            new_agents.append(self.spawn_agent(Last_ID))
            if settings.AGENT_NUMBER_DATA:
                print(f"{Last_ID + i}")
        return new_agents

setup()