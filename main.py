from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
import sys

app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec_())