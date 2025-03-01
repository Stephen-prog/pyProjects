import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 320, 500)  # Adjusted height
        self.setStyleSheet(self.load_styles())

        self.current_input = ""
        self.last_result = None
        self.new_input = True

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # Display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Helvetica", 24))
        self.display.setReadOnly(True)
        vbox.addWidget(self.display)

        # Buttons
        grid = QGridLayout()
        buttons = [
            ('C', 0, 0, 'operator'), ('±', 0, 1, 'operator'), ('%', 0, 2, 'operator'), ('÷', 0, 3, 'orange'),
            ('7', 1, 0, 'number'), ('8', 1, 1, 'number'), ('9', 1, 2, 'number'), ('×', 1, 3, 'orange'),
            ('4', 2, 0, 'number'), ('5', 2, 1, 'number'), ('6', 2, 2, 'number'), ('−', 2, 3, 'orange'),
            ('1', 3, 0, 'number'), ('2', 3, 1, 'number'), ('3', 3, 2, 'number'), ('+', 3, 3, 'orange'),
            ('0', 4, 0, 'zero'), ('.', 4, 2, 'number'), ('=', 4, 3, 'orange'),
        ]

        self.buttons = {}

        for text, row, col, style in buttons:
            button = QPushButton(text)
            button.setObjectName(style)
            button.setFont(QFont("Helvetica", 18))
            button.clicked.connect(self.on_button_click)
            grid.addWidget(button, row, col, 1, 2 if text == '0' else 1)
            self.buttons[text] = button

        vbox.addLayout(grid)
        self.setLayout(vbox)

    def on_button_click(self):
        sender = self.sender().text()

        if sender == "C":
            self.clear_display()
        elif sender == "±":
            self.toggle_sign()
        elif sender == "%":
            self.percentage()
        elif sender == "=":
            self.calculate_result()
        else:
            self.update_display(sender)

    def clear_display(self):
        """Clears the display and resets input tracking."""
        self.display.clear()
        self.current_input = ""
        self.last_result = None
        self.new_input = True

    def toggle_sign(self):
        """Toggles the sign of the current number."""
        try:
            value = float(self.display.text())
            self.display.setText(str(-value))
            self.current_input = self.display.text()
        except ValueError:
            pass

    def percentage(self):
        """Converts the current number to a percentage."""
        try:
            value = float(self.display.text()) / 100
            self.display.setText(str(value))
            self.current_input = self.display.text()
        except ValueError:
            pass

    def calculate_result(self):
        """Evaluates the expression and displays the result."""
        try:
            expression = self.current_input.replace("×", "*").replace("÷", "/").replace("−", "-")
            result = eval(expression)
            self.display.setText(str(result))
            self.last_result = str(result)
            self.new_input = True
        except Exception:
            self.display.setText("Error")
            self.new_input = True

    def update_display(self, value):
        """Handles number and operator input dynamically."""
        if self.new_input and value.isdigit():
            self.display.setText(value)
            self.current_input = value
        else:
            self.display.setText(self.display.text() + value)
            self.current_input += value

        self.new_input = False

    def keyPressEvent(self, event):
        """Handles keyboard input."""
        key_map = {
            Qt.Key_0: "0", Qt.Key_1: "1", Qt.Key_2: "2", Qt.Key_3: "3",
            Qt.Key_4: "4", Qt.Key_5: "5", Qt.Key_6: "6", Qt.Key_7: "7",
            Qt.Key_8: "8", Qt.Key_9: "9", Qt.Key_Plus: "+", Qt.Key_Minus: "−",
            Qt.Key_Asterisk: "×", Qt.Key_Slash: "÷", Qt.Key_Period: ".",
            Qt.Key_Enter: "=", Qt.Key_Return: "=", Qt.Key_Backspace: "C"
        }

        if event.key() in key_map:
            self.buttons[key_map[event.key()]].click()

    def load_styles(self):
        """Loads iPhone-style QSS for buttons and display."""
        return """
        QWidget {
            background-color: #1C1C1C;
        }
        QLineEdit {
            background: #1C1C1C;
            border: none;
            color: white;
            padding: 15px;
        }
        QPushButton {
            border-radius: 40px;
            height: 80px;
            width: 80px;
            margin: 5px;
            font-size: 22px;
        }
        QPushButton#number {
            background: #505050;
            color: white;
        }
        QPushButton#operator {
            background: #A5A5A5;
            color: black;
        }
        QPushButton#orange {
            background: #FF9500;
            color: white;
        }
        QPushButton#zero {
            background: #505050;
            color: white;
            border-radius: 40px;
            width: 160px;
        }
        QPushButton:pressed {
            background: #737373;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
