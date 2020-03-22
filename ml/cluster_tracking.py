import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import data_manipulation as dm
import json
from time import time
import haversine


def intersections(filename, cluster_filename):
    
    
    data = pd.read_json(filename)
    print("{}\n".format(filename))
    #print("User Frame:\n {} \n".format(str(data)))

    
    data = dm.pandas.series_to_columns(data, "timelineObjects")
    data = data[data.placeVisit.notna()]
    data = data.drop(columns = ['activitySegment'])
    
    cluster_data = pd.read_csv(cluster_filename)
    #print("Cluster Frame:\n {} \n".format(str(cluster_data)))
    #print(cluster_data)
    

    
    lats = []
    lngs = []
    start_timestamps = []
    end_timestamps = []
    
    for i in range(len(data)):
        lats.append(float(data.iloc[i].placeVisit['location']['latitudeE7']))
        lngs.append(float(data.iloc[i].placeVisit['location']['longitudeE7']))
        start_timestamps.append(float(data.iloc[i].placeVisit['duration']['startTimestampMs']))
        end_timestamps.append(float(data.iloc[i].placeVisit['duration']['endTimestampMs']))
        
    lats = np.array(lats)/10000000
    lngs = np.array(lngs)/10000000
    start_timestamps = np.array(start_timestamps)
    end_timestamps = np.array(end_timestamps)
    
    user_frame = pd.DataFrame({
        'latitude': lats, 
        'longitude': lngs, 
        'start_time': start_timestamps,
        'end_time': end_timestamps})
    user_frame.to_csv("user_frame.csv", index = False)
    #print("User Frame :\n{} \n".format(user_frame))
    
    #perform the matching
    #match_frame = pd.DataFrame(columns = list(cluster_data))
    user_match_frame = pd.DataFrame(columns = list(user_frame)+['matched_id'])
    matched_id = []
    for i in range(len(cluster_data)):
        
        #match for time
        cut1 = user_frame[user_frame.start_time <= cluster_data.iloc[i].timestamp]
        #print(cut1)
        #print(cluster_data.iloc[i].timestamp)
        cut2 = cut1[cut1.end_time >= cluster_data.iloc[i].timestamp]
        cut2['matched_id'] = [cluster_data.iloc[i].id_tag]*len(cut2)
        user_match_frame = user_match_frame.append(cut2)
        
    
    #print(user_match_frame)    
    if len(user_match_frame)>0:
        distances = []
        for j in range(len(user_match_frame)):
            matched_cluster_item = cluster_data[cluster_data.id_tag == user_match_frame.iloc[j].matched_id]
            
            distance = np.round(
                haversine.haversine(
                [user_match_frame.iloc[j].latitude,user_match_frame.iloc[j].longitude],
                [matched_cluster_item.iloc[0].latitude,matched_cluster_item.iloc[0].longitude]),4)
            #print(distance)
            distances.append(distance)
        user_match_frame['distance'] = distances
        user_match_frame=user_match_frame[user_match_frame.distance<=0.1]
        
    if len(user_match_frame)>0:
        print("User logs matched: ")
        print(user_match_frame)
        #user_match_frame.to_csv("user_match_frame.csv", index = False)
        print("\n")
        
        print("Cluster tag matched: ")
        matched_cluster_frame = cluster_data[cluster_data.id_tag.isin(user_match_frame.matched_id)]
        #matched_cluster_frame.to_csv("matched_cluster_frame.csv", index = False)
        print(matched_cluster_frame)
        print("\n")
        
        #return(user_match_frame, matched_cluster_frame)
        
        
    else:
        print("No known intersections")
        matched_cluster_frame = pd.DataFrame(columns=list(cluster_data))
    
    return(user_match_frame, matched_cluster_frame)

if __name__ == '__main__':
    intersections('user1_lh.json', 'sample_cluster2.csv')
    intersections('user2_lh.json', 'sample_cluster2.csv')
    
    
    
    
        