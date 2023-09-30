import functions
import sys
import os

def main():
    # Update this directory as per the location of your dataset folder
    input_dir = './data'
    output_dir = './output/train'
    languages = ['en', 'de', 'sw']

    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return

    if len(sys.argv) != 2:
        return

    function_name = sys.argv[1]

    # Check if the output directories exist and create them if not
    if function_name == "generate_excel_files":
        output_directory = 'output/xlsx'
    elif function_name == "separate_files":
        output_directory = 'output/ttd'
    elif function_name == "train_translations":
        output_directory = 'output/train'
    else:
        print(f"Function '{function_name}' not recognized.")
        return

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Call the specified function from the 'functions' module
    if function_name == "generate_excel_files":
        functions.create_excel_files(input_dir)
    elif function_name == "separate_files":
        functions.generate_partitioned_jsonl(input_dir)
    elif function_name == "train_translations":
        functions.generate_combined_json(input_dir, output_dir, languages)

if __name__ == "__main__":
    main()
