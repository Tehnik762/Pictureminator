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
from scipy.fftpack import fft2, fftshift
from sklearn.cluster import KMeans

register_heif_opener()


def processImage(url):
    """
    This function will accept a destination url of an image and return a dictionary of the image properties
    :param url: str
    :return: dict
    """

    res = {}
    if url.split(".")[-1].lower() == "heic":
        img = read_heic_image(url)
    else:
        img = cv2.imread(url)
    res['filesize'] = os.path.getsize(url)

    size = img.shape
    res['size_w'], res['size_h'] = size[1], size[0]
    res['aspect_ratio'] = res['size_h'] / res['size_w']
    if res['aspect_ratio'] > 1:
        res['landscape'] = 0
    else:
        res['landscape'] = 1

    res['sum_pixels'] = img.sum()
    res['std_pixels'] = img.std()
    res['mean_pixels'] = img.mean()

    pop_rare = calculate_popular_and_rare_pixels(img)

    c_name = ["b", "g", "r"]
    i = 0
    for ch in pop_rare:
        res["pop_" + c_name[i]], res["pop_n_" + c_name[i]], res["rare_" + c_name[i]], res["rare_n_" + c_name[i]] = ch
        i += 1

    #Resize image
    img = resize_image(img)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    res['mean_value_b'], res['mean_value_g'], res['mean_value_r'] = np.mean(img, axis=(0, 1))
    res['median_value_b'], res['median_value_g'], res['median_value_r'] = np.median(img, axis=(0, 1))
    res['std_deviation_b'], res['std_deviation_g'], res['std_deviation_r'] = np.std(img, axis=(0, 1))
    res['color_diversity'] = np.mean([res['std_deviation_b'], res['std_deviation_g'], res['std_deviation_r']])

    res["contrast"], res["brightness"] = calculate_contrast_brightness(gray_image)
    res['hist_std'] = calculate_hist_std(img)
    res.update(extract_color_histogram(img))
    features, hog_variance = calculate_hog_features(gray_image)
    res["hog_features_mean"] = np.mean(features)
    res["hog_features_median"] = np.median(features)
    res["hog_features_std"] = np.std(features)
    res["hog_features_len"] = len(features)
    res["hog_variance"] = hog_variance
    res['h_mean'], res['h_median'], res['h_std'], res['s_mean'], res['s_median'], \
        res['s_std'], res['v_mean'], res['v_median'], res['v_std'], res["color_harmony"] = extract_color_features(img)
    res['n_objects'], res['area'], res['area_mean'], res['area_std'], res['vert'], res['vert_mean'], res['vert_std'],\
        res['color_mean'], res['color_std'], res['object_density'], res['shape_complexity'] = extract_shape_and_size_features(img)
    res['corners'], res['lines'], res['edge_density'] = count_corners_and_lines(gray_image)
    res.update(detect_faces_opencv(img))
    res['has_text'] = has_text_opencv(gray_image)
    res.update(calculate_sharpness(gray_image))
    res["gaussian_blur"], res['edge_sharpness'] = estimate_blur_gaussian(gray_image)
    res['gibson_blur'], res['spectrum'] = estimate_blur_gibson(gray_image)
    res['gradient'], res['gradient_magnitude'], res['gradient_direction'] = calculate_gradients(gray_image)
    res.update(calculate_texture_features(gray_image))
    res["color_balance"] = np.mean([res['std_deviation_b'], res['std_deviation_g'], res['std_deviation_r']])
    res["focus_score"] = calculate_focus(gray_image)
    res.update(calculate_image_hashes(url))
    fft = np.fft.fft2(img)
    res.update(calculate_fourier_transform(fft))
    res.update(calculate_phase_congruency(fft))
    res.update(calculate_image_symmetry(img))
    res.update(get_dominant_color(img))


    del img
    del gray_image
    return res

def calculate_contrast_brightness(gray_image):
    contrast = np.std(gray_image)
    brightness = np.mean(gray_image)

    return contrast, brightness

