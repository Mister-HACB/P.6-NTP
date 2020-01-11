import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from NTP_control import *

class NTP_GUI(QMainWindow):

    
    def __init__(self, *args, **kwargs):
        super(NTP_GUI, self).__init__(*args, **kwargs)

        self.Akt_Adresse = "0.de.pool.ntp.org"
        self.Anzahl = 1
        self.Mode = 1

        self.setWindowTitle("Mein Fenster")
        
        self.layout = QGridLayout()
        #layout = QVBoxLayout()

        Infotext = QLabel("NTP-Zeitabgleich")
        Infotext_font = Infotext.font()
        Infotext_font.setPointSize(40)
        Infotext.setFont(Infotext_font)
        Infotext.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        AdressText = QLabel("NTP-Server Adresse:\nz.B. 0.de.pool.ntp.org oder de.pool.ntp.org")
        
        self.Adresseingabe = QLineEdit()
        self.Adresseingabe.setPlaceholderText("NTP-Server eintragen z.B.'0.de.pool.ntp.org'")
        self.Adresseingabe.textChanged.connect(self.Akt_Adresseingabe)

        self.b1 = QRadioButton("Einzelmessung")
        self.b1.setChecked(True)
        self.b1.ID = 1
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))

        self.b2 = QRadioButton("Durchschnittsmessung aus "+str(self.Anzahl)+" Anfragen"+" wip")
        self.b2.ID = 2
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))

        self.b3 = QRadioButton("Messung nur bester Delay aus "+str(self.Anzahl)+" Anfragen"+" wip")
        self.b3.ID = 3
        self.b3.toggled.connect(lambda:self.btnstate(self.b3))

        self.anzahl = QSlider(Qt.Horizontal)
        self.anzahl.setMinimum(1)
        self.anzahl.setMaximum(10)
        self.anzahl.setTickPosition(QSlider.TicksBothSides)
        self.anzahl.setTickInterval(1)
        self.anzahl.setPageStep(1)
        self.anzahl.valueChanged.connect(lambda:self.slider_Wert(self.anzahl))

        self.PC_Zeit = QLabel()

        self.Server_Zeit = QLabel()

        self.ergebnis_Text = QLabel()
        
        self.start_Button = QPushButton("Start")
        self.start_Button.clicked.connect(self.start_Button_Pressed)

        self.layout.addWidget(Infotext,1,0)
        self.layout.addWidget(AdressText,2,0)
        self.layout.addWidget(self.Adresseingabe,3,0)
        self.layout.addWidget(self.b1,4,0)
        self.layout.addWidget(self.b2,5,0)
        self.layout.addWidget(self.b3,6,0)
        self.layout.addWidget(self.anzahl,7,0)

        self.layout.addWidget(self.ergebnis_Text,10,0)
        self.layout.addWidget(self.start_Button,11,0)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def Akt_Adresseingabe(self, s):
        self.Akt_Adresse = s

    def start_Button_Pressed(self):
        print("Start")
        try:
            PC_Zeit, Server_Zeit, Offset = NTP_control.NTP_GUI_interface(self.Akt_Adresse, self.Anzahl, self.Mode)
            self.PC_Zeit.setText    ("PC Zeit: ------> " + str(PC_Zeit) + " (Zeit der Absendezeit vom PC)")
            self.Server_Zeit.setText("Server Zeit: -> " + str(PC_Zeit) + " (Zeit der Ankunftzeit am Server)")
            self.ergebnis_Text.setText(str(Offset))
            self.layout.addWidget(self.PC_Zeit,8,0)
            self.layout.addWidget(self.Server_Zeit,9,0)

        except Exception as err:
            print(err)
            self.PC_Zeit.setText("")
            self.Server_Zeit.setText("")
            self.layout.removeWidget(self.PC_Zeit)
            self.layout.removeWidget(self.Server_Zeit)
            self.ergebnis_Text.setText("Fehler - Adresse falsch?\nEingabe war: "'"'+str(self.Akt_Adresse)+'"')

    def btnstate(self,b):
        ID = self.sender().ID
        if ID == 1:
            if b.isChecked() == True:
                self.Mode = 1
                print("Mode is now ",self.Mode)

        if ID == 2:
            if b.isChecked() == True:
                self.Mode = 2
                print("Mode is now ",self.Mode)

        if ID == 3:
            if b.isChecked() == True:
                self.Mode = 3
                print("Mode is now ",self.Mode)

    def slider_Wert(self,s):
        self.Anzahl = s.value()
        self.b2.setText("Durchschnittsmessung aus "+str(self.Anzahl)+" Anfragen")
        self.b3.setText("Messung nur bester Delay von "+str(self.Anzahl)+" Anfragen")
        print("Anzahl ist jetzt ",self.Anzahl)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWindow = NTP_GUI()
    mainWindow.show()
    app.exec_()

    pass


