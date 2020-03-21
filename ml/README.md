# Data science

This directory contains all the code for data processing, detection and output.


## Setup environment

We use Anaconda to manage our Python environment. **Please download it** with the [Anaconda installation guide](https://docs.anaconda.com/anaconda/install/).

**NOT RECOMMENDED**: We included `requirements.txt` if you decide to use `venv`

### Create conda environment from environment.yml file

```bash
$ conda env create -f environment.yml
```

### Activate environment

You need to activate the environment for data-processing steps.

```bash
$ conda activate covid-19
```

[Full conda managing environments documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#removing-an-environment)


## Google takeout semantic location history 

The goal is to parse Google takeout semantic location history's JSON file

### JSON Data structure
```json
{
  "timelineObjects" : [ {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 373839174,
        "longitudeE7" : -1220129211,
        "placeId" : "ChIJx0rMKD-2j4ARPdGZBUk4e8A",
        "address" : "440 N Wolfe Rd\nSunnyvale, CA 94085\nUSA",
        "name" : "Plug and Play Tech Center",
        "sourceInfo" : {
          "deviceTag" : -11111111
        },
        "locationConfidence" : 99.33132
      },
      "duration" : {
        "startTimestampMs" : "1499205419000",
        "endTimestampMs" : "1499214841016"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 373838255,
      "centerLngE7" : -1220130278,
      "visitConfidence" : 93,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 373839775,
        "longitudeE7" : -1220127465,
        "placeId" : "ChIJx0rMKD-2j4ARPlQnNJY_SBI",
        "name" : "BetterHelp",
        "locationConfidence" : 0.23237103
      }, {
        "latitudeE7" : 373835649,
        "longitudeE7" : -1220130034,
        "placeId" : "ChIJx0rMKD-2j4ARzo9cjz0kO28",
        "name" : "BirdEye",
        "locationConfidence" : 0.05418158
      }, {
        ...
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 373839174,
        "longitudeE7" : -1220137948
      },
      "endLocation" : {
        "latitudeE7" : 373777922,
        "longitudeE7" : -1220301734
      },
      "duration" : {
        "startTimestampMs" : "1499214841016",
        "endTimestampMs" : "1499215096000"
      },
      "distance" : 1901,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 91.15432049039984
      }, {
        "activityType" : "IN_BUS",
        "probability" : 4.681641208332073
      }, {
        ...
      } ],
      "waypointPath" : {
        "waypoints" : [ {
          "latE7" : 373839187,
          "lngE7" : -1220137939
        }, {
          "latE7" : 373777503,
          "lngE7" : -1220301589
        } ]
      },
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  } ]
}
```

### Data parsing

There are 2 possible keys in JSON file: `placeVisit` and `activitySegment`. We parsed and transformed the nested json data structure into flat format for data science purpose.

### placeVisit (after parsed)

| placeConfidence | centerLatE7 | centerLngE7 | visitConfidence | otherCandidateLocations | editConfirmationStatus | childVisits | simplifiedRawPath | latitudeE7 | longitudeE7 | placeId | address | name | sourceInfo | locationConfidence | semanticType | startTimestampMs | endTimestampMs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HIGH_CONFIDENCE | 37.3838255 | -122.01302779999999 | 93 | [{'latitudeE7': 373839775, 'longitudeE7': -1220127465, 'placeId': 'ChIJx0rMKD-2j4ARPlQnNJY_SBI', 'name': 'BetterHelp', 'locationConfidence': 0.23237103}, {'latitudeE7': 373835649, 'longitudeE7': -1220130034, 'placeId': 'ChIJx0rMKD-2j4ARzo9cjz0kO28', 'name': 'BirdEye', 'locationConfidence': 0.05418158}, {...}] | NOT_CONFIRMED |  |  | 37.3839174 | -122.0129211 | ChIJx0rMKD-2j4ARPdGZBUk4e8A | "440 N Wolfe Rd Sunnyvale, CA 94085 USA" | Plug and Play Tech Center | {'deviceTag': -11111111} | 99.33132 |  | 2017-07-04 21:56:59.000 | 2017-07-05 00:34:01.016 |

- We do not flatten `otherCandidateLocations` as the primary location has the highest confidence
- Integer latitude and longtitude are converted to standard float format
- `startTimestampMs` & `endTimestampMs` converted to human readable datetime

### activitySegment (after parsed)

| distance | activityType | confidence | activities | waypointPath | editConfirmationStatus | transitPath | simplifiedRawPath | startLocationlatitudeE7 | startLocationlongitudeE7 | startLocationplaceId | startLocationaddress | startLocationname | startLocationlocationConfidence | startLocationsourceInfo | endLocationlatitudeE7 | endLocationlongitudeE7 | endLocationplaceId | endLocationaddress | endLocationname | endLocationlocationConfidence | startTimestampMs | endTimestampMs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1901.0 | IN_PASSENGER_VEHICLE | HIGH | [{'activityType': 'IN_PASSENGER_VEHICLE', 'probability': 91.15432049039984}, {'activityType': 'IN_BUS', 'probability': 4.681641208332073}, {...}] | {'waypoints': [{'latE7': 373839187, 'lngE7': -1220137939}, {'latE7': 373777503, 'lngE7': -1220301589}]} | NOT_CONFIRMED |  |  | 37.3839174 | -122.0137948 |  |  |  |  |  | 37.3777922 | -122.0301734 |  |  |  |  | 2017-07-05 00:34:01.016 | 2017-07-05 00:38:16.000 |

- We do not flatten `activites` as the primary activity has the highest confidence
- Integer latitude and longtitude (both startLocation & endLocation) are converted to standard float format
- `startTimestampMs` & `endTimestampMs` converted to human readable datetime

## Data processing

```bash
# Once again, activate environment if it's not
$ conda activate covid-19

# cd into current folder
$ cd ~/covid-19/ml/

# Import file (the code import 1 file at a time)
$ python data_import.py 2017_JULY.json
> Processing 2017_JULY.json ...
> Data exported:
>     - 2017_JULY_place_visit.csv
>     - 2017_JULY_activity_segment.csv
> Data import and processing completed. Program terminated ...
```
