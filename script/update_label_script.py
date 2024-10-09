import pandas as pd
import os
import glob

"""
This function is used to update the labels in specific columns of a CSV file based on a new label mapping provided in a separate file.
It processes one or more columns and replaces existing values with corresponding new labels from the mapping file.

Arguments:
- columns_to_update: A list of column names (strings) where the labels need to be updated.
- file_path: The path to the input CSV file that contains the data to be modified.
- new_label_file_path: The path to the CSV file that contains the new label mappings. This file must have a 'LABEL' column and a 'New Label' column.

The function reads the input data file, updates the specified columns using the mapping provided, 
and outputs a new CSV file with the modified data. The output file is saved with '_processed' appended to the original filename.

The new label mapping is provided in a separate CSV file, which must contain two columns:
- 'LABEL': The existing label in the data file.
- 'New Label': The new label that will replace the existing label.

Returns:
- A new CSV file with updated labels in the specified columns.
- Prints a log of each label update and the name of the file where the modified data is saved.
"""

def update_label(columns_to_update, file_path, new_label_file_path):
    # Load the DataFrame from the specified file path
    file_path = os.path.abspath(file_path)  # Get absolute path for the file
    df = pd.read_csv(file_path, low_memory=False)  # Read the CSV file into a DataFrame

    # Load the new label mapping from the specified new label file
    new_labels_df = pd.read_csv(new_label_file_path)  # Read new labels CSV
    new_labels_dict = dict(zip(new_labels_df['LABEL'], new_labels_df['New Label']))  # Create a dictionary for label mapping

    # Function to update labels based on the new label mapping
    def label_update(cell_value, column_name, row_idx, col_idx):
        # If the cell is empty, return it unchanged
        if pd.isnull(cell_value):
            return cell_value

        # Split cell value by '|' and initialize a list for updated tokens
        tokens = cell_value.split('|')
        updated_tokens = []

        for token in tokens:
            token = token.strip()  # Remove any leading/trailing whitespace

            if column_name == 'Equivalent Class':
                # For the 'Equivalent Class' column, add single quotes to the label
                token = token.strip("'")
                if token in new_labels_dict:
                    # If token matches a new label, update it
                    updated_tokens.append(f"'{new_labels_dict[token]}'")
                    print(f"Processed cell at row {row_idx + 1}, column {col_idx + 1} ('{column_name}'): {token} -> {new_labels_dict[token]}")
                else:
                    updated_tokens.append(f"'{token}'")  # Keep original token if not found
            else:
                if token in new_labels_dict:
                    updated_tokens.append(new_labels_dict[token])  # Update the token if found in the mapping
                    print(f"Processed cell at row {row_idx + 1}, column {col_idx + 1} ('{column_name}'): {token} -> {new_labels_dict[token]}")
                else:
                    updated_tokens.append(token)  # Keep original token if not found

        # Join the updated tokens back into a string separated by '|'
        return '|'.join(updated_tokens)

    # Apply the label_update function to each specified column in the DataFrame
    for col_idx, column in enumerate(columns_to_update):
        if column in df.columns:  # Check if the column exists in the DataFrame
            df[column] = df.apply(lambda row: label_update(row[column], column, row.name, col_idx), axis=1)

    # Prepare the output file path for the modified DataFrame
    dir_name, base_name = os.path.split(file_path)  # Split the path into directory and base filename
    name, ext = os.path.splitext(base_name)  # Split the filename into name and extension
    output_file = os.path.join(dir_name, f"{name}_processed{ext}")  # Create the output file path

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False, encoding='utf-8')  # Write DataFrame to CSV
    print(f"Modified data saved to {output_file}")


# Example Usage:

# 1. Define the path to your input CSV file (the data file you want to modify).
#    Replace 'your_input_file.csv' with the actual file path to your data file.
file_path = 'your_input_file.csv'

# 2. Define the path to the CSV file containing the new label mappings.
#    Replace 'your_new_label_file.csv' with the actual file path to your label mapping file.
new_label_file_path = 'your_new_label_file.csv'

# 3. Specify the list of column names where label updates are required.
#    Modify the list below with the column names you want to process.
columns_to_update = ['column_1', 'column_2', 'column_3']

# 4. Call the `update_label` function with the specified arguments.
#    This will update the specified columns in the input file based on the new label mappings.
update_label(columns_to_update, file_path, new_label_file_path)

# Example:
# If your file contains a 'Parent (name)' and 'Equivalent Class' column that need updating,
# and your input file is located at 'data/my_data.csv', while your new label file is at 'labels/new_labels.csv',
# you would call the function like this:

# update_label(['Parent (name)', 'Equivalent Class'], 'data/my_data.csv', 'labels/new_labels.csv')

# This will process the specified columns and save the modified data to a new CSV file.
