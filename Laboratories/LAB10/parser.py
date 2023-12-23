import argparse

def parse_arguments():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-al", "--ability_level", type=float, default=0.0, required=False, help= "teacher ability level")
    
    parser.add_argument("-p", "--path", type=str, default="q_agent.pkl", required=False, help= "path for the agent pickle file")
    
    parser.add_argument("-l", "--load", action="store_true", help="load trained agent")
    
    parser.add_argument("-t", "--teacher_episodes", default=None, type=int, help="teacher agent")
    
    args = parser.parse_args()
    
    return args