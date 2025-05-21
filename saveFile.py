import csv
import os

def GetUniqueFilepath(directory, filename):
    #thanks chatgpt
    name, ext = os.path.splitext(filename)
    candidate = os.path.join(directory, filename)
    counter = 1

    while os.path.exists(candidate):
        candidate = os.path.join(directory, f"{name}_{counter}{ext}")
        counter += 1

    return candidate

def SaveAsMd(outputDir,file_name,mdText):
    os.makedirs(outputDir, exist_ok=True)
    if not fileName.endswith('.md'): fileName += '.md'
    uniquePath = GetUniqueFilepath(outputDir, file_name)
    with open(uniquePath, "w", encoding="utf-8") as md_file:
        md_file.write(mdText)

def SaveAsCsv(outputDir,fileName,ticketDict):
    #check if has csv extension, if not add it # tick
    #check if outputs folder exists, if not create it
    # if it does exist validate uniqueness of file name, if not unique, modify
    #save file

    os.makedirs(outputDir, exist_ok=True)
    if not fileName.endswith('.csv'): fileName += '.csv'
    uniquePath = GetUniqueFilepath(outputDir,fileName)
    if not ticketDict: print("ERROR: no tickets were found"); return

    fieldnames = ticketDict[0].keys()
    
    with open(uniquePath, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(ticketDict)
    print(f"\n\tsaved to {uniquePath}")
