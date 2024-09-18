import pandas as pd
import os
import glob
# this code is used to replace ‘term label’ via correct term label
def update_label(columns_to_update, file_path, new_label_file_path):
    # Load the DataFrame
    file_path = os.path.abspath(file_path)
    df = pd.read_csv(file_path, low_memory=False)

    # Load the new label mapping
    new_labels_df = pd.read_csv(new_label_file_path)
    new_labels_dict = dict(zip(new_labels_df['LABEL'], new_labels_df['New Label']))

    # Function to update labels based on the new label mapping
    def label_update(cell_value, column_name, row_idx, col_idx):
        if pd.isnull(cell_value):
            return cell_value

        tokens = cell_value.split('|')
        updated_tokens = []

        for token in tokens:
            token = token.strip()

            if column_name == 'Equivalent Class':
                # Add single quotes to the label for Equivalent Class column
                token = token.strip("'")
                if token in new_labels_dict:
                    updated_tokens.append(f"'{new_labels_dict[token]}'")
                    print(
                        f"Processed cell at row {row_idx + 1}, column {col_idx + 1} ('{column_name}'): {token} -> {new_labels_dict[token]}")
                else:
                    updated_tokens.append(f"'{token}'")
            else:
                if token in new_labels_dict:
                    updated_tokens.append(new_labels_dict[token])
                    print(
                        f"Processed cell at row {row_idx + 1}, column {col_idx + 1} ('{column_name}'): {token} -> {new_labels_dict[token]}")
                else:
                    updated_tokens.append(token)

        return '|'.join(updated_tokens)

    # Apply the label_update function to the specified columns
    for col_idx, column in enumerate(columns_to_update):
        if column in df.columns:
            df[column] = df.apply(lambda row: label_update(row[column], column, row.name, col_idx), axis=1)

    dir_name, base_name = os.path.split(file_path)
    name, ext = os.path.splitext(base_name)
    output_file = os.path.join(dir_name, f"{name}_processed{ext}")

    # Save the modified DataFrame to a new file
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Modified data saved to {output_file}")


#the first argument is a list containing the category you want to process, and then the file_path and the label list you want to use
#  below is an example usage
'''file_path = "C:\\Users\\00000\\VO\\src\\templates\\vaccine.csv"
new_label_file_path = 'C:\\Users\\00000\\VO\\src\\sample_newLabel.csv'

# Call the update_label_fn
update_label(['Parent (name)', 'Equivalent Class', 'expresses', 'has part'], file_path, new_label_file_path)'''
