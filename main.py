import os
import argparse
import functions

# Define and parse command-line arguments
parser = argparse.ArgumentParser(description="Process data and generate files.")
parser.add_argument("--data_folder", type=str, required=True, help="Path to the data folder")
parser.add_argument("--output_folder", type=str, required=True, help="Path to the output folder")
parser.add_argument("--generate_excel", action="store_true", help="Generate separate Excel files")
parser.add_argument("--generate_jsonl", action="store_true", help="Generate separate JSONL files")
parser.add_argument("--generate_large_json", action="store_true", help="Generate a large JSON file")
args = parser.parse_args()

if not os.path.exists(args.output_folder):
    os.makedirs(args.output_folder)

data_folder_path = args.data_folder
output_directory = args.output_folder

if args.generate_excel:
    input_dataset_directory = data_folder_path
    output_excel_directory = os.path.join(output_directory, 'excel_files')
    functions.generate_excel_files(input_dataset_directory, output_excel_directory)

if args.generate_jsonl:
    # Generate separate JSONL files for train, test, and dev sets
    target_languages = ["sw", "en", "de"]
    test_ratio = 0.1
    dev_ratio = 0.1
    functions.partition_and_process_data(
        input_directory=data_folder_path,
        output_directory=output_directory,
        output_json_path="train_translations.jsonl",
        languages=target_languages,
        test_ratio=test_ratio,
        dev_ratio=dev_ratio
    )

if args.generate_large_json:
    # Generate a large JSON file for translations from English (en) to other languages (xx)
    target_languages = ["sw", "de"]  # Exclude English
    functions.generate_large_json_file(
        input_directory=data_folder_path,
        output_directory=output_directory,
        output_json_path="large_translations.json",
        languages=target_languages
    )

print("Processing completed.")
