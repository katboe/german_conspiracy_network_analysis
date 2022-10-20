import os
import sys
sys.path.append('../../')

import tweepy
import json
import yaml

import math
from datetime import date
from tqdm import tqdm

from src.utils import read_unique_users
from src.twitter_utils import establish_api


def extract_friends(config,  api, user_id):
   
    #get user stats for progress bar
    user = api.get_user(id=user_id)
    num_friends = user.friends_count
    print(num_friends)
    num_pages = math.ceil(num_friends / config['page_size'])
    
    
    #extract follower ids (waits when Twitter API rate limit is reached)
    friends_list = []
    with tqdm(total=num_pages) as progress_bar:
        for page in tweepy.Cursor(api.friends_ids, user_id=user_id, count= config['page_size']).pages():
            friends_list += page
            progress_bar.update(1) 
        
    print(f"Count of extracted followers {len(friends_list)}")
    
    return friends_list

def extract_all_friends(config_path, main_dir, process_id):
    """
    Extract all friends (users that user is following) of previously extracted users (followers of conspiracy source users)
    
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
    
    print(follower_list)

    #get to extractable part of follower ids list for process_id
    num_total = len(follower_list)
    len_per_process = math.ceil(num_total / config["total_num_process"])
    
    if process_id !=  config["total_num_process"] - 1:
        curr_follower_list = follower_list[process_id*len_per_process:(process_id + 1)*len_per_process]
    else:
        curr_follower_list = follower_list[process_id*len_per_process:]
    print(f"Number of accounts to be extracted: {len(curr_follower_list)}")

    #assert that process_id is valid
    assert process_id < config["total_num_process"]


    api = establish_api(os.path.join(main_dir, config["twitter_key_dir"]), process_id)
    
    friends_dir = {}
    for follower_id in curr_follower_list:
        friends_dir[follower_id] = extract_friends(config, api, follower_id)
        
    #save extracted "friends" relationships
    with open(os.path.join(main_dir + config['friends_dir'], f"{config['friends_fname']}_{process_id}.json"), 'w') as fp:
             json.dump(friends_dir, fp, indent=4)
    



if __name__ == '__main__':
    config_path = sys.argv[1]
    main_dir = sys.argv[2]
    process_id = int(sys.argv[3])

    extract_all_friends(config_path, main_dir, process_id)
