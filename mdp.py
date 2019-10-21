# -*- coding: utf-8 -*-
"""mdp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18ktsdsS5cuhqwIG0_xDKJb2UQkiNbc_Z
"""

import numpy as np
import random
import math

class State:
    def  __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.h = h
    
    def set_state(self, state):
        self.x = state.x
        self.y = state.y
        self.h = state.h
        
    def equals(self, new_state):
        if self.x == new_state.x and self.y == new_state.y and self.h == new_state.h:
            return True
        else:
            return False
        
    def print_state(self):
        print("State x,y,h is: " + str(self.x) + "," + str(self.y)+  "," + str(self.h))

#State is a class == x,y,h

class Matrix:
    # our complete grid 
    # includes dimensions, and structure
    # includes movement 
    # includes transition probability function
    def __init__(self, p_error, state, length=8, width=8):
        self.length = length
        self.width = width
        self.p_error = p_error
        self.state = state
        self.vertical_positive = [11,0,1]
        self.vertical_negative = [5,6,7]
        self.horizontal_positive = [2,3,4]
        self.horizontal_negative = [10,9,8]
        self.reward_dict = {} #dictionary
        state_space = []
        for i in range(self.length):
          for j in range(self.width):
            for h in range(12):
              s = State(i,j,h)
              state_space.append(s)
        self.statelist=state_space
       
    def set_state(self, new_state):
        self.state = new_state

    def pre_rotation(self):
        # returns pre rotation change -1 or 0 or 1
        v = random.random()
        #print("The pre rotation probability: " + str(v))
        if v < self.p_error:
            return -1
        elif v >= self.p_error and v < 2*self.p_error:
            return 1
        else:
            return 0
    
    def test_move(self, action, error):
        # no direct use... just for calculating probabilities of a transition
        h = (self.state.h + error) % 12
        multiplier = 1
        if h in self.horizontal_negative or h in self.vertical_negative:
            multiplier = -1
        new_x = self.state.x
        new_y = self.state.y
        if h in self.horizontal_negative or h in self.horizontal_positive:
            temp_x = self.state.x + (multiplier*action[0])
            if 0 <= temp_x <= self.length - 1:
                new_x += (multiplier*action[0])
        else:
            temp_y = self.state.y + (multiplier*action[0])
            if 0 <= temp_y <= self.width - 1:
                new_y += (multiplier*action[0])
        new_h = (h + action[1]) % 12
        return State(new_x, new_y, new_h)

    def probability_new_state(self, input_action, new_state):
        #answer to ques: 1)c)(using test_move)
        #probability function (transfer function)
        if input_action[0] == 0:
            if self.state.equals(new_state):
                return 1
            else:
                return 0
        else:
            probability = 0
            errors = [-1, 0, 1]
            for e in errors:
                result_state = self.test_move(input_action, e)
                if new_state.equals(result_state):
                    #if new_x == result_state[0] and new_y == result_state[1] and new_h == result_state[2]:
                    if e == 1 or e == -1:
                        probability += self.p_error
                    else:
                        probability += (1 - 2*self.p_error)
            return probability
        
    def move(self, action):
        #moves from m.state and takes action (includes randomness m.p_error)
        #ans to 1)d)
        h = (self.state.h + self.pre_rotation()) % 12
        multiplier = 1
        if h in self.horizontal_negative or h in self.vertical_negative:
            multiplier = -1
        new_x = self.state.x
        new_y = self.state.y
        if h in self.horizontal_negative or h in self.horizontal_positive:
            temp_x = self.state.x + (multiplier*action[0])
            if 0 <= temp_x <= self.length - 1:
                new_x += (multiplier*action[0])
        else:
            temp_y = self.state.y + (multiplier*action[0])
            if 0 <= temp_y <= self.width - 1:
                new_y += (multiplier*action[0])
        new_h = (h + action[1]) % 12
        return State(new_x, new_y, new_h)

    def get_next_state_probabilities(self, initial_state, action):
        #returns list of tuples (next_state, prob of that state, reward of this transition) for movement from a state given action
        #uses p_error
        return_value = []
        self.set_state(initial_state)
        new_states = []
        x,y,h = initial_state.x, initial_state.y, initial_state.h
        positions = [(x,y), (x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        new_positions = []
        for p in positions:
            if 0 <= p[0] <= self.length - 1 and 0 <= p[1] <= self.width - 1:
                new_positions.append((p[0],p[1]))
        new_headings = [(h-2)%12, (h-1)%12, h, (h+1)%12, (h+2)%12]
        for p in new_positions:
            for o in new_headings:
                new_states.append(State(p[0], p[1], o))
        probabilities = []
        for s in new_states:
            prob = self.probability_new_state(action, s)
            return_value.append((s, prob, self.get_reward(s)))
        return return_value
            
    def get_reward(self, input_state):
        x,y = input_state.x, input_state.y
        return self.reward_dict[(x,y)]

#so define m = p_error, inital state(x ,y, h) 
# then m.reward_dict= reward dictionary and you're set

#This part deals with Question 2 and setting the reward map.

goal_state = State(5,6,None)
def make_reward_map():
    d = {}
    for i in range(8):
        for j in range(8):
            if i == 7 or j == 7:
                d[(i,j)] = -100
            elif i == 0 or j == 0:
                d[(i,j)] = -100
            elif i == goal_state.x and j == goal_state.y:
                d[(i,j)] = 1
            else:
                d[(i,j)] = 0
    d[(3,6)] = -10
    d[(3,5)] = -10
    d[(3,4)] = -10
    return d

#you're set

#Question 3
#Algorithm for Part 3 initial question. We are using Manhattan distance as the metric. The algorithm just 
#returns the action which corresponds to the lowest Manhattan distance out of 6 possible actions. Unless the agent
#is in the goal state, it must move.

def manhattan_distance(current_state):
    return abs(current_state.x - goal_state.x) + abs(current_state.y - goal_state.y)

def initial_policy(current_state):
    #gives initial policy as the action that minimizes the distance left
    if current_state.x == goal_state.x and current_state.y == goal_state.y:
        return [0,0]
    actions = ([1,1],[1,0],[1,-1],[-1,1],[-1,0],[-1,-1])
    distances = []
    for a in actions:
        m.set_state(current_state)
        new_state = m.test_move(a, 0)
        distances.append(manhattan_distance(new_state))
    index = distances.index(min(distances))
    return actions[index]   

def plot_trajectory(initial_state, policy_dict):
    #plots movement of state from initial under policy_dict
    #returns list of states traversed
    s = initial_state
    m.set_state(initial_state)
    states = []
    steps = 100
    while steps > 0:
        if s.x == goal_state.x and s.y == goal_state.y:
            print("Found goal!")
            break
        else:
            action = policy_dict[(s.x,s.y,s.h)]
            s = m.move(action)
            m.set_state(s)
            states.append(s)
            steps -= 1
    return states

#Value iteration Question 4
import copy

def value_distance(V1, V2):
    diff = 0
    for k in V1:
        diff += abs(V1[k] - V2[k])
    return diff

def value_iteration(gamma, p_error):
    m.p_error = p_error
    V = {}
    for s in m.statelist:
        V[(s.x,s.y,s.h)]=0
    step = 0
    while step < 1000:
        V_prev = copy.deepcopy(V)
        for s in m.statelist:
            actions = ([1,1],[1,0],[1,-1],[-1,1],[-1,0],[-1,-1],[0,0])
            action_score = []
            for a in actions:
                score = np.sum([p*(r + gamma*V_prev[(n_s.x, n_s.y, n_s.h)]) for n_s, p, r in m.get_next_state_probabilities(s, a)])
                action_score.append(score)
            max_score=max(action_score)
            V[(s.x, s.y, s.h)] = max_score
        print(value_distance(V_prev, V))
        if abs(value_distance(V_prev, V)) < 0.001:
            return V, V_prev
        step += 1
        print(step)

def policy_from_value(V, gamma):
    policy={}    
    for s in m.statelist:
        actions = ([1,1],[1,0],[1,-1],[-1,1],[-1,0],[-1,-1],[0,0])
        action_score = []
        for a in actions:
            score = np.sum([p*(r + gamma*V[(n_s.x, n_s.y, n_s.h)]) for n_s, p, r in m.get_next_state_probabilities(s, a)])
            action_score.append(score)
        max_index = action_score.index(max(action_score))
        best_action = actions[max_index]
        policy[(s.x,s.y,s.h)] = best_action
    return policy

def policy_evaluation(policy, gamma):
    
    V = {}
    for s in m.statelist:
      V[(s.x,s.y,s.h)]=0
    step = 0
    while step < 1000:
        V_prev = copy.deepcopy(V)
        for s in m.statelist:
            action = policy[(s.x,s.y,s.h)]
            V[(s.x,s.y,s.h)] = np.sum([p*(r + gamma*V_prev[(n_s.x, n_s.y, n_s.h)]) for n_s, p, r in m.get_next_state_probabilities(s, action)])
        #print(value_distance(V_prev, V))
        if abs(value_distance(V_prev, V)) < 0.001:
            return V, V_prev
        step += 1
        #print(step)

def policy_difference(P1, P2):
    for k in P1:
        a1 = P1[k]
        a2 = P2[k]
        if a1[0] == a2[0] and a1[1] == a2[1]:
            continue
        else:
            return False
    return True

def policy_iteration(init_policy, gamma, p_error):
    m.p_error=p_error
    policy = copy.deepcopy(init_policy)
    step = 0
    while True:
        V,_ = policy_evaluation(policy, gamma)
        #print(len(list(V.keys())))
        #print("Done with V")
        policy_new = policy_from_value(V, gamma)
        #print("Finsihed getting new policy")
        if policy_difference(policy, policy_new):
            return policy
        else:
            policy = copy.deepcopy(policy_new)
            step += 1
            print(step)

''' definitions over: lets solve problems '''


# first define m
p_error=0
state=State(0,0,0) #initial state
m=Matrix(p_error,state) 
m.reward_dict = make_reward_map() 
#we're set

init_policy = {}

for s in m.statelist:
    a = initial_policy(s)
    init_policy[(s.x,s.y,s.h)] = a

#we have initial policy

states = plot_trajectory(State(3,3,0), init_policy)
for s in states:
    s.print_state()
    
V, _ = value_iteration(0.9, 0.25)    
trajectory = plot_trajectory(State(1,6,6), policy_from_value(V, 0.9))       
for t in trajectory:
    t.print_state()
    

policy = policy_iteration(init_policy, 0.9, 0.25)
trajectory = plot_trajectory(State(1,6,6), policy)       
for t in trajectory:
    t.print_state()

