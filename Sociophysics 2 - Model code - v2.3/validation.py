import pygame
import math
import settings
from environment import Environment, Wall, SpawningRectangle
from spawning import Spawner
import platform_environment
from forces import Forces
from targets import Targets
from display import Display
from legend import Legend
from control_buttons import Play, Pause, Save, Control
from agent import Agent
import numpy as np

# Template for separate code files that have code that need to be run on start.
def setup():
    if __name__ == '__main__':
        print("this is unfinished")
        lane_forming()
        


# Constants
WIDTH, HEIGHT = 1400, 300
oversteps_dt = 0
Last_ID = 0
elapsed_time = 0
paused = False

def lane_forming():
    global elapsed_time
    # Pygame setup
    pygame.init()
    
    clock = pygame.time.Clock()

    display_size = platform_environment.DISPLAY_SIZE

    display = Display("Social force model", display_size)

    agent_list = []
    platform = Environment("lane forming")

    # Top wall
    platform.add(Wall(0, 0, WIDTH, 10))

    # Left wall
    platform.add(Wall(0, 0, 10, HEIGHT))

    # Right wall
    platform.add(Wall(WIDTH-10, 0, 10, HEIGHT))

    # Bottom wall
    platform.add(Wall(0, (HEIGHT - 10), WIDTH, 10))

    # Left spawner
    platform.add(SpawningRectangle(10, 10, 10, HEIGHT-20, 1))

    # Right spawner
    platform.add(SpawningRectangle(WIDTH-20, 10, 10, HEIGHT-20, 1))
    
    targets = Targets(agent_list, platform)
    
    if settings.DISPLAY_WALLS:
        display.add(platform)

    if settings.DISPLAY_CONTROL:
        control = Control()
        display.add(Play(control, WIDTH+20, 30, 40, 40))
        display.add(Pause(control, WIDTH+20, 90, 40, 40))
        display.add(Save(control, WIDTH+20, 150, 40, 40))

    forces = create_forces(platform)
    spawner = create_spawner(platform)

    while (display.active):

        if len(agent_list) <= settings.MAX_AGENTS:
            for agent in spawner.spawn(settings.SPAWN_ATTEMPTS, settings.SPAWN_PROBABILITY):
                if agent.position[0] < WIDTH/2:
                    agent.target = agent.position + np.array([WIDTH - 30, 0])
                    agent.color = (0, 0, 0)
                elif agent.position[0] > WIDTH/2:
                    agent.target = agent.position - np.array([WIDTH - 30, 0])
                display.add(agent)
                agent_list.append(agent)

        progress(forces, agent_list) # Progress one step

        # Update the window, which will also draw it, also checks to de-active window on quit
        if math.fmod(elapsed_time, settings.UPDATE_DISPLAY) <= 0.005: # Only update the display on certain steps
            display.update()

            # remove_agents = []
            # remove_agents[:] = (person for person in agent_list if 
            #                 (person.body.position.x < 80 and person.direction == "left") 
            #                 or 
            #                 (person.body.position.x > WIDTH - 80 and person.direction == "right"))
            # agent_list[:] = (person for person in agent_list if 
            #             (person.body.position.x > 80 and person.direction == "left")
            #             or
            #             (person.body.position.x < WIDTH - 80 and person.direction == "right"))
            # for person in remove_agents:
            #     pass

            if settings.DISPLAY_CONTROL:
                control.check(display)

            # Limit the frame rate, if specified
            if settings.FRAME_RATE > 0:
                clock.tick(settings.FRAME_RATE)
            
            while (paused):
                display.update()

# Progress space simulation with STEP_SIZE
def progress(forces:Forces, agent_list:list):
    global oversteps_dt, elapsed_time
    forces.step(agent_list, settings.STEP_SIZE)
    oversteps_dt += Agent.update_oversteps(agent_list)
    elapsed_time += settings.STEP_SIZE
    elapsed_time = round(elapsed_time, 4)
    #print(oversteps_dt)

def create_platform(display:Display) -> Environment:
    # Create a file for the environment objects.
    platform = Environment("platform")
    display.add(platform)

    # Load the environment objects
    platform.load_objects()
    return platform

def create_spawner(environment:Environment) -> Spawner:
    spawning_areas = environment.get_spawning_areas()
    return Spawner(spawning_areas)

def create_forces(environment:Environment) -> Forces:
    environment_walls = environment.get_walls()
    return Forces(environment_walls)


setup()