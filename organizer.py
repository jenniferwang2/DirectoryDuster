import os
from pathlib import Path
from filecmp import cmp
  
subDirectories = {
        "DOCUMENTS":[".pdf",".docx",".txt"],
        "AUDIO":[".m4a",".m4b",".mp3"],
        "IMAGES":[".jpg",".jpeg",".png"],
        "CSVS":[".csv"],
        "CODE":[".py", ".html", ".java"]
        }

def pick_directory(value):
    '''
    value: str contain extension of the file.
    return name of the category who defined before.
    e.g. value = '.pdf' so the function will return DOCUMENTS.
    '''
    for category, extension in subDirectories.items():
        for suffix in extension:
            if suffix == value:
                return category

def organizeDir():
    '''
    this function will scan any files in the same directory, and then
    look at every extension of files and move that file to the exact category from calling the pickDirectory function.
    '''
    for item in os.scandir():

        #just looking for file, skip the directory
        if item.is_dir():
                continue

        filePath = Path(item)
        fileType = filePath.suffix.lower()
        directory = pick_directory(fileType)

        #just skip, if the file extension not defined.
        if directory == None:
            continue

        directoryPath = Path(directory)
        #make new directory if the category's directory not found.
        if directoryPath.is_dir() != True:
                directoryPath.mkdir()
        filePath.rename(directoryPath.joinpath(filePath))

  
# list of all documents
path = input("What directory do you want to clean? Copy and paste path here. To get current path, enter 'pwd' into terminal")
DATA_DIR = Path(path)
files = sorted(os.listdir(DATA_DIR))
  
# List having the classes of documents
# with the same content
duplicateFiles = []
  
# comparison of the documents
for file_x in files:
  
    if_dupl = False
  
    for class_ in duplicateFiles:
        # Comparing files having same content using cmp()
        # class_[0] represents a class having same content
        if_dupl = cmp(
            DATA_DIR / file_x,
            DATA_DIR / class_[0],
            shallow=False
        )
        if if_dupl:
            class_.append(file_x)
            break
  
    if not if_dupl:
        duplicateFiles.append([file_x])
#        continue
  
# Print results
print(duplicateFiles)
organizeDir()
