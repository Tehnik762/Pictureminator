from sys import argv
from scan_images import process_folder, process_file
import time
import os
from functions.duplicatefinder import group_similar_images
from functions.allowed import is_allowed
from functions.folders import create
import pandas as pd
from functions.sort_files import sort_files

if __name__ == "__main__":
    if len(argv) < 2:
        folder_path = "sort"
    else:
        folder_path = argv[1]
    start = time.time()
    if os.path.isdir(folder_path):
        parent_folder = os.path.dirname(os.path.abspath(folder_path))
        with os.scandir(parent_folder) as entries:
            for entry in entries:
                if entry.name == folder_path:
                    process_folder(entry, start)
                    folder = entry
                    break
        # Create folders
        create(folder.name)
        # importing data
        images_to_sort = pd.read_csv(f"{folder_path}/{folder.name}.csv")
        # Process screenshots
        sort_files(images_to_sort, "screenshots_et", f"{folder_path}/screenshots")
        # Process documents

        # Search for duplicates
        images = os.scandir(folder.name)
        image_paths = []
        for img in images:
            if is_allowed(img.name):
                image_paths.append(img.path)
        unique_images, grouped_images = group_similar_images(image_paths)
        #print(grouped_images)
        # {'sort/2015-02-14 11-23-30.JPG': ['sort/2015-02-14 11-23-31.JPG', 'sort/2015-02-14 11-23-26.JPG'], 'sort/2022-01-23_21-51-33.png': ['sort/2022-01-23_21-52-14.png'], 'sort/2015-02-14 11-22-07.JPG': ['sort/2015-02-14 11-21-47.JPG'], 'sort/2015-02-16 19-57-59.JPG': ['sort/2015-02-16 19-57-53.JPG'], 'sort/2015-02-14 11-08-30.JPG': ['sort/2015-02-14 11-08-31.JPG'], 'sort/2015-02-20 20-34-31.JPG': ['sort/2015-02-20 20-34-33.JPG'], 'sort/2015-02-14 10-45-01.JPG': ['sort/2015-02-14 10-44-59.JPG'], 'sort/2015-02-13 18-17-46.JPG': ['sort/2015-02-13 18-17-51.JPG']}

    else:
        print(f"{folder_path} is not a folder!")

