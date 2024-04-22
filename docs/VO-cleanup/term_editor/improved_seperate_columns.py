import pandas as pd

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


df = pd.read_csv("C:\\Users\\00000\\VO\\src\\templates\\vaccine.csv")

# Example usage
df["seeAlso_ed"], df["CVX code"] = zip(
    *df["seeAlso"].apply(lambda x: extract_identifiers(x, 'CVX', 'CXX code', 'CVX code')))

df.to_csv("processed_file.csv", index=False)