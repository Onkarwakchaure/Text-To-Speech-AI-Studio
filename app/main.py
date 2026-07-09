import sys

from PySide6.QtWidgets import ( # type: ignore
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QComboBox,
    QPushButton,
    QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Text-To-Speech AI Studio")
        self.resize(1000,700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Type your text here...")
        main_layout.addWidget(self.text_input)

        settings_layout = QHBoxLayout()

        self.engine_combo = QComboBox()
        self.engine_combo.addItems([
            "XTTS v2",
            "F5-TTS" ])

        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "English",
            "Hindi" ])

        settings_layout.addWidget(self.engine_combo)
        settings_layout.addWidget(self.language_combo)

        main_layout.addLayout(settings_layout)
        self.generate_button = QPushButton(
            "🎙 GENERATE SPEECH"
        )

        main_layout.addWidget(self.generate_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())