import sys
from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


@dataclass
class Note:
    title: str
    content: str


APP_STYLESHEET = """
QWidget {
    background-color: #f4f6fb;
    color: #202744;
    font-family: 'Segoe UI', 'Trebuchet MS', sans-serif;
    font-size: 13px;
}

QLabel#TitleLabel {
    font-size: 24px;
    font-weight: 700;
    color: #0f1e4a;
}

QLabel#SubtitleLabel {
    color: #55607e;
    font-size: 13px;
}

QFrame#Card {
    background-color: #ffffff;
    border: 1px solid #d9e0f2;
    border-radius: 12px;
}

QListWidget {
    background-color: #ffffff;
    border: 1px solid #d8dfef;
    border-radius: 10px;
    padding: 6px;
}

QListWidget::item {
    padding: 10px;
    border-radius: 8px;
}

QListWidget::item:selected {
    background-color: #d9e7ff;
    color: #0d2a6b;
}

QPushButton {
    background-color: #1f6feb;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #185cd0;
}

QPushButton:pressed {
    background-color: #134ea8;
}

QPushButton:disabled {
    background-color: #9ab3e5;
    color: #eef2ff;
}

QLineEdit, QTextEdit, QTextBrowser {
    background-color: #ffffff;
    border: 1px solid #cad6f2;
    border-radius: 8px;
    padding: 7px;
}

QDialog {
    background-color: #f5f7fe;
}
"""


class NoteDialog(QDialog):
    def __init__(self, parent=None, note: Note | None = None):
        super().__init__(parent)
        self.setWindowTitle("Not Ekle" if note is None else "Not Düzenle")
        self.setModal(True)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.resize(450, 320)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Not başlığı girin...")
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Not içeriğini buraya yazın...")

        save_button = QPushButton("Kaydet")
        cancel_button = QPushButton("İptal")
        save_button.setMinimumHeight(36)
        cancel_button.setMinimumHeight(36)

        save_button.clicked.connect(self.save_note)
        cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Başlık"))
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("İçerik"))
        layout.addWidget(self.content_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        if note is not None:
            self.title_input.setText(note.title)
            self.content_input.setPlainText(note.content)

    def save_note(self) -> None:
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Eksik Bilgi", "Başlık boş bırakılamaz.")
            return
        self.accept()

    def get_note_data(self) -> Note:
        return Note(
            title=self.title_input.text().strip(),
            content=self.content_input.toPlainText().strip(),
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Not Uygulaması")
        self.resize(860, 520)

        self.notes: list[Note] = []

        self.note_list = QListWidget()
        self.note_list.setAlternatingRowColors(True)
        self.note_list.currentRowChanged.connect(self.update_preview)

        self.add_button = QPushButton("Yeni Not Ekle")
        self.edit_button = QPushButton("Düzenle")
        self.delete_button = QPushButton("Sil")

        self.add_button.clicked.connect(self.add_note)
        self.edit_button.clicked.connect(self.edit_note)
        self.delete_button.clicked.connect(self.delete_note)

        self.preview_title = QLabel("Not Önizleme")
        self.preview_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #1a2f66;")
        self.preview_content = QTextBrowser()
        self.preview_content.setPlaceholderText("Listeden bir not seçtiğinizde içeriği burada görünür.")

        self.build_ui()
        self.update_action_buttons(-1)

    def build_ui(self) -> None:
        title_label = QLabel("Not Defteri")
        title_label.setObjectName("TitleLabel")
        subtitle_label = QLabel("Notlarınızı ekleyin, düzenleyin ve tek ekranda yönetin.")
        subtitle_label.setObjectName("SubtitleLabel")

        root = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(14)

        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(14, 14, 14, 14)
        card_layout.setSpacing(12)

        content_row = QHBoxLayout()
        content_row.setSpacing(12)

        left_col = QVBoxLayout()
        left_col.setSpacing(8)
        left_col.addWidget(QLabel("Notlar"))
        left_col.addWidget(self.note_list)

        right_col = QVBoxLayout()
        right_col.setSpacing(8)
        right_col.addWidget(self.preview_title)
        right_col.addWidget(self.preview_content)

        content_row.addLayout(left_col, 3)
        content_row.addLayout(right_col, 4)
        card_layout.addLayout(content_row)

        button_row = QHBoxLayout()
        button_row.addWidget(self.add_button)
        button_row.addWidget(self.edit_button)
        button_row.addWidget(self.delete_button)
        button_row.addStretch()

        card_layout.addLayout(button_row)
        card.setLayout(card_layout)

        main_layout.addWidget(card)
        root.setLayout(main_layout)
        self.setCentralWidget(root)

    def refresh_note_list(self) -> None:
        self.note_list.clear()
        for note in self.notes:
            item = QListWidgetItem(note.title)
            self.note_list.addItem(item)
        self.update_preview(self.note_list.currentRow())

    def update_preview(self, index: int) -> None:
        self.update_action_buttons(index)
        if index < 0 or index >= len(self.notes):
            self.preview_title.setText("Not Önizleme")
            self.preview_content.setText("Listeden bir not seçtiğinizde içeriği burada görünür.")
            return

        note = self.notes[index]
        self.preview_title.setText(note.title)
        content = note.content if note.content else "(Bu not için içerik girilmemiş.)"
        self.preview_content.setText(content)

    def update_action_buttons(self, index: int) -> None:
        has_selection = index >= 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def selected_index(self) -> int:
        return self.note_list.currentRow()

    def add_note(self) -> None:
        dialog = NoteDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.notes.append(dialog.get_note_data())
            self.refresh_note_list()
            self.note_list.setCurrentRow(len(self.notes) - 1)

    def edit_note(self) -> None:
        index = self.selected_index()
        if index < 0:
            QMessageBox.information(self, "Seçim Yok", "Lütfen düzenlemek için bir not seçin.")
            return

        dialog = NoteDialog(self, note=self.notes[index])
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.notes[index] = dialog.get_note_data()
            self.refresh_note_list()
            self.note_list.setCurrentRow(index)

    def delete_note(self) -> None:
        index = self.selected_index()
        if index < 0:
            QMessageBox.information(self, "Seçim Yok", "Lütfen silmek için bir not seçin.")
            return

        answer = QMessageBox.question(
            self,
            "Notu Sil",
            "Seçili notu silmek istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            del self.notes[index]
            self.refresh_note_list()
            if self.notes:
                self.note_list.setCurrentRow(min(index, len(self.notes) - 1))


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
