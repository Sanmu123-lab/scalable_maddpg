import os, sys
import math
import numpy as np

sys.path.insert(1,os.path.join(sys.path[0],'..'))
from pray_policy import Pray

from multiagent.environment import MultiAgentEnv
import multiagent.scenarios as scenarios

v_test=0.02
R_ad=0.075
R_prey=0.05

#max_edge=0.2

class Environ:
    def __init__(self,num_agents,max_edge):
        self.num_agents = num_agents
        self.max_edge=max_edge
        self.env, \
        self.current_obs \
            = self.create_env(num_agents)

        self.pray = Pray(max_edge)

    def re_create_env(self, num_agents):
        self.num_agents=num_agents
        self.env, \
        self.current_obs \
            = self.create_env(num_agents)

    def create_env(self, num_agents):
        scenario = scenarios.load('ev.py').Scenario(num_agents,self.max_edge)
        world = scenario.make_world()
        env = MultiAgentEnv(world, scenario.reset_world, scenario.reward, scenario.observation, info_callback=None,
                            shared_viewer=False)
        obs_n = env.reset()
        return env, obs_n[0]

    def render(self):
        self.env.render()

    def step(self,act_n):
        agent_actions = self.action_transfer(act_n,self.current_obs)
        pray_action = self.pray.action(self.current_obs)
        actions = np.vstack((agent_actions,pray_action))
        #print(actions)
        obs_n, reward_n, done_n, _ = self.env.step(actions)
        #agents_obs = obs_n[0][:self.num_agents, :]
        self.current_obs = obs_n[0]
        # ########################
        # observation=np.zeros([self.num_agents+1,4])
        # for ii in range(self.num_agents):
        #     for jj in range(4):
        #         if self.current_obs[ii,jj]>self.max_edge:
        #             observation[ii,jj]=self.current_obs[ii,jj]-self.max_edge
        #         if self.current_obs[ii,jj]<-self.max_edge:
        #             observation[ii,jj]=self.current_obs[ii,jj]+self.max_edge
        # #########################
        # agents_obs = observation[:self.num_agents, :]
        # for ii in range(self.num_agents+1):
        #     obs_n[ii]=observation

        Reset_pos=False

        done = False
        for ii in range(self.num_agents):
            x_dis=self.current_obs[ii,0]-self.current_obs[ii,2]
            y_dis=self.current_obs[ii,1]-self.current_obs[ii,3]
            dis=np.sqrt(np.square(x_dis)+np.square(y_dis))
            if dis<=R_ad+R_prey:
                done= True
            if abs(self.current_obs[ii,0])>self.max_edge or abs(self.current_obs[ii,1])>self.max_edge:
                if Reset_pos:
                    new_pos=np.random.uniform(-self.max_edge, +self.max_edge, 2)
                    self.current_obs[ii,0]=new_pos[0]
                    self.current_obs[ii, 1] = new_pos[1]
                else:
                    done=True
        agents_obs=self.current_obs[:self.num_agents, :]
        return agents_obs, np.squeeze(reward_n[:self.num_agents]), done

    def reset(self):
        return self.env.reset()[0]


    def action_transfer(self, action, current_obs):
        radio=1
        u = np.zeros((self.num_agents, 5))
        for i in range(self.num_agents):
            movable = 1
            #angle = action[i, 1]
            angle=action[i]
            if movable <= -1:
                u[i,0] += 1
            if movable > -1:
                direction_x = math.cos(angle * math.pi)
                direction_y = math.sin(angle * math.pi)
                # x=current_obs[i,0]
                # y = current_obs[i, 1]
                #
                if direction_x > 0:
                     u[i, 1] += direction_x
                if direction_x < 0:
                     u[i, 2] += -direction_x
                if direction_y > 0:
                     u[i, 3] += direction_y
                if direction_y < 0:
                     u[i, 4] += -direction_y
                # if u[i,1] > 0 and x+v_test*direction_x>= radio*self.max_edge:
                #     u[i,1] = (radio*self.max_edge-x)/v_test
                # if u[i,2] > 0 and x+v_test*direction_x <= -radio*self.max_edge:
                #    u[i,2] = -(radio*self.max_edge-x)/v_test
                # if u[i,3] > 0 and y+v_test*direction_y >= radio*self.max_edge:
                #     u[i,3] = (radio*self.max_edge-y)/v_test
                # if u[i,4] > 0 and y+v_test*direction_y <= -radio*self.max_edge:
                #    u[i,4] = -(radio*self.max_edge-y)/v_test
        return u

    def predator(self):
        action=np.zeros([self.num_agents,1])
        observation=self.current_obs
        pra=np.random.random()
        for ii in range(self.num_agents):
            if pra>0.2:
                action[ii,0]=2*np.random.random()-1
            else:
                x=-observation[ii,0]+observation[ii,2]
                y=-observation[ii,1]+observation[ii,3]
                action[ii,0]=np.arctan2(y,x)
        return action


