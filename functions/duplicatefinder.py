from PIL import Image
import imagehash
from collections import defaultdict
from pillow_heif import register_heif_opener
import exifread
from datetime import datetime
import os


def calculate_image_hash(image_path):
    """Calculate perceptual hash for an image.
    :param image_path:
    :return:
    """
    register_heif_opener()
    img = Image.open(image_path)
    return imagehash.average_hash(img)


def group_similar_images(image_paths, image_data):
    """Group similar images based on perceptual hash."""
    image_hashes = {path: calculate_image_hash(path) for path in image_paths}
    capture_times = {path: get_image_capture_time(path) for path in image_paths}
    unique_images = []
    duplicate_images = []
    processed_images = []

    for i, path1 in enumerate(image_paths):
        temp_dupl = []
        for path2 in image_paths[i + 1:]:
            if path2 not in processed_images:
                if are_images_similar(image_hashes[path1], image_hashes[path2]):
                    if capture_times[path1] is None or capture_times[path2] is None:
                        cont = True
                    else:
                        cont = abs((capture_times[path1] - capture_times[path2]).total_seconds()) <= 1000
                    face1 = image_data.loc[image_data.filename == path1.split("/")[-1], "faces"].values[0]
                    face2 = image_data.loc[image_data.filename == path2.split("/")[-1], "faces"].values[0]
                    if cont and face1 == face2:
                        temp_dupl.append(path2)
                        processed_images.append(path2)
        if path1 not in processed_images:
            if len(temp_dupl) > 0:
                temp_dupl.append(path1)
                processed_images.append(path1)
                duplicate_images.append(temp_dupl)
            else:
                unique_images.append(path1)

    return unique_images, duplicate_images


def are_images_similar(hash1, hash2, threshold=14):
    """Check if two image hashes are similar based on a threshold."""
    return hash1 - hash2 < threshold


def get_image_capture_time(image_path):
    """Get the capture time of the image from its EXIF data."""
    with open(image_path, 'rb') as f:
        try:
            tags = exifread.process_file(f, details=False)
            if 'EXIF DateTimeOriginal' in tags:
                capture_time = tags['EXIF DateTimeOriginal'].values
                capture_time = datetime.strptime(capture_time, "%Y:%m:%d %H:%M:%S")
                return capture_time
        except:
            pass
    try:
        filename = os.path.basename(image_path)
        date_str = ".".join(filename.split(".")[:-1]).split("(")[0].rstrip()
        capture_time = datetime.strptime(date_str, "%Y-%m-%d %H.%M.%S")
        return capture_time
    except Exception as e:
        print("Error while extracting capture time from filename:", e)
        pass
    return None
