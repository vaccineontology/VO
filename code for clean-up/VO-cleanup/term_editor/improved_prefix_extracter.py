import pandas as pd
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
want to detect."""
def improved_seperate_columns(file_path, *identifiers, process_columns = None):
    '''df = pd.read_csv("/src/templates/vaccine.csv")

    # Example usage
    df["seeAlso_ed"], df["CVX code"] = zip(
        *df["seeAlso"].apply(lambda x: extract_identifiers(x, 'CVX', 'CXX code', 'CVX code')))

    df.to_csv("processed_file.csv", index=False)'''
    df = pd.read_csv(file_path)

    df["seeAlso_ed"], df["CVX code"] = zip(
        *df["seeAlso"].apply(lambda x: extract_identifiers(x, *identifiers)))

    df.to_csv("processed_file1.csv", index=False)

#sample usage
improved_seperate_columns("C:\\Users\\00000\\VO\\src\\templates\\vaccine.csv", 'CVX', 'CXX code', 'CVX code')