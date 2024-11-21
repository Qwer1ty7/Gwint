import random
import sys
import traceback
from os import walk

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QLabel, QMainWindow

import card_params
import images  # Не удалять!!!
from Card import Deal, Deck, DropLabel
from gwint_designer import Ui_MainWindow
from py_choice_deck import Choice_deck_form


class MainWindow(QMainWindow):
    """
    Главное окно приложения, наследующее от QMainWindow.

    Этот класс отвечает за инициализацию интерфейса игры, создание
    необходимых виджетов и обработку событий.
    """
    def __init__(self):
        """
        Инициализация главного окна.

        Создает и настраивает основные элементы интерфейса, включая
        метки для различных типов атак (ближний бой, дальний бой, осадные орудия)
        и связывает кнопки с действиями.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.label = QLabel()

        # Инициализация меток для атак игрока
        self.myMelee_deal = DropLabel(
            self.ui.myMelee_deal_designer.geometry(),
            self,
            card_params.MELEE,
            card_params.ME,
            self.ui.myMelee_deal_designer,
        )
        self.myRanged_deal = DropLabel(
            self.ui.myRanged_deal_designer.geometry(),
            self,
            card_params.RANGED,
            card_params.ME,
            self.ui.myRanged_deal_designer,
        )
        self.mySiege_deal = DropLabel(
            self.ui.mySiege_deal_designer.geometry(),
            self,
            card_params.SIEGE,
            card_params.ME,
            self.ui.mySiege_deal_designer,
        )

        # Инициализация меток для атак противника
        self.enemyMelee_deal = DropLabel(
            self.ui.enemyMelee_deal_designer.geometry(),
            self,
            card_params.MELEE,
            card_params.ENEMY,
            self.ui.enemyMelee_deal_designer,
        )
        self.enemyRanged_deal = DropLabel(
            self.ui.enemyRanged_deal_designer.geometry(),
            self,
            card_params.RANGED,
            card_params.ENEMY,
            self.ui.enemyRanged_deal_designer,
        )
        self.enemySiege_deal = DropLabel(
            self.ui.enemySiege_deal_designer.geometry(),
            self,
            card_params.SIEGE,
            card_params.ENEMY,
            self.ui.enemySiege_deal_designer,
        )

        # Скрытие элементов интерфейса
        self.ui.me_win.hide()
        self.ui.enemy_win.hide()

        self.ui.enemy_minus_life1.hide()
        self.ui.enemy_minus_life2.hide()
        self.ui.me_minus_life1.hide()
        self.ui.me_minus_life2.hide()

        # Инициализация выбора колоды
        self.choice_deck = Choice_deck_form()
        self.choice_deck.window_closed.connect(self.close_choice)
        self.choice_deck.show()

        # Подключение кнопок к функциям закрытия окна
        self.ui.button_q.clicked.connect(self.close)
        self.ui.button_esc.clicked.connect(self.close)

    def get_my_deal(self):
        """
        Получение текущей сделки игрока.

        :return: Сделка игрока.
        """
        return self.myDeal

    def get_enemy_deal(self):
        """
        Получение текущей сделки противника.

        :return: Сделка противника.
        """
        return self.enemyDeal

    def close_choice(self):
        """
        Обработка закрытия окна выбора колоды.

        Если кнопка выбора колоды была нажата, выводит информацию в консоль.
        Иначе завершает программу. Инициализирует колоду после закрытия выбора.
        """
        if self.choice_deck.push_button is not None:
            print(self.choice_deck.push_button)
        else:
            sys.exit()

        self.init_deck()

    def init_deck(self):
        """
        Инициализация колоды.

        Вызывает методы для инициализации фракций и карт, а также
        отображает главное окно.
        """
        self.init_fractions()
        self.init_cards()

        self.init_deal()
        self.show()

    def init_fractions(self):
        """
        Инициализация фракций.
        Загружает изображения фракций из указанной директории и
        устанавливает их для игрока и противника.
        """
        fractions = []
        for dirpath, dirnames, filenames in walk(r".\images\\fraction"):
            fractions.extend(filenames)
            fractions.extend(dirpath)

        try:
            myPicture = fractions[
                fractions.index(f"{self.choice_deck.push_button}.png")
            ]
            self.myFraction = myPicture.rsplit(".")[0]
            self.ui.myDeck.setPixmap(QtGui.QPixmap(f"{dirpath}\\{myPicture}"))

            enemyPicture = str(random.choice(filenames))
            self.enemyFraction = enemyPicture.rsplit(".")[0]
            self.ui.enemyDeck.setPixmap(QtGui.QPixmap(f"{dirpath}\\{enemyPicture}"))
        except (ValueError, AttributeError) as cx:
            print(str(cx))
            sys.exit()

    def update_label_cards_in_my_deck(self):
        """
        Обновляет метку, отображающую количество карт в колоде игрока.

        Если возникает ошибка доступа к атрибуту, устанавливает значение метки в "0".
        """
        try:
            self.ui.cardsInMyDeck.setText(str(len(self.myDeck.my_quantity_card)))
        except AttributeError:
            self.ui.cardsInMyDeck.setText("0")

    def update_label_cards_in_enemy_deck(self):
        """
        Обновляет метку, отображающую количество карт в колоде противника.

        Если возникает ошибка доступа к атрибуту, устанавливает значение метки в "0".
        """
        try:
            self.ui.cardsInEnemyDeck.setText(
                str(len(self.enemyDeck.enemy_quantity_card))
            )
        except AttributeError:
            self.ui.cardsInEnemyDeck.setText("0")

    def update_label_cards_in_my_deal(self):
        """
            Обновляет метку, отображающую количество карт в сделке игрока.

            Если возникает ошибка доступа к атрибуту, устанавливает значение метки в "0".
        """
        try:
            self.ui.cardsInMyDeal.setText(str(len(self.myDeal.my_quantity_card)))
        except AttributeError:
            self.ui.cardsInMyDeal.setText("0")

    def update_label_cards_in_enemy_deal(self):
        """
            Обновляет метку, отображающую количество карт в сделке противника.

            Если возникает ошибка доступа к атрибуту, устанавливает значение метки в "0".
        """
        try:
            self.ui.cardsInEnemyDeal.setText(
                str(len(self.enemyDeal.enemy_quantity_card))
            )
        except AttributeError:
            self.ui.cardsInEnemyDeal.setText("0")

    def update_my_score(self):
        """
            Обновляет счет игрока, суммируя очки из различных типов атак.

            Отображает победу игрока или скрывает метки победы, если ничья.
        """
        self.ui.my_Score.setText(
            str(
                int(self.ui.my_melee_score.text())
                + int(self.ui.my_ranged_score.text())
                + int(self.ui.my_siege_score.text())
            )
        )

        if int(self.ui.my_Score.text()) > int(self.ui.enemy_Score.text()):
            self.ui.me_win.show()
            self.ui.enemy_win.hide()
        elif int(self.ui.enemy_Score.text()) == int(self.ui.my_Score.text()):
            self.ui.enemy_win.hide()
            self.ui.me_win.hide()

    def update_my_melee_score(self):
        """
        Обновляет счет игрока за ближний бой и обновляет общий счет.

        Вызывает метод для обновления счета на поле боя и обновляет
        соответствующую метку.
        """
        score, command_horn = self.update_score_in_battlefield(
            self.myMelee_deal.myMelee_deal
        )
        self.ui.my_melee_score.setText(str(score))
        self.myMelee_deal.command_horn = command_horn
        self.update_my_score()

    def update_my_ranged_score(self):
        """
            Обновляет счет игрока за дальний бой и обновляет общий счет.

            Вызывает метод для обновления счета на поле боя и обновляет
            соответствующую метку.
        """
        score, command_horn = self.update_score_in_battlefield(
            self.myRanged_deal.myRanged_deal
        )
        self.ui.my_ranged_score.setText(str(score))
        self.myRanged_deal.command_horn = command_horn
        self.update_my_score()

    def update_my_siege_score(self):
        """
        Обновляет счет игрока за осадные орудия и обновляет общий счет.

        Вызывает метод для обновления счета на поле боя и обновляет
        соответствующую метку.
        """
        score, command_horn = self.update_score_in_battlefield(
            self.mySiege_deal.mySiege_deal
        )
        self.ui.my_siege_score.setText(str(score))
        self.mySiege_deal.command_horn = command_horn
        self.update_my_score()

    def update_enemy_score(self):
        """
        Обновляет счет противника, суммируя очки из различных типов атак.

        Отображает победу противника или скрывает метки победы, если ничья.
        """
        self.ui.enemy_Score.setText(
            str(
                int(self.ui.enemy_melee_score.text())
                + int(self.ui.enemy_ranged_score.text())
                + int(self.ui.enemy_siege_score.text())
            )
        )

        if int(self.ui.enemy_Score.text()) > int(self.ui.my_Score.text()):
            self.ui.enemy_win.show()
            self.ui.me_win.hide()
        elif int(self.ui.enemy_Score.text()) == int(self.ui.my_Score.text()):
            self.ui.enemy_win.hide()
            self.ui.me_win.hide()

    def update_enemy_melee_score(self):
        """
        Обновляет счет противника за ближний бой и обновляет общий счет.

        Вызывает метод для обновления счета на поле боя и обновляет
        соответствующую метку.
        """
        score, command_horn = self.update_score_in_battlefield(
            self.enemyMelee_deal.enemyMelee_deal
        )
        self.ui.enemy_melee_score.setText(str(score))
        self.enemyMelee_deal.command_horn = command_horn
        self.update_enemy_score()

    def update_enemy_ranged_score(self):
        """
        Обновляет счет противника за дальний бой и обновляет общий счет.

        Вызывает метод для обновления счета на поле боя и обновляет
        соответствующую метку.
        """
        score, command_horn = self.update_score_in_battlefield(
            self.enemyRanged_deal.enemyRanged_deal
        )
        self.ui.enemy_ranged_score.setText(str(score))
        self.enemyRanged_deal.command_horn = command_horn
        self.update_enemy_score()

    def update_enemy_siege_score(self):
        """
        Обновляет счет противника за осадные орудия и обновляет общий счет.

        Вызывает метод для обновления счета на поле боя и обновляет
        соответствующую метку.
        """
        score, command_horn = self.update_score_in_battlefield(
            self.enemySiege_deal.enemySiege_deal
        )
        self.ui.enemy_siege_score.setText(str(score))
        self.enemySiege_deal.command_horn = command_horn
        self.update_enemy_score()

    def update_score_in_battlefield(self, battlefield_deal):
        """
        Обновляет очки всех карточек на поле боя, применяя эффекты от скиллов.

        Параметры:
        battlefield_deal (list): Список карточек на поле боя.

        Возвращает:
        tuple: Общая сумма очков всех карточек и флаг, указывающий, был ли использован командный рог.

        Описание:
        - Сначала устанавливает базовые очки для каждой карточки.
        - Применяет эффекты от скиллов карточек, включая увеличение очков для карточек с качеством NORMAL.
        - Обрабатывает эффект командного рога, который удваивает очки других карточек с таким же скиллом.
        - Суммирует очки всех карточек и возвращает общую сумму и статус командного рога.
        """
        # Сначала в отдельном атрибуте пропишем очки всех карточек, без каких-ибо бафов
        for card in battlefield_deal:
            card.score_in_battlefield = card.score

        command_horn = False
        # Теперь применим ко всем карточкам эффекты от скиллов, кроме командного рога - он отдельный случай
        for card in battlefield_deal:
            match card.skill:
                case card_params.COMMAND_HORN:
                    if command_horn is False:
                        command_horn = True

                case card_params.PLUS_ONE:
                    for card2 in battlefield_deal:
                        if (
                            card2.quality == card_params.NORMAL
                            and card2.uuid != card.uuid
                        ):
                            card2.score_in_battlefield += 1

        # Применим эффект командного рога. Командный рог не действует на карточку, с которой он вызывается!
        if command_horn:
            for card in battlefield_deal:
                if card.skill == card_params.COMMAND_HORN:
                    for card2 in battlefield_deal:
                        if (
                            card2.skill == card_params.COMMAND_HORN
                            and card2.uuid != card.uuid
                        ):
                            card2.score_in_battlefield *= 2
                else:
                    if card.quality == card_params.NORMAL:
                        card.score_in_battlefield += card.score_in_battlefield

        score = 0

        # Просуммируем все очки
        for card in battlefield_deal:
            score += card.score_in_battlefield

        return score, command_horn

    def init_cards(self):
        """
        Инициализирует карты для игрока и противника, загружая их из файловой системы.

        Описание:
        - Загружает карты из директории, соответствующей фракции игрока.
        - Создает объекты Deck для каждой карты, обрабатывая возможные исключения.
        - Обновляет метки, отображающие количество карт в колоде игрока.

        Затем выполняет аналогичные действия для противника, загружая карты из соответствующей директории.
        """
        cards = []
        for dirpath, dirnames, filenames in walk(rf".\images\cards\\{self.myFraction}"):
            cards.extend(filenames)

        for i in cards:
            try:
                self.myDeck = Deck(
                    i.rsplit(".")[0], fraction=self.myFraction, side=card_params.ME
                )
            except Exception:
                traceback.print_exc()
                continue

        self.update_label_cards_in_my_deck()

        cards.clear()

        for dirpath, dirnames, filenames in walk(
            rf".\images\cards\\{self.enemyFraction}"
        ):
            cards.extend(filenames)

        for i in cards:
            try:
                self.enemyDeck = Deck(
                    i.rsplit(".")[0],
                    fraction=self.enemyFraction,
                    side=card_params.ENEMY,
                )
            except Exception:
                traceback.print_exc()
                continue

        self.update_label_cards_in_enemy_deck()

    def init_deal(self):
        """
            Инициализирует сделку, добавляя случайные карты из колод игрока и противника.

            Описание:
            - Цикл выполняется 10 раз, пытаясь добавить по одной карте из колоды игрока и противника.
            - Использует метод add_card_mydeal для добавления карты игрока и add_card_enemydeal для добавления карты противника.
            - Обрабатывает возможные исключения при добавлении карт.
        """
        i = 0
        while i < 10:
            try:
                random_id = random.choice(range(len(self.myDeck.my_quantity_card)))
                self.add_card_mydeal(random_id)
            except (IndexError, AttributeError):
                traceback.print_exc()
                i += 1
                continue

            try:
                random_id_enemy = random.choice(
                    range(len(self.enemyDeck.enemy_quantity_card))
                )
                self.add_card_enemydeal(random_id_enemy)
            except (IndexError, AttributeError):
                traceback.print_exc()
                i += 1
                continue

            i += 1

    def update_card_pos_in_deal(self):
        """
        Обновляет позицию всех карт в сделке игрока.

        Описание:
        - Проходит по всем картам в сделке игрока и вызывает метод init_pos()
          для каждой карты, чтобы обновить её положение на экране.
        """
        for card in self.myDeal.my_quantity_card:
            card.label.init_pos()

    def add_card_mydeal(self, id):
        """
        Добавляет карту из колоды игрока в сделку.

        Параметры:
        id (int): Индекс карты в колоде игрока, которую необходимо добавить в сделку.

        Описание:
        - Создает объект Deal с выбранной картой из колоды игрока.
        - Если индекс карты недействителен, обрабатывает исключение IndexError и выводит сообщение об ошибке.
        - Удаляет добавленную карту из колоды и обновляет метки, отображающие количество карт в колоде и сделке игрока.
        """
        try:
            self.myDeal = Deal(
                card=self.myDeck.my_quantity_card[id],
                centralwidget=self.ui.centralwidget,
                geometry_parent=self.ui.myDeal_label_2.geometry(),
                side=card_params.ME,
            )
        except IndexError as i:
            print(str(i))
        else:
            self.myDeck.my_quantity_card.pop(id)
            self.update_label_cards_in_my_deck()
            self.update_label_cards_in_my_deal()

    def add_card_enemydeal(self, id):
        """
        Добавляет карту из колоды противника в сделку.

        Параметры:
        id (int): Индекс карты в колоде противника, которую необходимо добавить в сделку.

        Описание:
        - Создает объект Deal с выбранной картой из колоды противника.
        - Если индекс карты недействителен, обрабатывает исключение IndexError и выводит сообщение об ошибке.
        - Удаляет добавленную карту из колоды противника и обновляет метки, отображающие количество карт в колоде и сделке противника.
        """
        try:
            self.enemyDeal = Deal(
                card=self.enemyDeck.enemy_quantity_card[id],
                centralwidget=self.ui.centralwidget,
                side=card_params.ENEMY,
            )
        except IndexError as i:
            print(str(i))
        else:
            self.enemyDeck.enemy_quantity_card.pop(id)
            self.update_label_cards_in_enemy_deck()
            self.update_label_cards_in_enemy_deal()

    def enemy_move(self):
        """
        Выполняет ход противника, выбирая случайную карту из его колоды и добавляя её в соответствующее поле боя.

        Описание:
        - Метод выбирает случайную карту из колоды противника. Если колода пуста, выводит сообщение об ошибке.
        - В зависимости от типа карты (меле, дальняя атака или осадная) добавляет её в соответствующее поле боя у игрока.
        - Если карта имеет навык "Шпион", она может быть добавлена только в противоположное поле боя.
        - После добавления карты в поле боя, метод добавляет две случайные карты из колоды противника в его сделку.

        Исключения:
        - IndexError: Возникает, если колода противника пуста и не удается выбрать карту.
        - Exception: Обрабатывает любые другие исключения, возникающие при добавлении карт из колоды противника.
        """
        enemy_deal = self.get_enemy_deal()
        try:
            random_id_enemy = random.choice(range(len(enemy_deal.enemy_quantity_card)))
        except IndexError:
            traceback.print_exc()
            print("Закончились карточки")
            return

        count_cards_in_battlefield = 0
        x = 0
        y = 0
        deal = enemy_deal.enemy_quantity_card[random_id_enemy]

        # Карточки, со скиллом шпиона можно перетаскивать только на противоположное поле
        if deal.card.skill == card_params.SPY:
            match deal.card.combat:
                case card_params.MELEE:
                    count_cards_in_battlefield = len(self.myMelee_deal.myMelee_deal)
                    self.myMelee_deal.myMelee_deal.append(deal.card)
                    self.update_my_melee_score()
                    x = self.ui.myMelee_deal_designer.x()
                    y = self.ui.myMelee_deal_designer.y()
                case card_params.RANGED:
                    count_cards_in_battlefield = len(self.myRanged_deal.myRanged_deal)
                    self.myRanged_deal.myRanged_deal.append(deal.card)
                    self.update_my_ranged_score()
                    x = self.ui.myRanged_deal_designer.x()
                    y = self.ui.myRanged_deal_designer.y()
                case card_params.SIEGE:
                    count_cards_in_battlefield = len(self.mySiege_deal.mySiege_deal)
                    self.mySiege_deal.mySiege_deal.append(deal.card)
                    self.update_my_siege_score()
                    x = self.ui.mySiege_deal_designer.x()
                    y = self.ui.mySiege_deal_designer.y()

            # Добавить в свою колоду 2 карточки
            for i in range(2):
                try:
                    random_id = random.choice(
                        range(len(self.enemyDeck.enemy_quantity_card))
                    )
                    self.add_card_enemydeal(random_id)
                except Exception:
                    traceback.print_exc()
                    print("Не осталось карточек в колоде")
        else:
            match deal.card.combat:
                case card_params.MELEE:
                    count_cards_in_battlefield = len(
                        self.enemyMelee_deal.enemyMelee_deal
                    )
                    self.enemyMelee_deal.enemyMelee_deal.append(deal.card)
                    self.update_enemy_melee_score()
                    x = self.ui.enemyMelee_deal_designer.x()
                    y = self.ui.enemyMelee_deal_designer.y()
                case card_params.RANGED:
                    count_cards_in_battlefield = len(
                        self.enemyRanged_deal.enemyRanged_deal
                    )
                    self.enemyRanged_deal.enemyRanged_deal.append(deal.card)
                    self.update_enemy_ranged_score()
                    x = self.ui.enemyRanged_deal_designer.x()
                    y = self.ui.enemyRanged_deal_designer.y()
                case card_params.SIEGE:
                    count_cards_in_battlefield = len(
                        self.enemySiege_deal.enemySiege_deal
                    )
                    self.enemySiege_deal.enemySiege_deal.append(deal.card)
                    self.update_enemy_siege_score()
                    x = self.ui.enemySiege_deal_designer.x()
                    y = self.ui.enemySiege_deal_designer.y()
                case card_params.MELEE_RANGED:
                    random_battlefield = random.randint(0, 1)
                    match random_battlefield:
                        case 0:
                            count_cards_in_battlefield = len(
                                self.enemyMelee_deal.enemyMelee_deal
                            )
                            self.enemyMelee_deal.enemyMelee_deal.append(deal.card)
                            self.update_enemy_melee_score()
                            x = self.ui.enemyMelee_deal_designer.x()
                            y = self.ui.enemyMelee_deal_designer.y()
                        case 1:
                            count_cards_in_battlefield = len(
                                self.enemyRanged_deal.enemyRanged_deal
                            )
                            self.enemyRanged_deal.enemyRanged_deal.append(deal.card)
                            self.update_enemy_ranged_score()
                            x = self.ui.enemyRanged_deal_designer.x()
                            y = self.ui.enemyRanged_deal_designer.y()
                case card_params.SPECIAL_FIELD:
                    pass

        deal.label.move(
            x + (self.enemyMelee_deal.size_card.width() * count_cards_in_battlefield), y
        )
        deal.label.resize(self.enemyMelee_deal.size_card)
        deal.label.show()
        enemy_deal.pop_enemy_deal(random_id_enemy)
        self.update_label_cards_in_enemy_deal()

    def keyPressEvent(self, event):
        """
        Обрабатывает нажатия клавиш.

        Описание:
        - Закрывает приложение, если нажата клавиша 'Q' или 'Escape'.

        Параметры:
        - event: объект события, содержащий информацию о нажатой клавише.
        """
        key = event.key()

        match key:
            case QtCore.Qt.Key.Key_Q | QtCore.Qt.Key.Key_Escape:
                sys.exit()

    def keyReleaseEvent(self, event):
        """
        Обрабатывает отпускания клавиш.

        Описание:
        - Если отпущена клавиша 'Space' и кнопка удерживается, то:
          - Убирает состояние нажатия с кнопки.
          - Проверяет очки обоих игроков и определяет победителя.
          - Отображает соответствующие индикаторы жизни в зависимости от результата раунда.

        Параметры:
        - event: объект события, содержащий информацию о отпущенной клавише.
        """
        key = event.key()

        if key == QtCore.Qt.Key.Key_Space and self.ui.hold_button.isDown():
            self.ui.hold_button.setDown(False)

            # Спасовать и окончание раунда
            match key:
                case QtCore.Qt.Key.Key_Space:
                    # Вообще при пасе надо бы реализовать продолжение ходов противника, т.к. в настоящем гвинте после паса одного из игроков -
                    # другой игрок может продолжить накидывать карточки, а не пасовать сразу, но мне пока лень это делать))0)
                    # поэтому после паса заканчивается ход для обоих игроков и ведется подсчет очков

                    # Проверим, у кого больше очков
                    if int(self.ui.my_Score.text()) > int(self.ui.enemy_Score.text()):
                        if not self.ui.enemy_minus_life1.isVisible():
                            self.ui.enemy_minus_life1.show()
                        elif not self.ui.enemy_minus_life2.isVisible():
                            self.ui.enemy_minus_life2.show()
                            # Проигрыш противника - игра заканчивается

                    elif int(self.ui.my_Score.text()) < int(self.ui.enemy_Score.text()):
                        if not self.ui.me_minus_life1.isVisible():
                            self.ui.me_minus_life1.show()
                        elif not self.ui.me_minus_life2.isVisible():
                            self.ui.me_minus_life2.show()
                            # Мой проигрыш - игра заканчивается

                    elif int(self.ui.my_Score.text()) == int(
                        self.ui.enemy_Score.text()
                    ):
                        # Сначала проверим фракцию Нильфгарда. Особенность Нильфгарда в том, что они побеждают в случае ничьей
                        if self.myFraction == "nilf":
                            if not self.ui.enemy_minus_life1.isVisible():
                                self.ui.enemy_minus_life1.show()
                            elif not self.ui.enemy_minus_life2.isVisible():
                                self.ui.enemy_minus_life2.show()
                                # Проигрыш противника - игра заканчивается
                        if self.enemyFraction == "nilf":
                            if not self.ui.me_minus_life1.isVisible():
                                self.ui.me_minus_life1.show()
                            elif not self.ui.me_minus_life2.isVisible():
                                self.ui.me_minus_life2.show()
                                # Мой проигрыш - игра заканчивается

                        if self.myFraction != "nilf" and self.enemyFraction != "nilf":
                            if not self.ui.me_minus_life1.isVisible():
                                self.ui.me_minus_life1.show()
                            elif not self.ui.me_minus_life2.isVisible():
                                self.ui.me_minus_life2.show()
                            if not self.ui.enemy_minus_life1.isVisible():
                                self.ui.enemy_minus_life1.show()
                            elif not self.ui.enemy_minus_life2.isVisible():
                                self.ui.enemy_minus_life2.show()

                        if (
                            self.ui.enemy_minus_life2.isVisible()
                            and self.ui.me_minus_life2.isVisible()
                        ):
                            pass
                            # Ничья - игра заканчивается

                    # Сброс карточек в сброс
                    # for card in self.myMelee_deal.myMelee_deal:
                    #     card.hide()

    def closeEvent(self, a0):
        """
        Обрабатывает событие закрытия окна приложения.

        Описание:
        - Завершает работу приложения при закрытии окна.

        Параметры:
        - a0: объект события закрытия, содержащий информацию о закрытии окна.
        """
        sys.exit()
