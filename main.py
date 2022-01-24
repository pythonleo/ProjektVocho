import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from mainwindow import Ui_MainWindow
import engine


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    engine.cleanup()
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())