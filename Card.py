import os
import random
import uuid

from PyQt6 import QtCore
from PyQt6.QtCore import QMimeData, QSize, Qt
from PyQt6.QtGui import QDrag, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel

import card_params


class Card:
    """
    Класс, представляющий карточку с уникальными характеристиками.

    Атрибуты:
        _uuid (UUID): Уникальный идентификатор карточки.
        _name (str): Название карточки.
        _fraction (str): Фракция карточки.
        _score (int): Очки карточки.
        _quality (int): Качество карточки.
        _combat (int): Боевые характеристики карточки.
        _skill (int): Навыки карточки.
        score_in_battlefield (int): Очки на поле боя.
    """

    def __init__(self, name, fraction):
        """
        Инициализация карточки.

        Аргументы:
            name (str): Название карточки.
            fraction (str): Фракция карточки.

        Исключения:
            Exception: Если карточка не найдена в словаре параметров.
        """
        self._uuid = uuid.uuid4()
        self._name = name
        self._fraction = fraction
        params = card_params.CARD_PARAMS.get(name)
        if params is None:
            raise Exception(f"{name} не найден в словаре")

        self._score = params[0]
        self._quality = params[1]
        self._combat = params[2]
        self._skill = params[3]

        self.score_in_battlefield = 0

        self.__load_image()

    def __load_image(self):
        """Загрузка изображений лицевой и оборотной сторон карточки."""
        self.__path_face = os.path.join(
            "images", "cards", self._fraction, "%s.png" % self._name
        )
        self.__face = QPixmap(self.__path_face)
        self.__path_back = os.path.join(
            "images", "cards", self._fraction, "%s.png" % self._fraction
        )
        self.__back = QPixmap(self.__path_back)

    @property
    def face(self):
        """Возвращает изображение лицевой стороны карточки."""
        return self.__face

    @property
    def back(self):
        """Возвращает изображение оборотной стороны карточки."""
        return self.__back

    @property
    def path_face(self):
        """Возвращает путь к изображению лицевой стороны карточки."""
        return self.__path_face

    @property
    def path_back(self):
        """Возвращает путь к изображению оборотной стороны карточки."""
        return self.__path_back

    @property
    def name(self):
        """Возвращает название карточки."""
        return self._name

    @property
    def uuid(self):
        """Возвращает уникальный идентификатор карточки."""
        return self._uuid

    @property
    def score(self):
        """Возвращает очки карточки."""
        return self._score

    @property
    def combat(self):
        """Возвращает боевые характеристики карточки."""
        return self._combat

    @property
    def skill(self):
        """Возвращает навыки карточки."""
        return self._skill

    @property
    def quality(self):
        """Возвращает качество карточки."""
        return self._quality


class Deck(Card):
    """
    Класс, представляющий колоду карточек.

    Атрибуты:
        my_quantity_card (list): Список карточек игрока.
        enemy_quantity_card (list): Список карточек противника.
    """

    my_quantity_card = []
    enemy_quantity_card = []

    def __init__(self, name=0, fraction=None, side=None):
        """
        Инициализация колоды.

        Аргументы:
            name (str): Название колоды.
            fraction (str): Фракция колоды.
            side (str): Сторона колоды (игрок или противник).

        Исключения:
            Exception: Если карточка не найдена в словаре параметров.
        """
        try:
            Card.__init__(self, name, fraction)
        except Exception as a:
            print(name)
            raise Exception(str(a))

        self.fraction_deck = fraction
        if side is not None:
            self.add(side)

    def add(self, side):
        """
        Добавляет карточку в соответствующую сторону.

        Аргументы:
            side (str): Сторона, к которой добавляется карточка (игрок или противник).
        """
        if side == card_params.ME:
            self.my_quantity_card.append(self)
        else:
            self.enemy_quantity_card.append(self)


