from PyQt6.QtWidgets import(QMainWindow, QApplication, QPushButton, QLabel, QVBoxLayout, QWidget,QLineEdit)
from PyQt6.QtCore import Qt
import sys

class SayacEkran(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sayac = 0
        self.setWindowTitle("Sayaç Uygulaması")
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel("0",  self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttonArtir = QPushButton("Artır", self)
        self.buttonAzalt = QPushButton("Azalt", self)
        self.buttonSifirla = QPushButton("Sıfırla", self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.buttonArtir)
        layout.addWidget(self.buttonAzalt)
        layout.addWidget(self.buttonSifirla)

            

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        
        self.buttonArtir.clicked.connect(self.artir)
        self.buttonAzalt.clicked.connect(self.azalt)
        self.buttonSifirla.clicked.connect(self.sifirla)

    def artir(self):
        self.sayac += 1
        self.label.setText(str(self.sayac))

    def azalt(self):
        self.sayac -= 1
        self.label.setText(str(self.sayac))

    def sifirla(self):
        self.sayac = 0
        self.label.setText(str(self.sayac))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SayacEkran()
    window.show()
    sys.exit(app.exec())