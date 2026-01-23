# -*- coding: utf-8 -*-
"""
University of Michigan HW 1 

Created on Wed Jan 21 10:46:29 2026

@author: 343684
"""

import numpy as np 
import matplotlib.pyplot as plt
import scipy as sp 
import random
from matplotlib.patches import Circle
import math


class particle:
    def __init__(self, color: str, dir_color: str, velocity_x: int,velocity_y: int, direction: int, collisions: list, x: int, y:int):
       self.color = color
       self.velocity_x = velocity_x
       self.velocity_y = velocity_y
       self.direction = direction
       self.collisions = [collisions]
       self.x = x
       self.y = y
       self.dir_color = dir_color
       
       
    def display(self):
        print("color = " + self.color, 
              "direction color = " + self.dir_color,
              "x velocity = " + str(self.velocity_x),
              "y velocity = " +str(self.velocity_y),
              "direction = " +str(self.direction),
              "collisions = " +str(self.collisions),
              "x = " + str(self.x),
              "y = " + str(self.y))
        
    def report(self):
        if len(self.collisions) >= 1:
            for event in self.collisions:
                if event > 0:
                    print(event)
           
        
    def plot(self):
        plt.plot(self.x,self.y,self.color)
        plt.annotate('',
                     xy=(self.x + self.velocity_x, self.y + self.velocity_y),
                     xytext=(self.x,self.y),
                     arrowprops = dict(
                         facecolor = self.dir_color,
                         shrink = 0.005,
                         width = 2,
                         headwidth = 7
                         ))
        
    def move(self):
        x = self.x + self.velocity_x
        y = self.y + self.velocity_y
        if x > 100:
            self.x = -100+(-100 + x)
        elif x < -100:
            self.x = x + 200
        else:
            self.x = x 
        if y > 100:
            self.y = -100+(-100 + y)
        elif y < -100:
            self.y = y + 200
        else:
            self.y = y
            
    def collision_detection(self):
        pos = math.sqrt((self.x + self.velocity_x)**2 + (self.y + self.velocity_y)**2)
        if pos <= circ_r:
            print("collision imminent")
            return('colided')
        
    def change(self):
        self.color = "ro"
        self.dir_color = "red"
    
    
    
    def colide_move(self):
        a = (self.velocity_x**2) + (self.velocity_y**2)
        b = 2*((self.velocity_x*self.x) + (self.velocity_y*self.y))
        c = (self.x**2)+(self.y**2)-(circ_r**2)
        p = [a,b,c]
        collision_time = 0
        if np.roots(p)[0] > np.roots(p)[1]:
            collision_time = np.roots(p)[1] 
        else:
            collision_time = np.roots(p)[0]
        col_x = self.x + (collision_time*self.velocity_x)
        col_y = self.y + (collision_time*self.velocity_y)
        ax.plot(col_x,col_y, "go")
        
        # find the normal line  
        norm_line_y=[]
        norm_line_x=[]
        for x in range(-100,100):
            norm_line_x.append(x)
            y= (col_y/col_x)*x
            norm_line_y.append(y)
        #ax.plot(norm_line_x,norm_line_y)
        
        
        #find the tangent 
        m1 = (col_y/col_x)
        m = -(1/m1)
        tan_line_x = []
        tan_line_y = []
        for x in range(-100,100):
            tan_line_x.append(x)
            b = -(m*col_x)+col_y
            y = m*x + b
            tan_line_y.append(y)
        #ax.plot(tan_line_x,tan_line_y)
        
      
       
        
        #calculate distance to collision
        dist_x = (self.x - col_x)
        dist_y = (self.y - col_y)
        distance_to_collision = math.sqrt(dist_x**2 + dist_y**2)
        
        col_pos_array = np.array([col_x,col_y])
        
        p = math.atan(col_y/col_x)
        unit_notmal_vector = np.array([math.cos(p),math.sin(p)])
        velocity_array = np.array([self.velocity_x,self.velocity_y])
        v_new = velocity_array-2*(np.dot(velocity_array,unit_notmal_vector))*unit_notmal_vector
        new_pos = (1-collision_time)*v_new + col_pos_array
        
        self.velocity_x = v_new[0]
        self.velocity_y = v_new[1]
        self.x = new_pos[0]
        self.y = new_pos[1]
        
       
        
        
        
        
        
    def record_collision_event(self):
        a = (self.velocity_x**2) + (self.velocity_y**2)
        b = 2*((self.velocity_x*self.x) + (self.velocity_y*self.y))
        c = (self.x**2)+(self.y**2)-circ_r**2
        p = [a,b,c]
        if np.roots(p)[0] > np.roots(p)[1]:
            self.collisions.append(time_stamp + np.roots(p)[1]+1)
            return(np.roots(p)[1])
        else:
            self.collisions.append(time_stamp + np.roots(p)[0]+1)
            return(np.roots(p)[0])
        
    
            

# set up the plane and place some particles in it and intilize a particle list

d2r = np.pi/180
circ_r = 20
partickles = []

n = 20                                 ############# DEFINE PARTICLE NUMBER 
for x in range(n):
    color = "bo"
    dir_color = "blue"
    velocity_x = random.randint(-10,10)
    velocity_y = random.randint(-10,10)
    direction = random.randint(0,360)
    collisions = 0
    x = random.randint(-99,99)
    y = random.randint(-99,99)
    partickles.append(particle(color,dir_color,velocity_x,velocity_y,direction,collisions,x,y))




x = True
time_stamp = 0

while x == True:
    fig, ax = plt.subplots(figsize = (20,20))
    circle = Circle((0,0), radius=circ_r, edgecolor='black', facecolor='black')
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.add_artist(circle)

    

    
   
    inp = input("time step: " + str(time_stamp))
    
    if inp != str(1):
        
        for particles in partickles:
            particles.plot()
            if particles.collision_detection() == "colided":
                particles.record_collision_event()
                particles.change()
                particles.colide_move()
              
                
            else: 
                particles.move()
            
        plt.show()
        time_stamp += 1
            
            
    elif inp == str(1):
        for particles in partickles:
            particles.report()
        x =  False
         








'''
 newx = (dist_x * np.cos(p)) + (dist_y * np.sin(p))
 newy = (-1*dist_x*np.sin(p)) + (dist_y * np.cos(p))
 #theta = math.atan(newy/newx)
 #theta_deg = theta/d2r
 #print("x:" + str(dist_x), "y:" + str(dist_y), "H:" + str(distance_to_collision),"theta:" + str(theta_deg))
 #print('Self x: %.2f  Self y: %.2f \nColl x: %.2f Col y: %.2f'%(self.x,self.y,col_x,col_y))
 #print('delta x: %.3f delta y %.3f \n H: %.3f \n theta: %.3f'%(dist_x,dist_y,distance_to_collision,theta_deg))
 r = np.sqrt(self.velocity_x**2 + self.velocity_y**2) - distance_to_collision
 #x3p = r*np.sin(-theta)
 #y3p = r*np.cos(-theta)

 x3p = -1*newx
 y3p = newy
 x3 = col_x + x3p*np.cos(p)-y3p*np.sin(p)
 y3 = col_y + x3p*np.sin(p) + y3p * np.cos(p)
 
 print(x3,y3,r)
 
 self.x = x3
 self.y = y3 
 '''





