from PIL import Image
import imagehash
from collections import defaultdict
from pillow_heif import register_heif_opener
import exifread
from datetime import datetime

def calculate_image_hash(image_path):
    """Calculate perceptual hash for an image."""
    register_heif_opener()
    img = Image.open(image_path)
    return imagehash.average_hash(img)

def group_similar_images(image_paths, image_data):
    """Group similar images based on perceptual hash."""
    image_hashes = {path: calculate_image_hash(path) for path in image_paths}

    grouped_images = defaultdict(list)
    unique_images = []
    processed_imgs =[]

    for path1 in image_paths:
        is_unique = True

        path1_name = path1.split("/")[-1]

        for path2 in unique_images:
            path2_name = path2.split("/")[-1]
            if are_images_similar(image_hashes[path1], image_hashes[path2]) and \
                    abs((get_image_capture_time(path1) - get_image_capture_time(path2)).total_seconds()) <= 3000 and \
                    image_data.loc[image_data.filename == path1_name, "faces"].values[0] == \
                    image_data.loc[image_data.filename == path2_name, "faces"].values[0]:
                grouped_images[path2].append(path1)
                is_unique = False
                break

        if is_unique:
            unique_images.append(path1)

    return unique_images, grouped_images

def are_images_similar(hash1, hash2, threshold=14):
    """Check if two image hashes are similar based on a threshold."""
    return hash1 - hash2 < threshold


def get_image_capture_time(image_path):
    """Get the capture time of the image from its EXIF data."""
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
        if 'EXIF DateTimeOriginal' in tags:
            capture_time = tags['EXIF DateTimeOriginal'].values
            capture_time = datetime.strptime(capture_time, "%Y:%m:%d %H:%M:%S")
            return capture_time
    return None