class Deal:
    """
    Класс, представляющий сделку с карточкой.

    Атрибуты:
        my_quantity_card (list): Список карточек игрока.
        enemy_quantity_card (list): Список карточек противника.
    """

    my_quantity_card = []
    enemy_quantity_card = []

    def __init__(self, card: Card, centralwidget, geometry_parent=None, side=None):
        """
        Инициализация сделки с карточкой.

        Аргументы:
            card (Card): Карточка для сделки.
            centralwidget (QWidget): Центральный виджет для отображения.
            geometry_parent (QRect | None): Геометрия родительского элемента (по умолчанию None).
            side (str | None): Сторона сделки (по умолчанию None).

        Исключения:
            Exception: Если карточка не может быть инициализирована.
        """
        self.card = card
        self.geometry_parent = geometry_parent

        self.label = ClickableLabel(parent=centralwidget)

        if self.geometry_parent is not None:
            self.init_single_pos()

        self.label.setPixmap(card.face)
        self.label.setScaledContents(True)
        self.label.setObjectName(f"Label{self.card.uuid}")

        if side != card_params.ME:
            self.label.hide()
        else:
            self.label.show()

        if side is not None:
            self.add(side)

    def init_all_pos(self):
        """
        Инициализация позиции всех карточек игрока в колоде.

        Устанавливает геометрию для каждой карточки в списке my_quantity_card
        на основе их текущих позиций и ширины родительского элемента.
        """
        count = -1
        dif = self.geometry_parent.width() + 5

        if len(self.my_quantity_card) > 10:
            dif = int(
                (
                        self.geometry_parent.width() * len(self.my_quantity_card)
                        - self.geometry_parent.width() * 10
                )
                / len(self.my_quantity_card)
            )
            dif = int(self.geometry_parent.width() - dif)

        for card in self.my_quantity_card:
            count += 1
            if self.my_quantity_card[0].label.x() != self.geometry_parent.x():
                x = self.geometry_parent.x()
                y = self.geometry_parent.y()
            else:
                if count - 1 < 0:
                    continue
                x = self.my_quantity_card[count - 1].label.x() + dif
                y = self.my_quantity_card[count - 1].label.y()
            card.label.setGeometry(
                x, y, self.geometry_parent.width(), self.geometry_parent.height()
            )

    def init_single_pos(self):
        """
        Инициализация позиции одной карточки в сделке.

        Устанавливает геометрию для текущей карточки на основе ее положения
        относительно других карточек в списке my_quantity_card и родительского элемента.
        """
        if (
                not self.my_quantity_card
                or self.my_quantity_card[0].label.x() != self.geometry_parent.x()
        ):
            x = self.geometry_parent.x()
            y = self.geometry_parent.y()
        else:
            x = self.my_quantity_card[-1].label.x() + self.geometry_parent.width() + 5
            y = self.my_quantity_card[-1].label.y()

        self.label.setGeometry(
            x, y, self.geometry_parent.width(), self.geometry_parent.height()
        )

    def add(self, side):
        """
        Добавляет сделку в соответствующий список карточек.

        Аргументы:
            side (str): Сторона, к которой добавляется сделка (игрок или противник).
        """
        if side == card_params.ME:
            self.my_quantity_card.append(self)
        else:
            self.enemy_quantity_card.append(self)

    def pop_my_deal(self, i):
        """
        Удаляет карточку из списка сделок игрока.

        Аргументы:
            i (int): Индекс карточки для удаления из my_quantity_card.
        """
        self.my_quantity_card.pop(i)

    def pop_enemy_deal(self, i):
        """
        Удаляет карточку из списка сделок противника.

        Аргументы:
            i (int): Индекс карточки для удаления из enemy_quantity_card.
        """
        self.enemy_quantity_card.pop(i)


class ClickableLabel(QLabel):
    """
    Класс, представляющий кликабельную метку (label).

    Сигналы:
        clicked (pyqtSignal): Сигнал, который испускается при клике на метку.
    """

    clicked = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        """
        Инициализация кликабельной метки.

        Аргументы:
            *args: Позиционные аргументы для QLabel.
            **kwargs: Именованные аргументы для QLabel.
        """
        QLabel.__init__(self, *args, **kwargs)

    def mousePressEvent(self, ev):
        """
        Обрабатывает событие нажатия кнопки мыши.

        Аргументы:
            ev (QMouseEvent): Событие нажатия кнопки мыши.
        """
        if (
            ev.button() == Qt.MouseButton.LeftButton
            or ev.button() == Qt.MouseButton.RightButton
        ):
            self.drag_start_position = ev.pos()

    def mouseMoveEvent(self, ev):
        """
        Обрабатывает событие перемещения мыши.

        Запускает перетаскивание, если левая кнопка мыши нажата и перемещение
        превышает минимальное расстояние.

        Аргументы:
            ev (QMouseEvent): Событие перемещения мыши.
        """
        if not (ev.buttons() & Qt.MouseButton.LeftButton):
            return
        if (
            ev.pos() - self.drag_start_position
        ).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setObjectName(self.objectName())
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(ev.pos())
        drag.exec(Qt.DropAction.MoveAction)


