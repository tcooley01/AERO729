from __future__ import annotations
import numpy as np
from numpy.typing import NDArray\


class Particle():

    def __init__(self,
                 index: int,
                 initial_pos: NDArray,
                 initial_velocity: NDArray,
                 sigma: float,
                 epsilon: float,
                 mass: float = 1
                 ):
        
        self.index = index
        self.pos: NDArray = initial_pos
        self.vel: NDArray = initial_velocity
        self.force: NDArray = np.zeros(2)
        self.sigma: float = sigma
        self.epsilon: float = epsilon
        self.mass: float = mass
        self.trajectory = []
        self.velocities = []
       

    """
    Create settrs and gettrs
    """
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

    @property
    def hyperparameters(self) -> dict:
        
        hyp_dict = {
            'mass' : self.mass,
            'epsilon': self.epsilon,
            'sigma': self.sigma
        }

        return hyp_dict

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
        mult = 48*self.epsilon/self.sigma**2
        fp = (self.sigma/dist)**8
        sp = (self.sigma/dist)**14
        diff = self.pos - other_pos
        lmd = mult*(fp - sp)
        force = -lmd*diff

        return force

    def increment_force(self,
                        new_force: NDArray
                        ) -> NDArray:
        self.force += new_force


    def clear_force(self) -> None:
        self.force = np.zeros(2)

    def step(self, del_t) -> NDArray:
        """
        Steps forward del_t time steps 

        Params
        ------
        del_t: float
            time increment
        """
        #TODO: Make sure that if force is zero it still works
        acceleration = self.force/self.mass
        new_velocty = del_t*acceleration + self.velocity
        new_pos = del_t*new_velocty + self.pos

        self.trajectory.append(new_pos)
        self.velocities.append(new_velocty)

        self.velocity = new_velocty
        self.pos = new_pos

        return new_pos




