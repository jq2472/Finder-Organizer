
"""
Observer: the class that watches for any file system changes
and notifies the event handler - doesn't participate in any modification/action

Event Handler: So far I've seen in the if = main function,
    the actual event-handling can be separate functions

Note: PatternMatchingEventHandler inherits from the FileSystemEventHandler class
 and is used to do just that
 methods of this class:
    on_any_event: will be executed for any event.
    on_created: Executed when a file or a directory is created.
    on_modified: Executed when a file is modified or a directory renamed.
    on_deleted: Executed when a file or directory is deleted.
    on_moved: Executed when a file or directory is moved.

    Each one of those methods receives the event object as first parameter, and the event object has 3 attributes:
        event_type: modified/created/moved/deleted
        is_directory: True/False
        src_path: path/to/observe/file
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

import DuplicateRemover

filePath = "/Users/jolinqiu/Downloads"
dest_dir_sfx = "/Users/jolinqiu/Downloads/Sound"
dest_dir_music = "/Users/jolinqiu/Downloads/Sound/Music"
dest_dir_image =  "/Users/jolinqiu/Downloads/Downloaded Videos"
dest_dir_video =  "/Users/jolinqiu/Downloads/Downloaded Images"

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


def move(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists:
        shutil.move(entry, dest)


def on_modified(event):
    # os.scandir() returns a Python iterable containing the names of the files
    #  and subdirectories in the directory given by the path argument:
    #  items = os.scandir(filePath)
    with os.scandir(filePath) as items:
        for item in items:
            name = item.name
            dest = filePath
            if name.endswith(".wav") or name.endswith("mp3"):
                if (item.stat().st_size < 25000000) or "SFX" in name:
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move(dest, item, name)
            elif name.endswith(".mov") or name.endswith(".mp4"):
                dest = dest_dir_video
                move(dest, item, name)
            elif name.endswith(".jpg") or name.endswith(".jpeg") or name.endswith(".png"):
                dest = dest_dir_image
                move(dest, item, name)
    print(f"{event.src_path} has been modified")



def on_moved(event):
    print(f"moved {event.src_path} to {event.dest_path}")


# unique / special functions
def remove_current_dupes(response):
    """
    Gives the user the option to scan current directory and remove
    existing duplicates.
    :param response:
    """
    if response is True:
        DuplicateRemover.main()


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

    response = pymsgbox.prompt("Would you like to scan and remove the current Directory "
                "for duplicate files?\nDo note that the amount of time this "
                "takes is variable on the amount of data you have. "
                "(Y/N)")
    if len(response) == 1 and response.upper() == "Y":
        remove_current_dupes(True)
    # Initialize Observer
    observer = Observer()
    observer.schedule(my_event_handler, filePath, recursive=True)
    # Start the observer
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
