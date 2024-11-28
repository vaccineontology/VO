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

Contributor: Yuping Zheng 2024-10-30
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


import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.styles import PatternFill


def update_label_re(columns_to_update, file_path, new_label_file_path):
    """
    Update labels in specific columns of a CSV file based on a mapping provided in another CSV file.
    Additionally, generates a log of modifications and highlights changes in an Excel output file.

    Args:
        columns_to_update (list): List of column names to update.
        file_path (str): Path to the original CSV file to process.
        new_label_file_path (str): Path to the CSV file containing old and new labels for mapping.

    Raises:
        FileNotFoundError: If the input file(s) do not exist.
        ValueError: If the input file(s) or column structure is invalid.
    """

    # Resolve absolute paths for better handling of relative paths and cross-platform compatibility
    file_path = os.path.abspath(file_path)
    new_label_file_path = os.path.abspath(new_label_file_path)

    # Step 1: Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    if not os.path.exists(new_label_file_path):
        raise FileNotFoundError(f"The file '{new_label_file_path}' does not exist.")

    # Step 2: Load the original CSV data
    try:
        df = pd.read_csv(file_path, low_memory=False)  # Handle large files with low_memory=False
    except Exception as e:
        raise ValueError(f"Error reading the input file '{file_path}': {e}")

    # Step 3: Load the mapping of old and new labels
    try:
        new_labels_df = pd.read_csv(new_label_file_path)
    except Exception as e:
        raise ValueError(f"Error reading the label file '{new_label_file_path}': {e}")

    # Step 4: Validate the structure of the label mapping file
    if 'LABEL' not in new_labels_df.columns or 'New Label' not in new_labels_df.columns:
        raise ValueError("The new labels file must contain 'LABEL' and 'New Label' columns.")

    # Create a dictionary for quick lookup of new labels based on old labels
    new_labels_dict = dict(zip(new_labels_df['LABEL'], new_labels_df['New Label']))

    # Step 5: Validate that all specified columns exist in the input data
    missing_columns = [col for col in columns_to_update if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following columns are missing in the input data: {', '.join(missing_columns)}")

    # Initialize a log to track modifications for later output
    log_file_path = os.path.splitext(file_path)[0] + "_modifications.txt"
    modifications_log = []

    def label_update(cell_value, column_name, row_idx, col_idx, modified_flags):
        """
        Perform label updates on a single cell based on the new labels dictionary.

        Args:
            cell_value: Value of the cell to process.
            column_name: Name of the column being processed.
            row_idx: Row index of the cell in the DataFrame.
            col_idx: Column index of the cell.
            modified_flags: List tracking whether each row has been modified.

        Returns:
            Updated cell value, or the original if no modification was made.
        """
        if pd.isnull(cell_value):  # Skip processing if the cell is null
            return cell_value

        # Ensure the cell value is a string and strip any extra whitespace
        cell_value = str(cell_value).strip()

        # Skip if the value is empty or explicitly "nan"
        if cell_value.lower() in ('', 'nan'):
            return cell_value

        # Split the cell value into tokens for processing
        tokens = cell_value.split('|')
        updated_tokens = []
        modified = False

        # Process each token and apply replacements if applicable
        for token in tokens:
            updated_token = token
            for key, value in new_labels_dict.items():
                if key in token:
                    updated_token = token.replace(key, value)
                    if not modified:  # Log the first modification in the cell
                        modifications_log.append(
                            f"Row: {row_idx + 1}, Column: '{column_name}', Original: '{cell_value}', Modified: '{updated_token}'"
                        )
                    modified = True
            updated_tokens.append(updated_token)

        # Mark the row as modified if any token was updated
        if modified:
            modified_flags[row_idx] = 'Modified'

        # Return the updated cell value as a joined string
        return '|'.join(updated_tokens)

    # Step 6: Track which rows are modified
    modified_flags = ['Unchanged'] * len(df)

    # Apply label updates to each specified column
    for col_idx, column in enumerate(columns_to_update):
        if column in df.columns:
            df[column] = df.apply(
                lambda row: label_update(row[column], column, row.name, col_idx, modified_flags), axis=1
            )

    # Add a "Modified" column to track row status
    df['Modified'] = modified_flags

    # Step 7: Save the updated data to a new CSV file
    dir_name, base_name = os.path.split(file_path)
    name, ext = os.path.splitext(base_name)
    output_file = os.path.join(dir_name, f"{name}_processed{ext}")
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Modified data saved to {output_file}")

    # Step 8: Save the log of modifications to a text file
    if modifications_log:
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            log_file.write("\n".join(modifications_log))
        print(f"Modifications log saved to {log_file_path}")
    else:
        print("No modifications were made; no log file created.")

    # Step 9: Optional - Highlight modified rows in an Excel file
    try:
        excel_file = os.path.splitext(output_file)[0] + ".xlsx"
        df.to_excel(excel_file, index=False, engine='openpyxl')
        workbook = load_workbook(excel_file)
        sheet = workbook.active

        # Define a yellow fill pattern for highlighting
        fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
        for row_idx, status in enumerate(modified_flags, start=2):  # Start from row 2 (data rows)
            if status == 'Modified':
                for col_idx in range(1, sheet.max_column + 1):  # Apply to all columns
                    sheet.cell(row=row_idx, column=col_idx).fill = fill

        workbook.save(excel_file)
        print(f"Excel file with highlighting saved to {excel_file}")
    except Exception as e:
        print(f"Failed to apply Excel highlighting: {e}")


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

# 4. Call the `update_label_re` function with the specified arguments.
#    This will update the specified columns in the input file based on the new label mappings,
#    generate a log file for modifications, and save the modified data.

update_label_re(columns_to_update, file_path, new_label_file_path)

# Example:
# If your file contains a 'Parent (name)' and 'Equivalent Class' column that need updating,
# and your input file is located at 'data/my_data.csv', while your new label file is at 'labels/new_labels.csv',
# you would call the function like this:

# update_label_re(['Parent (name)', 'Equivalent Class'], 'data/my_data.csv', 'labels/new_labels.csv')

# This will process the specified columns, save the modified data to a new CSV file,
# generate a text file logging all modifications, and highlight modified rows in an Excel file.

