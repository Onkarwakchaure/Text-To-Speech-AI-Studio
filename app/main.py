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
    
    def toggle_upload_section(self):
        if self.voice_combo.currentText() == "Voice Cloning":
            self.upload_label.show()
            self.upload_button.show()
        else:
            self.upload_label.hide()
            self.upload_button.hide()   

    def __init__(self):
        super().__init__()
        
        ## Window Settings
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

        ## Text Input Section
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Type your text here...")
        left_layout.addWidget(self.text_input)

        # Generate Button
        self.generate_button = QPushButton(
            "🎙 GENERATE SPEECH"
        )
        left_layout.addWidget(self.generate_button)

        ## Settings Section
        settings_title = QLabel("Settings")
        right_layout.addWidget(settings_title)
        settings_title.setStyleSheet(
            "font-size: 16px;"
            "font-weight: bold;"
        )

        # Language Selection
        language_label = QLabel("Language")

        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "English",
            "Hindi"
        ])
        right_layout.addWidget(language_label)
        right_layout.addWidget(self.language_combo)

        # Engine Selection
        engine_label = QLabel("Engine")

        self.engine_combo = QComboBox()
        self.engine_combo.addItems([
            "XTTS v2",
            "F5-TTS"
        ])
        right_layout.addWidget(engine_label)
        right_layout.addWidget(self.engine_combo)

        # Voice Mode Selection
        voice_label = QLabel("Voice Mode")

        self.voice_combo = QComboBox()
        self.voice_combo.addItems([
            "Default Voice",
            "Voice Cloning"
        ])
        right_layout.addWidget(voice_label)
        right_layout.addWidget(self.voice_combo)

        # Reference Audio Upload     
        self.upload_label = QLabel("Reference Audio")
        self.upload_button = QPushButton(
            "Select Audio File"
        )

        self.voice_combo.currentTextChanged.connect(self.toggle_upload_section)        
        right_layout.addWidget(self.upload_label)
        right_layout.addWidget(self.upload_button)
        self.upload_label.hide()
        self.upload_button.hide()

        # Output Format
        output_label = QLabel("Output Format")

        self.output_combo = QComboBox()
        self.output_combo.addItems([
            "MP3",
            "WAV"
        ])
        right_layout.addWidget(output_label)
        right_layout.addWidget(self.output_combo)

        # Download Button
        self.download_button = QPushButton(
            "Download Output"
        )
        right_layout.addWidget(
            self.download_button
        )

        right_layout.addSpacing(10)
        right_layout.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())