import os
import sys
sys.path.append('../../')

import tweepy
import json
import yaml


def find_keyfile(directory=".", process_id=0):
    """
    Helper function: Find the keyfile in a list of possible locations.
    The function iterates recursively through the directory and
    its subdirectories, emitting full paths for matching files.

    :returns: generator for keyfile paths
    """
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename == f'keys_{process_id}.yaml':
                yield os.path.join(root, filename)
         

def get_authorization_details(directory='.', process_id=0):
    """
    Helper function: Read authorization keys in correct format

    :returns: twitter API authorization keys
    """
    try:
        filepath = next(find_keyfile(directory, process_id))
    except StopIteration:
        raise Exception(f"No Keyfile found - please place keys_{process_id}.yaml with your tokens in the project directory or pass a custom filepath to the authorize() function")
    # Load credentials from keyfile
    with open(filepath, 'r') as f:
        keys = yaml.safe_load(f)

    auth_details = {
            'consumer_key': keys['consumer_key'],
            'consumer_secret': keys['consumer_secret'],
            'access_token': keys['access_token'],
            'access_token_secret': keys['access_token_secret'],
            }
    return auth_details


def establish_api(directory='.', process_id=0):
    """
    Helper function: Establishes tweepy API

    :returns: tweepy API
    """
    
    auth_details = get_authorization_details(directory, process_id)
    auth = tweepy.OAuthHandler(auth_details['consumer_key'], auth_details['consumer_secret'])  
    auth.set_access_token(auth_details['access_token'], auth_details['access_token_secret'])  

    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api
