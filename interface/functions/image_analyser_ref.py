import cv2
import numpy as np
import pandas as pd
import face_recognition
import time
from skimage.feature import hog
from skimage import exposure
import os

def processImage(url):
    start_time = time.time()

    img = cv2.imread(url)
    res = extract_basic_features(img)
    res.update(calculate_hog_features(img))
    res.update(extract_color_features(img))
    res.update(extract_shape_and_size_features(img))
    res.update(count_corners_and_lines(img))
    res['faces'] = detect_faces_opencv(img)
    res['has_text'] = has_text_opencv(img)
    res['filesize'] = os.path.getsize(url)
    res['depth'] = img.dtype


    end_time = time.time()
    elapsed_time = end_time - start_time

    return res, elapsed_time

def extract_basic_features(img):
    size = img.shape
    basic_features = {
        'size_w': size[0],
        'size_h': size[1],
        'ch': size[2],
        'mean_value_b': np.mean(img, axis=(0, 1))[0],
        'mean_value_g': np.mean(img, axis=(0, 1))[1],
        'mean_value_r': np.mean(img, axis=(0, 1))[2],
        'median_value_b': np.median(img, axis=(0, 1))[0],
        'median_value_g': np.median(img, axis=(0, 1))[1],
        'median_value_r': np.median(img, axis=(0, 1))[2],
        'std_deviation_b': np.std(img, axis=(0, 1))[0],
        'std_deviation_g': np.std(img, axis=(0, 1))[1],
        'std_deviation_r': np.std(img, axis=(0, 1))[2],
        'contrast': 0,
        'brightness': 0
    }
    basic_features['contrast'], basic_features['brightness'] = calculate_contrast_brightness(img)

    return basic_features

def calculate_contrast_brightness(image):
    # Преобразование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Вычисление стандартного отклонения и среднего значения яркости
    contrast = np.std(gray_image)
    brightness = np.mean(gray_image)

    return contrast, brightness

def calculate_hog_features(image):
    # Преобразование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Вычисление HOG-признаков
    features, _ = hog(gray_image, orientations=8, pixels_per_cell=(8, 8),
                              cells_per_block=(1, 1), visualize=True)

    # Нормализация HOG-признаков для лучшей интерпретации
    features = exposure.rescale_intensity(features, in_range=(0, 10))

    # Возвращение HOG-признаков в виде словаря
    return {"hog_features_mean": np.mean(features),
            "hog_features_median": np.median(features),
            "hog_features_std": np.std(features),
            "hog_features_len": len(features)}

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

    # Возвращение извлеченных признаков в виде словаря
    return {"h_mean": h_mean, "h_median": h_median, "h_std": h_std,
            "s_mean": s_mean, "s_median": s_median, "s_std": s_std,
            "v_mean": v_mean, "v_median": v_median, "v_std": v_std}


def extract_shape_and_size_features(image):
    # Преобразование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение пороговой обработки для выделения объектов
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

    # Поиск контуров в бинарном изображении
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Инициализация списка для хранения признаков формы и размера
    shape_and_size_features = []

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

        # Добавление признаков в список
        # shape_and_size_features.append((len(approx_shape), area))
        n += 1

        area += area_sq
        area_list.append(area_sq)
        vert += len(approx_shape)
        vert_list.append(len(approx_shape))

        x, y, w, h = cv2.boundingRect(contour)

        # Выделение области на изображении
        region = image[y:y + h, x:x + w]

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

    return {"n_objects": n, "area": area, "area_mean": area_mean, "area_std": area_std,
            "vert": vert, "vert_mean": vert_mean, "vert_std": vert_std,
            "color_mean": color_mean, "color_std": color_std}
def count_corners_and_lines(image):
    # Преобразование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Детектор углов (Shi-Tomasi)
    corners = cv2.goodFeaturesToTrack(gray_image, maxCorners=100, qualityLevel=0.01, minDistance=10)
    corners_count = len(corners)

    # Применение детектора Хафа для обнаружения прямых линий
    edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)
    lines_count = len(lines) if lines is not None else 0

    return {"corners": corners_count, "lines": lines_count}

def detect_faces_opencv(image):
    # Конвертировать изображение из формата OpenCV BGR в RGB (который используется face_recognition)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Найти все лица на изображении
    face_locations = face_recognition.face_locations(rgb_image)

    # Вернуть количество обнаруженных лиц
    return len(face_locations)
def has_text_opencv(image):
    # Конвертировать изображение в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применить адаптивную бинаризацию для выделения текста
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Найти контуры на бинарном изображении
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Проверить, есть ли найденные контуры (текст)
    return 1 if contours else 0




result, time = processImage("/Users/admin/Yandex.Disk.localized/Projects/WBS/final_project/images/screenshots/IMG_9500.HEIC")
print(len(result), time)
print(result)