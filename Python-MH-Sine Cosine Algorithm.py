############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Course: Metaheuristics
# Lesson: Sine Cosine Algorithm

# Citation: 
# PEREIRA, V. (2018). Project: Metaheuristic-Sine_Cosine_Algorithm, File: Python-MH-Sine Cosine Algorithm.py, GitHub repository: <https://github.com/Valdecy/Metaheuristic-Sine Cosine_Algorithm>

############################################################################

# Required Libraries
import pandas as pd
import numpy  as np
import math
import random
import os

# Function: Initialize Variables
def initial_position(solutions = 5, min_values = [-5,-5], max_values = [5,5]):
    position = pd.DataFrame(np.zeros((solutions, len(min_values))))
    position['Fitness'] = 0.0
    for i in range(0, solutions):
        for j in range(0, len(min_values)):
             position.iloc[i,j] = random.uniform(min_values[j], max_values[j])
        position.iloc[i,-1] = target_function(position.iloc[i,0:position.shape[1]-1])
    return position

# Function: Initialize Destination Position
def destination_position(dimension = 2):
    destination = pd.DataFrame(np.zeros((1, dimension)))
    destination['Fitness'] = 0.0
    for j in range(0, dimension):
        destination.iloc[0,j] = 0.0
    destination.iloc[0,-1] = target_function(destination.iloc[0,0:destination.shape[1]-1])
    return destination

# Function: Updtade Destination by Fitness
def update_destination(position, destination):
    updated_position = position.copy(deep = True)
    for i in range(0, position.shape[0]):
        if (updated_position.iloc[i,-1] < destination.iloc[0,-1]):
            for j in range(0, updated_position.shape[1]):
                destination.iloc[0,j] = updated_position.iloc[i,j]
    return destination

# Function: Updtade Position
def update_position(position, destination, r1 = 2, min_values = [-5,-5], max_values = [5,5]):
    updated_position = position.copy(deep = True)
    
    for i in range(0, updated_position.shape[0]):
        for j in range (0, len(min_values)):
           
            r2 = 2*math.pi*(int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1))
            r3 = 2*(int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1))
            r4 = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            
            if (r4 < 0.5):
                updated_position.iloc[i,j] = updated_position.iloc[i,j] + (r1*math.sin(r2)*abs(r3*destination.iloc[0,j] - updated_position.iloc[i,j]))
                if (updated_position.iloc[i,j] > max_values[j]):
                    updated_position.iloc[i,j] = max_values[j]
                elif (updated_position.iloc[i,j] < min_values[j]):
                    updated_position.iloc[i,j] = min_values[j] 
            else:
                updated_position.iloc[i,j] = updated_position.iloc[i,j] + (r1*math.cos(r2)*abs(r3*destination.iloc[0,j] - updated_position.iloc[i,j]))
                if (updated_position.iloc[i,j] > max_values[j]):
                    updated_position.iloc[i,j] = max_values[j]
                elif (updated_position.iloc[i,j] < min_values[j]):
                    updated_position.iloc[i,j] = min_values[j]        
        
        updated_position.iloc[i,-1] = target_function(updated_position.iloc[i,0:updated_position.shape[1]-1])
            
    return updated_position

# SCA Function
def sine_cosine_algorithm(solutions = 5, a_linear_component = 2,  min_values = [-5,-5], max_values = [5,5], iterations = 50):    
    count = 0
    position = initial_position(solutions = solutions, min_values = min_values, max_values = max_values)
    destination = destination_position(dimension = len(min_values))
    

    while (count <= iterations):
        
        print("Iteration = ", count, " f(x) = ", destination.iloc[destination['Fitness'].idxmin(),-1])
        r1 = a_linear_component - count*(a_linear_component/iterations)
                
        destination = update_destination(position, destination)
        position = update_position(position, destination, r1 = r1, min_values = min_values, max_values = max_values)
        
        count = count + 1 
        
    print(destination.iloc[destination['Fitness'].idxmin(),:].copy(deep = True))    
    return destination.iloc[destination['Fitness'].idxmin(),:].copy(deep = True)

######################## Part 1 - Usage ####################################

# Function to be Minimized. Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def target_function (variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

sca = sine_cosine_algorithm(solutions = 5, a_linear_component = 2,  min_values = [-5,-5], max_values = [5,5], iterations = 100)
