import csv
from ParseIssues import GetParsedIssues

def save_dicts_to_csv(dict_list, csv_file_path):
    """
    Takes a list of dictionaries and writes them to a CSV file.
    
    :param dict_list: List of dictionaries to be saved.
    :param csv_file_path: The output CSV file path.
    """
    # If the list is empty, there’s nothing to write
    if not dict_list:
        print("The list of dictionaries is empty. No CSV file created.")
        return
    
    # Grab the fieldnames from the keys of the first dictionary
    fieldnames = dict_list[0].keys()
    
    # Open the CSV file in write mode
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        writer.writerows(dict_list)  # Write all rows at once

if __name__ == "__main__":
    # Example usage:
    data = GetParsedIssues()
    
    output_file = "PatchNotes.csv"
    save_dicts_to_csv(data, output_file)
    print(f"CSV file '{output_file}' saved successfully!")
