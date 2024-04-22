import csv
import glob

def process_file(filename):
    term_editors = []
    try:
        with open(filename, 'r', encoding='utf-8') as f_in:
            reader = csv.DictReader(f_in)
            next(reader)
            for row in reader:
                editors = row['term editor']
                editors = editors.replace('|', ',').split(',')
                editors = [editor.strip() for editor in editors]
                term_editors.extend(editors)
        return set(term_editors), None
    except UnicodeDecodeError:
        return None, filename

# Specify the path to your CSV files
path = r'C:\Users\00000\Downloads\VO\src\templates\*.csv'

# Get a list of all CSV files in the specified directory
csv_files = glob.glob(path)

# Process each file
all_term_editors = set()
non_utf8_files = []
for file in csv_files:
    term_editors, non_utf8_file = process_file(file)
    if term_editors is not None:
        all_term_editors.update(term_editors)
    if non_utf8_file is not None:
        non_utf8_files.append(non_utf8_file)

print("Files not encoded in UTF-8:", non_utf8_files)

# Step 1: Read the CSV file
with open('C:\\Users\\00000\\Downloads\\VO\\src\\templates\\cancer_vaccine.csv', 'r', encoding='latin-1') as f_in:
    reader = csv.DictReader(f_in)
    term_editors = []
    next(reader)
    # Step 2: Process each row
    for row in reader:
        editors = row['term editor']
        # Split the string by '|' or ','
        editors = editors.replace('|', ',').split(',')
        # Remove leading or trailing whitespace
        editors = [editor.strip() for editor in editors]
        term_editors.extend(editors)

# Step 3: Get unique term editors
unique_term_editors = set(term_editors)


all_term_editors.update(unique_term_editors)

print("Unique term editors across all files:", all_term_editors)

print("Total unique term editors:", len(all_term_editors))





