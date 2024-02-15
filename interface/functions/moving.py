import os

def moving_files(max_score, folder_path, best_image, best_image_name):
    if max_score > 1:
        os.rename(best_image, f"{folder_path}/super/{best_image_name}")
    elif max_score >= 0:
        os.rename(best_image, f"{folder_path}/good/{best_image_name}")
    else:
        os.rename(best_image, f"{folder_path}/not_good/{best_image_name}")