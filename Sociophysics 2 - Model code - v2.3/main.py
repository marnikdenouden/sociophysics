import pygame
import math
import numpy as np
import settings
import time
from interfaces import Drawable
from environment import Environment, Rail_wall
from spawning import Spawner
import platform_environment
from platform_environment import InDangerZone
from forces import Forces
from targets import Targets
from display import Display, Text
from legend import Legend
from control_buttons import Play, Pause, Save, Control
from agent import Agent

# Constants
WIDTH, HEIGHT = platform_environment.WIDTH, platform_environment.HEIGHT
oversteps_dt = 0
Last_ID = 0
elapsed_time = 0

def main():
    global elapsed_time
    # Pygame setup
    pygame.init()
    
    clock = pygame.time.Clock()

    display_size = platform_environment.DISPLAY_SIZE
    
    if settings.DISPLAY_LEGEND:
        legend = Legend(2)
        display_size = (WIDTH + legend.width, HEIGHT)
        legend.x = WIDTH
        if (legend.height < HEIGHT):
            legend.y = (int)(HEIGHT - legend.height) / 2

    display = Display("Social force model", display_size)
    display.add(platform_environment.BACKGROUND)

    agent_list = list[Agent]()

    if settings.NUDGE_BONUS_BENCH == True and settings.NUDGE_MOVE_PATH == True:
        platform = platform_environment.PLATFORM_NUDGE_BOTH
    elif settings.NUDGE_BONUS_BENCH == True:
        platform = platform_environment.PLATFORM_NUDGE_BENCH
    elif settings.NUDGE_MOVE_PATH == True:
        platform = platform_environment.PLATFORM_NUDGE_WALKING_PATH
    else:
        platform = platform_environment.PLATFORM

    targets = Targets(agent_list, platform)
    
    if settings.DISPLAY_WALLS:
        display.add(platform)

    if settings.DISPLAY_LEGEND:
        display.add(legend)

    if settings.DISPLAY_CONTROL:
        control = Control()
        display.add(Play(control, 737, 132, 40, 40))
        display.add(Pause(control, 797, 132, 40, 40))
        display.add(Save(control, 857, 132, 40, 40))
        
    if settings.DISPLAY_TARGET_SELCTION:
        display.add(targets)

    if settings.DISPLAY_CLOCK:
        display.add(Clock())
    
    if settings.DISPLAY_OVERSTEPPED_SECONDS:
        display.add(Danger())

    forces = create_forces(platform)
    spawner = create_spawner(platform)

    if settings.DISPLAY_PERFORMANCE_TIME:
        spawning_time = 0
        target_time = 0
        progress_time = 0
        display_time = 0
        spawning_time_total = 0
        target_time_total = 0
        progress_time_total = 0
        display_time_total = 0

    while (display.active):
        
        if settings.DISPLAY_PERFORMANCE_TIME:
            start = time.time()

        if len(agent_list) <= settings.MAX_AGENTS:
            for agent in spawner.spawn(settings.SPAWN_ATTEMPTS, settings.SPAWN_PROBABILITY):
                display.add(agent)
                agent_list.append(agent)
        
        if settings.DISPLAY_PERFORMANCE_TIME:
            spawning_time = time.time() - start
            spawning_time_total += spawning_time
            start = time.time()
                
        # Update the targets of the agents with the new agent list
        targets.update(agent_list)

        # for agent in agent_list:
        #    if InDangerZone((agent.position[0], agent.position[1])) and InDangerZone((agent.target[0], agent.target[0])):
        #        agent.target = agent.position + np.array([30,0])
        
        if settings.DISPLAY_PERFORMANCE_TIME:
            target_time = time.time() - start
            target_time_total += target_time
            start = time.time()
            
        progress(forces, agent_list) # Progress one step

        if settings.DISPLAY_PERFORMANCE_TIME:
            progress_time = time.time() - start
            progress_time_total += progress_time
            start = time.time()

        # Update the window, which will also draw it, also checks to de-active window on quit
        display.update()

        if settings.DISPLAY_CONTROL:
            control.check(display)

        # Limit the frame rate, if specified
        if settings.FRAME_RATE > 0:
            clock.tick(settings.FRAME_RATE)
        
        if settings.DISPLAY_PERFORMANCE_TIME:
            display_time = time.time() - start
            display_time_total += display_time

            print("* Means total time, other is time of this iteration.")
            print(f"Spawning: [{spawning_time}], Target: [{target_time}], Progress: [{progress_time}], Display: [{display_time}]")
            print(f"Spawning*:[{spawning_time_total}], Target*:[{target_time_total}], Progress*:[{progress_time_total}], Display*:[{display_time_total}]")

    if settings.PLATFORM_DISTIBUTION_MEASUREMENT == True:
        area1 = []
        area2 = []
        area3 = []
        area4 = []
        area5 = []
        area6 = []
        area7 = []
        area8 = []
        for agent in agent_list:
            if agent.position[0] < 1/8 * WIDTH:
                area1.append(agent)
            elif agent.position[0] < 2/8 * WIDTH:
                area2.append(agent)
            elif agent.position[0] < 3/8 * WIDTH:
                area3.append(agent)
            elif agent.position[0] < 4/8 * WIDTH:
                area4.append(agent)
            elif agent.position[0] < 5/8 * WIDTH:
                area5.append(agent)
            elif agent.position[0] < 6/8 * WIDTH:
                area6.append(agent)
            elif agent.position[0] < 7/8 * WIDTH:
                area7.append(agent)
            elif agent.position[0] < 8/8 * WIDTH:
                area8.append(agent)
        print(len(area1), len(area2), len(area3), len(area4), len(area5), len(area6), len(area7), len(area8))


# Progress space simulation with STEP_SIZE
def progress(forces:Forces, agent_list:list):
    global oversteps_dt, elapsed_time
    forces.step(agent_list, settings.STEP_SIZE)
    oversteps_dt += Agent.update_oversteps(agent_list)
    elapsed_time += settings.STEP_SIZE
    elapsed_time = round(elapsed_time, 4)

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
    environment_rail_walls = environment.get(Rail_wall)
    return Forces(environment_walls, environment_rail_walls)

class Clock(Drawable):
    def draw(self, surface: pygame.Surface):
        Text(f"Time: {round(elapsed_time, 1)}", 1320, 0).draw(surface)
    
class Danger(Drawable):
    def draw(self, surface: pygame.Surface):
        Text(f"Overstepped seconds: {round(oversteps_dt,1)}", 1000, 0).draw(surface)

main()