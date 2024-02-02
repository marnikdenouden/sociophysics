from pygame import Surface
import settings
import random
import math
import colors
import numpy as np
from collections.abc import Callable
from interfaces import Vector, Drawable
from forces import Forces
from agent import Agent
from matplotlib import colormaps
from display import Circle, Text
from environment import Environment
from platform_environment import InDangerZone

class Targets(Drawable):
    agent_spot_list_dictionary = dict[Agent, list['Spot']]()
    colormap = colormaps["inferno"].resampled(settings.HEATMAP_STEPS)

    def __init__(self, agent_list:list[Agent], environment:Environment):
        self.agent_list = agent_list
        self.agent_spot_list_dictionary = dict.fromkeys(agent_list)
        self.environement = environment
        self.forces = Forces(environment.get_walls(), environment.get_rail_walls())

    def update(self, agent_list:list[Agent]):
        self.agent_list = agent_list
        wait_influence_range = settings.WAIT_INFLUENCE_RANGE
        for agent in self.agent_list:
            # Give agents their first target
            if not agent.has_target:
                self.select_target(agent)
                self.waiting = False
                agent.has_target = True
                continue

            if settings.DISPLAY_TARGET_SELCTION:
                if self.agent_spot_list_dictionary.get(agent) == None:
                    self.agent_spot_list_dictionary[agent] = list()

            wait_chance = settings.WAIT_CHANCE
            for person in agent_list:
                if person.waiting == True:
                    if Vector.length(agent.get_distance_vector(person.position)) < wait_influence_range:
                        wait_chance *= settings.WAIT_CHANCE_MULTIPLIER
            if agent.position[0] >= 1030:
                wait_chance *= 2

            in_move_path = False        
            for move_path in self.environement.get_mvove_paths():
                if move_path.containsPoint(agent.position) and agent.aware_move_path:
                    in_move_path = True
                else:
                    in_move_path = False

            if not agent.waiting:
                if (agent.reached_target() and (random.random() < wait_chance)
                     and (not InDangerZone(tuple(agent.position))) and (agent.position[0] > settings.WAIT_FROM) and (in_move_path == False)):
                    agent.waiting = True
                elif agent.reached_target():
                    self.select_target(agent)
                # elif Vector.length(agent.velocity) <= 0.5 and random.random() < settings.WAIT_CHANCE/10:
                #     agent.waiting = True
                elif random.random() < settings.SWITCH_TARGET_CHANCE:
                    self.select_target(agent)
                elif random.random() < settings.SWITCH_TARGET_LOW_VELOCITY and Vector.length(agent.velocity) < settings.VELOCITY_TARGET_SWITCH and agent.last_target_time <= 0: 
                    self.select_target(agent)
                    print("oi")

                for bench in self.environement.get_benches():
                    if bench.containsPoint(Vector.extract(agent.position)):
                        agent.velocity *= 0
                        agent.waiting = True
                        agent.target = agent.position
    
    def draw(self, surface:Surface):
        if settings.DISPLAY_TARGET_SELCTION:
            for agent in self.agent_list:
                if agent.selected:
                    for spot in self.agent_spot_list_dictionary[agent]:
                        spot.draw(surface)
                    return

    def select_target(self, agent:Agent):
        agent.last_target_time = 4
        spot_list = self.get_potential_spots(agent)
        
        if settings.DISPLAY_TARGET_SELCTION:
            self.agent_spot_list_dictionary[agent] = spot_list

        if agent.dangerzone_awareness:
            Dangerzone_multiplier = settings.dangerzone_target_multiplier_aware
        else:
            Dangerzone_multiplier = settings.dangerzone_target_multiplier_unaware

        # Please try to keep all the spots weights between 0 and 1 between adjusting the values.
        
        def set_sight_value(spot:Targets.Spot) -> float:
            if not self.forces.is_visible(agent, spot.position):
                return settings.TARGET_SPOT_WALL_WEIGHT
            else:
                return (spot.weight + self.forces.get_sight_value(agent, spot.position)*settings.TARGET_IN_SIGHT_MULTIPLIER)
        Targets.adjust_spot_weights(set_sight_value, spot_list)

        def avoid_known_crowd(spot:Targets.Spot) -> float:
            adjusted_weight = spot.weight
            crowd_list = self.agent_list
            
            if settings.USE_AGENT_AWARENESS_FOR_TARGET:
                crowd_list = agent.get_known_crowd(self.agent_list)    

            for crowd_agent in crowd_list:
                if spot.target_area.containsPoint(Vector.extract(crowd_agent.position)):
                    adjusted_weight *= settings.CROWD_AVOIDANCE
            return adjusted_weight
        Targets.adjust_spot_weights(avoid_known_crowd, spot_list)

        def add_bench_bonus(spot:Targets.Spot) -> float:
            for bench in self.environement.get_benches():
                if bench.containsPoint(Vector.extract(spot.position)):
                    return spot.weight * settings.BENCH_MULTIPLIER
            return spot.weight
        Targets.adjust_spot_weights(add_bench_bonus, spot_list)

        def avoid_danger_zone(spot:Targets.Spot) -> float:
            if InDangerZone(tuple(spot.position)):
                return spot.weight * Dangerzone_multiplier
            return spot.weight
        Targets.adjust_spot_weights(avoid_danger_zone, spot_list)

        # Maybe this can be adjusted to be a bonues for distance to an agents train?
        # Forward bias could just be the velocity at the start when creating the agent.
        #
        def forward_bonus(spot:Targets.Spot) -> float:
            if spot.position[0] >= agent.position[0] + 20:
                return spot.weight * settings.FORWARDS_MULTIPLIER
            return spot.weight
        Targets.adjust_spot_weights(forward_bonus, spot_list)

        Targets.scale_weights(spot_list)

        if Targets.has_valid_weight(spot_list):
            agent.target = Targets.select_spot(agent, spot_list)
        
    class Spot(Drawable):
        def __init__(self, position:np.ndarray, weight:float=settings.TARGET_SPOT_BASE_WEIGHT):
            self.position = position
            self.weight = weight
            '''Please try to keep the weight between 0 and 1'''
            self.target_area = Circle(position[0], position[1], settings.TARGET_RADIUS, colors.SPOT_COLOR)

        def draw(self, surface:Surface):
            background_color = colors.SPOT_COLOR
            if settings.DISPLAY_ADVANCED_SPOT_COLORS:
                color_values = Targets.colormap(self.weight)
                background_color = (255 * color_values[0], 255 * color_values[1], 255 * color_values[2])
                Circle(self.position[0], self.position[1], settings.TARGET_RADIUS, background_color).draw(surface)
            else:
                self.target_area.draw(surface)
            if settings.DISPLAY_ADVANCED_SPOT_WEIGHT:
                Text(str(round(self.weight, 4)), self.position[0], self.position[1], 8, True, colors.SPOT_WEIGHT_COLOR, background_color).draw(surface)
                
    def has_valid_weight(spot_list:list[Spot]) -> bool:
        for spot in spot_list:
            if spot.weight > 0:
                return True
        return False

    def select_spot(agent:Agent, spot_list:list[Spot]) -> np.ndarray:
        #spot_list.append(Targets.Spot(Vector.create([agent.position[0] + 20, -20*agent.velocity[1]/agent.velocity[1]])))
        positions = list(spot.position for spot in spot_list)
        weights = list(spot.weight for spot in spot_list)
        chosen_spot = random.choices(positions, weights)[0]
        if chosen_spot[1] < 50:
            chosen_spot[1] = 50
        elif chosen_spot[1] > 270:
            chosen_spot[1] = 270
        return chosen_spot
    
    def adjust_spot_weights(function:Callable[[Spot], float], spot_list:list[Spot]):
        for spot in spot_list:
            spot.weight = function(spot)

    def scale_weights(spot_list:list[Spot]):
        max_weight = max(spot.weight for spot in spot_list)
        for spot in spot_list:
            spot.weight = spot.weight / max_weight

    def get_potential_spots(self, agent:Agent) -> list[Spot]:
        spot_list = []
        for _ in range(settings.NUMBER_OF_POTENTIAL_TARGETS):
            spot_list.append(self.get_spot(agent))
        return spot_list

    def get_spot(self, agent:Agent) -> Spot:
        # Select a distance that is at least the target radius away
        distance = (settings.NEXT_TARGET_RANGE - settings.TARGET_RADIUS) * math.sqrt(random.random()) + 2*settings.TARGET_RADIUS
        theta = random.random() * 2 * math.pi
        x = agent.position[0] + distance * math.cos(theta)
        y = agent.position[1] + distance * math.sin(theta)
        return Targets.Spot(Vector.create((x, y)))
