'''import pandas as pd

def replace_names(cell, replacements):
    if isinstance(cell, str):
        parts = cell.replace('|', ',').split(',')
        for i, part in enumerate(parts):
            print(part)
            part = part.strip()  # Strip any extra whitespace
            if part in replacements:
                parts[i] = replacements[part]
        cell = '|'.join(parts)
    return cell

# Example DataFrame
data = {'term editor': ['John', 'Alice,Oliver He  ', 'Kate|Sam']}
df = pd.DataFrame(data)

# Example replacement data from Excel file

correct_names_data = {
    'Wrong Term Editor': [  'Oliver'],
    'Correct Term Editor': [  'Oliver He']
}
# Convert replacement data to a dictionary
replacements = dict(zip(correct_names_data['Wrong Term Editor'], correct_names_data['Correct Term Editor']))

# Apply the function to the DataFrame column
df['term editor'] = df['term editor'].apply(replace_names, args=(replacements,))

print(df)
'''
txt = ",,,,,rrttgg  .....banana....rrr"

txt = txt.strip(",")
x = txt.capitalize()

print(x)

