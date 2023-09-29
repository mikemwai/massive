import pandas as pd
import os
import json
import random


def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                parsed_data = json.loads(line)
                data.append(parsed_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON in line: {line}")
                continue
    return data


def yield_jsonl_entries(file_path):  # Add this function
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield json.loads(line)


def generate_excel_files(data_folder_path, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(data_folder_path):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(data_folder_path, filename)
            data = read_jsonl_file(file_path)  # Read all entries from the file
            language_data = {}  # Initialize language_data for each file
            for entry in data:
                locale = entry['locale']
                language_code = locale.split('-')[0]

                # Initialize language_data for each language
                if language_code not in language_data:
                    language_data[language_code] = []

                language_data[language_code].append(entry)

            for language_code, data in language_data.items():
                if language_code == 'en':
                    continue
                output_filename = os.path.join(output_directory, f'en-{language_code}.xlsx')
                df = pd.DataFrame(data)
                df.to_excel(output_filename, index=False, engine='openpyxl')

    english_output_path = os.path.join(output_directory, 'en-xx.xlsx')
    english_df = pd.DataFrame(language_data.get('en', []))
    english_df.to_excel(english_output_path, index=False, engine='openpyxl')


def process_data_in_batches(input_directory, output_directory, output_json_path, languages, batch_size):
    batch = []
    batch_count = 0
    language_data = {}

    for filename in os.listdir(input_directory):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                language_data = {}  # Initialize language_data for each file
                for entry in yield_jsonl_entries(file_path):
                    language = entry['locale'].split('-')[0]
                    if language in languages:
                        batch.append(entry)
                        batch_count += 1

                        if batch_count >= batch_size:
                            # Process the current batch
                            process_entries(batch, language_data, output_directory)
                            batch = []
                            batch_count = 0

            if batch:
                # Process any remaining entries in the last batch
                process_entries(batch, language_data, output_directory)

    # Save language data to a JSON file
    save_data(language_data, output_json_path)


def process_entries(entries, language_data, output_directory):
    for entry in entries:
        locale = entry['locale']
        language_code = locale.split('-')[0]
        language_data.setdefault(language_code, []).append(entry)  # Update language_data


def load_data(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                entry = json.loads(line)
                data.append(entry)
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
    return data


def save_data(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")


def add_entry(translations, entry_id, language, content):
    if entry_id not in translations:
        translations[entry_id] = {}
    translations[entry_id][language] = content


def generate_large_json_file(input_directory, output_directory, output_json_path, languages):
    translations = {}

    for language in languages:
        train_file_path = os.path.join(input_directory, f'{language}-train.jsonl')
        data = load_data(train_file_path)

        for entry in data:
            entry_id = entry['id']
            entry_utt = entry['utt']
            add_entry(translations, entry_id, language, entry_utt)

    # Save translations to individual JSONL files based on locale
    for language in languages:
        locale = f'{language}-xx'
        output_filename = os.path.join(output_directory, f'{locale}.jsonl')
        translations_data = translations.get(language, {})
        save_jsonl_data(translations_data, output_filename)


def save_jsonl_data(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as output_file:
            for entry in data:
                output_file.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")


def partition_and_process_data(input_directory, output_directory, output_json_path, languages, test_ratio=0.1,
                               dev_ratio=0.1):
    partitioned_data = {language: {'test': [], 'train': [], 'dev': []} for language in languages}
    translations = {}

    for filename in os.listdir(input_directory):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(input_directory, filename)
            data = load_data(file_path)

            for entry in data:
                language = entry['locale'].split('-')[0]
                if language not in languages:
                    continue
                partition = entry['partition']

                if partition == 'test':
                    split = 'test'
                elif partition == 'dev':
                    split = 'dev'
                else:
                    split = 'train'

                partitioned_data[language][split].append(entry)

                if split == 'train':
                    entry_id = entry['id']
                    entry_utt = entry['utt']
                    add_entry(translations, entry_id, language, entry_utt)

    for language in languages:
        for split in ['test', 'train', 'dev']:
            output_filename = os.path.join(output_directory, f'{language}-{split}.jsonl')
            save_data(partitioned_data[language][split], output_filename)

    save_data(translations, output_json_path)
