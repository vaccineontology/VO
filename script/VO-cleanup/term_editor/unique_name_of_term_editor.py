import csv
import glob
import os

# Function to process a CSV file and extract unique values from a user-specified column.
# Arguments:
# - filename: Path to the CSV file to be processed.
# - column_name: Name of the column from which to extract unique values.
# Returns:
# - A set of unique values from the specified column.
# - None if there is a Unicode decoding issue or column not found, along with the filename.
def process_file(filename, column_name):
    column_values = []  # To store the values from the specified column
    try:
        with open(filename, 'r', encoding='utf-8') as f_in:
            reader = csv.DictReader(f_in)
            next(reader)  # Skip header row
            for row in reader:
                # Retrieve data from the user-specified column
                column_data = row.get(column_name, "")
                column_data = column_data.replace('|', ',').split(',')  # Replace pipe and split by commas
                column_data = [item.strip() for item in column_data]  # Strip whitespace from values
                column_values.extend(column_data)  # Collect values from the column
        return set(column_values), None  # Return unique values as a set
    except UnicodeDecodeError:
        return None, filename  # Handle Unicode errors (e.g., non-UTF-8 encoded files)
    except KeyError:
        print(f"Column '{column_name}' not found in {filename}")  # Handle missing column error
        return None, filename


# Function to process all CSV files in a folder and extract unique values from a specified column.
# Arguments:
# - folder_path: Path to the directory containing CSV files or the file path itself.
# - column_name: Name of the column from which to extract and replace unique values.
# This function handles multiple CSV files, checks for encoding issues, and aggregates unique values.
def replace_unique_name_in_column(folder_path, column_name):
    # Find all CSV files in the specified directory (or use a single file if directory not found)
    file_paths = glob.glob(os.path.join(folder_path, "*.csv"))  # Get all CSV files in the folder
    if len(file_paths) == 0:  # Handle the case when no CSV files are found
        file_paths = [folder_path]  # Assume the folder_path is actually a file

    # Initialize containers for unique values and non-UTF-8 files
    all_values = set()  # To store unique values across all files
    non_utf8_files = []  # To track files that are not encoded in UTF-8

    # Process each file to extract unique values from the specified column
    for file in file_paths:
        values, non_utf8_file = process_file(file, column_name)
        if values is not None:  # If no errors, update the set with unique values
            all_values.update(values)
        if non_utf8_file is not None:  # Track files that had issues
            non_utf8_files.append(non_utf8_file)

    # Output the list of files that were not in UTF-8 encoding
    print("Files not encoded in UTF-8:", non_utf8_files)

    # Output the unique values found in the specified column across all processed files
    print(f"Unique values in column '{column_name}' across all files:", all_values)
    print(f"Total unique values in column '{column_name}':", len(all_values))


# Example Usage:
# Call the `replace_unique_name_in_column` function with the following arguments:
# - folder_path: Path to the directory containing CSV files or a specific CSV file.
# - column_name: The column in which to find unique values.
# 
# Example:
# replace_unique_name_in_column('path/to/your/csv/folder', 'column_name_to_process')

# The following example processes a single CSV file and extracts unique values from the "term editor" column:
replace_unique_name_in_column('path/to/your/csv_file.csv', 'term editor')
