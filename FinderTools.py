"""
Finder Organizer
Jolin Qiu
"""
import shutil
from tkinter.filedialog import askdirectory
from tkinter import Tk
import os
import hashlib
from pathlib import Path


unique_files = dict()
dest_dir_sfx = "/Users/jolinqiu/Downloads/Sound"
dest_dir_music = "/Users/jolinqiu/Downloads/Sound/Music"
dest_dir_image =  "/Users/jolinqiu/Downloads/Downloaded Videos"
dest_dir_video =  "/Users/jolinqiu/Downloads/Downloaded Images"
dest_dir_pdfs = "/Users/jolinqiu/Downloads/PDFS"


def detect_duplicates(hashed, file):
    """
    In order to detect the duplicate files, define an empty dictionary.
    Add elements to this dictionary and the key of each element
    is going to be file hash and the value is going to be the file path.

    If file hash has already been added to this unique files dictionary
    that means that we have found a duplicate file and we need to delete that file
    :return:
    """
    try:
        if hashed in unique_files:
            if os.path.exists(file):
                os.remove(file)
            print(f"{file} has been deleted")
        else:
            unique_files[hashed] = file
    except Exception as err:
        print(f"{err} ERROR FOUND from removing duplicates")


def move(dest, file):
    file_exists = os.path.exists(file)
    if file_exists:
        shutil.move(file, dest)


def organize_folders(file):
    try:
        if file.name.endswith(".wav") or file.name.endswith("mp3"):
            if (file.stat().st_size < 25000000) or "SFX" in file:
                dest = dest_dir_sfx
            else:
                dest = dest_dir_music
            move(dest, file)
        elif file.name.endswith(".mov") or file.name.endswith(".mp4"):
            dest = dest_dir_video
            move(dest, file)
        elif file.name.endswith(".jpg") or file.name.endswith(".jpeg") or file.name.endswith(".png"):
            dest = dest_dir_image
            move(dest, file)
        elif file.name.endswith(".pdf"):
            dest = dest_dir_pdfs
            move(dest, file)
    except shutil.Error as err:
        # file already exists in that location,
        # continue to move and replace with the latest version
        print(f"{err} ERROR FOUND from organizing files")


def scan_files(files, rmv, organize):
    """
    Organizing:
    call helper function
    Removing:
    Take the content of each file & pass it through a hash function
    which is going to generate a unique string corresponding to a unique file.
    :return:
    """
    for dirPath, dirNames, fileNames in files:
        # list out all the files in each and every subdirectory and the main directory
        # hash ea. file
        for file in fileNames:
            file_path = Path(os.path.join(dirPath, file))
            # True if the file is writable, or False if the file is not writable.
            if os.access(file_path, os.W_OK) == 0:

                # if organize is True:
                #     organize_folders(file_path)
                if rmv is True:
                    # files that are links or symlinks shouldn't be deleted
                    if Path(file_path).is_symlink() is False or Path(file_path).is_file() is False:
                        # convert our file into a md5 hash and get the hash string
                        hashed = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                        detect_duplicates(hashed, file_path)
                    else:
                        break


def main(rmv, organize):
    """
    calls the function to start removing duplicate files
    """
    try:
        Tk().withdraw()
        print("Select a folder & we will search under this umbrella directory for all the duplicate and redundant files.")
        file_path = askdirectory(title="Select a folder")
        list_of_files = os.walk(file_path)
        # file actions
        scan_files(list_of_files, rmv, organize)
        print("completed task(s)")
    except Exception as err:
        print(f"{err} from main call")


if __name__ == "__main__":
    main()
