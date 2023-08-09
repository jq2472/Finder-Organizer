
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
# neeeded for os.scandir
import os
# initially imported modules
import sys
import time
import logging
from watchdog.observers import Observer
# make changes at a time a file is created or modified
from watchdog.events import PatternMatchingEventHandler

filePath = "/Users/jolinqiu/Downloads"

def getSumn():
    """

    :return:
    """
    # os.scandir() returns a Python iterable containing the names of the files
    # and subdirectories in the directory given by the path argument:
    # items = os.scandir(filePath)

    with os.scandir(filePath) as items:
        for item in items:
            print(item.name)

# handling all events
def on_created(event):
    print(f"{event.src_path} has been created!")

def on_deleted(event):
    print(f"ruh roh.... someone deleted {event.src_path}")

def on_modified(event):
    print(f"{event.src_path} has been modified")

def on_moved(event):
    print(f"moved {event.src_path} to {event.dest_path}")

# event handler
if __name__ == "__main__":
    """
    The event handler is the object that will be notified when something happen on the filesystem you are monitoring.
    """
    patterns = ["*"] # the file patterns we want to handle
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    # ______________________
    # Initialize event handler
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    # ______________________
    # specify to the handler that we want these functions to be called when the corresponding event is raised
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    # ______________________
    # Initialize Observer
    observer = Observer()
    filePath = "."
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
