import warnings

import data_manipulation as dm
import haversine
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None

warnings.simplefilter(action='ignore', category=FutureWarning)


def intersections(filename, cluster_data):
    """Load User Json"""
    data = pd.read_json(filename)

    data = dm.pandas.series_to_columns(data, "timelineObjects")
    data = data[data.placeVisit.notna()]
    data = data.drop(columns=['activitySegment'])

    """Load Cluster Data"""
    # cluster_data = pd.read_csv(cluster_filename)
    id_tags = [x for x in range(len(cluster_data))]
    cluster_data['id_tag'] = id_tags

    lats = []
    lngs = []
    start_timestamps = []
    end_timestamps = []

    """Extract User Data"""
    for i in range(len(data)):
        lats.append(float(data.iloc[i].placeVisit['location']['latitudeE7']))
        lngs.append(float(data.iloc[i].placeVisit['location']['longitudeE7']))
        start_timestamps.append(float(data.iloc[i].placeVisit['duration']['startTimestampMs']))
        end_timestamps.append(float(data.iloc[i].placeVisit['duration']['endTimestampMs']))

    """Convert latlngs to standard decimals and extend time window to +-12 hours around known timestamp"""
    lats = np.array(lats) / 10000000
    lngs = np.array(lngs) / 10000000
    start_timestamps = np.array(start_timestamps) - 43200000
    end_timestamps = np.array(end_timestamps) + 43200000

    """Create Frame for User Data"""
    user_frame = pd.DataFrame({
        'latitude': lats,
        'longitude': lngs,
        'start_time': start_timestamps,
        'end_time': end_timestamps
    })
    user_match_frame = pd.DataFrame(columns=list(user_frame) + ['matched_id'])
    matched_id = []

    """Look for matches by time"""
    for i in range(len(cluster_data)):
        cut1 = user_frame[user_frame.start_time <= cluster_data.iloc[i].timestamp]
        cut2 = cut1[cut1.end_time >= cluster_data.iloc[i].timestamp]
        cut2['matched_id'] = [cluster_data.iloc[i].id_tag] * len(cut2)
        user_match_frame = user_match_frame.append(cut2)

    """Look for matches by distance"""
    if len(user_match_frame) > 0:
        distances = []
        for j in range(len(user_match_frame)):
            matched_cluster_item = cluster_data[cluster_data.id_tag == user_match_frame.iloc[j].matched_id]

            distance = np.round(
                haversine.haversine(
                    [user_match_frame.iloc[j].latitude, user_match_frame.iloc[j].longitude],
                    [matched_cluster_item.iloc[0].latitude, matched_cluster_item.iloc[0].longitude]), 4)
            distances.append(distance)
        user_match_frame['distance'] = distances
        user_match_frame = user_match_frame[user_match_frame.distance <= 0.15]

    """Return Matches."""
    if len(user_match_frame) > 0:
        matched_cluster_frame = cluster_data[cluster_data.id_tag.isin(user_match_frame.matched_id)]
    else:
        matched_cluster_frame = pd.DataFrame(columns=list(cluster_data))

    return matched_cluster_frame
