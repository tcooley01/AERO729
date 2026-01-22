import numpy as np
from numpy.typing import NDArray
def calculate_circle_collision(position: NDArray,
                               velocity: NDArray,
                               radius: float
                               )-> float | bool:
    
    t_2 = velocity[0]**2 + velocity[1]**2
    t = 2*(velocity[0]*position[0] + velocity[1]*position[1]) 
    t_0 = position[0]**2 + position[1]**2 - radius**2

    coeffs = [t_2, t, t_0]

    roots = np.roots(coeffs)
    
    if np.iscomplex(roots)[0] or np.iscomplex(roots)[1]:
        return False

    if roots[0] < 0:
        return False
    

    return float(np.min(roots))

def calculate_collision_point(position: NDArray,
                              velocity: NDArray,
                              time_to_collision: float
                              ) -> NDArray:

    return velocity*time_to_collision + position

def calculate_square_collision(position: NDArray,
                               velocity: NDArray,
                               length: float
                               ) -> float:
    x_0 = length/2
    x_1 = -length/2
    y_0 = x_0
    y_1 = x_1
    times = np.zeros(2)

    if velocity[0] <= 0:
        if velocity[0] == 0:
            times[0] = np.inf
        else:
            time = np.abs((x_1 - position[0])/velocity[0])
            times[0] = time
    else:
        time = np.abs((x_0 - position[0])/velocity[0])
        times[0] = time    

    if velocity[1] <= 0:
        if velocity[1] == 0:
            times[1] = np.inf
        else:
            time = np.abs((y_1 - position[1])/velocity[1])
            times[1] = time
            
    else:
        time = np.abs((y_0 - position[1])/velocity[1])
        times[1] = time          

    return float(np.min(times))

    
def calulate_reflection(position: NDArray,
                        velocity: NDArray
                        ) ->  NDArray:
    
    normal_angle = np.arctan(position[1]/position[0])
    normal_vec = np.array([np.cos(normal_angle), np.sin(normal_angle)])
    normal_vec /= np.linalg.norm(normal_vec)

    v_new = velocity - 2*(np.dot(normal_vec, velocity))*normal_vec

    return v_new

def approximate_collisions(num_particles: int,
                           lmb: float,
                           tau: float
                           ) -> NDArray:
    
    collisions = np.random.poisson(
        lam = lmb*tau,
        size = num_particles
    )    

    return collisions