from __future__ import annotations
import numpy as np
from numpy.typing import NDArray\


class Particle():

    def __init__(self,
                 initial_pos: NDArray,
                 initial_velocity: NDArray,
                 sigma: float,
                 epsilon: float,
                 mass: float = 1
                 ):

        self.pos: NDArray = initial_pos
        self.vel: NDArray = initial_velocity
        self.force: NDArray = np.zeros(2)
        self.sigma: float = sigma
        self.epsilon: float = epsilon,
        self.mass: float = mass,
        self.trajectory = []

    @property
    def position(self) -> NDArray: return self.pos

    @position.setter
    def position(self,
                 new_pos: NDArray
                 ) -> None:
        self.pos = new_pos
        
    @property
    def velocity(self) -> NDArray: return self.vel
    
    @velocity.setter
    def velocity(self,
                 new_vel: NDArray
                 ) -> None:
        self.vel = new_vel


    def calculate_force(self,
                        other_pos: NDArray,
                        ) -> NDArray:
        """
        Calculate the force between two interacting particles with a 
        Lennard-Jones potential. if the potential is given U(r) where r
        is scalar distance between the particles, then the force between 
        them is F = -grad(U). 

        Params
        ------
        other_pos: NDArray
            The position vector of the other particle

        Returns
        -------
            NDArray
            The force vector between the two particles
        """

        # calculate the distance
        dist = np.linalg.norm(self.pos - other_pos)

        # calculate the gradient
        mult = (48*self.epsilon)/(self.sigma**2)



    def increment_force(self,
                        force: NDArray
                        ) -> NDArray:
        
        pass


    def clear_force(self) -> None:
        self.force = np.zeros(2)

    def step(self) -> NDArray:
        pass



