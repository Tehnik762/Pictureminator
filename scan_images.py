from functions.image_analyser import processImage
import os
import pandas as pd
import time
from multiprocessing import Pool
from functions.format_time import format_seconds


def process_file(file_path, start, i):
    data = []
    small_time = time.time()
    filename = os.path.basename(file_path)
    try:
        info_img = processImage(file_path)
        info_img['filename'] = filename
        data = [info_img]
    except Exception as e:
        print(f"ERROR - {filename}")
        print(e)
        print(type(e))
        os.rename(file_path, f"./images/error/{filename}")
    elapsed_time = format_seconds(round(time.time() - start, 2))
    small_time = format_seconds(round(time.time() - small_time, 2))
    print(f"{filename} -Nr {i} - {small_time} of the {elapsed_time}")
    return data


def process_folder(folder, start):
    try: exclude
    except: exclude = [".DS_Store"]
    file_csv = f"{folder.path}/{folder.name}.csv"
    if not os.path.exists(file_csv):
        db = pd.DataFrame()
        already_scanned = []
    else:
        db = pd.read_csv(file_csv)
        already_scanned = db.filename.to_list()
        already_scanned.append(f"{folder.name}.csv")
    files_to_process = []
    if folder.is_dir():
        file_list = os.scandir(folder)
        i = 1
        for one_file in file_list:
            if one_file.name not in exclude and one_file.name not in already_scanned:
                files_to_process.append((one_file.path, start, i))
                i += 1

        print(f"Ready to scan {i} files")
        num_processes = 4
        with Pool(num_processes) as pool:
            results = pool.starmap(process_file, files_to_process)

        data = [item for sublist in results for item in sublist]

        df = pd.DataFrame(data)
        df = pd.concat([db, df], ignore_index=True)

        df.to_csv(file_csv, index=False)
        print(f"Folder - {folder.name} finished!")


if __name__ == "__main__":
    start = time.time()
    # SETTINGS
    dir_to_scan = "images"
    exclude = [".DS_Store", "0", "1", "error"]
    # WORKFLOW
    dirs = os.scandir(dir_to_scan)
    n = len(os.listdir(dir_to_scan))
    print(f"Ready to scan images from {n} directories")
    for directory in dirs:
        n -= 1
        if directory.name not in exclude:
            print(f"Scanning {directory.name}, {n} directories left")
            process_folder(directory, start)

    elapsed_time = format_seconds(time.time() - start)
    print(f"Final - {elapsed_time}")
