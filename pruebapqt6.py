from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt6.QtCore import QSize, Qt, QStandardPaths
import sys

#Personaliza el la ventana base
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TxtToMDNotes")
        button = QPushButton("Press Me!")

        #Creo que centraliza el boton
        self.setCentralWidget(button)

        #cambia el tamaño
        self.setFixedSize(QSize(720, 480))

app = QApplication(sys.argv)

#Crea la ventana base
window = MainWindow()
window.show() #Muestra la ventana

#Mantiene la ventana abierta y responde a eventos
app.exec()