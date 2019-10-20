
'''

                            Lab 1
                        Computational Robotics
                        Code by Rohan Dutta 
'''

import numpy as np
import random



#Boundary
L_max = 8
W_max = 8

#State Variables
L = 0
W = 0
o = 1

#Action Variables
move_or_not = 1 #Takes values 0 or 1
forward_or_not = -1 #Takes values 1 or -1
left_or_not = -1 #Takes values 1,0,-1

L_array = np.arange(0,L,1)
W_array = np.arange(0,W,1)
o_array = np.arange(0,12,1)

class myState():
    def __init__(self, x, y, o):
        self.x = x #Length
        self.y = y #Width
        self.o = o #Orientation
        
current_state = myState(L,W,o)
        
class myAction():
    def __init__(self, move_or_not, forward_or_not, left_or_not):
        """
        move_or_not: Can take values 0 or 1, 0- Does not move or turn, 1 - Moves and orients
        forward_or_not: Can take values 1 (forward), -1 (backward)
        left_or_not: Can take values 1(left),-1(right),0(No turn)
        """
        self.move = move_or_not
        if self.move ==0:
            self.horizontal = 0
            self.turn = 0
        else:
            self.horizontal= forward_or_not
            self.turn = left_or_not
            
action = myAction(move_or_not, forward_or_not, left_or_not)
        

def update_orientation(current_state,action):
    current_state.o= np.mod(current_state.o+action.turn,12)


def update_position(current_state,action):
    if np.absolute(current_state.o-3)<=1:
        current_state.x = current_state.x + action.horizontal
    elif np.absolute(current_state.o-9)<=1:
        current_state.x = current_state.x - action.horizontal
    elif np.absolute(current_state.o-6)<=1:
        current_state.y = current_state.y - action.horizontal
    else:
        current_state.y = current_state.y + action.horizontal
        
    #Boundary Conditions
    if current_state.x > L_max:
        current_state.x = L_max
    elif current_state.x < 0:
        current_state.x = 0
    if current_state.y > W_max:
        current_state.y = W_max
    elif current_state.y < 0:
        current_state.y = 0

        
        
        
print(current_state.x)
print(current_state.y)
print(current_state.o)
update_position(current_state,action)        
update_orientation(current_state,action)
print(current_state.x)
print(current_state.y)
print(current_state.o)

def error_simulation(current_state,action):
    pe= 0.7
    print(random.choices(movement=['1', '-1', '0'], weights=[pe, pe, 1-2*pe], k=10))
    
    if action.move ==1:
        if error:
            update_orientation(current_state,action)        
            update_position(current_state,action)
        else:
            update_position(current_state,action)        
            update_orientation(current_state,action)
            
def reward_calculation(current_state):
        if (current_state.x ==0) || (current_state.x ==L_max) || (current_state.y ==0) || (current_state.y ==W_max):
            reward = -100
        elif (current_state.x==3) & (np.absolute(5-current_state.y)<=1):
            reward = -10
        elif (current_state.x==5) & (current_state.y==6):
            reward = 1
        else:
            reward =0
        return reward
            
