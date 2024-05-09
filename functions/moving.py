import os
import exifread
from datetime import datetime


def moving_files(max_score, folder_path, best_image, best_image_name, period=0):
    date_info = get_image_capture_time(best_image)
    best_image = os.path.abspath(best_image)
    if max_score > 1:
        path_to_go = create_folders(f"{folder_path}/super/", period, date_info)
        os.rename(best_image, path_to_go + best_image_name)
    elif max_score >= 0:
        path_to_go = create_folders(f"{folder_path}/good/", period, date_info)
        os.rename(best_image,  path_to_go + best_image_name)
    else:
        os.rename(best_image, f"{folder_path}/not_good/{best_image_name}")



def create_folders(origin, period, date_info):
    if period == 0:
        return origin
    if period == "month":
        if os.path.isdir(f"{origin}{date_info[0]}/{date_info[1]}"):
            return f"{origin}{date_info[0]}/{date_info[1]}/"
        else:
            os.makedirs(f"{origin}{date_info[0]}/{date_info[1]}/")
            return f"{origin}{date_info[0]}/{date_info[1]}/"
    if period == "year":
        if os.path.isdir(f"{origin}{date_info[0]}"):
            return f"{origin}{date_info[0]}/"
        else:
            os.makedirs(f"{origin}{date_info[0]}/")
            return f"{origin}{date_info[0]}/"


def get_image_capture_time(image_path):
    """Get the capture time of the image from its EXIF data."""
    with open(image_path, 'rb') as f:
        try:
            tags = exifread.process_file(f, details=False)
            if 'EXIF DateTimeOriginal' in tags:
                capture_time = tags['EXIF DateTimeOriginal'].values
                capture_time = datetime.strptime(capture_time, "%Y:%m:%d %H:%M:%S")
                return capture_time.year, f"{capture_time.month:02}"
        except:
            pass
    return ["None", "None"]

def move_video(video_name, new_path="video"):
    video_path = os.path.abspath(new_path)
    f_name = video_name.split("/")[-1]
    os.rename(video_name, f"{video_path}/{f_name}")

