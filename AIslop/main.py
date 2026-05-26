
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from reg import Ui_Form










if __name__ == "__main__":
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())