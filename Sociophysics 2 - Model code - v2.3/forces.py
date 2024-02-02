import math
import numpy as np
import settings
import random
import time
from agent import Agent
from interfaces import Vector
from environment import Wall, Rail_wall

def setup():
    if __name__ == '__main__':
        print("For heatmaps of force functions please run heatmaps.py")

class Forces:
    distance_threshold = settings.DISTANCE_THRESHOLD
    target_scalar = settings.TARGET_FORCE_SCALER
    repulsion_scalar = settings.REPULSION_FORCE_SCALAR
    repulsion_dangerzone_scalar = settings.REPULSION_DANGER_ZONE_SCALAR
    unaware_dangerzone_scalar = settings.dangerzone_awerness_false_multiplier
    friction_value = settings.FRICTION_FORCE_SCALAR
    wall_value = settings.WALL_FORCE_SCALAR
    def __init__(self, environment_walls:list[Wall], environment_rail_walls:list[Rail_wall]):
        self.environment_walls = environment_walls
        self.environment_rail_walls = environment_rail_walls

    def get_repulsion_walls(self, position:tuple,agent:Agent = None) -> tuple:
        # We want to compute the cummalative repulsion vector for the specified point
        repulsion_vector = Vector.zero()

        # From all the physics objects from the environment we get a distance vector
        for physics_object in self.environment_walls:
            distance_vector = physics_object.get_distance_vector(position)

            # Check if the distance vector is small enough to be applied
            length = Vector.length(distance_vector)
            if 0 < length < Forces.distance_threshold:  
                # Make the length of the vector equal 1 / sqrt(length) and add it to the repulsion vector
                if math.sqrt(length) > 0:
                    scalar = Forces.wall_value / math.sqrt(length)
                    repulsion_vector += Vector.scale_to_length(distance_vector, scalar)

        for physics_object in self.environment_rail_walls:
            distance_vector = physics_object.get_distance_vector(position)

            # Check if the distance vector is small enough to be applied
            length = Vector.length(distance_vector)
            if 0 < length < Forces.distance_threshold:  
                # Make the length of the vector equal 1 / sqrt(length) and add it to the repulsion vector
                if math.sqrt(length) > 0:
                    scalar_aware = Forces.repulsion_dangerzone_scalar / math.sqrt(length)
                    scalar_unaware = (Forces.unaware_dangerzone_scalar * Forces.repulsion_dangerzone_scalar)/ math.sqrt(length)
                    if agent:
                        if agent.dangerzone_awareness == True:
                            repulsion_vector += Vector.scale_to_length(distance_vector, scalar_aware)
                        elif agent.dangerzone_awareness == False:
                            repulsion_vector += Vector.scale_to_length(distance_vector, scalar_unaware)
                    else:
                        repulsion_vector += Vector.scale_to_length(distance_vector, scalar)
        return repulsion_vector
    
    def is_visible(self, agent:Agent, position:np.ndarray) -> bool:
        inside_wall = False
        blocked_by_wall = False
        for wall in self.environment_walls:
            inside_wall = inside_wall or wall.containsPoint(position)
            blocked_by_wall = blocked_by_wall or wall.blocks_line(agent.position, position)
            if inside_wall or blocked_by_wall:
                return False
        for wall in self.environment_rail_walls:
            inside_wall = inside_wall or wall.containsPoint(position)
            blocked_by_wall = blocked_by_wall or wall.blocks_line(agent.position, position)
            if inside_wall or blocked_by_wall:
                return False
        return True
    
    def get_sight_value(self, agent:Agent, position:np.ndarray) -> float:                
        distance_vector = agent.get_distance_vector(position)
        agent_distance = Vector.length(distance_vector)

            # New way to calculate
        distance_modifier = Forces.map_range_function(agent_distance, 
            settings.AGENT_SIGHT_DISTANCE, settings.AGENT_SIGHT_UNIFORM_DISTANCE)
        
            # old way to calculate
        # # A better function can be made to map the distance value to a prefered sight value curve.
        # sight_range = settings.AGENT_SIGHT_DISTANCE # A value to determine the range at which the sight value is larger than 0
        # uniform_sight_range = 60 # Value to determine what range has max value
        # distance_modifier = np.clip(sight_range - agent_distance, 0, uniform_sight_range) / uniform_sight_range
        
        if (Vector.length(agent.velocity) != 0 and Vector.length(distance_vector) != 0):
            agent_angle = Vector.find_angle(agent.velocity, distance_vector)
        else:
            agent_angle = 0

            # New way to calculate
        angle_modifier = Forces.map_range_function(agent_angle, 
            settings.AGENT_SIGHT_ANGLE, settings.AGENT_SIGHT_UNIFORM_ANGLE)
        
            # Old way to calculate
        # # A better function can be made to map the distance value to a prefered sight value curve.
        # sight_angle = settings.AGENT_SIGHT_ANGLE # A value to determine the angle at which the sight value is larger than 0
        # uniform_sight_angle = 100 # Value to determine what range has max value
        # angle_modifier = np.clip(sight_angle - agent_angle, 0, uniform_sight_angle) / uniform_sight_angle

        # Lots of options for how to bring these modifiers, which are both between 0 and 1 together. + * ...
        return distance_modifier * angle_modifier
    
    def map_range_function(value:float, range:float, uniform_range:float) -> float:
        if value > range:
            return 0
        elif value > uniform_range:
            return 1 - (value - uniform_range) / (range - uniform_range)
        else:
            return 1

    def in_sight_moving(person:Agent, agent:Agent, forces:'Forces') -> bool:
        # Check if the agent is not in or behind a wall
        if not forces.is_visible(person, agent.position):
            return False
        
        # Check if the agent is spotted by the person for moving person
        return random.random() < forces.get_sight_value(person, agent.position)

    def in_sight_standing(person:Agent, agent:Agent) -> bool:
        # check if the agent is within sight distance for stationary person
        distance = Vector.length(person.get_distance_vector(agent.position))
        return distance <= settings.AGENT_SIGHT_DISTANCE

    def in_sight(self, agent_list:list['Agent']):
        '''Check for each person if any agent is in sight, if so the agent is added in the persons memory.'''
        for person in agent_list:
            agent = random.choice(agent_list)
            # Skip the case of looking for themselves
            if person == agent:
                continue

            spots_agent = False
            # Skip if the person is standing still
            if Vector.length(person.velocity) <= settings.AGENT_VELOCITY_BOUNDRY:
                spots_agent = Forces.in_sight_standing(person, agent)
            else:
                spots_agent = Forces.in_sight_moving(person, agent, self)

            # Add the agent to the person memory under the sight conditions
            if spots_agent:                        
                person.add_to_memory(agent)

    def get_repulsion_agent(agent:Agent, position) -> np.ndarray:
        distance_vector = agent.get_distance_vector(position)
        repulsion = Vector.zero()
        # Check if the distance vector is small enough to be applied
        length = Vector.length(distance_vector)
        if 0 < length < Forces.distance_threshold:  
            # Make the length of the vector equal 1 / sqrt(length) and add it to the repulsion vector
            if math.sqrt(length) > 0:
                scalar = 1 / math.sqrt(length) * Forces.repulsion_scalar
                repulsion = Vector.scale_to_length(distance_vector, scalar)
        return repulsion

    def get_repulsion_agents(self, person:Agent, agent_list:list[Agent]) -> np.ndarray:
        repulsion = np.array([0.0, 0.0])
        for agent in agent_list:
            if agent != person:
                if person.knows_agent(agent) or not settings.USE_AGENT_AWARENESS_FOR_FORCE:
                    repulsion += Forces.get_repulsion_agent(agent, person.position)
        return repulsion
    
    def get_attraction(self, agent:Agent) -> np.ndarray:
        # We want to compute the attraction vector for an agent
        attraction_vector = Vector.zero()

        # If the agent has not reached their target we add an attraction force
        if not agent.reached_target():
            distance_vector = agent.get_distance_vector(agent.target)
            attraction_vector = Vector.scale_to_length(distance_vector, Forces.target_scalar)

        return attraction_vector
    
    def get_friction_vector(self, agent:Agent) -> np.ndarray:
        if Vector.length(agent.velocity) > settings.MIN_VELOCITY_FOR_FRICTION:
            return -agent.velocity * Forces.friction_value
        else:
            return Vector.zero()

    def get_total_force(self, agent:Agent, agent_list:list[Agent]) -> np.ndarray: 
        attraction_force = self.get_attraction(agent)
        repustion_force = self.get_repulsion_agents(agent, agent_list)
        wall_force = self.get_repulsion_walls(agent.position, agent = agent)
        friction_force = self.get_friction_vector(agent)
        return attraction_force + repustion_force + wall_force + friction_force

    def step(self, agent_list:list[Agent], dt:float):
        Agent.update_memory(agent_list)
        self.in_sight(agent_list)
        
        for agent in agent_list: # Only update if an agent is not waiting
            if not agent.waiting:
                force = self.get_total_force(agent, agent_list)
                force = force * settings.pmc
                agent.step(force, dt)

            if agent.selected: #show agent data of selected agent
                if settings.AGENT_DATA:
                    print(f"Agent data: ID: {agent.ID}, mass: {agent.mass}, position: {(agent.position / 18.5).round(1)}, velocity: {(agent.velocity / 18.5).round(1)}, target: {(agent.target / 18.5).round(1)}, in_danger_zone: {agent.in_danger_zone}, dangerzone_awareness: {agent.dangerzone_awareness}, waiting: {agent.waiting}")
                
                if settings.FORCE_DATA:
                    if agent.waiting:
                        print("waiting")
                    else:
                        print(f"Force data: ID: {agent.ID}, Agent force: {self.get_repulsion_agents(agent, agent_list).round(1)}, Wall force: {self.get_repulsion_walls(agent.position, agent = agent).round(1)}, Attraction force: {self.get_attraction(agent).round(1)}, Friction force: {self.get_friction_vector(agent).round(1)}, Total force: {self.get_total_force(agent, agent_list).round(1)}, velocity: {(agent.velocity / 18.5).round(1)}")

setup()