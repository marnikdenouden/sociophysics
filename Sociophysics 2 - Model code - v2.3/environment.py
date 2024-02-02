import pygame
import json
import os
import random
import math
import numpy as np
import colors
from interfaces import JsonObject, SpawningArea, Drawable, Vector
from display import Rectangle, Circle, Display
import settings

def setup():
    if __name__ == '__main__':
        ### Code to test this file. ###
        
        # Pygame setup
        pygame.init()

        # Create a file for the environment objects.
        environment = Environment("environment")

        # Clear the environment, so you don't expand the environment with add each run
        environment.clear()

        # Add environment objects to the file, making sure they are specified in the environmentobject.types().
        environment.add(Wall(140, 160, 160, 50, (255, 255, 255)))
        environment.add(Wall(370, 100, 10, 70, (255, 255, 255)))
        environment.add(SpawningCircle(60, 200, 30, 1))
        environment.add(Bench(200, 250, 60, 20))
        environment.add(MovePath(100, 50, 60, 20))

        # Set the list of spawning area's
        environment.set(SpawningRectangle, [SpawningRectangle(40, 60, 300, 30, 4)])

        # Also possible to get the list of spawning area's
        print(environment.get(SpawningRectangle)[0].get_spawn_position())

        # Save the objects, which overwrites the existing environment objects.
        environment.save_objects()
        
        # Load the objects, which load all environment objects stored to access from file.
        # environment.load_objects()

        # Create a new display to showcase the environment int
        display = Display("Testing environment.py")

        # Add the environment to display all environment objects
        display.add(environment)

        # Also able to individually add drawables to the display
        # # Add the walls to the display
        # for i in range(len(environment.get(Wall))):
        #     display.add(environment.get(Wall)[i])

        # # Add the spawning areas to the display
        # for i in range(len(environment.get(SpawningRectangle))):
        #     display.add(environment.get(SpawningRectangle)[i])
            
        # # Add the spawning areas to the display
        # for i in range(len(environment.get(SpawningCircle))):
        #     display.add(environment.get(SpawningCircle)[i])

        while(display.active):
            display.update()

class EnvironmentObject(JsonObject):
    environment_type = "basic environment type"

    def types() -> list:
        return [Wall, Rail_wall, Bench, MovePath, SpawningRectangle, SpawningCircle] # All types need to be an environment object

    # Load the environment objects from the list of deserialized dictionaries
    def load_json_objects(json_list:list) -> dict:
        objectTypes = EnvironmentObject.types()

        # Create a object dictionary with type as key and for value an empty list
        object_dictionary = {}
        for type in objectTypes:
            object_dictionary.update({type:[]})

        # For all deserialized json objects we add them to the list that has the matching type
        for i in range(len(json_list)):
            type = json_list[i].get("type")
            for key in object_dictionary:
                if type == key.environment_type:
                    object = key.load_object(json_list[i])
                    object_dictionary.get(key).append(object)

        return object_dictionary        

    # Save the environment objects to a list of serializable dictionaries
    def save_json_list(objects:list) -> list:
        json_list = []
        for i in range(len(objects)):
            dictionary = {"type": objects[i].environment_type}
            dictionary.update(objects[i].save_dictionary())
            json_list.append(dictionary)
        return json_list

