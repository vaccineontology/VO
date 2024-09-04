import pandas as pd

def replace_names(cell, replacements):
    if isinstance(cell, str):
        parts = cell.replace('|', ',').split(',')
        for i, part in enumerate(parts):
            part = part.strip()  # Strip any extra whitespace
            if part in replacements:
                parts[i] = replacements[part]
        cell = '|'.join(parts)
    return cell
# Read the CSV file
df = pd.read_csv("C:\\Users\\00000\\VO\\src\\templates\\vaccine.csv")

# Read the replacement data from the same Excel file
replacements_df = pd.read_excel("C:\\Users\\00000\\VO\\docs\\VO-cleanup\\term_editor\\term_editor_names.xlsx", sheet_name='Sheet1')

# Convert replacement data to a dictionary with string values
replacements = dict(zip(replacements_df['term editor names'].astype(str), replacements_df['Correct Term Editor'].astype(str)))

# Apply the function to the 'term editor' column
df['term editor'] = df['term editor'].apply(replace_names, args=(replacements,))

# Output the modified DataFrame to a new CSV file
output_file = 'processed_file2.csv'
df.to_csv(output_file, index=False)
print(f"Modified data saved to {output_file}")
