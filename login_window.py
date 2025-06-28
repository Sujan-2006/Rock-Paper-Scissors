from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from firebase_config import auth, db
from game_window import GameWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Sign Up")
        self.setGeometry(300, 200, 300, 150)

        layout = QVBoxLayout()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet("font-weight: bold;")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet("font-weight: bold;")

        self.login_btn = QPushButton("Login")
        self.signup_btn = QPushButton("Sign Up")

        self.login_btn.setStyleSheet("background-color: red;font-weight: bold;")
        self.signup_btn.setStyleSheet("background-color: red;font-weight: bold;")

        self.login_btn.clicked.connect(self.login)
        self.signup_btn.clicked.connect(self.signup)

        layout.addWidget(QLabel("Enter your credentials:"))
        layout.addWidget(self.email_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.signup_btn)
        self.setLayout(layout)

    def login(self):
        try:
            user = auth.sign_in_with_email_and_password(
                self.email_input.text(), self.pass_input.text()
            )
            self.load_game(user)
        except Exception as e:
            error = str(e)
            QMessageBox.warning(self, "Login Failed", f"Error: {error}")

    def signup(self):
        try:
            user = auth.create_user_with_email_and_password(
                self.email_input.text(), self.pass_input.text())
            db.child("users").child(user["localId"]).set({"score": 0})
            self.load_game(user)
        except Exception as e:
            error = str(e)
            if "EMAIL_EXISTS" in error:
                msg = "This email is already registered. Please log in instead."
            elif "WEAK_PASSWORD" in error:
                msg = "Password too weak. Use at least 6 characters."
            elif "INVALID_EMAIL" in error:
                msg = "Invalid email format. Use something like user@gmail.com."
            else:
                msg = f"Error: {error}"
            QMessageBox.warning(self, "Signup Failed", msg)

    def load_game(self, user):
        from game_window import GameWindow
        self.hide()
        self.game = GameWindow(user)
        self.game.show()