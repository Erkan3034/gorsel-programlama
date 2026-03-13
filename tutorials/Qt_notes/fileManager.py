import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QMessageBox, QToolBar, QStatusBar, QInputDialog
)
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtCore import Qt


class TextEditor(QMainWindow):

    def __init__(self):
        super().__init__()
        self.current_file = None 
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Metin Düzenleyici")
        self.setGeometry(200, 200, 800, 600)

        # --- Metin Alanı ---
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Consolas", 12))
        self.setCentralWidget(self.text_edit)

        # --- Menü Çubuğu ---
        menu_bar = self.menuBar()

        # Dosya menüsü
        file_menu = menu_bar.addMenu("Dosya")

        new_action = QAction("Yeni Dosya", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Dosya Aç", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Kaydet", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Farklı Kaydet", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction("Çıkış", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # --- Araç Çubuğu ---
        toolbar = QToolBar("Ana Araç Çubuğu")
        self.addToolBar(toolbar)
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)

        # --- Durum Çubuğu ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Hazır")

        # Metin değiştiğinde başlığı güncelle
        self.text_edit.textChanged.connect(self.on_text_changed)

    # ---- Dosya İşlemleri ----

    def new_file(self):
        """Yeni bir boş dosya oluşturur."""
        if not self.maybe_save():
            return
        self.text_edit.clear()
        self.current_file = None
        self.setWindowTitle("Metin Düzenleyici - Yeni Dosya")
        self.status_bar.showMessage("Yeni dosya oluşturuldu")

    def open_file(self):
        """Kullanıcıdan dosya adı alarak mevcut bir dosyayı açar."""
        if not self.maybe_save():
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Dosya Aç", "",
            "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)"
        )
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        """Verilen yoldaki dosyayı okuyup editöre yükler."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_edit.setPlainText(content)
            self.current_file = file_path
            self.setWindowTitle(f"Metin Düzenleyici - {os.path.basename(file_path)}")
            self.status_bar.showMessage(f"Dosya açıldı: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya açılamadı:\n{e}")

    def save_file(self):
        """Mevcut dosyayı kaydeder. Dosya yoksa 'Farklı Kaydet' açılır."""
        if self.current_file:
            self.write_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        """Dosyayı yeni bir isimle kaydeder."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Farklı Kaydet", "",
            "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)"
        )
        if file_path:
            self.write_file(file_path)

    def write_file(self, file_path):
        """İçeriği belirtilen dosya yoluna yazar."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())
            self.current_file = file_path
            self.setWindowTitle(f"Metin Düzenleyici - {os.path.basename(file_path)}")
            self.status_bar.showMessage(f"Kaydedildi: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{e}")

    # ---- Yardımcı Metotlar ----

    def on_text_changed(self):
        """Metin değiştiğinde başlığa '*' ekler (kaydedilmemiş değişiklik)."""
        title = self.windowTitle()
        if not title.endswith("*"):
            self.setWindowTitle(title + " *")

    def maybe_save(self):
        """Kaydedilmemiş değişiklik varsa kullanıcıya sorar.
        True dönerse işleme devam edilir, False dönerse iptal."""
        if not self.text_edit.document().isModified():
            return True

        result = QMessageBox.question(
            self, "Kaydet?",
            "Kaydedilmemiş değişiklikler var.\nKaydetmek ister misiniz?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel
        )

        if result == QMessageBox.StandardButton.Save:
            self.save_file()
            return True
        elif result == QMessageBox.StandardButton.Discard:
            return True
        else:  # Cancel
            return False

    def closeEvent(self, event):
        """Pencere kapatılırken kaydedilmemiş değişiklik kontrolü."""
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())
