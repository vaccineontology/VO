import pandas as pd


def update_label_fn(columns_to_update, file_path, new_label_file_path):
    # Load the DataFrame
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

    # Save the updated DataFrame
    output_file_path = file_path.replace('.csv', '_new.csv')
    df.to_csv(output_file_path, index=False, encoding='utf-8-sig')


file_path = "C:\\Users\\00000\\VO\\src\\templates\\vaccine.csv"
new_label_file_path = 'C:\\Users\\00000\\VO\\src\\sample_newLabel.csv'

# Call the update_label_fn
update_label_fn(['Parent (name)', 'Equivalent Class', 'expresses', 'has part'], file_path, new_label_file_path)
