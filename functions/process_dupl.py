
import os

def process_duplicates(similar_images, folder_path, models, image_data, debug=False):
    for pack in similar_images:
        scores = []
        for img in pack:
            f_name = img.split("/")[-1]
            img_info = image_data.loc[image_data["filename"] == f_name]
            file_name = img_info.pop("filename")
            if debug: print(img_info)
            scores.append(calculate_a_score(img_info, models))

        if debug: print(f"Scores: {scores}, Pack: {pack}")
        max_score = max(scores)
        best_image = pack[scores.index(max_score)]
        if debug: print(best_image, max_score)
        best_image_name = best_image.split("/")[-1]
        os.rename(best_image, f"{folder_path}/good/{best_image_name}")
        for bad in pack:
            if bad != best_image:
                if debug: print(f"Moving {bad} to {folder_path}/duplicates")
                bad_name = bad.split("/")[-1]
                os.rename(bad, f"{folder_path}/duplicates/{bad_name}")

def calculate_a_score(img_data, models):
    score = 0

    for model in models:

        score += models[model][0].predict(img_data)[0]*models[model][1]

    return score
