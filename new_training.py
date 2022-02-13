import numpy as np
import gym
from stable_baselines3 import PPO
# from stable_baselines3.common import make_vec_env
from openDSSenv34 import openDSSenv34
#import json
#import datetime as dt
#import torch
from stable_baselines3.common.utils import set_random_seed
from feedforwardPolicy import *
from stable_baselines3 import A2C
from CustomPolicies import ActorCriticGCAPSPolicy


import pickle
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv


class CustomNN(BaseFeaturesExtractor):

    """
    :param observation_space: (gym.Space)
    :param features_dim: (int) Number of features extracted.
        This corresponds to the number of unit for the last layer.
    """

    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 256):
        from torch import nn
        super(CustomNN, self).__init__(observation_space, features_dim)


        n_flatten = 1521
        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU())

    def forward(self, observations):

        if len(observations["loss"].shape) == 1:
            data_loss = observations["loss"][:, None]
        else:
            data_loss = observations["loss"]

        statevec = np.concatenate((data_loss,
                                    observations['NodeFeat(BusVoltage)'].flatten(1,2),
                                    observations['EdgeFeat(branchflow)'][:,:],
                                    observations['Adjacency'].flatten(1,2)), axis=1)
        statevec = np.array(statevec)
        statevec = th.from_numpy(statevec)
        # print(observations['loss'])
        # print(observations['NodeFeat(BusVoltage)'])
        # print(observations['EdgeFeat(branchflow)'])
        # print(observations['Adjacency'])
        #print(np.shape(statevec))
        
        # loss = th.from_numpy(np.array([observations['loss']]))
        # nodefeat = th.from_numpy(observations['NodeFeat(BusVoltage)'])
        # edgefeat = th.from_numpy(observations['EdgeFeat(branchflow)'])
        # adjc = th.from_numpy(observations['Adjacency'])
  
        #loss = th.tensor([[observations['loss']]], dtype=th.float32)
        # nodefeat = observations['NodeFeat(BusVoltage)']
        # edgefeat = observations['EdgeFeat(branchflow)']
        # adjc = observations['Adjacency']
        
        # #loss = th.reshape(loss,(1,1))
        # nodefeat = th.reshape(nodefeat,(1,48))
        # edgefeat = th.reshape(edgefeat,(1,15))
        # adjc = th.reshape(adjc,(1,256))
        
        # statevec = th.cat((
        #                       th.flatten(nodefeat)[None, :],
        #                       th.flatten(edgefeat)[None, :],
        #                       th.flatten(adjc)[None, :]), 1)
        # #th.flatten(loss)[None, :],
        # print(statevec)
        return self.linear(statevec)
def learning_rate_schedule(initial_value: float) -> Callable[[float], float]:

    def func(progress_remaining: float) -> float:

        return (progress_remaining**2) * initial_value
    return func
# env = openDSSenv()

def make_env(rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = openDSSenv34()
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init

if __name__ == '__main__':
# env = openDSSenv34()
    num_cpu = 4
    env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])

    rms_prop_eps = 1e-5
    # policy_kwargs = dict(
    #     features_extractor_class=CustomCNN,
    #     features_extractor_kwargs=dict(features_dim=32),
    #     optimizer_class = th.optim.RMSprop,
    #     optimizer_kwargs = dict(alpha=0.89, eps=rms_prop_eps, weight_decay=0)
    # )
    # model = A2C('MultiInputPolicy', env,tensorboard_log="logger/", policy_kwargs=policy_kwargs, verbose=1, n_steps=100,
    #         use_rms_prop=False,
    #             gamma=1.00,
    #             learning_rate=learning_rate_schedule(0.07),
    #             ).learn(total_timesteps=20000, n_eval_episodes=1, log_interval=1, tb_log_name="R1_MLP")

    policy_kwargs = dict(
        features_extractor_class=CustomNN,
        features_extractor_kwargs=dict(features_dim=128),
        activation_fn=th.nn.Tanh,
        net_arch=[dict(vf=[128, 128])]
        # optimizer_class = th.optim.RMSprop,
        # optimizer_kwargs = dict(alpha=0.89, eps=rms_prop_eps, weight_decay=0)
    )


    model = PPO('MultiInputPolicy', env,tensorboard_log="logger/", policy_kwargs=policy_kwargs, verbose=1, n_steps=200, batch_size=100,
                gamma=1.00,
                learning_rate=learning_rate_schedule(0.00001),
                    ent_coef=0.05
                    ).learn(total_timesteps=80000, n_eval_episodes=1, log_interval=1, tb_log_name="R1_34_env_mlp")

    # model = A2C(ActorCriticGCAPSPolicy, env,tensorboard_log="logger/", policy_kwargs=policy_kwargs, verbose=1, n_steps=1).learn(total_timesteps=20000, n_eval_episodes=1)
    # model = A2C('MultiInputPolicy', env,tensorboard_log="logger/", policy_kwargs=policy_kwargs, verbose=1, n_steps=1).learn(total_timesteps=20000, n_eval_episodes=1)
    #model.learn(total_timesteps=2000)


    log_dir = "."
    model.save(log_dir + "r1_34_bus_mlp_with_entropy_05_multi_env")
    
    
# with open('obsservation.pkl', 'wb') as handle:
#     pickle.dump(observations, handle, protocol=pickle.HIGHEST_PROTOCOL)
# print(env.total_distance_travelled)
    # env.render()
# if __name__ == '__main__':
#
#     env = mTSPEnv(
#         n_locations = 21,
#         n_agents = 5
#     )
#     action_sequence = [3,4,1,10,2,8,6,9,7,5,11,14,12,16,13,15,20,19,17,18]
#     i = 0
#     while not env.done:
#         action =  action_sequence[i]
#         i += 1
#         env.step(action)