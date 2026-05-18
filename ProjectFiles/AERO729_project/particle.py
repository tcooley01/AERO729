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
                 env_width: float,
                 env_height: float,
                 grid_width: float,
                 grid_height:float,
                 mass: float = 1
                 ):
        
        self.index = index
        self.grid_pos = 'unassigned'
        self.pos: NDArray = initial_pos
        self.vel: NDArray = initial_velocity
        self.force: NDArray = np.zeros(2)
        self.sigma: float = sigma
        self.epsilon: float = epsilon
        self.env_width: float = env_width
        self.env_height: float = env_height
        self.grid_width: float = grid_width
        self.grid_height: float = grid_height
        self.mass: float = mass
        self.trajectory = []
        self.velocities = []
        self.trajectory.append(initial_pos)
        self.velocities.append(initial_velocity)
       

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
    def grid_position(self) -> NDArray: return self.grid_pos

    @grid_position.setter
    def grid_position(self,
                      new_grid_pos
                      ) -> None:
        self.grid_pos = new_grid_pos

    @property
    def hyperparameters(self) -> dict:
        
        hyp_dict = {
            'mass' : self.mass,
            'epsilon': self.epsilon,
            'sigma': self.sigma
        }

        return hyp_dict

    def calculate_force(self,
                        other_pos: NDArray
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
        # TODO: boundarys currently cause this to crap out 
        # this must be fixed
        dist = np.linalg.norm(self.pos - other_pos)

        if dist == 0:
            raise Exception(f'got zero')

        if dist > np.sqrt(4*(self.grid_width**2) + 4*(self.grid_height**2)):
            
            # case I am in the far left
            if self.grid_pos[0] == 0:

                shifted_x = other_pos[0] - self.env_width
                other_pos[0] = shifted_x

            # case other is on left
            else: 

                shifted_x = other_pos[0] + self.env_width
                other_pos[0] = shifted_x
        
            # case I am on bottom
            if self.grid_pos[1] == 0:

                shifted_y = other_pos[1] - self.env_height
                other_pos[1] = shifted_y
            
            # case other is on bottom
            else:

                shifted_y = other_pos[1] + self.env_height
                other_pos[1] = shifted_y

            

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

        # new pos needs to have bc taken into acount
        new_x = new_pos[0]%self.env_width
        new_y = new_pos[1]%self.env_height

        new_pos = np.array([new_x, new_y])

        self.trajectory.append(new_pos)
        self.velocities.append(new_velocty)

        self.velocity = new_velocty
        self.pos = new_pos

        return new_pos