def calculate_hog_features(gray_image):
    """
    Calculate Histogram of Oriented Gradients (HOG) features for the given gray image.

    :param gray_image: The input grayscale image.
    :return: A tuple containing the calculated HOG features and the variance of the HOG features.
    """
    features, _ = hog(gray_image, orientations=8, pixels_per_cell=(8, 8),
                              cells_per_block=(1, 1), visualize=True)
    # Calculate variance of HOG features
    hog_variance = np.var(features)

    features = exposure.rescale_intensity(features, in_range=(0, 10))

    return features, hog_variance

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

    # Calculate overall color harmony score as the mean of standard deviations
    color_harmony_score = np.mean([h_std, s_std, v_std])

    return h_mean, h_median, h_std, s_mean, s_median, s_std, v_mean, v_median, v_std, color_harmony_score


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

    # Calculate shape complexity for each contour
    complexities = []

    for contour in contours:
        # Вычисление периметра контура
        perimeter = cv2.arcLength(contour, True)

        # Вычисление приближенной формы контура
        epsilon = 0.02 * perimeter
        approx_shape = cv2.approxPolyDP(contour, epsilon, True)

        # Вычисление площади контура
        area_sq = cv2.contourArea(contour)

        if area_sq > 0:
            complexity = perimeter / np.sqrt(area_sq)
            complexities.append(complexity)
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

    # Calculate the number of detected objects (contours)
    num_objects = len(contours)

    # Calculate object density relative to image size
    image_area = gray_image.shape[0] * gray_image.shape[1]
    object_density = num_objects / image_area

    # Calculate average shape complexity across contours
    if complexities:
        shape_complexity = np.mean(complexities)
    else:
        shape_complexity = 0.0

    del gray_image, binary_image, contours, region_features
    return n, area, area_mean, area_std, vert, vert_mean, vert_std, color_mean, color_std, object_density, shape_complexity

def count_corners_and_lines(gray_image):
    """
    This function counts the corners and lines in the given gray image.

    :param gray_image: The input gray image to detect corners and lines.
    :return: A tuple containing the number of corners, number of lines, and edge density.
    """
    # Finding corners (Shi-Tomasi)
    corners = cv2.goodFeaturesToTrack(gray_image, maxCorners=1000, qualityLevel=0.01, minDistance=10)
    corners_count = len(corners)

    # Hough Detector for lines
    edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)
    lines_count = len(lines) if lines is not None else 0

    edge_density = np.count_nonzero(edges) / (gray_image.shape[0] * gray_image.shape[1])

    del corners, edges, lines
    return corners_count, lines_count, edge_density

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
    if faces > 0:
        humans = 1
    else:
        humans = 0
    del rgb_image, face_locations, face_landmarks_list

    return {"faces": faces, "blink": blink_count, "has_humans": humans}
	
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
    """
    Calculate gradients using Sobel operators and compute sharpness, gradient magnitude, and orientation.

    :param gray_image: The input grayscale image.
    :return: A tuple containing the sharpness, gradient magnitude, and average gradient direction.
    """
    # Compute gradients using Sobel operators
    gradient_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

    # Compute sharpness
    sharpness = np.mean(gradient_x**2 + gradient_y**2)

    # Compute gradient magnitude and orientation
    magnitude, angle = cv2.cartToPolar(gradient_x, gradient_y, angleInDegrees=True)

    # Calculate average gradient direction
    gradient_direction = np.mean(angle)
    magnitude = np.mean(magnitude)

    return sharpness, magnitude, gradient_direction

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

    # Compute Laplacian to highlight edges
    laplacian = cv2.Laplacian(blurred, cv2.CV_64F)

    # Calculate variance of Laplacian to measure edge sharpness
    edge_sharpness = np.var(laplacian)

    return blur_metric, edge_sharpness

