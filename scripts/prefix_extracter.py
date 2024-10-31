import pandas as pd
import os
import glob
"""
This script is used to extract and process information with specific prefixes (e.g., 'CVX', 'CXX code', 'CVX code')
from a specified column in a CSV file, and outputs a processed file with the extracted identifiers.

Contributor: Yuping Zheng 2024-10-30
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
"""
