import pygame
import numpy as np
import math

# Used in display.py
class Drawable:
    def draw(self, surface:pygame.Surface):
        """Draws the representation to the specified surface."""
        pass

# Used in display.py
class Clickable:
    def click(self, position:tuple[float, float]):
        """Activates the click function for this object."""
        pass

# Used in environment.py
class JsonObject:
    def save_dictionary(self) -> dict:
        pass

    def load_object(dictornary:dict):
        pass

# Used in environment.py
class SpawningArea:
    def __init__(self, weight:int):
        self.weight = weight

    def get_spawn_position(self) -> tuple[float, float]:
        """Gets a random spawn point that is uniformly distributed in the spawning area."""
        pass

class Vector():
    def create(position:tuple[float, float]) -> np.ndarray:
        """Creates a vector representation of the specified position. Using np.array"""
        coordinate_list = []
        for coordinate in position:
            coordinate_list.append(coordinate)
        return np.array(coordinate_list)

    def extract(position:np.ndarray) -> tuple:
        """Extracts a position tuple from a np.array vector representation"""
        return (position[0], position[1])

    def length(vector:np.ndarray) -> float:
        """Returns the length of the specified vector."""
        return np.linalg.norm(vector)

    def scale_to_length(vector:np.ndarray, length:float) -> np.ndarray:
        """Returns the vector scaled to the specified length."""
        return vector / Vector.length(vector) * length

    def zero() -> np.ndarray:
        """Returns a zero cooridnate as ndarray."""
        return np.array([0.0, 0.0])
    
    def rotate(vector:np.ndarray, angle:float) -> np.ndarray: #angle in radians!! (probably) ##I don't think I need it but just in case we need it later I'll keep it in
        """returns a vector rotate by the angle"""
        rotation_matrix = np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])
        return vector.dot(rotation_matrix)
    
    def find_angle(vector1:np.ndarray, vector2:np.ndarray) -> float:
        """Finds the angle between two vectors in degrees"""
        if Vector.length(vector1) == 0 or Vector.length(vector2) == 0:
            print("Tried to compute angle with vector of length 0")
            return 0

        angle_ish = (vector1.dot(vector2))/(Vector.length(vector1) * Vector.length(vector2))
        cliped_angle = np.clip(angle_ish,  -1, 1) #restricts the value to the domain of the arccos to prevent domain error
        return (math.acos(cliped_angle) * 180/math.pi)
    
    def point_orientation(A:tuple, B:tuple, C:tuple) -> bool:
        '''Check if the points are in a counter clock wise orientation to each other in the 2d space.'''
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
    
    def lines_cross(line_1_start:np.ndarray, line_1_end:np.ndarray, line_2_start:np.ndarray, line_2_end:np.ndarray) -> bool:
        '''Checks if two lines defined by the specified 4 points cross, it will return false if the points are all on one line.
        For discussion details on this implementation and credit: https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect'''
        A = Vector.extract(line_1_start)
        B = Vector.extract(line_1_end)
        C = Vector.extract(line_2_start)
        D = Vector.extract(line_2_end)
        return Vector.point_orientation(A,C,D) != Vector.point_orientation(B,C,D) and Vector.point_orientation(A,B,C) != Vector.point_orientation(A,B,D)