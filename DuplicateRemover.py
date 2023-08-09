"""
We need to make a way for us to select the folder in which we want to do
this cleaning process so every time we run the code we should get a file
dialog to select a folder
-> Tkinter library: provides a method called “askdirectory” which can be used
to ask user to choose a directory.

The hash string is going to be a fixed size and the size is going to depend on the type of hash function we are using. We have many hash functions like md5, SHA1 or SHA 256, and many others. In this article, we’ll use the md5 hash and it’s always going to produce a hash value of 32 characters long irrespective of the size of the file & type of the file.
In order to detect duplicate files and then delete those files, we are going to maintain a python dictionary.
We are going to pass the hash string of each and every file inside every subfolder of the root directory as keys of dictionary & file paths as values of the dictionary.
Every time while inserting a new file record we will check if we are getting any duplicate entries in our dictionary. If we find any duplicate file we will take the path of the file and delete that file.
"""

from tkinter.filedialog import askdirectory

from tkinter import Tk
import os
import hashlib
from pathlib import Path

unique_files = dict()

def detect_duplicates(hashed, file):
    """
    In order to detect the duplicate files, define an empty dictionary.
    Add elements to this dictionary and the key of each element
    is going to be file hash and the value is going to be the file path.

    If file hash has already been added to this unique files dictionary
    that means that we have found a duplicate file and we need to delete that file
    :return:
    """
    if hashed in unique_files:
        os.remove(file)
    else:
        unique_files[hashed] = file
        print(f"{file} has been deleted")


def hash_file(files):
    """
    Take the content of each file & pass it through a hash function
    which is going to generate a unique string corresponding to a unique file.
    :return:
    """
    for dirPath, dirNames, fileNames in files:
        # list out all the files in each and every subdirectory and the main directory
        # hash ea. file
        for file in fileNames:
            # In order to open a file we need to first have the path to it
            # os.path.join() just concatenates
            file_path = Path(os.path.join(dirPath, file))
            # files that are links or symlinks shouldn't be deleted
            if Path(file_path).is_symlink() is False or Path(file_path).is_file() is False:
                # So we’ll say open the file using file path in read mode.
                # This will convert our file into a md5 hash.
                # hexdigest method gets the hash string
                hashed = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                detect_duplicates(hashed, file_path)
            else:
                break


if __name__ == "__main__":
    Tk().withdraw()
    print("select a folder & we will search under this umbrella directory for all the duplicate and redundant files.")
    file_path = askdirectory(title="Select a folder")
    # # Directory Path:  /Users/jolinqiu/Downloads/drive-download-20220425T185745Z-001/7 pir8s golds
    #     # 	File Name:  .DS_Store
    #     # 	File Name:  MoleMash2.apk
    #     # 	File Name:  pir8Gold.aia
    #     # 	File Name:  pir8Gold.apk
    #     # 	File Name:  wakeUp.mp3
    list_of_files = os.walk(file_path)
    # remove duplicate files
    hash_file(list_of_files)
