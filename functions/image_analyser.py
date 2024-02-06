import cv2
import numpy as np
import face_recognition
from skimage.feature import hog
from skimage import exposure
import os
from skimage.feature import graycomatrix
from PIL import Image
import imagehash
from skimage import img_as_ubyte
from pillow_heif import register_heif_opener
import dlib
from scipy.fftpack import fft2, fftshift
register_heif_opener()


def processImage(url):
    """
    This function will accept a destination url of an image and return a dictionary of the image properties
    :param url: str
    :return: dict
    """

    res = {}
    img = cv2.imread(url)
    size = img.shape
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res['size_w'], res['size_h'] = size[0], size[1]
    res['aspect_ratio'] = res['size_h'] / res['size_w']
    res['mean_value_b'], res['mean_value_g'], res['mean_value_r'] = np.mean(img, axis=(0, 1))
    res['median_value_b'], res['median_value_g'], res['median_value_r'] = np.median(img, axis=(0, 1))
    res['std_deviation_b'], res['std_deviation_g'], res['std_deviation_r'] = np.std(img, axis=(0, 1))
    res["contrast"], res["brightness"] = calculate_contrast_brightness(gray_image)
    res.update(extract_color_histogram(img))
    features = calculate_hog_features(gray_image)
    res["hog_features_mean"] = np.mean(features)
    res["hog_features_median"] = np.median(features)
    res["hog_features_std"] = np.std(features)
    res["hog_features_len"] = len(features)
    res['h_mean'], res['h_median'], res['h_std'], res['s_mean'], res['s_median'], \
        res['s_std'], res['v_mean'], res['v_median'], res['v_std'] = extract_color_features(img)
    res['n_objects'], res['area'], res['area_mean'], res['area_std'], res['vert'], res['vert_mean'], res['vert_std'],\
        res['color_mean'], res['color_std'] = extract_shape_and_size_features(img)
    res['corners'], res['lines'] = count_corners_and_lines(gray_image)
    res.update(detect_faces_opencv(img))
    res['has_text'] = has_text_opencv(gray_image)
    res['filesize'] = os.path.getsize(url)
    res.update(calculate_sharpness(gray_image))
    res["gaussian_blur"] = estimate_blur_gaussian(gray_image)
    res['gibson_blur'] = estimate_blur_gibson(gray_image)
    res['gradient'] = calculate_gradients(gray_image)
    res.update(calculate_texture_features(gray_image))
    res["color_balance"] = np.mean([res['std_deviation_b'], res['std_deviation_g'], res['std_deviation_r']])
    res["focus_score"] = calculate_focus(gray_image)
    res.update(calculate_image_hashes(url))
    del img
    del gray_image
    return res

def calculate_contrast_brightness(gray_image):
    contrast = np.std(gray_image)
    brightness = np.mean(gray_image)

    return contrast, brightness

def calculate_hog_features(gray_image):
    # Вычисление HOG-признаков
    features, _ = hog(gray_image, orientations=8, pixels_per_cell=(8, 8),
                              cells_per_block=(1, 1), visualize=True)
    # Нормализация HOG-признаков для лучшей интерпретации
    features = exposure.rescale_intensity(features, in_range=(0, 10))

    return features

def extract_color_features(image):
    # Преобразование изображения в цветовое пространство HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Разделение каналов цветности
    h_channel, s_channel, v_channel = cv2.split(hsv_image)

    # Пример: вычисление среднего, медианы и стандартного отклонения для каждого канала
    h_mean = np.mean(h_channel)
    h_median = np.median(h_channel)
    h_std = np.std(h_channel)

    s_mean = np.mean(s_channel)
    s_median = np.median(s_channel)
    s_std = np.std(s_channel)

    v_mean = np.mean(v_channel)
    v_median = np.median(v_channel)
    v_std = np.std(v_channel)
    del hsv_image, h_channel, s_channel, v_channel
    # Возвращение извлеченных признаков
    return h_mean, h_median, h_std, s_mean, s_median, s_std, v_mean, v_median, v_std


