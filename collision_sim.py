from typing import Generator, Any, Optional

import random
import math

import numpy as np
import simpy as sp

from particle_simulation import (calculate_circle_collision,
                                 calculate_square_collision,
                                 calculate_collision_point,
                                 calulate_reflection)



class ParticleEnviroment():
    def __init__(self,
                 num_particles: int,
                 run_time: float,
                 init_velocity: str = 'unit_horizontal',
                 circle_radius: float = 2,
                 box_length: float = 10):
        
        #box edges
        self.edges = [box_length/2, -box_length/2]
        self.box_length = box_length
        self.sigma = circle_radius
        self.run_time = run_time


        #dictionary of particles
        self.num_particles = num_particles
        self.particles = {}

        #simpy env
        self.env = sp.Environment()

        #cumulative collisions
        self.cumulative_collisions = 0

        #populate particles
        for i in range(num_particles):

            pos = np.random.uniform(low = -5, high=5, size=2)
            while np.linalg.norm(pos, ord = 2) <= self.sigma:
                pos = np.random.uniform(low = -5, high=5, size=2)

            if init_velocity == 'unit_horizontal':
            
                particle = {
                'particle_number'  : i,
                'velocity'         : np.array([1, 0]),
                'position'         : pos,
                'number_collisions': 0,
                'collision_times'  : [] 
                }

            if init_velocity == 'random':

                particle = {
                'particle_number'  : i,
                'velocity'         : np.random.rand(2),
                'position'         : pos,
                'number_collisions': 0,
                'collision_times'  : []                   
                }    

            self.particles[f'particle_{i}'] =  particle

    def _calculate_collision_time(self,
                                  particle: int
                                  ) -> Generator[Any, Any, Any]:
        
        particle = self.particles[f'particle_{particle}']
        while True:

            cumulative_wait_time = 0

            time = calculate_circle_collision(
                position = particle['position'],
                velocity = particle['velocity'],
                radius   = self.sigma
            )

            while time == False:

                square_time = calculate_square_collision(
                    position = particle['position'],
                    velocity = particle['velocity'],    
                    length = self.box_length               
                )

                collision_point = calculate_collision_point(
                    position = particle['position'],
                    velocity = particle['velocity'],
                    time_to_collision = square_time
                )

                cumulative_wait_time += square_time

                #collision with x
                if abs(collision_point[0]) == self.box_length/2:

                    new_position = collision_point - \
                        2*np.array([collision_point[0], 0])
                    
                #collision with y
                else:

                    new_position = collision_point - \
                        2*np.array([0, collision_point[1]])

                particle['position'] = new_position

                #recalculate wait time till collision with circle
                time = calculate_circle_collision(
                    position = particle['position'],
                    velocity = particle['velocity'],
                    radius   = self.sigma
                )
                
                if cumulative_wait_time > self.run_time:
                    break
            
            cumulative_wait_time += time

            if cumulative_wait_time < 0:
                print(particle['position'])
                print(np.linalg.norm(particle['position'], ord = 2))

            yield self.env.timeout(cumulative_wait_time)

            new_position = calculate_collision_point(
                position = particle['position'],
                velocity = particle['velocity'],
                time_to_collision = time
            )

            new_velocity = calulate_reflection(
                position = new_position,
                velocity = particle['velocity']
            )

            particle['position'] = new_position
            particle['velocity'] = new_velocity
            particle['number_collisions'] += 1
            particle['collision_times'].append(self.env.now)
            self.cumulative_collisions += 1

    def run_sim(self
                ) -> None:

        for i in range(self.num_particles):
            particle = self.particles[f'particle_{i}']

            #x-component of velocity is 0
            if particle['velocity'][0] == 0:
                
                #if x-position is within circle
                if abs(particle['position'][0]) < self.sigma:
                    self.env.process(self._calculate_collision_time(i))

                #will never intercept 
                else:
                    continue
            
            #y-component of velocity is 0
            elif particle['velocity'][1] == 0:

                #if y-position is within circle
                if abs(particle['position'][1]) < self.sigma:
                    self.env.process(self._calculate_collision_time(i))

                #will never intercept 
                else:
                    continue

            else:
                self.env.process(self._calculate_collision_time(i))

        self.env.run(until = self.run_time)

        print(f'Sim complete total collisions: {self.cumulative_collisions}')