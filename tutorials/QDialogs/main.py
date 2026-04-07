import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDialog, QLabel


# Non-Modal pencere (show ile açılacak)
class NonModalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Non-Modal Window")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bu pencere NON-MODAL.\nAna pencereyi kullanmaya devam edebilirsin."))
        self.setLayout(layout)


# Modal pencere (exec ile açılacak)
class ModalDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modal Dialog")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bu pencere MODAL.\nKapatmadan ana pencereye dönemezsin."))
        self.setLayout(layout)


# Ana pencere
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ana Pencere")

        layout = QVBoxLayout()

        # Non-modal buton
        self.btn_non_modal = QPushButton("Non-Modal Aç (show)")
        self.btn_non_modal.clicked.connect(self.open_non_modal)

        # Modal buton
        self.btn_modal = QPushButton("Modal Aç (exec)")
        self.btn_modal.clicked.connect(self.open_modal)

        layout.addWidget(self.btn_non_modal)
        layout.addWidget(self.btn_modal)

        self.setLayout(layout)

    def open_non_modal(self):
        self.non_modal_window = NonModalWindow()
        self.non_modal_window.show()  # NON-MODAL

    def open_modal(self):
        dialog = ModalDialog()
        dialog.exec()  # MODAL


# Uygulama başlatma
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())