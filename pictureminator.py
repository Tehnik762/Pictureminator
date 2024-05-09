from sys import argv
from scan_images import process_folder, process_file
import time
import os
from functions.duplicatefinder import group_similar_images
from functions.allowed import is_allowed
from functions.folders import create
import pandas as pd
from functions.sort_files import sort_files
from functions.process_dupl import process_duplicates
from functions.d_models import loadModels
import time
from functions.format_time import format_seconds
import logging
from functions.moving import moving_files
from functions.d_models import loadModels
from functions.process_dupl import calculate_a_score

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w')
    start_time = time.time()
    logging.info(f"Starting")
    if len(argv) < 2:
        folder_path = "sort"
        f_name = "sort"
        full_path = os.path.abspath(folder_path)
    else:
        folder_path = argv[1]
        if folder_path[-1] == "/":
            folder_path = folder_path[:-1]
        full_path = folder_path
        f_name = folder_path.split("/")[-1]
    if len(argv) < 3:
        period = 0
    else:
        period = argv[2]

    start = time.time()
    if os.path.isdir(folder_path):
        parent_folder = os.path.dirname(os.path.abspath(folder_path))

        with os.scandir(parent_folder) as entries:
            for entry in entries:
                if entry.name == f_name:
                    # Create folders
                    create(full_path)
                    process_folder(entry, start, rescan=True)
                    folder = entry
                    break

        # importing data
        images_to_sort = pd.read_csv(f"{folder_path}/{f_name}.csv")
        images_to_sort = images_to_sort.fillna(0)

        # Process screenshots
        images_to_sort = sort_files(images_to_sort, "screenshots_final", f"{folder_path}/screenshots", source_fld=folder_path, debug=True)
        images_to_sort = sort_files(images_to_sort, "screenshots_ph_final", f"{folder_path}/screenshots", source_fld=folder_path, debug=True)
        # Process documents
        images_to_sort = sort_files(images_to_sort, "docs_final", f"{folder_path}/documents", source_fld=folder_path, debug=True)
        images_to_sort = sort_files(images_to_sort, "receipts_final", f"{folder_path}/documents", source_fld=folder_path, debug=True)
        # Search for duplicates
        images = os.scandir(full_path)
        image_paths = []
        for img in images:
            if is_allowed(img.name):
                image_paths.append(folder_path + '/' + img.name)
        logging.info(f"Dividing {len(image_paths)} images into duplicates")

        unique_images, grouped_images = group_similar_images(image_paths, images_to_sort)
        logging.info(f"Found {len(unique_images)} unique images")
        logging.info(unique_images)
        logging.info(f"Found {len(grouped_images)} groups of duplicate images")
        logging.info(grouped_images)
        # Let's move unique images
        models = loadModels()

        for img in unique_images:
            img_name = img.split("/")[-1]
            path_to_send = folder_path + "/good/" + img_name
            img_data = images_to_sort.loc[images_to_sort["filename"] == img_name]
            img_data.pop("filename")
            score = calculate_a_score(img_data, models)
            moving_files(score, folder_path, img, img_name, period)


        logging.info(f"Processing {len(grouped_images)} groups of duplicate images")

        process_duplicates(grouped_images, folder_path, models, images_to_sort, period)

        end_time = time.time()
        total_time = format_seconds(end_time - start)

        print(f"Total time: {total_time}")
        logging.info(f"Total time: {total_time}")

    else:
        print(f"{folder_path} is not a folder!")

