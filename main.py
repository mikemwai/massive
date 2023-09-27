import os
import json

# Specify the base directory where your folders are located
base_directory = 'C:/Users/User/OneDrive/Desktop/today/1.1/data'  # Adjust the path accordingly

# Initialize an empty list to store all data
all_data = []

# Iterate through all folders in the base directory
for folder_name in os.listdir(base_directory):
    folder_path = os.path.join(base_directory, folder_name)

    # Check if it's a directory
    if os.path.isdir(folder_path):
        # Iterate through all JSONL files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.jsonl'):
                jsonl_file_path = os.path.join(folder_path, filename)

                # Initialize an empty list to store data from this file
                data = []

                # Open the JSONL file and read it line by line
                with open(jsonl_file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        # Parse each line as a JSON object and append it to the data list
                        json_object = json.loads(line)
                        data.append(json_object)

                # Append the data from this file to the all_data list
                all_data.extend(data)

# Now, 'all_data' contains a list of dictionaries from all JSONL files in all folders
