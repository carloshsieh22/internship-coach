import csv
import re

# Function to extract ZIP code from an address, starting from the end of the string
def extract_zip_code(address):
    # Regular expression pattern for ZIP codes, favoring matches at the end of the string
    pattern = re.compile(r'\b\d{5}(?:-\d{4})?\b$')
    match = pattern.search(address)
    return match.group(0) if match else None

def main():
    input_file = 'businesses.csv'  # Replace with your CSV file name
    output_file = 'business_updated.csv'  # Output file name

    # Open the input CSV file and read it
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Get the column names from the input file
        fieldnames = reader.fieldnames
        if fieldnames is None:
            raise ValueError("CSV file has no header row")

        address_column = 'address'  # Replace with your column name

        # Check if the address column exists
        if address_column not in fieldnames:
            raise ValueError(f"Column '{address_column}' not found in the CSV file")

        # Open the output CSV file for writing
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            fieldnames.append('zip_code')  # Add the new column for ZIP codes
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            
            # Write the header to the output file
            writer.writeheader()

            # Process each row in the input file
            for row in reader:
                address = row[address_column]
                zip_code = extract_zip_code(address)
                row['zip_code'] = zip_code  # Add the ZIP code to the row
                writer.writerow(row)

if __name__ == '__main__':
    main()

