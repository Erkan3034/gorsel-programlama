import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStatusBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont


"""

algoritma mantığımı geliştirmek adına renklendirme konusunu araştırdım 
ve buna ek olarak her tıklama eventinde random olarak backgorun rengi değiştirme algoritmasını düşünerek bunu da uyguladım.
"""


class SayacEkran(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sayac = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sayaç Uygulaması")
        self.setGeometry(100, 100, 320, 220)
        self._widgetleri_olustur()
        self._layoutu_ayarla()
        self._sinyalleri_bagla()
        self._durum_cubugunu_ayarla()

    def _widgetleri_olustur(self):
        self.label = QLabel("0")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #1a1a2e;")

        self.btn_artir   = QPushButton("▲ Artır")
        self.btn_azalt   = QPushButton("▼ Azalt")
        self.btn_sifirla = QPushButton("↺ Sıfırla")

        self.btn_artir.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 6px; padding: 6px;")
        self.btn_azalt.setStyleSheet("background-color: #e53935; color: white; border-radius: 6px; padding: 6px;")
        self.btn_sifirla.setStyleSheet("background-color: #1565C0; color: white; border-radius: 6px; padding: 6px;")


    def _layoutu_ayarla(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.btn_artir)
        h_layout.addWidget(self.btn_azalt)
        h_layout.addWidget(self.btn_sifirla)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label)
        v_layout.addLayout(h_layout)

        container = QWidget()
        container.setLayout(v_layout)
        self.setCentralWidget(container)
        self.setStyleSheet("background-color: #f5f5f5;")

    def _sinyalleri_bagla(self):
        self.btn_artir.clicked.connect(self.artir)
        self.btn_azalt.clicked.connect(self.azalt)
        self.btn_sifirla.clicked.connect(self.sifirla)

    def _durum_cubugunu_ayarla(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Hazır")
        self.status_bar.setStyleSheet("color: #555555;")

    # --- İş Mantığı ---

    def artir(self):
        self.sayac += 1
        self._sayaci_guncelle()
        

    def azalt(self):
        self.sayac -= 1
        self._sayaci_guncelle()

    def sifirla(self):
        self.sayac = 0
        self._sayaci_guncelle()

    def _sayaci_guncelle(self):
        if self.sayac > 0:
            self.label.setStyleSheet("color: #4CAF50;")
        elif self.sayac < 0:
            self.label.setStyleSheet("color: #e53935;")
        else:
            self.label.setStyleSheet("color: #1a1a2e;")    
        self.label.setText(str(self.sayac))

        if self.sayac<0:
            self.status_bar.showMessage(f"Sayaç negatif: {self.sayac}")
            self.setStyleSheet(f"background-color: {self._random_renk().name()};")
        elif self.sayac>0:
            self.status_bar.showMessage(f"Sayaç güncellendi: {self.sayac}")
            self.setStyleSheet(f"background-color: {self._random_renk().name()};")

    def _random_renk(self):
        import random
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return QColor(r, g, b)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SayacEkran()
    window.show()
    sys.exit(app.exec())