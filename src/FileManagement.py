
"""
Finder file
"""
# needed for os.scandir
import os
# initially imported modules
import shutil
import time

import pymsgbox
# make changes at a time a file is created or modified
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

import FinderTools

file_path = "/Users/jolinqiu/Downloads"

# handling all events
def on_created(event):
    item = event.src_path.lower()
    print(f"{item} has been created!")
    # duplicate made ./IMG_20151231_143053 (2).jpg
    if item.endswith(").pdf") or (").pdf") \
            or item.endswith("copy.pdf") or item.endswith("copy.png"):
        os.remove(item)
    elif item.endswith(".png") or item.endswith(".pdf"):
        print("balls")


def on_deleted(event):
    print(f"ruh roh.... someone deleted {event.src_path}")

def on_modified(event):
    print(f"{event.src_path} has been modified")


# helpers
def on_moved(event):
    print(f"moved {event.src_path} to {event.dest_path}")


def ask_user():
    response_rmv = pymsgbox.prompt("Would you like to scan and remove the current Directory "
                               "for duplicate files?\nDo note that the amount of time this "
                               "takes is variable on the amount of data you have. "
                               "(Y/N)")
    response1_organize = pymsgbox.prompt("Would you like organize your files? (Y/N)")
    if len(response_rmv) == 1 and len(response_rmv) == 1:
        if response_rmv.upper() == "Y" and response1_organize.upper() == "Y":
            FinderTools.main(True, True)
        elif response_rmv.upper() == "Y" and response1_organize.upper() == "N":
            FinderTools.main(True, False)
        elif response_rmv.upper() == "N" and response1_organize.upper() == "Y":
            FinderTools.main(False, True)
        else:
            print("please respond with Y or N to indicate yes or no respectively")


# event handler
if __name__ == "__main__":
    """
    The event handler is the object that will be notified when something happen on the filesystem you are monitoring.
    """
    patterns = ["*"] # the file patterns we want to handle
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    # Initialize event handler
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    # specify to the handler that we want these functions to be called when the corresponding event is raised
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved
    ask_user()
    # Initialize Observer
    observer = Observer()
    observer.schedule(my_event_handler, file_path, recursive=True)
    # Start the observer
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
