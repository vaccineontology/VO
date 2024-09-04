import pandas as pd

def extract_pmid(value):
    # Check if the value is a string
    if isinstance(value, str):
        # Split the value by '|' and ','
        parts = value.replace('|', ';').split(';')
        # Initialize a list to store PMID numbers
        pmid_numbers = []
        # Initialize a list to store non-PMID parts
        non_pmid_parts = []
        # Iterate over the parts
        for part in parts:
            # Check if the part contains "PMID" or "pmid"
            if "PMID:" in part or "pmid:" in part:
                #print(part)
                # Extract the PMID number
                pmid_number = "".join(filter(str.isdigit, part))
                # Append the PMID number to the list of PMID numbers
                pmid_numbers.append(pmid_number)
                #print(pmid_number)
            else:
                # Append the part to the list of non-PMID parts
                non_pmid_parts.append(part)

        # Join the non-PMID parts with '|' separator
        non_pmid_string = '|'.join(non_pmid_parts)
        # Join the PMID numbers with ';' separator
        pmid_string = ';'.join(pmid_numbers)
        #print(pmid_string)
        return non_pmid_string, pmid_string
    else:
        return value, None


# Read the CSV file into a DataFrame
df = pd.read_csv("C:\\Users\\00000\\VO\\src\\templates\\vaccine_component.csv")

# Create a new column "seeAlso_ed" containing the rest of the value without PMID numbers
df["seeAlso_ed"], df["PMID"] = zip(*df["seeAlso"].apply(extract_pmid))

# Save the modified DataFrame to a new CSV file
df.to_csv("processed_file.csv", index=False)


