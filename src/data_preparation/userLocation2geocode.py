import sys
sys.path.append('../../')
import os 

import json

# spatial analysis
# import geonamescache
import geopy
from geopy.geocoders import Nominatim

from src.utils import read_users


def userloc2geocode(config_path, main_dir):
    #load config file
    assert os.path.exists(config_path)
    with open(config_path) as file:
        config = json.load(file)
     
    
    users = read_users(main_dir, config)
    
    coord_dict = {}

    #load agent specialized for twitter locations (user-generated locations, noisy)
    nom = Nominatim(user_agent="spat_tweet_ana")

    for user in users:
        if users[user]['location'] != "":
            loc = users[user]['location']
            try:
                lat = nom.geocode(loc).latitude
                lon = nom.geocode(loc).longitude
                location = nom.reverse([lat, lon])
                country = location.raw['address']['country']

                loc_dict = {}
                loc_dict['lat'] = lat
                loc_dict['lon'] = lon
                loc_dict['country'] = country
                loc_dict['name'] = loc
                coord_dict[user] = loc_dict
                
                print(loc_dict)

            except KeyboardInterrupt:
                raise
            except:
                print(loc)
                print('location not found')
                pass
           
    results_path = os.path.join(main_dir, config['results_dir'])
    with open(os.path.join(results_path, f"{config['location_fname']}.json"), 'w') as json_file:
        json.dump(coord_dict, json_file) 


if __name__ == '__main__':
    config_path = sys.argv[1]
    main_dir = sys.argv[2]

    userloc2geocode(config_path, main_dir)
