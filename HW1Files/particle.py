import numpy as np
import math

# 
class Particle:
    def __init__(self):
        self.position:np.array = [-10,0]
        self.velocity:np.array = np.array([1,0])
        self.time:float = 0
        self.history:np.ndarray = []
        self.collision_counter:int = 0

    def update_position(self, timestep=0.1) -> None:
        self.position += self.timestep*(self.velocity)
        
    
class Circle:
    def __init__(self):
        self.center:list[float] = [0.0,0.0]
        self.radius:float = 1.0
        self.collision_counter:int = 0
    
class Box:
    def __init__(self):
        self.size:float = 10

def collided(particle:Particle, circle:Circle) -> bool:
    dist_from_center = math.sqrt(particle.position[0]**2 + particle.position[1]**2)
    collided = dist_from_center <= circle.radius #true if inside or on circle
    if collided:
        circle.collision_counter+=1
        particle.collision_counter+=1
        particle.history[particle.collision_counter] = particle.position
    return collided

def get_normal_vec(point_on_circle:tuple) -> float:
    vec = np.array(math.cos(math.atan(point_on_circle[1], point_on_circle[0])), math.sin(math.atan(point_on_circle[1], point_on_circle[0])))
    return vec / np.linalg.norm(vec)

def reflect(old_velocity:np.array, normal_vec:np.array)-> np.array:
    return old_velocity - 2*np.dot(old_velocity, normal_vec)*normal_vec

def willbe_inbox(position:np.array, velocity:np.array, timestep:float, box:Box)-> bool:
    next_position:np.array = position + (timestep*velocity)
    return True if abs(next_position[0]) < (box.size/2) & abs(next_position[1]) < (box.size/2) else False

def isbetween(value, ub, lb):
    return True if (value > lb & value < ub) else False

def wrap_position(oob_position:np.array) -> np.array:
    #if will not be in box, wrap around to next position that will be in box
    new_position = np.array()
    if oob_position[0] > 5:
        oob_position[0] = oob_position[0] -10
    if oob_position[0] < -5:
        oob_position[0] = oob_position[0] +10
    if oob_position[1] > 5:
        oob_position[1] = oob_position[1] -10
    if oob_position[1] < -5:
        oob_position[1] = oob_position[1] +10

    return new_position