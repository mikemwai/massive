# Import the functions module
import functions

# Define this directory as per where your dataset folder is located
input_dir = 'dataset/data'


# Step 1: Generate Excel files containing language translations
generate_excel_files=functions.create_excel_files(input_dir)

# Step 2: Create separate JSONL files for English (en), Swahili (sw), and German (de) for test, train, and dev datasets.
separate_files=functions.generate_partitioned_jsonl(input_dir)

# Step 3: Generate a unified JSON file with translations from English (en) to all languages,
# including unique IDs and utterances for all the training sets.
train_translations=functions.generate_combined_json(input_dir)

