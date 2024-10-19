import pandas as pd
import os
import glob

"""
This script is used to extract and process information with specific prefixes (e.g., 'CVX', 'CXX code', 'CVX code')
from a specified column in a CSV file, and outputs a processed file with the extracted identifiers.
"""

# Function to extract identifiers based on specific prefixes (identifiers) from a given string.
# Arguments:
# - x: The string to process (usually from a column in the CSV).
# - *identifiers: The list of prefixes to detect (e.g., 'CVX', 'PMID').
# Returns:
# - A tuple containing:
#   - non_identifier_string: The remaining string after extracting all identifier-related parts.
#   - combined_string: A string combining all extracted identifier values.
def extract_identifiers(x, *identifiers):
    if isinstance(x, str):
        # Split the string into parts using ';' as a separator (after replacing '|' with ';')
        parts = x.replace('|', ';').split(';')
        identifier_values = {identifier: [] for identifier in identifiers}  # Dictionary to store identifier values
        non_identifier_parts = []  # List to store parts that don't match any identifier

        # Loop through each part of the string to check for identifiers
        for part in parts:
            for identifier in identifiers:
                if identifier in part:  # Check if the part contains the identifier
                    # Extract the digits from the part and store in the corresponding identifier list
                    identifier_values[identifier].append("".join(part))
                    break
            else:
                non_identifier_parts.append(part)  # If no identifier matches, add to non_identifier_parts

        # Create strings for each identifier, joining the extracted values with ';'
        identifier_strings = {identifier: ';'.join(values) if values else '' for identifier, values in
                              identifier_values.items()}
        # Combine the non-identifier parts back into a string, using '|' as a separator
        non_identifier_string = '|'.join(non_identifier_parts)

        # Combine all identifier values into a single string
        combined_string = '|'.join([value for value in identifier_strings.values() if value])
        return non_identifier_string, combined_string
    else:
        return x, None  # Return original value if the input is not a string


"""
Function to process a CSV file by extracting identifiers (based on specified prefixes) from a given column,
and creating new columns with the extracted information.

Arguments:
- file_path: The path to the input CSV file.
- *identifiers: The prefixes to detect in the column (e.g., 'CVX', 'PMID').
- process_columns: The name of the column you want to process for prefix extraction.
- new_columns: The name of the new column that will store the extracted identifier information.
"""
def improved_prefix_extracter(file_path, *identifiers, process_columns, new_columns):
    # Convert relative path to absolute path for better file handling
    file_path = os.path.abspath(file_path)
    
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path, low_memory=False)

    # Apply the extract_identifiers function to the specified column, creating two new columns
    df[f"{process_columns}_ed"], df[f"{new_columns}"] = zip(
        *df[f"{process_columns}"].apply(lambda x: extract_identifiers(x, *identifiers)))

    # Create an output file path by appending '_processed' to the original file name
    dir_name, base_name = os.path.split(file_path)
    name, ext = os.path.splitext(base_name)
    output_file = os.path.join(dir_name, f"{name}_processed{ext}")

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Modified data saved to {output_file}")


# Example Usage:
# The following demonstrates how to use the `improved_prefix_extracter` function:

# Define the path to your input CSV file, the prefixes you want to detect, and the columns to process.
# Replace 'path/to/your/csv_file.csv' with your actual CSV file path.

'''
improved_prefix_extracter('path/to/your/csv_file.csv', 'CVX', 'CXX code', 'CVX code',
                          process_columns='seeAlso', new_columns='CVX code')

improved_prefix_extracter('path/to/your/csv_file.csv', 'PMID', 'pmid',
                          process_columns='seeAlso', new_columns='PMID')
'''

# In these examples:
# - 'process_columns' is the name of the column in the input CSV from which prefixes are extracted.
# - 'new_columns' is the name of the new column that will store the extracted identifier information.
# - The extracted data is saved to a new CSV file with '_processed' appended to the original file name.
