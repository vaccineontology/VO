import pandas as pd
import os
import glob
"""This code script is used to retrieve information with prefix, for instance: ‘CVX’, ‘CXX code’, ‘CVX code’ ,
 which eventually will output a processed file"""
def extract_identifiers(x, *identifiers):
    if isinstance(x, str):
        parts = x.replace('|', ';').split(';')
        identifier_values = {identifier: [] for identifier in identifiers}
        non_identifier_parts = []

        for part in parts:
            for identifier in identifiers:
                if identifier in part:
                    identifier_values[identifier].append("".join(filter(str.isdigit, part)))
                    break
            else:
                non_identifier_parts.append(part)

        identifier_strings = {identifier: ';'.join(values) if values else '' for identifier, values in
                              identifier_values.items()}
        non_identifier_string = '|'.join(non_identifier_parts)

        combined_string = '|'.join([value for value in identifier_strings.values() if value])
        return non_identifier_string, combined_string
    else:
        return x, None

"""input argument: file path, usually .csv file, which is the file you need to process, *identifiers, which refers to the prefix you 
want to detect, the process_column is the column you want to process, the new columns is the standard column name you want, which 
means the processed column name you want."""
def improved_prefix_extracter(file_path, *identifiers, process_columns, new_columns):

    file_path = os.path.abspath(file_path)
    df = pd.read_csv(file_path,low_memory = False)

    df[f"{process_columns}_ed"], df[f"{new_columns}"] = zip(
        *df[f"{process_columns}"].apply(lambda x: extract_identifiers(x, *identifiers)))

    dir_name, base_name = os.path.split(file_path)
    name, ext = os.path.splitext(base_name)
    output_file = os.path.join(dir_name, f"{name}_processed{ext}")

    # Save the modified DataFrame to a new file
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Modified data saved to {output_file}")

#sample usage
'''improved_prefix_extracter("C:\\Users\\00000\\VO\\src\\templates\\vaccine.csv", 'CVX', 'CXX code', 'CVX code'
                          , process_columns = 'seeAlso', new_columns = 'CVX code')
improved_prefix_extracter("C:\\Users\\00000\\VO\\src\\templates\\vaccine_component.csv", 'PMID', 'pmid',
                          process_columns = 'seeAlso', new_columns = 'PMID')'''