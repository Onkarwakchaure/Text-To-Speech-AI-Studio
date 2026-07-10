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
        self.resize(1200, 800)
        self.setMinimumSize(900, 650)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 1)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Type your text here...")
        left_layout.addWidget(self.text_input)

        settings_layout = QHBoxLayout()
        engine_layout = QVBoxLayout()
        language_layout = QVBoxLayout()
        voice_layout = QVBoxLayout()

        engine_label = QLabel("Engine")
        language_label = QLabel("Language")
        voice_label = QLabel("Voice Mode")
    
        self.engine_combo = QComboBox()
        self.engine_combo.addItems([
            "XTTS v2",
            "F5-TTS"
        ])

        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "English",
            "Hindi"
        ])
        
        self.voice_combo = QComboBox()
        self.voice_combo.addItems([
            "Default Voice",
            "Voice Cloning"
        ])
        
        engine_layout.addWidget(engine_label)
        engine_layout.addWidget(self.engine_combo)

        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)

        voice_layout.addWidget(voice_label)
        voice_layout.addWidget(self.voice_combo)

        settings_layout.addLayout(engine_layout)
        settings_layout.addLayout(language_layout)
        settings_layout.addLayout(voice_layout)

        settings_layout.addWidget(self.engine_combo)
        settings_layout.addWidget(self.language_combo)

        right_layout.addLayout(settings_layout)
        
        self.generate_button = QPushButton(
            "🎙 GENERATE SPEECH"
        )
        left_layout.addWidget(self.generate_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())