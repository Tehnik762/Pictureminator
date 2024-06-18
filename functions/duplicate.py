import os
import pandas as pd
from datetime import datetime, timedelta


def group_similar(image_paths, images_to_sort, time_interval=5, hash_threshold=10):
    def get_image_timestamp(image_path):
        try:
            return datetime.fromtimestamp(os.path.getmtime(image_path))
        except:
            return None

    def hash_similarity(hash1, hash2):
        # Compute the Hamming distance between two hashes
        return bin(hash1 ^ hash2).count('1')

    # Step 1: Sort the DataFrame by average_hash
    images_to_sort = images_to_sort.sort_values(by='average_hash').reset_index(drop=True)

    # Step 2: Group images by average_hash similarity
    potential_groups = []
    for i in range(len(images_to_sort)):
        image_data = images_to_sort.iloc[i]
        image_name = image_data['filename']
        image_path = next((p for p in image_paths if image_name in p), None)
        if image_path is None:
            continue

        if not potential_groups:
            potential_groups.append([image_path])
        else:
            last_group = potential_groups[-1]
            last_image_path = last_group[-1]
            last_image_name = os.path.basename(last_image_path)
            last_image_data = images_to_sort[images_to_sort['filename'] == last_image_name].iloc[0]

            if hash_similarity(image_data['average_hash'], last_image_data['average_hash']) <= hash_threshold:
                last_group.append(image_path)
            else:
                potential_groups.append([image_path])

    unique_images = []
    remaining_groups = []

    # Step 3: Filter out distant images based on time interval
    for group in potential_groups:
        if len(group) == 1:
            unique_images.append(group[0])
        else:
            timestamps = [get_image_timestamp(image_path) for image_path in group]
            timestamps = [ts for ts in timestamps if ts is not None]

            if not timestamps:
                unique_images.extend(group)
                continue

            min_timestamp = min(timestamps)
            max_timestamp = max(timestamps)
            if (max_timestamp - min_timestamp) > timedelta(minutes=time_interval):
                unique_images.extend(group)
            else:
                remaining_groups.append(group)

    # Step 4: Check face count within remaining groups
    final_grouped_images = []
    for group in remaining_groups:
        faces_count = images_to_sort[images_to_sort['filename'] == os.path.basename(group[0])]['faces'].values[0]
        final_group = [group[0]]
        for image_path in group[1:]:
            image_name = os.path.basename(image_path)
            image_faces_count = images_to_sort[images_to_sort['filename'] == image_name]['faces'].values[0]
            if image_faces_count == faces_count:
                final_group.append(image_path)

        if len(final_group) > 1:
            final_grouped_images.append(final_group)
        else:
            unique_images.extend(final_group)

    return unique_images, final_grouped_images
