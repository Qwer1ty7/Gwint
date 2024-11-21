import sys

from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow

from choice_deck_ds import Ui_choice_deck_form


class Choice_deck_form(QMainWindow):
    """
    Класс для создания формы выбора колоды в приложении.

    Наследуется от QMainWindow и предоставляет интерфейс для выбора различных
    колод, таких как Северное королевство, Нильфгаард, Скоэтаэл, Монстры и Скеллиге.

    Атрибуты:
        window_closed (pyqtSignal): Сигнал, который испускается при закрытии окна.
        push_button (str): Имя кнопки, которая вызвала закрытие окна.
    """

    window_closed = pyqtSignal()
    push_button = None

    def __init__(self):
        """
        Инициализация формы выбора колоды.

        Устанавливает интерфейс, настраивает флаги окна и соединяет кнопки
        с методом закрытия формы.
        """
        super(Choice_deck_form, self).__init__()
        self.ui = Ui_choice_deck_form()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        self.ui.kingdom_north.clicked.connect(self.close)  # type: ignore
        self.ui.nilf.clicked.connect(self.close)  # type: ignore
        self.ui.skoetael.clicked.connect(self.close)  # type: ignore
        self.ui.monsters.clicked.connect(self.close)  # type: ignore
        self.ui.skellege.clicked.connect(self.close)  # type: ignore

    def close_form(self):
        """
        Закрывает форму выбора колоды.

        Вызывается для закрытия текущего окна.
        """
        self.close()

    def closeEvent(self, event):
        """
        Обработчик события закрытия окна.

        Испускает сигнал window_closed и сохраняет имя кнопки, которая вызвала
        закрытие формы.

        Args:
            event (QCloseEvent): Событие закрытия окна.
        """
        if self.sender() is not None:
            self.push_button = self.sender().objectName()

        self.window_closed.emit()
        event.accept()

    def keyPressEvent(self, event):
        """
        Обработчик нажатий клавиш.

        Закрывает приложение при нажатии клавиш 'Q' или 'Escape'.

        Args:
            event (QKeyEvent): Событие нажатия клавиши.
        """
        key = event.key()

        if key == QtCore.Qt.Key.Key_Q or key == QtCore.Qt.Key.Key_Escape:
            sys.exit()