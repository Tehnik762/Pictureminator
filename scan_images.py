from functions.image_analyser import processImage
import os
import pandas as pd
import time
# SETTINGS

dir_to_scan = "images"
exclude = [".DS_Store"]
# WORKFLOW
start = time.time()
dirs = os.scandir(dir_to_scan)

for folder in dirs:
    if folder.name not in exclude:
        data = []
        file_csv = (f"{folder.path}/{folder.name}.csv")
        if not os.path.exists(file_csv):
            db = pd.DataFrame()
            already_scanned = []
        else:
            db = pd.read_csv(file_csv)
            already_scanned = db.filename.to_list()
            already_scanned.append(f"{folder.name}.csv")
        for file in os.scandir(folder.path):
            if file.name not in already_scanned and file.name not in exclude:
                small_time = time.time()
                try:
                    info_img = processImage(file.path)
                    info_img['filename'] = file.name
                    data.append(info_img)
                except:
                    print(f"ERROR - {file.name}")
                elapsed_time = time.time() - start
                small_time = time.time() - small_time
                print(f"{file.name} - {small_time} of the {elapsed_time}")
            else:
                pass

        df = pd.DataFrame(data)
        df = pd.concat([db, df], ignore_index=True)
        df.to_csv(f"{folder.path}/{folder.name}.csv", index=False)
        print(f"Folder - {folder.name} finished!")
elapsed_time = time.time() - start
print(f"Final - {elapsed_time}")