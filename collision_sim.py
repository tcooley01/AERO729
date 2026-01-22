import numpy as np
import simpy
import random as rand
import math
import particle_simulator



class ParticleEnviroment():
    def __init__(self,
                 num_particles,
                 init_position,
                 init_velocity,
                 circle_radius,
                 box_length):
        
        #box edges
        self.edges = [box_length/2, -box_length/2]
        self.sigma = circle_radius

        #dictionary of particles
        self.particles = {}

        #simpy env
        self.env = simpy.Enviroment

        for i in range(num_particles):

            if init_velocity == 'unithorizontal'
            
                pos = np.random(1, 2)
                while np.linalg.norm(pos, ord = 2) <= self.sigma:
                    pos = np.random(1, 2)

                particle = {
                'particle_number'  : i,
                'velocity'         : np.array([1, 0]),
                'position'         : pos,
                'number_collisions' : 0
                }


            self.particles.update(f'particle_{i}', particle)

