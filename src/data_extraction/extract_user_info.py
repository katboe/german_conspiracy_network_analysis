import os
import sys
sys.path.append('../../')


import rest
import json
import yaml

import math
from datetime import date
from tqdm import tqdm

from src.utils import read_unique_users

def extract_user_info(config_path, main_dir, process_id):
    """
    Extract information on previously extracted users (followers of conspiracy source Twitter users)
    
	:param config_path:
    :type config_path: str
    :param main_dir:
    :type main_dir: str
    :param process_id:
    :type process_id: int
    """
    
    #load config file
    assert os.path.exists(config_path)
    with open(config_path) as file:
        config = json.load(file)
     
    #check validity of process_id
    assert process_id < config["total_num_process"]
        
    #get list of all unique followers
    follower_list = read_unique_users(main_dir, config)
    
    #get to extractable part of follower ids list for process_id
    num_total = len(follower_list)
    len_per_process = math.ceil(num_total / config["total_num_process"])
    
    if process_id !=  config["total_num_process"] - 1:
        user_ids = follower_list[process_id*len_per_process:(process_id + 1)*len_per_process]
    else:
        user_ids = follower_list[process_id*len_per_process:]
    print(f"Number of accounts to be extracted: {len(user_ids)}")

    #assert that process_id is valid
    assert process_id < config["total_num_process"]

    print('before reauthorized')
    rest.reauthorize(key_id=process_id, directory=os.path.join(main_dir, config["twitter_key_dir"]))
    print('reauthorized')
    
    
    user_dict = {}
    try:
        pages = rest.fetch_user_list_by_id(user_ids)
        print("user list fetched")
        count = 0

        for i, user_list in enumerate(pages):
            print(f'page {i}')
            for i in range(len(user_list)):
                user_dict[user_list[i]['id']] = user_list[i]
                 
    except (RuntimeError, TypeError, NameError, ValueError) as e:
        print(e)
        pass
    print(len(user_dict))
    #save extracted "friends" relationships
    with open(os.path.join(main_dir + config['users_dir'], f"{config['users_fname']}_{process_id}.json"), 'w') as fp:
             json.dump(user_dict, fp, indent=4)
    

if __name__ == '__main__':
    config_path = sys.argv[1]
    main_dir = sys.argv[2]
    process_id = int(sys.argv[3])
     
    extract_user_info(config_path, main_dir, process_id)
