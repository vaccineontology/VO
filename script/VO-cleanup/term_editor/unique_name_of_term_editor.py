import csv
import glob
import os


# File used to find the unique words in a user-specified column
def process_file(filename, column_name):
    column_values = []
    try:
        with open(filename, 'r', encoding='utf-8') as f_in:
            reader = csv.DictReader(f_in)
            next(reader)  # Skip header
            for row in reader:
                # Access the user-specified column
                column_data = row.get(column_name, "")
                column_data = column_data.replace('|', ',').split(',')  # Replace pipe and split by comma
                column_data = [item.strip() for item in column_data]  # Strip whitespace
                column_values.extend(column_data)
        return set(column_values), None
    except UnicodeDecodeError:
        return None, filename
    except KeyError:
        print(f"Column '{column_name}' not found in {filename}")
        return None, filename


# Generalized function to replace unique names in the specified column across all CSV files
def replace_unique_name_in_column(folder_path, column_name):
    # Get a list of all CSV files in the specified directory
    file_paths = glob.glob(os.path.join(folder_path, "*.csv"))
    if len(file_paths) == 0:
        file_paths = [folder_path]

    # Process each file
    all_values = set()
    non_utf8_files = []
    for file in file_paths:
        values, non_utf8_file = process_file(file, column_name)
        if values is not None:
            all_values.update(values)
        if non_utf8_file is not None:
            non_utf8_files.append(non_utf8_file)

    print("Files not encoded in UTF-8:", non_utf8_files)

    # Output unique values across all files
    print(f"Unique values in column '{column_name}' across all files:", all_values)

    print(f"Total unique values in column '{column_name}':", len(all_values))


# Example usage
replace_unique_name_in_column(r"C:\Users\00000\VO\src\templates\vaccine_adjuvant.csv", "term editor")
# input argument first is the folder path, second is the column you want to process