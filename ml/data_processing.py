import data_manipulation as dm
import pandas as pd


def parse_google_takeout_semantic_location_history(json_filepath):
    """
    Parse Google takeout semantic location history

    Parameters
    ----------
    json_filepath: str
        Json file path

    Returns
    -------
    csv
        Return 2 csv, placeVisit & activitySegment
    """
    df = pd.read_json(json_filepath)
    df = dm.pandas.series_to_columns(df, "timelineObjects")

    def _parse_place_visit(df):
        place_visit_df = df[["placeVisit"]].copy()
        place_visit_df.dropna(inplace=True)

        def __data_transform(place_visit_df):
            place_visit_df = dm.pandas.series_to_columns(place_visit_df, "placeVisit")
            place_visit_df = dm.pandas.series_to_columns(place_visit_df, "location")
            place_visit_df = dm.pandas.series_to_columns(place_visit_df, "duration")
            place_visit_df = place_visit_df.where(pd.notnull(place_visit_df), None)

            for col in ["centerLatE7", "centerLngE7", "latitudeE7", "longitudeE7"]:
                place_visit_df[col] = place_visit_df[col].apply(lat_lng_parser)

            for col in ["startTimestampMs", "endTimestampMs"]:
                place_visit_df[col] = pd.to_datetime(place_visit_df[col], unit="ms")

            place_visit_df = place_visit_df.where(pd.notnull(place_visit_df), None)
            return place_visit_df

        return __data_transform(place_visit_df)

    def _parse_activity_segment(df):
        activity_segment_df = df[["activitySegment"]].copy()
        activity_segment_df.dropna(inplace=True)

        def __data_transform(activity_segment_df):
            activity_segment_df = dm.pandas.series_to_columns(activity_segment_df, "activitySegment")
            name_mapper = {c: "startLocation" + c for c in
                           activity_segment_df["startLocation"].apply(pd.Series).columns}
            activity_segment_df = dm.pandas.series_to_columns(activity_segment_df, "startLocation")
            activity_segment_df.rename(columns=name_mapper, inplace=True)
            name_mapper = {c: "endLocation" + c for c in activity_segment_df["endLocation"].apply(pd.Series).columns}
            activity_segment_df = dm.pandas.series_to_columns(activity_segment_df, "endLocation")
            activity_segment_df.rename(columns=name_mapper, inplace=True)
            activity_segment_df = dm.pandas.series_to_columns(activity_segment_df, "duration")
            activity_segment_df = activity_segment_df.where(pd.notnull(activity_segment_df), None)

            for col in ["startLocationlatitudeE7", "startLocationlongitudeE7",
                        "endLocationlatitudeE7", "endLocationlongitudeE7"]:
                activity_segment_df[col] = activity_segment_df[col].apply(lat_lng_parser)

            for col in ["startTimestampMs", "endTimestampMs"]:
                activity_segment_df[col] = pd.to_datetime(activity_segment_df[col], unit="ms")

            activity_segment_df = activity_segment_df.where(pd.notnull(activity_segment_df), None)
            return activity_segment_df

        return __data_transform(activity_segment_df)

    place_visit_df = _parse_place_visit(df)
    activity_segment_df = _parse_activity_segment(df)
    return place_visit_df, activity_segment_df


def lat_lng_parser(integer):
    """
    Transform an integer latitude / longitude into standard format

    Parameters
    ----------
    integer: int
        Integer representation of latitude / longitude

    Returns
    -------
    float
        Standard latitude / longitude float format
    """
    if isinstance(integer, (int, float)):
        scaler_e7 = 0.0000001
        output = integer * scaler_e7

        if output > 180:
            output = output - pow(2, 32) * scaler_e7
        return output
    else:
        return
