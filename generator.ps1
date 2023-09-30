# Define the Python script to run (main.py in this case)
$pythonScript = "main.py"

# Define the function to execute (e.g., "generate_excel_files", "separate_files", or "train_translations")
$functionName = $args[0]

# Run the Python script using the python command with the chosen function as an argument
python $pythonScript $functionName

python $pythonScript

#./generator.ps1 generate_excel_files
#./generator.ps1 separate_files
#./generator.ps1 train_translations
#./generator.ps1


