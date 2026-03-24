from PySide6.QtWidgets import QWidget
from ui_form import Ui_Widget


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.sayac = 0
        self.ui.labelSayac.setText(str(self.sayac))

        self.ui.buttonArtir.clicked.connect(self.artir)
        self.ui.butonAzalt.clicked.connect(self.azalt)
        self.ui.butonSifirla.clicked.connect(self.sifirla)

    def artir(self):
        self.sayac += 1
        self.ui.labelSayac.setText(str(self.sayac))

    def azalt(self):
        self.sayac -= 1
        self.ui.labelSayac.setText(str(self.sayac))

    def sifirla(self):
        self.sayac = 0
        self.ui.labelSayac.setText(str(self.sayac))
