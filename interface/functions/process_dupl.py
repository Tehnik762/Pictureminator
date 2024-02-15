import logging
import os
from functions.moving import moving_files

def process_duplicates(similar_images, folder_path, models, image_data):
    logging.basicConfig(level=logging.INFO, filename='../app.log', filemode='a')
    for pack in similar_images:
        scores = []
        for img in pack:
            f_name = img.split("/")[-1]
            img_info = image_data.loc[image_data["filename"] == f_name]
            file_name = img_info.pop("filename")
            scores.append(calculate_a_score(img_info, models))

        max_score = max(scores)
        min_score = min(scores)
        if max_score == min_score:
            b_faces = []
            for img in pack:
                f_name = img.split("/")[-1]
                img_info = image_data.loc[image_data["filename"] == f_name]
                b_faces.append(calculate_b_faces(img_info))
            max_b_face = max(b_faces)
            best_image = pack[b_faces.index(max_b_face)]
            logging.info(f"{best_image} - B_faces: {max_b_face} - other B_faces: {b_faces}")
        else:
            best_image = pack[scores.index(max_score)]
            logging.info(f"{best_image} - {max_score} - other scores: {scores}")
        logging.info(f"Pack - {pack}")
        best_image_name = best_image.split("/")[-1]

        moving_files(max_score, folder_path, best_image, best_image_name)

        for bad in pack:
            if bad != best_image:
                bad_name = bad.split("/")[-1]
                os.rename(bad, f"{folder_path}/duplicates/{bad_name}")

def calculate_a_score(img_data, models):
    score = 0

    for model in models:

        score += models[model][0].predict(img_data)[0]*models[model][1]

    return score

def calculate_b_faces(img_data):
    return img_data["faces"].values[0] - img_data["blink"].values[0]