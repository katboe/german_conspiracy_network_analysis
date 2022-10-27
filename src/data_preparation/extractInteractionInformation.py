import os
import sys
sys.path.append('../../')

import json
import yaml
import pandas as pd
import numpy as np

from src.utils import get_tweet_filepaths,read_users


def extractInteractionInformation(config_path, main_dir):

	#load config file
	assert os.path.exists(config_path)
	with open(config_path) as file:
	    config = json.load(file)

	#read required data
	tweet_filepaths = get_tweet_filepaths(main_dir, config)
	users = read_users(main_dir, config)


	#extract interactions (mentionings and retweets)
	interactions = {}

	for filepath in tweet_filepaths:
	    
	    try:
	        #files are large so loading each file can take a while
	        with open(filepath) as json_file:
	            print(f'Loading {filepath}')
	            tmp_tweets = json.load(json_file)

	        #for each user's tweets: count hashtags and extract tweets containing specific hashtags
	        for user in tmp_tweets:
	            curr_user_tweets = tmp_tweets[user]
	            
	            for tweet_id in curr_user_tweets:
	                tweet = curr_user_tweets[tweet_id]
	                print(tweet)
	                
	                for annot in tweet['entities']['user_mentions']:
	                    if annot['id'] in users:
	                        edge = {}
	                        edge['tweet'] = tweet['id']
	                        edge['sender'] = tweet['user']['id']
	                        edge['receiver'] = annot['id']

	                        if tweet['user']['id'] in interactions:
	                            tweet_list = interactions[tweet['user']['id']] 
	                            tweet_list.append(edge)
	                            interactions[tweet['user']['id']] = tweet_list
	                        else:
	                            interactions[tweet['user']['id']] = [edge]

	                if tweet['retweeted']:
	                    print(tweet)
	                    try:
	                        user_id = tweet['retweeted_status']['user']['id']  
	                        if user_id in users:
	                            edge = {}
	                            edge['tweet'] = tweet['id']
	                            edge['sender'] = tweet['user']['id']
	                            edge['receiver'] = user_id

	                            if tweet['user']['id'] in interactions:
	                                tweet_list = interactions[tweet['user']['id']] 
	                                tweet_list.append(edge)
	                                interactions[tweet['user']['id']] = tweet_list
	                            else:
	                                interactions[tweet['user']['id']] = [edge]
	                    except:
	                        pass
	        
	        del tmp_tweets
	        
	    except Exception as e:
	        print(e)
	        print(f"Skipping file {filepath}")

	#save interaction tweets
	tweets_path = os.path.join(main_dir, config['tweets_dir'])
	with open(os.path.join(tweets_path, 'interaction_tweets.json'),'w') as json_file:
	    json.dump(interactions, json_file)  



if __name__ == '__main__':
    config_path = sys.argv[1]
    main_dir = sys.argv[2]

    extractInteractionInformation(config_path, main_dir)
