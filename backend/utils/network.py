from PIL import Image
import itertools
import cv2
import numpy as np
import tensorflow as tf
from skimage.color import rgb2gray
from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks, rotate
from io import BytesIO
import zipfile
import base64


class ImageProcessor:
    """Класс для обработки изображений."""

    def __init__(self, background_size=(1024, 1024), background_color=(255, 0, 0)):
        """
        Инициализация класса ImageProcessor.

        Args:
            background_size (tuple[int, int]): Размер фона.
            background_color (tuple[int, int, int]): Цвет фона в формате RGB.
        """
        self.background_size = background_size
        self.background_color = background_color

    def create_red_background_image(self, image: Image.Image) -> Image.Image:
        """
        Создание изображения с красным фоном и центровка входного изображения.

        Args:
            image (Image.Image): Входное изображение.

        Returns:
            Image.Image: Изображение с красным фоном.
        """
        background = Image.new('RGB', self.background_size, self.background_color)
        image.thumbnail(self.background_size, Image.LANCZOS)
        img_position = ((self.background_size[0] - image.size[0]) // 2,
                        (self.background_size[1] - image.size[1]) // 2)
        background.paste(image, img_position)
        return background

    def process_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Обработка изображения: добавление красного фона и конвертация в формат OpenCV.

        Args:
            image_bytes (bytes): Изображение в виде байт.

        Returns:
            np.ndarray: Обработанное изображение в формате OpenCV.
        """
        pil_image = Image.open(BytesIO(image_bytes))
        processed_image = self.create_red_background_image(pil_image)

        with BytesIO() as output:
            processed_image.save(output, format="JPEG")
            processed_image_bytes = output.getvalue()

        image = cv2.imdecode(np.frombuffer(processed_image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return image


class LicensePlateRecognition:
    """Класс для распознавания номерных знаков."""

    def __init__(self, model_resnet_path: str, model_nomer_path: str, letters: list[str]):
        """
        Инициализация класса LicensePlateRecognition.

        Args:
            model_resnet_path (str): Путь к модели ResNet.
            model_nomer_path (str): Путь к модели для распознавания номеров.
            letters (list[str]): Список допустимых символов для распознавания номеров.
        """
        self.model_resnet_path = model_resnet_path
        self.model_nomer_path = model_nomer_path
        self.letters = letters
        self.image_processor = ImageProcessor()

    def decode_batch(self, out: np.ndarray) -> list[str]:
        """
        Декодирование выхода модели в строку.

        Args:
            out (np.ndarray): Выход модели.

        Returns:
            list[str]: Список распознанных строк.
        """
        ret = []
        for j in range(out.shape[0]):
            out_best = list(np.argmax(out[j, 2:], 1))
            out_best = [k for k, g in itertools.groupby(out_best)]
            outstr = ''
            for c in out_best:
                if c < len(self.letters):
                    outstr += self.letters[c]
            ret.append(outstr)
        return ret

    def load_model(self, model_path: str) -> tf.lite.Interpreter:
        """
        Загрузка TFLite модели.

        Args:
            model_path (str): Путь к модели.

        Returns:
            tf.lite.Interpreter: Интерпретатор модели TFLite.
        """
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter

    def predict_with_model(self, interpreter: tf.lite.Interpreter, image: np.ndarray) -> list[np.ndarray]:
        """
        Предсказание с помощью модели.

        Args:
            interpreter (tf.lite.Interpreter): Интерпретатор модели.
            image (np.ndarray): Входное изображение.

        Returns:
            list[np.ndarray]: Результаты предсказания.
        """
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        input_index = input_details[0]['index']
        interpreter.set_tensor(input_index, image)
        interpreter.invoke()
        return [interpreter.get_tensor(output_detail['index']) for output_detail in output_details]

    def process_image(self, image_bytes: bytes) -> tuple[np.ndarray, np.ndarray, int, int]:
        """
        Обработка входного изображения.

        Args:
            image_bytes (bytes): Изображение в виде байт.

        Returns:
            tuple[np.ndarray, np.ndarray, int, int]: Оригинальное изображение, измененное изображение, высота и ширина изображения.
        """
        image0 = self.image_processor.process_image(image_bytes)
        image_height, image_width, _ = image0.shape
        image = cv2.resize(image0, (1024, 1024)).astype(np.float32)
        return image0, image, image_height, image_width

    def detect_plate(self, image: np.ndarray, interpreter: tf.lite.Interpreter) -> list[np.ndarray]:
        """
        Обнаружение номерного знака на изображении.

        Args:
            image (np.ndarray): Входное изображение.
            interpreter (tf.lite.Interpreter): Интерпретатор модели.

        Returns:
            list[np.ndarray]: Координаты обнаруженных объектов.
        """
        X_data1 = np.float32(image.reshape(1, 1024, 1024, 3))
        detections = self.predict_with_model(interpreter, X_data1)
        return detections

    def get_bounding_box(self, detection: np.ndarray, image_height: int, image_width: int) -> tuple[int, int, int, int]:
        """
        Получение координат ограничивающего прямоугольника.

        Args:
            detection (np.ndarray): Данные обнаружения.
            image_height (int): Высота изображения.
            image_width (int): Ширина изображения.

        Returns:
            tuple[int, int, int, int]: Координаты ограничивающего прямоугольника.
        """
        box_x = int(detection[0, 0, 0] * image_height)
        box_y = int(detection[0, 0, 1] * image_width)
        box_width = int(detection[0, 0, 2] * image_height)
        box_height = int(detection[0, 0, 3] * image_width)
        return box_x, box_y, box_width, box_height

    def rotate_image(self, image: np.ndarray, angle: float) -> np.ndarray:
        """
        Поворот изображения на заданный угол.

        Args:
            image (np.ndarray): Входное изображение.
            angle (float): Угол поворота.

        Returns:
            np.ndarray: Повернутое изображение.
        """
        rotated = rotate(image, angle, resize=True) * 255
        rotated = rotated.astype(np.uint8)
        return rotated

    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        """
        Улучшение качества изображения.

        Args:
            image (np.ndarray): Входное изображение.

        Returns:
            np.ndarray: Улучшенное изображение.
        """
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return final

    def extract_text(self, image: np.ndarray, interpreter: tf.lite.Interpreter) -> list[str]:
        """
        Извлечение текста из изображения.

        Args:
            image (np.ndarray): Входное изображение.
            interpreter (tf.lite.Interpreter): Интерпретатор модели.

        Returns:
            list[str]: Список распознанных строк.
        """
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (128, 64)).astype(np.float32) / 255
        img1 = img.T
        X_data1 = np.float32(img1.reshape(1, 128, 64, 1))
        net_out_value = self.predict_with_model(interpreter, X_data1)[0]
        pred_texts = self.decode_batch(net_out_value)
        return pred_texts

    def process(self, image_bytes: bytes) -> tuple[list[str], bytes]:
        """
        Основной процесс обработки изображения.

        Args:
            image_bytes (bytes): Изображение в виде байт.

        Returns:
            tuple[list[str], bytes]: Список распознанных строк и выровненное изображение в байтах.
        """
        image0, image, image_height, image_width = self.process_image(image_bytes)

        interpreter_resnet = self.load_model(self.model_resnet_path)
        detection = self.detect_plate(image, interpreter_resnet)[0]

        box_x, box_y, box_width, box_height = self.get_bounding_box(detection, image_height, image_width)

        if np.min(detection[0, 0, :]) >= 0:
            cropped_image = image0[box_x:box_width, box_y:box_height, :]
            grayscale = rgb2gray(cropped_image)
            edges = canny(grayscale, sigma=3.0)
            out, angles, distances = hough_line(edges)
            _, angles_peaks, _ = hough_line_peaks(out, angles, distances, num_peaks=20)
            angle = np.mean(np.rad2deg(angles_peaks))

            if 0 <= angle <= 90:
                rot_angle = angle - 90
            elif -45 <= angle < 0:
                rot_angle = angle - 90
            elif -90 <= angle < -45:
                rot_angle = 90 + angle
            if abs(rot_angle) > 20:
                rot_angle = 0

            rotated_image = self.rotate_image(cropped_image, rot_angle)
            minus = np.abs(int(np.sin(np.radians(rot_angle)) * rotated_image.shape[0]))

            if rotated_image.shape[1] / rotated_image.shape[0] < 2 and minus > 10:
                rotated_image = rotated_image[minus:-minus, :, :]

            final_image = self.enhance_image(rotated_image)
            final_pil_image = Image.fromarray(cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB))

            with BytesIO() as output:
                final_pil_image.save(output, format="JPEG")
                final_image_bytes = output.getvalue()

            interpreter_nomer = self.load_model(self.model_nomer_path)
            pred_texts = self.extract_text(final_image, interpreter_nomer)
            return pred_texts, final_image_bytes
        else:
            raise ValueError('Номерной знак не обнаружен.')

    def process_zip(self, zip_bytes: bytes) -> dict[str, tuple[list[str], bytes]]:
        """
        Обработка изображений из zip-архива.

        Args:
            zip_bytes (bytes): Zip-архив в виде байт.

        Returns:
            dict[str, tuple[list[str], bytes]]: Словарь с именами файлов, распознанными текстами и выровненными изображениями в байтах.
        """
        results = {}
        with zipfile.ZipFile(BytesIO(zip_bytes), 'r') as zip_ref:
            for file_name in zip_ref.namelist()[0:3]:
                with zip_ref.open(file_name) as file:
                    image_bytes = file.read()
                    try:
                        text, aligned_image_bytes = self.process(image_bytes)
                        aligned_image_base64 = base64.b64encode(
                            aligned_image_bytes
                        )
                        results[file_name] = (text, aligned_image_base64)
                    except ValueError as e:
                        results[file_name] = ([str(e)], None)
        return results
