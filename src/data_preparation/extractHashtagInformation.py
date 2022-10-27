import os
import sys
sys.path.append('../../')

import json
import yaml
import pandas as pd
import numpy as np

from src.utils import get_tweet_filepaths

def extractHashtagOccurences(config_path, main_dir): 

	#load config file
	assert os.path.exists(config_path)
	with open(config_path) as file:
	    config = json.load(file)

	#determine all filepaths to tweets
	tweet_filepaths = get_tweet_filepaths(main_dir, config)

	#hashtag count dictionary
	hashtag_dict = {}

	#specific hashtag tweet dictionaries
	qanon = {}
	hnerds = {}
	fakenews = {}
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
	                
	                hashtags = tweet['entities']['hashtags']
	                for tag in hashtags:

	                    #collect tweets containing specific hashtags
	                    if tag['text'].lower() == 'qanon' or tag['text'].lower() == 'wwg1wga':
	                        qanon[tweet_id] = tweet
	                    if tag['text'].lower() == '12hnerds':
	                        hnerds[tweet_id] = tweet
	                    if tag['text'].lower() == 'fakenews':
	                        fakenews[tweet_id] = tweet

	                    #increment count of all occuring hashtags
	                    if tag['text'].lower() in hashtag_dict:
	                        count = hashtag_dict[tag['text'].lower()]
	                        hashtag_dict[tag['text'].lower()] = count + 1
	                    else:
	                        hashtag_dict[tag['text'].lower()] = 1
	        
	        del tmp_tweets
	        
	    except Exception as e:
	        print(e)
	        print(f"Skipping file {filepath}")


	#save all specially collected tweets
	tweets_path = os.path.join(main_dir, config['tweets_dir'])
	with open(os.path.join(tweets_path, 'qanon_tweets.json'),'w') as json_file:
	    json.dump(qanon, json_file)  
	with open(os.path.join(tweets_path, 'hnerds_tweets.json'),'w') as json_file:
	    json.dump(hnerds, json_file)  
	with open(os.path.join(tweets_path, 'fakenews_tweets.json'),'w') as json_file:
	    json.dump(fakenews, json_file)  


	#save all hashtag counts as csv
	df_hashtags = pd.DataFrame()
	df_hashtags['tag'] = hashtag_dict.keys()
	df_hashtags['count'] =  hashtag_dict.values()

	results_path= os.path.join(main_dir, config['results_dir'])
	df_hashtags.to_csv(os.path.join(results_path, 'hashtags_all.csv'), index=False)



if __name__ == '__main__':
    config_path = sys.argv[1]
    main_dir = sys.argv[2]

    extractHashtagOccurences(config_path, main_dir)