class Wall(Rectangle, EnvironmentObject):
    environment_type = "wall"
    color = colors.WALL_COLOR
    elasticity = 0.5 # range from 0 to 1. Where 0 is no bounce and 1 is max bounce.
    
    def __init__(self, x:int, y:int, width:int, height:int, color:tuple=color):
        # Create rectangle for the display
        super().__init__(x, y, width, height, color)

    # Gets the distance vector for a specified position.
    # Returning vector points away from the wall with the lenght equal to the distance to the wall
    def get_distance_vector(self, position:tuple) -> np.ndarray:
        # Set the x and y variable
        x = position[0]
        y = position[1]

        # Compute the closest x and y coordinate within the wall to the point
        closest_x = np.clip(x, self.x, self.x + self.width)
        closest_y = np.clip(y, self.y, self.y + self.height)

        # To remove the distance vector when the point is not directly to one side of the rectangle
        if not settings.WALL_CORNER_FORCE:
            if abs(x - closest_x) > 0 and abs(y - closest_y) > 0:
                return Vector.zero()

        # Create the vector from the distance of the point to the wall
        return Vector.create((x - closest_x, y - closest_y))

    def blocks_line(self, pos1:np.ndarray, pos2:np.ndarray):
        '''Checks if the specified line, defined by the two points, crosses any of the edges of the wall.'''
        # Get the corner points of the wall.
        top_left = Vector.create((self.x, self.y))
        top_right = Vector.create((self.x + self.width, self.y))
        bottom_left = Vector.create((self.x, self.y + self.height))
        bottom_right = Vector.create((self.x + self.width, self.y + self.height))

        # Check if any of the edges of the wall is crossed by the specified line.
        cross_top = Vector.lines_cross(pos1, pos2, top_left, top_right)
        cross_bottom = Vector.lines_cross(pos1, pos2, bottom_left, bottom_right)
        cross_left = Vector.lines_cross(pos1, pos2, top_left, bottom_left)
        cross_right = Vector.lines_cross(pos1, pos2, top_right, bottom_right)

        # Return if any of the edges if crossed by the specified line.
        return cross_top or cross_bottom or cross_left or cross_right

    def load_object(dictionary:dict):
        x = dictionary.get("x")
        y = dictionary.get("y")
        width = dictionary.get("width")
        height = dictionary.get("height")
        return Wall(x, y, width, height)
    
class Rail_wall(Wall):
    environment_type = "Rail_wall"
    
    def __init__(self, x:int, y:int, width:int, height:int):
        # Create rectangle for the display
        super().__init__(x, y, width, height)

    def load_object(dictionary:dict):
        x = dictionary.get("x")
        y = dictionary.get("y")
        width = dictionary.get("width")
        height = dictionary.get("height")
        return Rail_wall(x, y, width, height)
    
class MovePath(Rectangle, EnvironmentObject):
    environment_type = "move path"
    
    def __init__(self, x:int, y:int, width:int, height:int):
        # Create rectangle for the display
        super().__init__(x, y, width, height, colors.MOVE_PATH_COLOR)

    def load_object(dictionary:dict):
        x = dictionary.get("x")
        y = dictionary.get("y")
        width = dictionary.get("width")
        height = dictionary.get("height")
        return MovePath(x, y, width, height)
    
    def draw(self, surface: pygame.Surface):
        if settings.NUDGE_MOVE_PATH:
            super().draw(surface)
        
class Bench(Rectangle, EnvironmentObject):
    environment_type = "bench"
    color = colors.BENCH_COLOR

    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, Bench.color)

    def load_object(dictionary:dict):
        x = dictionary.get("x")
        y = dictionary.get("y")
        width = dictionary.get("width")
        height = dictionary.get("height")
        return Bench(x, y, width, height)

class DangerZone(Rectangle):
    color = colors.DANGER_ZONE_COLOR
    def __init__(self, x:int, y:int, width:int, height:int, color:tuple=color):
        # Create rectangle for the display
        super().__init__(x, y, width, height, color)

class SpawningRectangle(SpawningArea, Rectangle, EnvironmentObject):    
    environment_type = "spawning rectangle"
    color = colors.SPAWNING_AREA_COLOR

    def __init__(self, x:int, y:int, width:int, height:int, weight:int, color:tuple=color):
        SpawningArea.__init__(self, weight)
        Rectangle.__init__(self, x, y, width, height, color)

    def save_dictionary(self) -> dict:
        dictionary = Rectangle.save_dictionary(self)
        dictionary.update({"weight":self.weight})
        return dictionary

    def load_object(dictionary:dict):
        x = dictionary.get("x")
        y = dictionary.get("y")
        width = dictionary.get("width")
        height = dictionary.get("height")
        weight = dictionary.get("weight")
        return SpawningRectangle(x, y, width, height, weight)
    
    def get_spawn_position(self) -> tuple:
        x = random.randint(self.x, self.x + self.width)
        y = random.randint(self.y, self.y + self.height)
        return (x, y)

