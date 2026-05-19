from __future__ import annotations
from typing import Optional, Union
import math
import numpy as np
from numpy.typing import NDArray

from particle import Particle
from utilities import calculate_box_width

class SimulationEnviroment():

    def __init__(self,
                 particles: Union[int, list[Particle]],
                 env_height: float,
                 env_width: float,
                 tolerance: float,
                 sigma: float,
                 epsilon: float
                 ) -> None:
        """
        Enviroment for molecular dynamics sim, creates and keeps track of particles 
        and time steps the simulation.

        Parameters
        ----------

        particles: int, list

            If int then the enviroment creates that many particles and chooses random\n
            initial positions and velocities for each of them. If a list is passed in\n
            it should be a list of Particles. 

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

        Notes
        -----

        If n particles are initialized at random there isnitial position will be evenly distributed\n
        in the domain and the velocities will be initialized in any direction with unit magnitude.
        """
        # create enviroment parameters

        self.height: float = env_height
        self.width: float = env_width
        self.tolerance: float = tolerance
        self.sigma: float = sigma
        self.epsilon: float = epsilon

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
            (i, j) : [] for i in range(self.num_width_boxes) for j in range(self.num_height_boxes)
        }

        # list of all particles for ease of access for plotting and data analytics 
        self.particle_list = []

        # create particles in the enviroment
        if isinstance(particles, int):
        
            for i in range(particles):
                # TODO: look into initializtion of velocity
                # generate initial positions and velocities
                # TODO: Look into initializing postions randomly then 
                # doing gradient descent to find viable 
                init_pos = np.random.rand(2)*np.array([self.width, self.height])

                if init_pos[0] > 1 or init_pos[1] > 1:
                    print(init_pos)

                # TODO: current init velovity is zero idk if this is smart
                # currently going to make zero init velocity
                # init_vel = np.random.rand(2)*2 - 1
                # init_vel /= np.linalg.norm(init_vel)
                init_vel = np.zeros(2)

                particle = Particle(
                    index=i,
                    initial_pos=init_pos,
                    initial_velocity=init_vel,
                    sigma=self.sigma,
                    epsilon=self.epsilon,
                    env_width=self.width,
                    env_height=self.height,
                    grid_width=self.sub_width,
                    grid_height=self.sub_height,
                )

                # figure out index of the grid the particle belongs to and add to dict and list
                x_ind = int((init_pos[0]%self.width)//self.sub_width)
                y_ind = int((init_pos[1]%self.height)//self.sub_height)
                particle.grid_position = np.array([x_ind, y_ind])
                self.grid_node_dict[(x_ind, y_ind)].append(particle)
                self.particle_list.append(particle)

        
        elif isinstance(particles, list):
            
            for particle in particles:
                
                if not isinstance(particle, Particle):
                    raise ValueError('SimulationEnviroment expected a list or Parcitles')
                
                x_ind = int((particle.position[0]%self.width)//self.sub_width)
                y_ind = int((particle.position[1]%self.height)//self.sub_height)
                self.grid_node_dict[(x_ind, y_ind)].append(particle)
                self.particle_list.append(particle)


        else:

            raise ValueError('particles must be either an int or a list')
        

    def steepest_descent_initialization(self,
                                        gamma: float = 1e-3,
                                        num_iters: int = 1000
                                        ) -> None:

        """
        This will be a gradient descent initialization that is going to calculate gradient but 
        then update initial position in the direction of minima, this will hopefully converge
        to physically plausible initial positions. Updates with standard GD:

                                    x_new = x_old - gamma*Grad(U)

        Parameters
        ----------
        
        gamma: float
            
            GD step size
        
        num_iters: int

            number of iterations
        """

        for _ in range(num_iters):

            for prtcl in self.particle_list:

                self.calculate_particle_force(
                    particle=prtcl
                )

            for prtcl in self.particle_list:

                old_pos = prtcl.position
                new_pos = old_pos + gamma*prtcl.force

                new_x = new_pos[0]%self.width
                new_y = new_pos[1]%self.height
                prtcl.position = np.array([new_x, new_y])
                
                if prtcl.position[0] > 1 or prtcl.position[1] > 1:
                    print(prtcl.position)
                
                x_ind = int((prtcl.position[0]%self.width)//self.sub_width)
                y_ind = int((prtcl.position[1]%self.height)//self.sub_height)

                new_grid_idx = np.array([x_ind, y_ind])

                grid_key = (
                    int(prtcl.grid_position[0]), 
                    int(prtcl.grid_position[1])
                    )


                if not np.array_equal(new_grid_idx, prtcl.grid_position):

                    _ = self.grid_node_dict[grid_key].remove(prtcl)

                    self.grid_node_dict[(x_ind, y_ind)].append(prtcl)

                    prtcl.grid_position = new_grid_idx
            
            prtcl.clear_force()

    def calculate_particle_force(self,
                                 particle: Particle
                                 ) -> None:
        
        """
        Calculates the force acting on a given particle for each other particle in its own cell 
        or neighboring cells.

        Params
        ------

        particle: Particle

            the particle of which the force acting on it is to be calculated

        """

        grid_key = (int(particle.grid_position[0]), int(particle.grid_position[1]))

        # first calculate the force on the particle from particles in its own grid space
        for othr_prtcl in self.grid_node_dict[grid_key]:

            if particle is othr_prtcl:
                continue

            force = particle.calculate_force(
                other_pos=othr_prtcl.position
            )

            particle.increment_force(
                new_force=force
            )
        
        # Now we go through and calculate for each adjacent grid space

        # right no vertical movement
        grid_key = (
            int((particle.grid_position[0]+1)%self.num_width_boxes), 
            int(particle.grid_position[1])
            )

        for othr_prtcl in self.grid_node_dict[grid_key]:

            force = particle.calculate_force(
                other_pos=othr_prtcl.position
            )

            particle.increment_force(
                new_force=force
            )

        # left no vertical
        grid_key = (
            int((particle.grid_position[0]-1)%self.num_width_boxes), 
            int(particle.grid_position[1])
            )

        for othr_prtcl in self.grid_node_dict[grid_key]:

            force = particle.calculate_force(
                other_pos=othr_prtcl.position
            )

            particle.increment_force(
                new_force=force
            )

        # up no horizontal
        grid_key = (
            int(particle.grid_position[0]), 
            int((particle.grid_position[1]+1)%self.num_height_boxes)
            )

        for othr_prtcl in self.grid_node_dict[grid_key]:

            force = particle.calculate_force(
                other_pos=othr_prtcl.position
            )

            particle.increment_force(
                new_force=force
            )

        # down no horizontal
        grid_key = (
            int(particle.grid_position[0]), 
            int((particle.grid_position[1]-1)%self.num_height_boxes)
            )

        for othr_prtcl in self.grid_node_dict[grid_key]:

            force = particle.calculate_force(
                other_pos=othr_prtcl.position
            )

            particle.increment_force(
                new_force=force
            )

        # up right
        grid_key = (
            int((particle.grid_position[0]+1)%self.num_width_boxes), 
            int((particle.grid_position[1]+1)%self.num_height_boxes)
            )

        for othr_prtcl in self.grid_node_dict[grid_key]:

            force = particle.calculate_force(
                other_pos=othr_prtcl.position
            )

            particle.increment_force(
                new_force=force
            )

        # up left
        grid_key = (
            int((particle.grid_position[0]-1)%self.num_width_boxes), 
            int((particle.grid_position[1]+1)%self.num_height_boxes)
            )

        for othr_prtcl in self.grid_node_dict[grid_key]:

            force = particle.calculate_force(
                other_pos=othr_prtcl.position
            )

            particle.increment_force(
                new_force=force
            )

        # down right
        grid_key = (
            int((particle.grid_position[0]+1)%self.num_width_boxes), 
            int((particle.grid_position[1]-1)%self.num_height_boxes)
            )

        for othr_prtcl in self.grid_node_dict[grid_key]:

            force = particle.calculate_force(
                other_pos=othr_prtcl.position
            )

            particle.increment_force(
                new_force=force
            )

        # down left
        grid_key = (
            int((particle.grid_position[0]-1)%self.num_width_boxes), 
            int((particle.grid_position[1]-1)%self.num_height_boxes)
            )

        for othr_prtcl in self.grid_node_dict[grid_key]:

            force = particle.calculate_force(
                other_pos=othr_prtcl.position
            )

            particle.increment_force(
                new_force=force
            )

    def run_sim(self,
                duration: float,
                del_t: float
                ) -> None:
        """
        Main driver code of the simulation, at each time step loops through the particles
        in each particles own and neighbouring grid spaces, then updates there positions 
        and does the bookkeeping regarding new grid assignments

        Params
        ------

        duration: float

            How long to run the sim for

        del_t: float

            size of each time step
        
        Notes
        -----

       if del_t doesn't evenly divide duration the floor is taken for th enumber of timesteps
        """

        num_steps = math.floor(duration/del_t)

        for i in range(num_steps):
        
            # calculate force acting on each particle
            for prtcl in self.particle_list:

                self.calculate_particle_force(
                    particle=prtcl
                )
        

            # step each particle and figure out its grid position
            for prtcl in self.particle_list:

                grid_key = (
                    int(prtcl.grid_position[0]), 
                    int(prtcl.grid_position[1])
                    )

                _ = prtcl.step(
                    del_t=del_t
                )

                x_ind = int((prtcl.position[0]%self.width)//self.sub_width)
                y_ind = int((prtcl.position[1]%self.height)//self.sub_height)

                new_grid_idx = np.array([x_ind, y_ind])

                if not np.array_equal(new_grid_idx, prtcl.grid_position):

                    _ = self.grid_node_dict[grid_key].remove(prtcl)

                    self.grid_node_dict[(x_ind, y_ind)].append(prtcl)

                    prtcl.grid_position = new_grid_idx

                prtcl.clear_force()