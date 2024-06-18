import logging
import os
from functions.moving import moving_files
from PIL import Image, ImageDraw, ImageFont

def process_duplicates(similar_images, folder_path, models, image_data, debug=False, period=0):
    folder_path = os.path.abspath(folder_path)
    log_path = os.path.abspath("../app.log")
    logging.basicConfig(level=logging.INFO, filename=log_path, filemode='a')
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
        logging.info(f"Best image: {best_image_name}")

        if debug:
            debug_collage_path = create_debug_collage(folder_path, pack, best_image_name, max_score, )
            logging.info(f"Debug collage created: {debug_collage_path}")

        moving_files(max_score, folder_path, best_image, best_image_name, period)

        for bad in pack:
            logging.info(f"Bad image: {bad}")
            if bad != best_image:
                logging.info(f"Moving {bad} to {folder_path}/duplicates")
                bad_name = bad.split("/")[-1]
                os.rename(bad, f"{folder_path}/duplicates/{bad_name}")

def calculate_a_score(img_data, models):
    score = 0

    for model in models:

        score += models[model][0].predict_proba(img_data)[0][1]*models[model][1]

    return score

def calculate_b_faces(img_data):
    return img_data["faces"].values[0] - img_data["blink"].values[0]


def create_debug_collage(folder_path, pack, best_image_name, best_score, debug_folder="debug"):
    try:
        debug_folder = os.path.join(folder_path, debug_folder)
        os.makedirs(debug_folder, exist_ok=True)


        try:
            font = ImageFont.truetype("arial.ttf", 45)
        except IOError:
            font = ImageFont.load_default()

        num_images = len(pack)
        if num_images == 0:
            print("No images in the pack.")
            return None


        resized_images = []
        for image_path in pack:
            image = Image.open(image_path)
            image = image.resize((image.width // 4, image.height // 4))
            resized_images.append(image)

        collage_height = resized_images[0].height
        collage_width = resized_images[0].width * num_images
        collage = Image.new("RGB", (collage_width, collage_height), color="white")

        draw = ImageDraw.Draw(collage)
        text_color = "black"
        text_padding = 10
        text_background_color = (255, 255, 255, 128)

        for i, image in enumerate(resized_images):
            collage.paste(image, (i * image.width, 0))
            if os.path.basename(pack[i]) == best_image_name:

                best_image_text = f"BEST\nScore: {best_score}"
                text_bbox = font.getbbox(best_image_text)
                text_box_width = text_bbox[2] - text_bbox[0] + 2 * text_padding
                text_box_height = text_bbox[3] - text_bbox[1] + 2 * text_padding
                text_box = Image.new("RGBA", (text_box_width, text_box_height), text_background_color)
                collage.paste(text_box, (i * image.width, 0), text_box)


                draw.multiline_text((i * image.width + text_padding, text_padding), best_image_text, fill=text_color,
                                    font=font)
            else:
                image_name = os.path.basename(pack[i])
                score_text = f"Name: {image_name}"
                text_bbox = font.getbbox(score_text)
                text_box_width = text_bbox[2] - text_bbox[0] + 2 * text_padding
                text_box_height = text_bbox[3] - text_bbox[1] + 2 * text_padding
                text_box = Image.new("RGBA", (text_box_width, text_box_height), text_background_color)
                collage.paste(text_box, (i * image.width, 0), text_box)


                draw.multiline_text((i * image.width + text_padding, text_padding), score_text, fill=text_color,
                                    font=font)

        collage_path = os.path.join(debug_folder, f"debug_collage_{best_image_name}.png")
        collage.save(collage_path)
        return collage_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None