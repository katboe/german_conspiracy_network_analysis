import os
import sys
sys.path.append('../../')

import json
import yaml
import pandas as pd
import numpy as np

import botometer


from src.twitter_utils import get_authorization_details


def determineBotScores(config_path, main_dir):
    """
    Determine bot scores of Twitter users using Botometer API

    :param config_path:
    :type config_path: str
    :param main_dir:
    :type main_dir: str
    """

    main_dir = '../..'
    config_path = os.path.join(main_dir, 'config/config.json')

    #load config file
    assert os.path.exists(config_path)
    with open(config_path) as file:
        config = json.load(file)

    #connect to Botometer API   
    bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=config["rapidapi_key"],
                          **get_authorization_details(os.path.join(main_dir, config["twitter_key_dir"])))


    #read information on influencers
    results_path = os.path.join(main_dir, config['results_dir'])
    influencer_filepath = os.path.join(results_path, f"{config['influencer_fname']}_{config['influencer_lower_limit']}.csv")

    df_influencer = pd.read_csv(influencer_filepath)
    influencer_screen_names = [f"@{name}" for name in df_influencer['screen_name']]


    # Check botomer score for a sequence of accounts (needs a while)
    result_dict = {}
    count = 0
    for screen_name, result in bom.check_accounts_in(influencer_screen_names):
        result_dict[screen_name] = result
        count += 1
        print(count)

    #save bot scores for influencers
    results_path = os.path.join(main_dir, config['results_dir'])
    with open(os.path.join(results_path, f"{config['bot_scores_fname']}_{config['influencer_lower_limit']}.json"), 'w') as json_file:
        json.dump(result_dict, json_file) 
                    
                    
if __name__ == '__main__':
    config_path = sys.argv[1]
    main_dir = sys.argv[2]

    determineBotScores(config_path, main_dir)
