import csv
import os

from get_from_jira import GetParsedIssues

def GetUniqueFilepath(directory, filename):
    #thanks chatgpt
    name, ext = os.path.splitext(filename)
    candidate = os.path.join(directory, filename)
    counter = 1

    while os.path.exists(candidate):
        candidate = os.path.join(directory, f"{name}_{counter}{ext}")
        counter += 1

    return candidate

def SaveAsCsv(dict_list, output_path,file_name):
    #mostly thanks chatgpt
    os.makedirs(output_path, exist_ok=True)
    unique_path = GetUniqueFilepath(output_path, file_name)

    if not dict_list:
        print("Failed at CSV creation: no issues found")
        return
    fieldnames = dict_list[0].keys()
    
    with open(unique_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(dict_list)


def SaveAsMd(mdText,output_path,file_name):
    os.makedirs(output_path, exist_ok=True)
    unique_path = GetUniqueFilepath(output_path, file_name)



if __name__ == "__main__":
    data = GetParsedIssues()
    output_file = "PatchNotes.csv"
    SaveAsCsv(data, output_file)
    print(f"CSV file '{output_file}' saved successfully!")