def extract_shape_and_size_features(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Применение пороговой обработки для выделения объектов
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

    # Поиск контуров в бинарном изображении
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Количество объектов
    n = 0
    # Площадь суммарная
    area = 0
    # Площадь средняя
    area_mean = 0
    area_list = []
    # Количество вершин
    vert = 0
    vert_list = []
    # Среднее количество вершин
    vert_mean = 0
    vert_list = []
    region_features = []

    for contour in contours:
        # Вычисление периметра контура
        perimeter = cv2.arcLength(contour, True)

        # Вычисление приближенной формы контура
        epsilon = 0.02 * perimeter
        approx_shape = cv2.approxPolyDP(contour, epsilon, True)

        # Вычисление площади контура
        area_sq = cv2.contourArea(contour)

        n += 1

        area += area_sq
        area_list.append(area_sq)
        vert += len(approx_shape)
        vert_list.append(len(approx_shape))

        x, y, w, h = cv2.boundingRect(contour)

        # Выделение области на изображении
        region = img[y:y + h, x:x + w]

        # Вычисление среднего цвета в области
        average_color = np.mean(region, axis=(0, 1))

        # Добавление характеристик области в список
        region_features.append(average_color)

    area_mean = np.mean(area_list)
    area_std = np.std(area_list)
    vert_mean = np.mean(vert_list)
    vert_std = np.std(vert_list)
    color_mean = np.mean(region_features)
    color_std = np.std(region_features)
    del gray_image, binary_image, contours, region_features
    return n, area, area_mean, area_std, vert, vert_mean, vert_std, color_mean, color_std

def count_corners_and_lines(gray_image):
    # Детектор углов (Shi-Tomasi)
    corners = cv2.goodFeaturesToTrack(gray_image, maxCorners=100, qualityLevel=0.01, minDistance=10)
    corners_count = len(corners)

    # Применение детектора Хафа для обнаружения прямых линий
    edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)
    lines_count = len(lines) if lines is not None else 0
    del corners, edges, lines
    return corners_count, lines_count

def detect_faces_opencv(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    faces = len(face_locations)
    face_landmarks_list = face_recognition.face_landmarks(rgb_image)

    blink_count = 0


    for landmarks in face_landmarks_list:
        left_eye = landmarks['left_eye']
        right_eye = landmarks['right_eye']

        left_eye_aspect_ratio = eye_aspect_ratio(left_eye)
        right_eye_aspect_ratio = eye_aspect_ratio(right_eye)

        blink_threshold = 0.25

        if abs(left_eye_aspect_ratio) < blink_threshold and abs(right_eye_aspect_ratio) < blink_threshold:
            blink_count += 1
    del rgb_image, face_locations, face_landmarks_list

    return {"faces": faces, "blink": blink_count}
	
def has_text_opencv(gray_image):

    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_area = np.sum([cv2.contourArea(cnt) for cnt in contours])
    del binary_image, contours
    return total_area

def calculate_sharpness(gray_image):
    # Вычисление Лапласиана
    laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
    blur_metric = laplacian.var()
    sharpness = np.mean(laplacian**2)
    del laplacian
    return {"sharpness": sharpness, "blur_metric": blur_metric}

def calculate_gradients(gray_image):

    # Вычисление градиентов по осям X и Y с использованием оператора Собеля
    gradient_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

    # Вычисление среднеквадратичного значения градиентов (оценка резкости)
    sharpness = np.mean(gradient_x**2 + gradient_y**2)

    return sharpness

def calculate_texture_features(gray_image):
    # Преобразование в формат uint8 для использования с GLCM
    gray_image = img_as_ubyte(gray_image)

    # Вычисление GLCM
    glcm = graycomatrix(gray_image, [1], [1], symmetric=True, normed=True)

    # Вычисление энергии текстуры
    texture_energy = np.sum(glcm**2)
    del gray_image, glcm
    return {"texture_energy": texture_energy}

def calculate_focus(gray_image):
    # Вычисление градиентов по осям X и Y с использованием оператора Собеля
    gradient_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    # Вычисление среднеквадратичного значения градиентов (оценка фокусировки)
    focus_score = np.mean(gradient_x**2 + gradient_y**2)

    return focus_score

def calculate_image_hashes(image_path):

    img = Image.open(image_path)

    average_hash = imagehash.average_hash(img)
    dhash = imagehash.dhash(img)
    phash = imagehash.phash(img)
    colorhash = imagehash.colorhash(img)
    del img
    return {
        "average_hash": int(str(average_hash), 16),
        "dhash": int(str(dhash), 16),
        "phash": int(str(phash), 16),
        "colorhash": int(str(colorhash), 16)
    }

def extract_color_histogram(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hist_hue = cv2.calcHist([hsv_image], [0], None, [256], [0, 256])
    hist_saturation = cv2.calcHist([hsv_image], [1], None, [256], [0, 256])
    hist_value = cv2.calcHist([hsv_image], [2], None, [256], [0, 256])

    hist_hue /= np.sum(hist_hue)
    hist_hue = np.mean(hist_hue)
    hist_saturation /= np.sum(hist_saturation)
    hist_saturation = np.median(hist_saturation)
    hist_value /= np.sum(hist_value)
    hist_value = np.std(hist_value)

    del hsv_image

    return {"hue": hist_hue, "saturation": hist_saturation, "value": hist_value}

def estimate_blur_gaussian(gray_image):
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    blur_metric = np.sum((gray_image - blurred) ** 2)
    return blur_metric

def estimate_blur_gibson(gray_image):
    f_transform = fftshift(fft2(gray_image))
    spectrum = np.abs(f_transform)
    blur_metric = np.sum(np.log(1 + spectrum))
    return blur_metric

def eye_aspect_ratio(eye):
    vertical_dist = eye[1][1] - eye[5][1]

    horizontal_dist = eye[3][0] - eye[0][0]
    ear = vertical_dist / horizontal_dist

    return ear