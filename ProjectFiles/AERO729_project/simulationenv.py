from __future__ import annotations
from typing import Optional, Union
import math
import numpy as np
from numpy.typing import NDArray

from particle import Particle
from utilitiies import calculate_box_width

class SimulationEnviroment():

    def __init__(self,
                 particles: Union[int, list[tuple]],
                 env_height: float,
                 env_width: float,
                 tolerance: float,
                 sigma: float,
                 epsilon: float,
                 del_t: float
                 ) -> None:
        """
        Enviroment for molecular dynamics sim, creates and keeps track of particles 
        and time steps the simulation.

        Parameters
        ----------

        particles: int, list

            If int then the enviroment creates that many particles and chooses random\n
            initial positions and velocities for each of them. If a list is passed in\n
            it should be a list of tuples where the frst element is each particles\n
            initial position and the second is their initial velocity. 

        env_height: float

            The height of the domain

        env_width: float
            
            The width of the domain

        tolerance: float

            value for which the potential function is considered negligable, this determines\n
            the size of each box in the sub-grid.

        sigma: float

            The distance at which the value of the Lennard-Jones potential is zero
        
        epsilon: float

            the depth of th well in the Lennard-Jones potential
        
        del_t: flaot

            change in time for one time step.

        Notes
        -----

        If n particles are initialized at random there isnitial position will be evenly distributed\n
        in the domain and the velocities will be initialized in any direction with unit magnitude.
        """
        # create enviroment parameters

        self.height: float = env_height
        self.width: float = env_width
        self.tolerance: float = tolerance
        self.del_t: float = del_t

        # calculate the minimum sub-grid box sizes
        min_size = calculate_box_width(
            tol=tolerance,
            sigma=sigma,
            epsilon=epsilon
        )

        # calculate how many sub-boxes there should be width wise
        self.num_width_boxes: int = int(self.width//min_size)
        self.sub_width: float = min_size + \
            (self.width%min_size)/self.num_width_boxes
        
        # calculate how many sub-boxes there should be height wise
        self.num_height_boxes: int = int(self.height//min_size)
        self.sub_height: float = min_size + \
            (self.height%min_size)/self.num_height_boxes

        # I am pretty sure you do not need these except maybe for plotting
        self.subgrid_w_edges: NDArray = np.arange(
            start=0,
            stop=self.width,
            step=self.sub_width
        )
        self.subgrid_h_edges: NDArray = np.arange(
            start=0,
            stop=self.height,
            step=self.sub_height
        )

        # build dictionary which tracks which particles are in which grid spaces
        self.grid_node_dict: dict = {
            (i, j) : [] for i in range(self.num_width_bounds) for j in range(self.num_height_boxes)
        }

        # create particles in the enviroment
        if isinstance(particles, int):
            pass
        
        elif isinstance(particles, list):
            pass

        else:

            raise ValueError('particles must be either an int or a list')
        