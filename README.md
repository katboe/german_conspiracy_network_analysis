## Analysis of German Conspiracy ("Querdenker") Twitter Network
During the early Covid-19 days, a community of people, so called 'Querdenker', believing in various conspiracy theories and fake news emerged in Germany. Beside Telegram, they majorily connected on Twitter to spread their believes and recruit like minded. 

In this project, I analyse the characteristics of the 'Querdenker'-network in fall 2020. Based on a [report](https://www.newsguardtech.com/special-reports/twitter-superspreaders-europe/) of 'NewsGuard', three main fake news accounts regarding Covid-19 were identified: '@Compact-Magazin', '@KenFM.de', '@RT_Deutsch' (some of these accounts have since been blocked or deleted by Twitter). From these accounts, I extract all followers, their tweets and friendship relations. Based on this data, I analyse characteristics of the users, the topics discussed as well as the general follower and interaction dynamics within the network. The presentation with the results of the analysis can be viewed [here](https://drive.google.com/file/d/1zEYxB5MpACXth9bJGpoPhPqdo5NGuHk5/view?usp=sharing).

### Setup
First, in the main directory, install all requirements: ```pip install -r requirements.txt```

For the Twitter API access, Twitter keys need to be copied into the 'config/keys_{number}.yaml' files. If multiple keys are available, the extraction can be done in parallel.

For computing bot scores of Twitter accounts, 'Botometer' by RapidAPI is employed. For API access, a RapidAPI key and Twitter keys are required. The RapidAPI key needs to be copied into the 'config/config.json' file.

### Data Extraction
For a comprehensive study of the Conspiracy Network, I extract not only information on the follower relationships but also tweets and user information.

For the extraction, I procede as followed:
1. Extract alll follower ids of the three main fake news sources in Germany.
 
    ```src/data_extraction/extract_follower_ids.py config/config.json . {screen_name}```
    
2. For all followers, extract their user information.

    ```src/data_extraction/extract_user_info.py config/config.json . {process_id}```
    
3. For all followers, extract their tweet archives. 

    ```src/data_extraction/extract_user_tweets.py config/config.json . {process_id}```
    
4. For all followers, extract all friend ids, i.e. accounts they are following.

   ```src/data_extraction/extract_friends_ids.py config/config.json . {process_id}```


### Data Preparation
1. Prepare user information: 
    - For spatial analysis, determine coordinates of user location, if available. 
    - For bot analysis, determine botometer scores of useres.

2. Prepare hashtag information:
     - For general analysis, determine hashtags occurences.
     - For 'QAnon' network analysis, extract qanon tweets seperately.
  
3. Create follower and interaction (mentions and retweets) networks: The three main fake news accounts and all their followers correspond to the nodes in the networks.
     - For the follower network, a directed edge from a to b corresponds to a following b on Twitter. The resulting network is a directed Graph.
     - For the interaction network, a directed edge from a to b corresponds to a mentioning or retweeting b on Twitter. The resulting network is a directed Multipgraph.


### Data Analysis
The analysis and visualization of the extracted and prepared data is divided into User, Topic and Network Analysis. 

1. User Analysis: Spatial Distribution of Twitter Accounts, Analysis of Bot-Scores, Creation-Date Analysis
2. Topic Analysis: Hashtag occurence distribution of Top10 hashtags, conspiracy theory hashtags, vaccination-related hashtags.
3. Network Analysis:
For visualisation, degree analysis, clustering, etc, the follower and interaction graphs are loaded into the graph software ['visone'] (https://visone.ethz.ch/). 
