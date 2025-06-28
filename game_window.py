from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from firebase_config import db
import time

class GameWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.uid = user['localId']
        self.setWindowTitle("Rock Paper Scissors")
        self.setGeometry(300, 200, 400, 300)

        self.layout = QVBoxLayout()
        self.status = QLabel("Choose your move")
        self.score_label = QLabel("Your Score: Loading...")

        self.rock = QPushButton("Rock")
        self.paper = QPushButton("Paper")
        self.scissors = QPushButton("Scissors")

        self.rock.setStyleSheet("background-color: lightblue;font-weight: bold;")
        self.paper.setStyleSheet("background-color: lightblue;font-weight: bold;")
        self.scissors.setStyleSheet("background-color: lightblue;font-weight: bold;")

        for btn in [self.rock, self.paper, self.scissors]:
            self.layout.addWidget(btn)
            btn.clicked.connect(self.make_move)

        self.layout.addWidget(self.status)
        self.layout.addWidget(self.score_label)
        self.setLayout(self.layout)

        self.get_score()

    def get_score(self):
        data = db.child("users").child(self.uid).get().val()
        score = data.get("score", 0)
        self.score_label.setText(f"Your Score: {score}")

    def make_move(self):
        move = self.sender().text().lower()
        match_id = "match_1" 
        db.child("matches").child(match_id).child("moves").child(self.uid).set(move)
        self.status.setText(f"You chose: {move}. Waiting for friend...")

        self.check_result_later(match_id, move)

    def check_result_later(self, match_id, my_move):
        time.sleep(4)
        moves = db.child("matches").child(match_id).child("moves").get().val()

        if moves and len(moves) == 2:
            opponent_id = [uid for uid in moves if uid != self.uid][0]
            opponent_move = moves[opponent_id]
            result = self.get_result(my_move, opponent_move)

            if result == "win":
                self.status.setText("🎉 You won!")
                self.update_score()
            elif result == "lose":
                self.status.setText("😞 You lost!")
            else:
                self.status.setText("🤝 It's a tie!")
        else:
            self.status.setText("Waiting for opponent...")

    def get_result(self, my, opponent):
        rules = {
            "rock": "scissors",
            "scissors": "paper",
            "paper": "rock"
        }
        if my == opponent:
            return "tie"
        elif rules[my] == opponent:
            return "win"
        else:
            return "lose"

    def update_score(self):
        score = db.child("users").child(self.uid).child("score").get().val()
        db.child("users").child(self.uid).update({"score": score + 1})
        self.get_score()