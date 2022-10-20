import os
import sys
sys.path.append('../../')

import numpy as np
import json


def read_unique_users(main_dir, config):
    """
    Get a list of all unique users for the "follower" network. This includes the conspiracy source
    Twitter users as well as all their followers
 
    :param main_dir:
    :type main_dir: str
    :param config:
    :type config: dict
    :returns: list of unique user ids
    """ 
    
    #read all files in follower directory:
    follower_path = os.path.join(main_dir, config['follower_dir'])
    print(follower_path)
    follower_file_list = os.listdir(follower_path)
    follower_files = [filename for filename in follower_file_list if (filename.startswith(config['follower_fname']) and filename.endswith('.json'))]
    print(f"Reading follower files: {follower_files}")
    
    follower_list = []
    for filename in follower_files:
        filepath = os.path.join(follower_path, filename)
        print(filepath)
        follower_dir = {}
        with open(os.path.join(follower_path, filename))as fp:
            follower_dir = json.load(fp)
        for key in follower_dir:
            follower_list.append(key)
            follower_list += follower_dir[key]
                
    print(f'number of total follower_ids {len(follower_list)}')
    
    #get unique follower ids (don't extract friends of twitter user multiple times)
    follower_unique = list(set(follower_list))
    print(f'number of unique follower_ids {len(follower_unique)}')

    return follower_unique


def read_friends(main_dir, config):
    """
    Read all extracted friend relationships into one dictionary
    
    :param main_dir:
    :type main_dir: str
    :param config:
    :type config: dict
    :returns: dictionary with all friend relationships
    """ 
    
    #read all files in friends directory starting with friends filename prefix:
    friends_path = os.path.join(main_dir, config['friends_dir'])
    file_list = os.listdir(friends_path)
    files = [filename for filename in file_list if (filename.startswith(config['friends_fname']) and filename.endswith('.json'))]
    print(f"Reading friends files: {files}")
    
    #combine all friend dictionaries in one dictionary
    friends_dict = {}
    for filename in files:
        with open(os.path.join(friends_path, filename))as fp:
            friends_dict.update(json.load(fp))

    return friends_dict


def read_users(main_dir, config):
    """
    Read all extracted user informations into one dictionary
    
    :param main_dir:
    :type main_dir: str
    :param config:
    :type config: dict
    :returns: dictionary with all user information
    """ 
    
    #read all files in friends directory starting with user filename prefix:
    users_path = os.path.join(main_dir, config['users_dir'])
    file_list = os.listdir(users_path)
    files = [filename for filename in file_list if (filename.startswith(config['users_fname']) and filename.endswith('.json'))]
    print(f"Reading user information files: {files}")
    
    #combine all friend dictionaries in one dictionary
    users_dict = {} 
    for filename in files:
        with open(os.path.join(users_path, filename))as fp:
            users_dict.update(json.load(fp))

    return users_dict

def get_tweet_filepaths(main_dir, config):
    """
    Get filespaths to all tweet files
    
    :param main_dir:
    :type main_dir: str
    :param config:
    :type config: dict
    :returns: list of twitter filepaths
    """ 

    #read all files in friends directory starting with tweets filename prefix:
    tweets_path = os.path.join(main_dir, config['tweets_dir'])
    file_list = os.listdir(tweets_path)
    files = [os.path.join(tweets_path, filename) for filename in file_list if (filename.startswith(config['tweets_fname']) and filename.endswith('.json'))]
    
    return files