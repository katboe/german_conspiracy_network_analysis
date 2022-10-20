import os
import sys
sys.path.append('../../')

import tweepy
import json
import yaml

import math
from datetime import date
from tqdm import tqdm


from src.twitter_utils import establish_api

def extract_followers(config_path,  main_dir, process_id, screen_name):
    """
    Establish tweepy API access and extract all follower_ids of Twitter user with given screen_name
    
    :param config_path:
    :type config_path: str
    :param main_dir:
    :type main_dir: str
    :param process_id:
    :type process_id: int
    :param screen_name:
    :type screen_name: str
    """
    
    #load config file
    assert os.path.exists(config_path)
    with open(config_path) as file:
        config = json.load(file)

    #assert that process_id is valid
    assert process_id < config["total_num_process"]

    print(os.path.join(main_dir, config["twitter_key_dir"]))
    api = establish_api(os.path.join(main_dir, config["twitter_key_dir"]), process_id)
    
    #get user stats for progress bar
    user = api.get_user(screen_name=screen_name)
    num_followers = user.followers_count
    num_pages = math.ceil(num_followers / config['page_size'])

    #extract follower ids (waits when Twitter API rate limit is reached)
    followers_list = [] 
    with tqdm(total=num_pages) as progress_bar:
        for page in tweepy.Cursor(api.followers_ids, screen_name= screen_name, count= config['page_size']).pages():
            followers_list += page
            progress_bar.update(1) 
        
    print(f"Count of extracted followers {len(followers_list)}")

    followers_dir = {user.id: followers_list}

    #save follower ids
    with open(os.path.join(main_dir + config['follower_dir'], f"{config['follower_fname']}_{screen_name}.json"), 'w') as fp:
        json.dump(followers_dir, fp, indent=4)

if __name__ == '__main__':
    config_path = sys.argv[1]
    main_dir = sys.argv[2]
    process_id = int(sys.argv[3])
    screen_name = sys.argv[4]
    
    extract_followers(config_path, main_dir, process_id, screen_name)
