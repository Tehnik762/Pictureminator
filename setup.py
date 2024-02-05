import urllib.request
import bz2
import shutil
import os
from tqdm import tqdm


def download_and_extract_model(force_download=False):
    model_url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    compressed_file_path = "./external/shape_predictor_68_face_landmarks.dat.bz2"
    extracted_file_path = "./external/shape_predictor_68_face_landmarks.dat"

    if not force_download and os.path.exists(extracted_file_path):
        user_response = input("File already exists. Do you want to overwrite it? (y/n): ").lower()
        if user_response != 'y':
            print("File not overwritten.")
            return

    with urllib.request.urlopen(model_url) as response, \
            open(compressed_file_path, 'wb') as out_file, \
            tqdm(total=int(response.info().get("Content-Length", 0)), unit='B', unit_scale=True,
                 unit_divisor=1024) as progress_bar:

        while True:
            chunk = response.read(8192)
            if not chunk:
                break
            out_file.write(chunk)
            progress_bar.update(len(chunk))

    try:
        with bz2.BZ2File(compressed_file_path, 'rb') as f_in, open(extracted_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        print(f"Error decompressing file: {e}")
        return

    # Удалить сжатый файл, если необходимо
    os.remove(compressed_file_path)

    print(f"Model downloaded and extracted to {extracted_file_path}")


if __name__ == "__main__":
    download_and_extract_model()
