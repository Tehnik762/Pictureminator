from functions.image_analyser import processImage
import os
import pandas as pd
import time
from multiprocessing import Pool, freeze_support, set_start_method
# SETTINGS
dir_to_scan = "images"
exclude = [".DS_Store"]
# WORKFLOW
start = time.time()
dirs = os.scandir(dir_to_scan)

def process_file(file_path):
    data = []
    small_time = time.time()
    filename = os.path.basename(file_path)
    try:
        info_img = processImage(file_path)
        info_img['filename'] = filename
        data = [info_img]
    except:
        print(f"ERROR - {filename}")
    elapsed_time = time.time() - start
    small_time = time.time() - small_time
    print(f"{filename} - {small_time} of the {elapsed_time}")
    return data


def process_folder(folder):
    file_csv = (f"{folder.path}/{folder.name}.csv")
    if not os.path.exists(file_csv):
        db = pd.DataFrame()
        already_scanned = []
    else:
        db = pd.read_csv(file_csv)
        already_scanned = db.filename.to_list()
        already_scanned.append(f"{folder.name}.csv")
    files_to_process= []
    if folder.is_dir():
        file_list = os.scandir(folder)
        for one_file in file_list:
            if one_file.name not in exclude and one_file.name not in already_scanned:
                files_to_process.append(one_file.path)

        #files_to_process = [file.path for file in os.scandir(folder_path)
        #                    if file.name not in already_scanned and file.name not in exclude]

        with Pool() as pool:
            results = pool.map(process_file, files_to_process)

        data = [item for sublist in results for item in sublist]

        df = pd.DataFrame(data)
        df = pd.concat([db, df], ignore_index=True)

        df.to_csv(file_csv, index=False)
        print(f"Folder - {folder.name} finished!")


if __name__ == "__main__":
    for directory in dirs:
        if directory.name not in exclude:
            process_folder(directory)

    elapsed_time = time.time() - start
    print(f"Final - {elapsed_time}")

