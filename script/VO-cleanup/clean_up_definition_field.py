import pandas as pd
import os
import glob

"""
This script is used to clean up and capitalize cell values in specific columns of one or more CSV files. 
You can specify a folder containing CSV files and the columns you want to clean up.
The cleaning process:
- Strips leading/trailing whitespace
- Capitalizes the first letter of the string
- Removes 'A' or 'An' from the start of the string, if applicable
"""

# Function to clean up and capitalize the content of a cell.
# Arguments:
# - cell: The individual cell value to be processed (string).
# Returns:
# - The cleaned-up and capitalized cell value, with leading/trailing whitespace removed,
#   and 'A'/'An' removed from the start if applicable.
def clean_up(cell):
    if isinstance(cell, str):  # Ensure the cell is a string before processing
        cell = cell.strip()  # Remove leading and trailing whitespace
        cell = cell.capitalize()  # Capitalize the first letter
        # Remove leading 'A' or 'An' if applicable
        if cell.startswith('A '):
            cell = cell.lstrip('A')
        elif cell.startswith('An '):
            cell = cell.lstrip('An')
        # Re-strip and capitalize to ensure cleanliness after removal
        cell = cell.strip()
        cell = cell.capitalize()
    return cell


# Function to clean up specified columns in all CSV files within a given folder.
# Arguments:
# - columns_to_clean: A list of column names to be cleaned (strings).
# - folder_path: The path to the folder containing the CSV files to be processed.
# This function applies the `clean_up` function to each specified column in all matching files.
def strip_capitalize(columns_to_clean, folder_path):
    # Find all CSV files in the specified folder
    file_paths = glob.glob(os.path.join(folder_path, "*.csv"))
    
    if len(file_paths) == 0:  # Handle the case where no CSV files are found
        file_paths = [folder_path]  # Assume the path is to a single file if no folder is found

    # Process each CSV file in the folder
    for file_path in file_paths:
        df = pd.read_csv(file_path)  # Load the CSV into a pandas DataFrame

        # Apply the clean_up function to each specified column
        for column in columns_to_clean:
            if column in df.columns:  # Check if the column exists in the DataFrame
                df[column] = df[column].apply(clean_up)  # Apply the cleaning function to the column

        # Construct the output file path by appending '_processed' to the original file name
        dir_name, base_name = os.path.split(file_path)
        name, ext = os.path.splitext(base_name)
        output_file = os.path.join(dir_name, f"{name}_processed{ext}")

        # Save the modified DataFrame to a new CSV file
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Modified data saved to {output_file}")


# Example Usage:
# To clean up and capitalize columns in all CSV files within a folder:
# 
# 1. Define the path to the folder containing the CSV files.
# 2. Specify the columns you want to clean up in the CSV files.
# 3. Call the `strip_capitalize` function.
#
# Example:
'''
folder_path = 'path/to/your/csv_folder'
columns_to_clean = ['definition', 'LABEL']  # Replace with the actual column names you want to clean

strip_capitalize(columns_to_clean, folder_path)
'''

# This will:
# - Process all CSV files in the specified folder.
# - Clean up the specified columns by stripping whitespace, capitalizing the first letter,
#   and removing 'A'/'An' where applicable.
# - Save the processed files with '_processed' appended to the original file name.
