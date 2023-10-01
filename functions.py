import json
import glob
import pandas as pd
import os


def create_excel_files(input_dir):
    # Create a dictionary to organize data by language
    language_data = {}
    
    # Use glob to find all JSONL files in the directory

    jsonl_file_paths = glob.glob(input_dir + '/*.jsonl')


    # Iterate through the list of JSONL file paths
    for jsonl_file_path in jsonl_file_paths:
        with open(jsonl_file_path, 'r', encoding='utf-8') as jsonl_file:
            for line in jsonl_file:
                try:
                    json_object = json.loads(line)
                    # Assuming each JSON object has 'locale', 'id', 'utt', and 'annot_utt'
                    language_id = json_object['locale']
                    if language_id not in language_data:
                        language_data[language_id] = []
                    language_data[language_id].append({
                        'id': json_object['id'],
                        'utt': json_object['utt'],
                        'annot_utt': json_object['annot_utt']
                    })
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON in file {jsonl_file_path}: {e}")
    
    # Identify all unique languages (excluding English)
    languages = [lang for lang in language_data.keys() if lang != 'en']
    
    # Create and save Excel files for each language
    for language in languages:
        # Create a pandas DataFrame from the data for the current language
        df = pd.DataFrame(language_data[language])
        
        # Create the Excel file (en-xx.xlsx)
        excel_file_name = os.path.join('output', 'xlsx', f'en-{language}.xlsx')
        df.to_excel(excel_file_name, index=False)
        print(f"Excel file '{excel_file_name}' generated for language '{language}'")


def generate_partitioned_jsonl(input_dir):
    locales = ['en-US', 'sw-KE', 'de-DE']
    partitions = ['test', 'train', 'dev']

    # Iterate through languages and partitions
    for lang in locales:
        for partition in partitions:
            # Define the input JSONL file path
            input_file_path = os.path.join(input_dir, f'{lang}.jsonl')
            
            # Define the output JSONL file path
            output_dir = os.path.join('output', 'ttd')
            output_file_path = os.path.join(output_dir, f'{lang}_{partition}.jsonl')
            
            # Read the input JSONL file and filter data based on the partition
            filtered_data = []
            with open(input_file_path, 'r', encoding='utf-8') as input_file:
                for line in input_file:
                    record = json.loads(line)
                    if 'partition' in record and record['partition'] == partition:
                        filtered_data.append(record)
            
            # Write the filtered data to the output JSONL file
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for record in filtered_data:
                    json.dump(record, output_file, ensure_ascii=False)
                    output_file.write('\n')
    
    print('Separate JSONL files created successfully.')


def generate_combined_json(input_dir):
    output_file = os.path.join('output', 'train', 'combined_train_data.json')
    # Create an empty list to store the combined data
    combined_data = []
    
    # Find all JSONL files in the input directory
    jsonl_files = glob.glob(os.path.join(input_dir, '*.jsonl'))
    
    # Iterate through JSONL files
    for jsonl_file in jsonl_files:
        # Determine the language from the file name
        lang = os.path.basename(jsonl_file).split('.')[0]
        
        # Read the JSONL file and extract id and utt columns for "train" set
        with open(jsonl_file, 'r', encoding='utf-8') as input_file:
            for line in input_file:
                record = json.loads(line)
                if 'partition' in record and record['partition'] == 'train':
                    combined_data.append({
                        'id': record['id'],
                        'utt': record['utt'],
                        'language': lang  # Include the language for reference
                    })


    # Write the combined data to the output JSON file

    with open(output_file, 'w', encoding='utf-8') as output_json:
        json.dump(combined_data, output_json, ensure_ascii=False, indent=2)
    print('Combined JSONL file created successfully.')


