from multiagent.environment import MultiAgentEnv
from multiagent.scenarios.ev import Scenario
import multiagent.interact as intera

import numpy as np
from pyglet.window import key
import random

# individual agent policy
class Policy(object):
    def __init__(self):
        pass
    def action(self, obs):
        raise NotImplementedError()

# interactive policy based on keyboard input
# hard-coded to deal only with movement, not communication
class InteractivePolicy(Policy):
    def __init__(self, env, agent_index):
        super(InteractivePolicy, self).__init__()
        self.env = env
        self.move = [False for i in range(4)]
        self.comm = [False for i in range(env.world.dim_c)]

    def action(self, obs):
        # ignore observation and just act based on keyboard events
        length=obs.ndim
        max_edge=1.5
        ################policy for the agent
        if length==1:
            prey_x=obs[2]
            prey_y=obs[3]
            x_pos=obs[0]
            y_pos=obs[1]

            if self.env.discrete_action_input:
                action=[]
                ########
                #add the policy
                ########
                u=intera.action_tranfer(action)
                if u == 1 and x_pos >= max_edge:
                    u = 0
                if u == 2 and x_pos <= -max_edge:
                    u = 0
                if u == 3 and y_pos >= max_edge:
                    u = 0
                if u == 4 and y_pos <= -max_edge:
                    u = 0
            else:
                action = []
                ########
                # add the policy
                ########
                u = intera.action_tranfer(action)
                if u[1] > 0 and x_pos >= max_edge:
                    u[1] = 0
                if u[2] > 0 and x_pos <= -max_edge:
                    u[2] = 0
                if u[3] > 0 and y_pos >= max_edge:
                    u[3] = 0
                if u[4] > 0 and y_pos <= -max_edge:
                    u[4] = 0
        ###############################################################
        else:
            prey_x = obs[0,2]
            prey_y = obs[0,3]
            gravity_x = 0
            gravity_y = 0
            for i in range(0,length):
                gravity_x += obs[i, 0]
                gravity_y += obs[i, 1]
            gravity_x = gravity_x / length
            gravity_y = gravity_y / length
            proba = random.random()
            if proba > 0.8:
                if self.env.discrete_action_input:
                    random_pick = random.randint(1, 5)
                    u = random_pick - 1
                    if u == 1 and prey_x >= max_edge:
                        u = 0
                    if u == 2 and prey_x <= -max_edge:
                        u = 0
                    if u == 3 and prey_y >= max_edge:
                        u = 0
                    if u == 4 and prey_y <= -max_edge:
                        u = 0

                else:
                    u = np.zeros(5)  # 5-d because of no-move action
                    if random.random() < 0.5: u[1] += 1.0
                    if random.random() < 0.5: u[2] += 1.0
                    if random.random() < 0.5: u[3] += 1.0
                    if random.random() < 0.5: u[4] += 1.0
                    if sum(u) == 0:
                        u[0] += 1.0
                    if u[1] > 0 and prey_x >= max_edge:
                        u[1] = 0
                    if u[2] > 0 and prey_x <= -max_edge:
                        u[2] = 0
                    if u[3] > 0 and prey_y >= max_edge:
                        u[3] = 0
                    if u[4] > 0 and prey_y <= -max_edge:
                        u[4] = 0
            else:
                x = gravity_x - prey_x
                y = gravity_y - prey_y
                if self.env.discrete_action_input:
                    u = 0
                    if abs(x) > abs(y):
                        if x > 0: u = 2
                        if x < 0: u = 1
                    if abs(y) > abs(x):
                        if y > 0: u = 4
                        if y < 0: u = 3
                    if u == 1 and prey_x >= max_edge:
                        u = 0
                    if u == 2 and prey_x <= -max_edge:
                        u = 0
                    if u == 3 and prey_y >= max_edge:
                        u = 0
                    if u == 4 and prey_y <= -max_edge:
                        u = 0

                else:
                    u = np.zeros(5)
                    if x < 0: u[1] += 1
                    if x > 0: u[2] += 1
                    if y > 0: u[4] += 1
                    if y < 0: u[3] += 1
                    if sum(u) == 0:
                        u[0] += 1.0
                    if u[1] > 0 and prey_x >= max_edge:
                        u[1] = 0
                    if u[2] > 0 and prey_x <= -max_edge:
                        u[2] = 0
                    if u[3] > 0 and prey_y >= max_edge:
                        u[3] = 0
                    if u[4] > 0 and prey_y <= -max_edge:
                        u[4] = 0

        return np.concatenate([u, np.zeros(self.env.world.dim_c)])



