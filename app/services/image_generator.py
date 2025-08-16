# -*- coding: utf-8 -*-
"""
Этот модуль отвечает за генерацию изображения купона на основе шаблона.
"""

import os
import skia

# Определяем базовые пути
APP_DIR = os.path.dirname(os.path.dirname(__file__))
FONT_PATH = os.path.join(APP_DIR, 'static', 'fonts', 'IntroDemoCond-LightCAPS.otf')
COUPON_TEMPLATE_PATH = os.path.join(APP_DIR, 'static', 'kupon.png')

def create_coupon_image(user_fio: str) -> str:
    """
    Вставляет ФИО пользователя в готовый шаблон купона.

    Args:
        user_fio (str): ФИО пользователя для вставки в купон.

    Returns:
        str: Путь к сгенерированному изображению.
    """
    # --- Проверка наличия шаблона ---
    if not os.path.exists(COUPON_TEMPLATE_PATH):
        raise FileNotFoundError(f"Шаблон купона не найден по пути: {COUPON_TEMPLATE_PATH}")

    # --- Загрузка изображения-шаблона ---
    image = skia.Image.open(COUPON_TEMPLATE_PATH)
    if not image:
        raise IOError("Не удалось загрузить изображение шаблона.")

    WIDTH, HEIGHT = image.width(), image.height()

    # --- Создание поверхности на основе изображения ---
    surface = skia.Surface(WIDTH, HEIGHT)
    canvas = surface.getCanvas()
    canvas.drawImage(image, 0, 0)

    # --- Шрифты и стили ---
    try:
        font_typeface = skia.Typeface.MakeFromFile(FONT_PATH)
        if not font_typeface:
            raise IOError("Не удалось создать шрифт из файла")
    except IOError as e:
        print(f"Ошибка загрузки шрифта: {e}. Используется шрифт по умолчанию.")
        font_typeface = skia.Typeface.MakeDefault()

    paint_white = skia.Paint(Color=skia.ColorWHITE, AntiAlias=True)
    font_fio = skia.Font(font_typeface, 62) # Размер шрифта можно подобрать

    # --- Отрисовка ФИО ---
    x_pos = 50
    y_pos = 360
    line_height = 65 # Расстояние между строками

    words = user_fio.split()
    if len(words) > 2:
        line1 = " ".join(words[:2])
        line2 = " ".join(words[2:])
        canvas.drawString(line1, x_pos, y_pos, font_fio, paint_white)
        canvas.drawString(line2, x_pos, y_pos + line_height, font_fio, paint_white)
    else:
        canvas.drawString(user_fio, x_pos, y_pos, font_fio, paint_white)


    # --- Сохранение файла ---
    output_filename = f"coupon_{user_fio.replace(' ', '_')}.png"
    snapshot = surface.makeImageSnapshot()
    snapshot.save(output_filename, skia.kPNG)

    return output_filename
