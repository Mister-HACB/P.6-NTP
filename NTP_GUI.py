import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit

class NTP_GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.button1_counter = 0

        self.setWindowTitle("Mein Fenster")
        self.resize(600, 300)
       
        self.textbox1 = QLineEdit(self)
        self.textbox1.setText("noch nicht gedrückt")
        self.textbox1.move(20, 20)
        self.textbox1.resize(200, 50)

        self.button1 = QPushButton(self)
        self.button1.setText("NTP_Ausführen")
        self.button1.move(20,80)
        self.button1.resize(100,30)
        self.button1.clicked.connect(self.on_button1_pressed)

        self.show()

    def on_button1_pressed(self):
        self.button1_counter += 1
        text = str(self.button1_counter) + "-mal gedrückt"
        self.textbox1.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = NTP_GUI()
    app.exec_()

    pass


