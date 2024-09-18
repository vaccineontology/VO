import pandas as pd
import os
import glob

def clean_up(cell):
    if isinstance(cell, str):
        cell = cell.strip()
        cell = cell.capitalize()
        if cell.startswith('A ') == True:
            cell = cell.lstrip('A')
        elif cell.startswith('An ') == True:
            cell = cell.lstrip('An')
        cell = cell.strip()
        cell = cell.capitalize()
    return cell


def clean_up_fn(columns_to_clean, folder_path):
    # Use glob to find all CSV files in the folder
    file_paths = glob.glob(os.path.join(folder_path, "*.csv"))
    print(file_paths)
    for file_path in file_paths:
        df = pd.read_csv(file_path)

        # Apply the clean_up function to each specified column
        for column in columns_to_clean:
            if column in df.columns:
                df[column] = df[column].apply(clean_up)

        # Construct the output file path
        dir_name, base_name = os.path.split(file_path)
        name, ext = os.path.splitext(base_name)
        output_file = os.path.join(dir_name, f"{name}_processed{ext}")

        # Save the modified DataFrame to a new file
        df.to_csv(output_file, index=False, encoding = 'utf-8')
        print(f"Modified data saved to {output_file}")


# Example usage: Process all CSV files in a folder
folder_path = "C:\\Users\\00000\\VO\\docs\\VO-cleanup\\term_editor"
# first argument is of the type list
clean_up_fn(['definition', 'LABEL'], folder_path)