class SpawningCircle(SpawningArea, Circle, EnvironmentObject):
    environment_type = "spawning circle"
    color = colors.SPAWNING_AREA_COLOR

    def __init__(self, x:int, y:int, radius:int, weight:int, color:tuple=color):
        SpawningArea.__init__(self, weight)
        Circle.__init__(self, x, y, radius, color)

    def save_dictionary(self) -> dict:
        dictionary = Circle.save_dictionary(self)
        dictionary.update({"weight":self.weight})
        return dictionary

    def load_object(dictionary:dict):
        x = dictionary.get("x")
        y = dictionary.get("y")
        radius = dictionary.get("radius")
        weight = dictionary.get("weight")
        return SpawningCircle(x, y, radius, weight)
    
    def get_spawn_position(self) -> tuple:
        rotation = self.radius * math.sqrt(random.random())
        theta = random.random() * 2 * math.pi
        x = self.x + rotation * math.cos(theta)
        y = self.y + rotation * math.sin(theta)
        return (x, y)

class Environment(Drawable):

    def __init__(self, name:str):
        # Make sure that the environment file exists
        self.file_name = f"{name}.json"
        if not os.path.isfile(self.file_name):
            file = open(self.file_name, "w")
            file.closed
        self.clear()

    # Create an empty object dictionary for all environement object types
    def clear(self):
        self.object_dictionary = {}
        for type in EnvironmentObject.types():
            self.object_dictionary.update({type:[]})

    # Add an environment object to their respective list on the dictionary 
    def add(self, object:EnvironmentObject):
        self.object_dictionary.get(type(object)).append(object)

    # Get the list of objects for a specified environment object type 
    # Returns all environment objects, if type is unspecified
    def get(self, type=None):
        if type != None:
            return self.object_dictionary.get(type)
        environment_objects = []
        for object_list in self.object_dictionary.values():
            environment_objects.extend(object_list)
        return environment_objects
    
    # Set the list of objects for a specified environment object type
    def set(self, type, objects:list):
        self.object_dictionary.get(type).clear()
        self.object_dictionary.get(type).extend(objects)

    def load_objects(self):
        # Open the environment file to read the json string
        with open(self.file_name, 'r') as file:
            environment = (list)(json.load(file))

        # Set the object dictionary to the newly loaded instance
        self.object_dictionary = EnvironmentObject.load_json_objects(environment)
    
    def save_objects(self): 
        # Create a list called environment
        environment = []

        # Add for each environment object type a list of json serializable object representations
        for type in self.object_dictionary:
            environment.extend(type.save_json_list(self.object_dictionary.get(type)))

        # Serialize the environment list to a string
        json_string = json.dumps(environment, indent=4)

        # Save the json string in the environment file
        with open(self.file_name, "w") as outfile:
            outfile.write(json_string)

    def draw(self, surface:pygame.Surface):
        for type in self.object_dictionary:
            for object in self.object_dictionary.get(type):
                if isinstance(object, Drawable):
                    object.draw(surface)

    def get_walls(self) -> list[Wall]:
        walls = list[Wall]()
        for environment_object in self.get():
            if isinstance(environment_object, Wall) and not isinstance(environment_object, Rail_wall):
                walls.append(environment_object)
        return walls
    
    def get_rail_walls(self) -> list[Rail_wall]:
        rail_walls = list[Rail_wall]()
        for environment_object in self.get():
            if isinstance(environment_object, Rail_wall):
                rail_walls.append(environment_object)
        return rail_walls
    
    def get_mvove_paths(self) -> list[MovePath]:
        move_paths = list[MovePath]()
        for environment_object in self.get():
            if isinstance(environment_object, MovePath):
                move_paths.append(environment_object)
        return move_paths

    def get_spawning_areas(self) -> list[SpawningArea]:
        spawning_areas = list[SpawningArea]()
        for environment_object in self.get():
            if isinstance(environment_object, SpawningArea):
                spawning_areas.append(environment_object)
        return spawning_areas
    
    def get_benches(self) -> list[Bench]:
        benches = list[Bench]()
        for environment_object in self.get():
            if isinstance(environment_object, Bench):
                benches.append(environment_object)
        return benches

setup()