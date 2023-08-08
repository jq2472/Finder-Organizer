
import os
import time
from dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import sys
import logging
from watchdog.events import LoggingEventHandler

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


# event handler
if __name__ == "__main__":
    """
    The event handler is the object that will be notified when something happen on the filesystem you are monitoring.
    """
    # Set the format for logging info
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Set format for displaying path
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    # Initialize logging event handler
    event_handler = LoggingEventHandler()

    # Initialize Observer
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    # Start the observer
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
