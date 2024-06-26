import numpy as np
import gymnasium as gym
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import SubprocVecEnv
import data_generator
import argparse



def main(args):

# Instantiate the env

    read_OD = data_generator.process_csv()
    
    print(read_OD)
    
    env = gym.make("Skip-v0", num_trains=args.train, num_stations=args.station, num_time = args.time, pass_od = read_OD)
    
    n_steps = 100

    model = A2C("MlpPolicy", env, verbose=1).learn(n_steps)

    # using the vecenv
    obs,_ = env.reset()
    
    
    for step in range(n_steps):

        action, _ = model.predict(obs, deterministic=True)
        print(f"Step {step + 1}")
        print("Action: ", action)
        obs, reward, done,_, info = env.step(action)
        print("obs=", obs, "reward=", reward, "done=", done)
        env.render()
        if done:
            # Note that the VecEnv resets automatically
            # when a done signal is encountered
            print("Goal reached!", "reward=", reward)
            break

# Instantiate the env
parser = argparse.ArgumentParser(
        prog='skip_env', # 程序名
        description='Skip'
    )
# Train the agent
    # 此参数必须为int类型:
parser.add_argument('--port', default='3306', type=int)
# 允许用户输入简写的-u:
parser.add_argument('-t',  '--train', default=6, type=int )
parser.add_argument('-s','--station', default=6, type=int )
parser.add_argument('--time',  default=60, type=int)

# 解析参数:
args = parser.parse_args()

main(args)