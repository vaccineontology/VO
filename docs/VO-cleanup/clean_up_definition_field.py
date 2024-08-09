import pandas as pd
import os
from clean_up_data import clean_up_article

def clean_up(cell):
    if isinstance(cell, str):
        cell = cell.strip()
        cell = cell.capitalize()
    return cell


def clean_up_fn(columns_to_clean, file_paths):
    for file_path in file_paths:
        df = pd.read_csv(file_path)

        # Apply the clean_up function to each specified column
        for column in columns_to_clean:
            if column in df.columns:
                df[column] = df[column].apply(clean_up_article)

        # Construct the output file path
        dir_name, base_name = os.path.split(file_path)
        name, ext = os.path.splitext(base_name)
        output_file = os.path.join(dir_name, f"{name}_processed{ext}")

        # Save the modified DataFrame to a new file
        df.to_csv(output_file, index=False)
        print(f"Modified data saved to {output_file}")


# Example usage
clean_up_fn(['definition', 'LABEL'], ["C:\\Users\\00000\\VO\\docs\\VO-cleanup\\term_editor\\processed_file2.csv",
                                      'C:\\Users\\00000\\VO\\src\\templates\\vaccine_adjuvant.csv'])
