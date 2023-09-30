import functions
import sys
import os

def main():
    # Update this directory as per the location of your dataset folder
    input_dir = 'dataset/data'
    output_dir = 'output/'
    languages = ['en', 'de', 'sw']

    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return

    if len(sys.argv) < 2:
        print("Please provide at least one function name.")
        return

    # Retrieve all provided function names
    function_names = sys.argv[1:]

    # Define flags to control behavior
    generate_excel_files_flag = "generate_excel_files" in function_names
    separate_files_flag = "separate_files" in function_names
    train_translations_flag = "train_translations" in function_names

    # Check and create the main output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Check and create subdirectories based on flags
    if generate_excel_files_flag:
        excel_output_directory = os.path.join(output_dir, 'xlsx')
        if not os.path.exists(excel_output_directory):
            os.makedirs(excel_output_directory)

    if separate_files_flag:
        ttd_output_directory = os.path.join(output_dir, 'ttd')
        if not os.path.exists(ttd_output_directory):
            os.makedirs(ttd_output_directory)

    if train_translations_flag:
        train_output_directory = os.path.join(output_dir, 'train')
        if not os.path.exists(train_output_directory):
            os.makedirs(train_output_directory)

    # Check and run functions based on the flags
    if generate_excel_files_flag:
        functions.create_excel_files(input_dir)
    if separate_files_flag:
        functions.generate_partitioned_jsonl(input_dir)
    if train_translations_flag:
        functions.generate_combined_json(input_dir, train_output_directory, languages)

if __name__ == "__main__":
    main()