class DropLabel(QLabel):
    """
    Класс, представляющий метку для сброса карточек.

    Атрибуты:
        myMelee_deal (list): Список сделок игрока с ближним боем.
        myRanged_deal (list): Список сделок игрока с дальним боем.
        mySiege_deal (list): Список сделок игрока с осадой.

        enemyMelee_deal (list): Список сделок противника с ближним боем.
        enemyRanged_deal (list): Список сделок противника с дальним боем.
        enemySiege_deal (list): Список сделок противника с осадой.
    """
    myMelee_deal = []
    myRanged_deal = []
    mySiege_deal = []

    enemyMelee_deal = []
    enemyRanged_deal = []
    enemySiege_deal = []

    def __init__(self, size, main, battlefield, player, *args, **kwargs):
        """
        Инициализация метки для сброса карточек.

        Аргументы:
            size (QSize): Размер метки.
            main (MainClass): Основной класс приложения.
            battlefield (str): Поле боя для размещения карточек.
            player (str): Игрок, которому принадлежит метка.
            *args: Позиционные аргументы для QLabel.
            **kwargs: Именованные аргументы для QLabel.
        """
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.resize(QSize(size.width(), size.height()))
        self.size = size
        self.main = main
        self.player = player
        self.battlefield = battlefield
        self.size_card = QSize(int(self.size.width() / 10), int(self.size.height()))
        self.command_horn = False

    def dragEnterEvent(self, event):
        """
        Обрабатывает событие входа перетаскиваемого объекта в область метки.

        Аргументы:
            event (QDragEnterEvent): Событие входа перетаскиваемого объекта.
        """
        event.acceptProposedAction()
        event.accept()

    def dropEvent(self, event):
        """
        Обрабатывает событие сброса перетаскиваемого объекта на метку.

        Аргументы:
            event (QDropEvent): Событие сброса перетаскиваемого объекта.
        """
        my_deal = self.main.get_my_deal()
        count = -1
        my_move = False
        for deal in my_deal.my_quantity_card:
            count += 1

            if deal.label.objectName() == event.mimeData().objectName():
                my_move = True
                # Проверить, что тип карточки совпадает с типом поля, на которое карточку перетаскивают
                if self.battlefield not in deal.card.combat:
                    event.ignore()
                    my_move = False
                    break

                count_cards_in_battlefield = 0

                # Карточки, со скиллом шпиона можно перетаскивать только на противоположное поле
                if deal.card.skill == card_params.SPY:
                    if self.player != card_params.ENEMY:
                        event.ignore()
                        my_move = False
                        break
                    else:
                        match deal.card.combat:
                            case card_params.MELEE:
                                count_cards_in_battlefield = len(self.enemyMelee_deal)
                                self.enemyMelee_deal.append(deal.card)
                                self.main.update_enemy_melee_score()
                            case card_params.RANGED:
                                count_cards_in_battlefield = len(self.enemyRanged_deal)
                                self.enemyRanged_deal.append(deal.card)
                                self.main.update_enemy_ranged_score()
                            case card_params.SIEGE:
                                count_cards_in_battlefield = len(self.enemySiege_deal)
                                self.enemySiege_deal.append(deal.card)
                                self.main.update_enemy_siege_score()

                        # Добавить в свою колоду 2 карточки
                        for i in range(2):
                            try:
                                random_id = random.choice(
                                    range(len(self.main.myDeck.my_quantity_card))
                                )
                                self.main.add_card_mydeal(random_id)
                            except Exception:
                                print("Не осталось карточек в колоде")

                else:
                    # Обычная обработка перетаскивания карточки на своё поле
                    match deal.card.combat:
                        case card_params.MELEE:
                            count_cards_in_battlefield = len(self.myMelee_deal)
                            self.myMelee_deal.append(deal.card)
                            self.main.update_my_melee_score()
                        case card_params.RANGED:
                            count_cards_in_battlefield = len(self.myRanged_deal)
                            self.myRanged_deal.append(deal.card)
                            self.main.update_my_ranged_score()
                        case card_params.SIEGE:
                            count_cards_in_battlefield = len(self.mySiege_deal)
                            self.mySiege_deal.append(deal.card)
                            self.main.update_my_siege_score()
                        case card_params.MELEE_RANGED:
                            match self.battlefield:
                                case card_params.MELEE:
                                    count_cards_in_battlefield = len(self.myMelee_deal)
                                    self.myMelee_deal.append(deal.card)
                                    self.main.update_my_melee_score()
                                case card_params.RANGED:
                                    count_cards_in_battlefield = len(self.myRanged_deal)
                                    self.myRanged_deal.append(deal.card)
                                    self.main.update_my_ranged_score()

                deal.label.move(
                    self.size.x()
                    + (self.size_card.width() * count_cards_in_battlefield),
                    self.size.y(),
                )
                deal.label.resize(self.size_card)
                my_deal.pop_my_deal(count)
                deal.init_all_pos()
                self.main.update_label_cards_in_my_deal()
                break

        if my_move is True:
            # Ход противника
            self.main.enemy_move()

        event.acceptProposedAction()