def estimate_blur_gibson(gray_image):
    f_transform = fftshift(fft2(gray_image))
    spectrum = np.abs(f_transform)
    blur_metric = np.sum(np.log(1 + spectrum))
    return blur_metric, np.mean(spectrum)

def eye_aspect_ratio(eye):
    vertical_dist = eye[1][1] - eye[5][1]

    horizontal_dist = eye[3][0] - eye[0][0]
    ear = vertical_dist / horizontal_dist

    return ear

def read_heic_image(file_path):
    img = Image.open(file_path)
    img = np.array(img)
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def resize_image(image, max_dimension=1000):
    height, width = image.shape[:2]
    if max(height, width) > max_dimension:
        scale_factor = max_dimension / max(height, width)
        resized_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)
        return resized_image
    else:
        return image


def calculate_popular_and_rare_pixels(image):
    result = []

    height, width, channels = image.shape

    for channel in range(channels):
        unique_values, counts = np.unique(image[:, :, channel], return_counts=True)

        popular_index = np.argmax(counts)
        rare_index = np.argmin(counts)

        popular_pixel = unique_values[popular_index]
        rare_pixel = unique_values[rare_index]
        popular_count = counts[popular_index]
        rare_count = counts[rare_index]

        result.append((popular_pixel, popular_count, rare_pixel, rare_count))

    return result

def calculate_hist_std(image):
    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    hist = hist / np.sum(hist)
    return np.std(hist)


def calculate_fourier_transform(fft):

    fft_shift = np.fft.fftshift(fft)
    dominant_frequency = np.argmax(np.abs(fft_shift))
    frequency_spread = np.std(np.angle(fft_shift))
    frequency_asymmetry = np.mean(np.abs(fft_shift) * np.exp(1j * np.angle(fft_shift)))
    return {"dominant_frequency": dominant_frequency, "frequency_spread": frequency_spread, "frequency_asymmetry": np.abs(frequency_asymmetry)}

def calculate_phase_congruency(fft):
    phase = np.angle(fft)
    coherence = np.abs(np.fft.ifft2(fft * np.conj(fft)).real)
    phase_congruency = coherence * np.exp(1j * phase)
    return {"phase_congruency": np.abs(np.mean(phase_congruency))}

def calculate_image_symmetry_axis(img, axis):
    # Flip the image along the specified axis
    flipped_img = np.flip(img, axis)

    # Calculate the difference between the original and flipped images
    diff = np.abs(img - flipped_img)

    # Calculate the symmetry as 1 - (average difference / maximum possible difference)
    symmetry = 1 - (np.mean(diff) / 255)

    return symmetry

def calculate_image_symmetry(img):

    symmetry = [0, 0]
    symmetry[0] = calculate_image_symmetry_axis(img, 0)
    symmetry[1] = calculate_image_symmetry_axis(img, 1)


    return {"symmetry_0": symmetry[0], "symmetry_1": symmetry[1]}


def get_dominant_color(image, k=3):
    """
    Get the dominant color from an image using K-Means clustering.

    :param image: numpy.ndarray
        Input image in RGB format.
    :param k: int, optional
        Number of clusters for K-Means. Default is 3.
    :return: numpy.ndarray
        Dominant color in RGB format.
    """
    # Reshape the image to a 2D array of pixels
    pixels = image.reshape(-1, 3)

    # Fit K-Means clustering to identify dominant colors
    kmeans = KMeans(n_clusters=k, n_init="auto")
    kmeans.fit(pixels)

    # Get the cluster centers (dominant colors)
    dominant_colors = kmeans.cluster_centers_

    # Find the cluster with the most pixels (dominant cluster)
    pixel_counts = np.bincount(kmeans.labels_)
    dominant_cluster = np.argmax(pixel_counts)

    # Get the dominant color
    dominant_color = dominant_colors[dominant_cluster]
    col_bgr = dominant_color.astype(int)
    return {"dominant_b": col_bgr[0], "dominant_g": col_bgr[1], "dominant_r": col_bgr[2]}