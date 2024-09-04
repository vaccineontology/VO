import pandas as pd

def clean_up_article(cell):
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

# Read the CSV file
df = pd.read_csv("processed_file3.csv")

# Apply the function to the 'term editor' column
df['definition'] = df['definition'].apply(clean_up_article)

# Output the modified DataFrame to a new CSV file
output_file = 'processed_file_4.csv'
df.to_csv(output_file, index=False)
print(f"Modified data saved to {output_file}")