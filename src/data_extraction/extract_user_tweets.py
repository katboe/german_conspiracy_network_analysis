import sys
sys.path.append('../../')
import os 

import rest
import json
import yaml

import math
from datetime import date
from tqdm import tqdm

from src.utils import read_unique_users


def scrape_tweets(config_path, main_dir, process_id):
	"""
    Extract tweet archives (max. last 2500 tweets) of previously extracted users (followers of conspiracy source Twitter users)
    
    :param config_path:
    :type config_path: str
    :param main_dir:
    :type main_dir: str
    :param process_id:
    :type process_id: int
    """

	#load config
	assert os.path.exists(config_path)

	with open(config_path) as file:
	        config = json.load(file)

	#check validity of process_id
	if process_id >=  config["total_num_process"]:
		print(f"process_id has to be smaller than {config['total_num_process']}")
		sys.exit()

	
	#load ids of all users in conspiracy network
	user_list = read_unique_users(main_dir, config)

	#get to extractable part of user ids list
	num_total = len(user_list)
	len_per_process = math.ceil(num_total / config["total_num_process"])

	if process_id !=  config["total_num_process"] - 1:
	    curr_user_list = user_list[process_id*len_per_process:(process_id + 1)*len_per_process]
	else:
	    curr_user_list = user_list[process_id*len_per_process:]
	print(f"Number of accounts to be extracted: {len(curr_user_list)}")

	#extract all tweets of users in current part of list
	tweetsDict = dict()
	with tqdm(total=len(curr_user_list)) as progress_bar:
		for userid in curr_user_list:
		    print(f'userid: {userid}')
		    try:
		        archive = rest.fetch_user_archive(userid)
		        tweetcount = 0
		        tweetlist = dict()
		        for page in archive:
		            for tweet in page:
		                tweetlist[tweet["id"]] = tweet

	        	tweetsDict[userid] = tweetlist
		            
		    except (RuntimeError, NameError, ValueError) as error:
		        print(error)
		        if error[0]['code'] == 34:
		            print("account deleted")
		        else:
		            errorCount = errorCount + 1
		            print("error")
		            print(error)
		        pass
		    except Exception as e:
		        print(e)
		        pass
		progress_bar.update(1) 

	#save tweets  
	tweet_path = os.path.join(main_dir, config['tweets_dir'])
	if tweetsDict != {}:
	    with open(os.path.join(tweet_path, f'{config["tweets_fname"]}_{process_id}.json'), 'w') as fp:
	        json.dump(tweetsDict, fp, indent=4)


if __name__ == '__main__':
    config_path = sys.argv[1]
    main_dir = sys.argv[2]
    process_id = int(sys.argv[3])

    scrape_tweets(config_path, main_dir, process_id)
