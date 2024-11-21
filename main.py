import sys

from PyQt6 import QtWidgets

from py_gwint import MainWindow


class mywindow(QtWidgets.QMainWindow):
    """
    Основное окно приложения, наследующее от QMainWindow.

    Это класс представляет главное окно приложения, в котором
    используется виджет MainWindow из модуля py_gwint.
    """
    def __init__(self):
        """
        Инициализация главного окна приложения.

        Вызывает конструктор родительского класса и создает
        экземпляр MainWindow, который устанавливается как центральный виджет.
        """
        super(mywindow, self).__init__()
        self.main_gwint = MainWindow()


if __name__ == "__main__":
    """
    Запуск приложения.

    Создает экземпляр QApplication и запускает главный цикл обработки событий.
    """
    app = QtWidgets.QApplication(sys.argv)
    application = mywindow()
    # application.show()
    sys.exit(app.exec())
