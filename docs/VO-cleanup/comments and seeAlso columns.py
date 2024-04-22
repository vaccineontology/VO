import csv
import glob

def process_file(filename):
    results = set()
    unique_values = set()
    try:
        with open(filename, 'r', encoding='utf-8') as f_in:
            reader = csv.DictReader(f_in)
            next(reader)  # Skip the header row
            for row in reader:
                if 'comment' in row or 'seeAlso' in row:
                    combined_values = (row.get('comment') or '') + ',' + (row.get('seeAlso') or '')
                    values = combined_values.replace('|', ',').split(',')
                    unique_value = tuple(value.strip() for value in values if value.strip())
                    if unique_value:  # Check if unique_value is not empty
                        unique_values.add(unique_value)
                    for value in values:
                        if any(key in value.strip() for key in ["VIOLIN ID", "violinID", "VIOLIN Vaccine ID"]):
                            value = value.split(':')[-1].strip()  # Extract value after ":"
                            results.add(value)
        return unique_values, results, None
    except UnicodeDecodeError:
        return None, None, filename

# Specify the paths to your CSV files
paths = [
    r"C:\Users\00000\VO\src\templates\vaccine.csv",
    r"C:\Users\00000\VO\src\templates\vaccine_component.csv",
    r"C:\Users\00000\VO\src\templates\vaccine_adjuvent.csv"
]

# Process each file
all_unique_values = set()
all_results = set()
non_utf8_files = []
for path in paths:
    csv_files = glob.glob(path)
    for file in csv_files:
        unique_values, results, non_utf8_file = process_file(file)
        if unique_values is not None and results is not None:
            all_unique_values.update(unique_values)
            all_results.update(results)
        if non_utf8_file is not None:
            non_utf8_files.append(non_utf8_file)

# Write results to output.txt
with open('output.txt', 'w', encoding='utf-8') as txt_file:
    txt_file.write("Files not encoded in UTF-8:\n")
    for filename in non_utf8_files:
        txt_file.write(filename + '\n')

    txt_file.write("\nUnique values:\n")
    for value in all_unique_values:
        txt_file.write(str(value) + '\n')

    txt_file.write("\nResults:\n")
    for result in all_results:
        txt_file.write(str(result) + '\n')

print("Output written to output.txt")
