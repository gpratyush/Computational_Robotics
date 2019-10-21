# -*- coding: utf-8 -*-
'''
                            Lab 1
                        Computational Robotics
                        Code by Rohan Dutta, Pratyush Garg 
'''
import numpy as np
import random

#Boundary
L_max = 7
W_max = 7

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

def error_simulation(current_state,action, pe):
  next_state=myState(current_state.x,current_state.y,current_state.o)
  outcome = np.random.choice(['1', '-1', '0'], 1,p = [pe, pe, 1-2*pe])
  if int(outcome)!=0:
    print("ERROR")
  next_state.o = np.mod(next_state.o + int(outcome),12)
  update_position(next_state,action)
  update_orientation(next_state,action)        

  return next_state

def reward_calculation(current_state):
    if (current_state.x ==0) or (current_state.x ==L_max) or (current_state.y ==0) or (current_state.y ==W_max):
        reward = -100
    elif (current_state.x==3) & (np.absolute(5-current_state.y)<=1):
        reward = -10
    elif (current_state.x==5) & (current_state.y==6):
        reward = 1
    else:
        reward =0
    return reward

def pe_s(current_state,action,next_state,pe):
  update_position(current_state,action)        
  update_orientation(current_state,action)


  if (next_state.x==current_state.x)and(next_state.y==current_state.y)and(next_state.o==current_state.o):
    return 1-2*pe
  else:
    return pe

print(current_state.x,current_state.y,current_state.o)
next_state = error_simulation(current_state,action,0.1)
print(current_state.x,current_state.y,current_state.o)

print(next_state.x,next_state.y,next_state.o)
print(pe_s(current_state,action,next_state,0.1))

def initial_policy(current_state):
  action_list =[]
  error_list =[]
  move_or_not=1
  if (current_state.x==5)and(current_state.y==6):
    move_or_not=0
    action=myAction(0,0,0)
  else:
    for forward_or_not in [1,-1]:
      for left_or_not in [1,0,-1]:
        action = myAction(1, forward_or_not, left_or_not)
        next_state = error_simulation(current_state,action, 0)
        pos_error=np.absolute(5-next_state.x)+np.absolute(6-next_state.y)
        action_list.append([move_or_not, forward_or_not, left_or_not])
        error_list.append(pos_error)
    min_index = error_list.index(min(error_list))
    action=myAction(1,action_list[min_index][1],action_list[min_index][2])
  return action

def plot_generator(current_state,pe):
  state_list =[]
  state_list.append([current_state.x,current_state.y,current_state.o])
  while not((current_state.x==5)and(current_state.y==6)):
    a =initial_policy(current_state)
    next_state = error_simulation(current_state,a, pe)
    current_state.x = next_state.x
    current_state.y = next_state.y
    current_state.o = next_state.o
    state_list.append([current_state.x,current_state.y,current_state.o])
  return state_list

current_state=myState(0,5,6)
tr = plot_generator(current_state,0.1)

def policy_evaluation(current_state,gamma,pe):
  t=0
  v=0
  while current_state!=final_state:
    r = reward_calculation(current_state)
    action = initial_policy(current_state)
    v = v + np.power(gamma,t)*r
    t=t+1
    next_state = error_simulation(current_state,action,pe)




#