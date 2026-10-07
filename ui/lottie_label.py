"""Виджет для отображения Lottie-анимаций в CustomTkinter.

Lottie — векторный формат анимации. Не теряет качество при любом
размере и всегда имеет прозрачный фон.

Для рендеринга используется библиотека rlottie-python,
которая преобразует Lottie-анимацию в кадры Pillow.
"""

import customtkinter as ctk
from rlottie_python import LottieAnimation
from PIL import Image


class LottieLabel(ctk.CTkLabel):
    """Метка, которая проигрывает Lottie-анимацию.

    Attributes:
        _frames (list): Список кадров CTkImage.
        _duration (int): Задержка между кадрами в мс.
        _current_frame (int): Индекс текущего кадра.
    """

    def __init__(self, master, json_path, size=(200, 200),
                 duration=50, **kwargs):
        """Инициализация Lottie-метки.

        Args:
            master: Родительский виджет.
            json_path (str): Путь к JSON-файлу Lottie.
            size (tuple): Размер в пикселях (ширина, высота).
            duration (int): Задержка между кадрами (мс).
            **kwargs: Дополнительные параметры CTkLabel.
        """
        self._size = size

        kwargs.setdefault("width", size[0])
        kwargs.setdefault("height", size[1])
        kwargs.setdefault("text", "")
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(master, **kwargs)

        # Загружаем анимацию
        self._anim = LottieAnimation.from_file(json_path)
        total_frames = self._anim.lottie_animation_get_totalframe()

        # Рендерим все кадры
        self._frames = []
        for i in range(total_frames):
            pil_frame = self._anim.render_pillow_frame(frame_num=i)
            pil_frame = pil_frame.resize(size, Image.LANCZOS)
            ctk_img = ctk.CTkImage(
                light_image=pil_frame,
                dark_image=pil_frame,
                size=size
            )
            self._frames.append(ctk_img)

        self._duration = duration
        self._current_frame = 0
        self._animate()

    def _animate(self):
        """Перелистывает кадры по кругу."""
        self.configure(image=self._frames[self._current_frame])
        self._current_frame = (
            self._current_frame + 1
        ) % len(self._frames)
        self.after(self._duration, self._animate)