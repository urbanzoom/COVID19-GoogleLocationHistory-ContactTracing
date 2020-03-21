import argparse
import os
import sys

from data_processing import *

# Parse bash arguments
impt_parser = argparse.ArgumentParser(description="Import JSON data")

impt_parser.add_argument("json_path",
                         metavar="json_path",
                         type=str,
                         help="json file path")

json_file = impt_parser.parse_args().json_path

if not os.path.exists(json_file):
    print("The file doesn't exists (maybe in wrong path?). Data import terminated ...")
    sys.exit()

if not json_file.endswith("json"):
    print(
        "The argument doesn't end with json file extension. Please provide a json file type. Data import terminated ...")
    sys.exit()

# Run data processing
print(f"Processing {json_file} ...")
place_visit_df, activity_segment_df = parse_google_takeout_semantic_location_history(json_file)

filename1 = json_file.split(".json")[0] + "_place_visit.csv"
place_visit_df.to_csv(filename1, index=False)
filename2 = json_file.split(".json")[0] + "_activity_segment.csv"
activity_segment_df.to_csv(filename2, index=False)

print(f"Data exported:\n\t- {filename1}\n\t- {filename2}")
print("Data import and processing completed. Program terminated ...")
