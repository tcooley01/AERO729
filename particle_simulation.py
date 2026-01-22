import numpy as np

def calculate_circle_collision(position: np.ndarray,
                               velocity: np.ndarray,
                               radius: float
                               )-> float | bool:
    
    t_2 = velocity[0]**2 + velocity[1]**2
    t = 2*(velocity[0]*position[0] + velocity[1]*position[1]) 
    t_0 = position[0]**2 + position[1]**2 - radius**2

    coeffs = [t_2, t, t_0]

    roots = np.roots(coeffs)

    if np.iscomplex(roots)[0]:
        return False

    return float(np.min(roots))


def calculate_square_collision(position: np.ndarray,
                               velocity: np.ndarray,
                               length: float
                               ) -> float:
    x_0 = length/2
    x_1 = -length/2
    y_0 = x_0
    y_1 = x_1
    times = np.zeros(2)

    if velocity[0] <= 0:
        time = np.abs((x_1 - position[0])/velocity[0])
        times[0] = time
    else:
        time = np.abs((x_0 - position[0])/velocity[0])
        times[0] = time    

    if velocity[1] <= 0:
        time = np.abs((y_1 - position[1])/velocity[1])
        times[1] = time
    else:
        time = np.abs((y_0 - position[1])/velocity[1])
        times[1] = time          

    return float(np.min(times))

    
def calulate_reflection(position: np.ndarray,
                        velocity: np.ndarray
                        ) ->  np.ndarray:
    
    normal_angle = np.arctan(position[1]/position[0])
    normal_vec = np.array([np.cos(normal_angle), np.sin(normal_angle)])
    normal_vec /= np.linalg.norm(normal_vec)

    v_new = velocity - 2*(np.dot(normal_vec, velocity))*normal_vec

    return v_new
