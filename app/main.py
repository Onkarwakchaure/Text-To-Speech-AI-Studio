import sys
from PySide6.QtCore import Qt, QUrl, QTime, QTimer, QThread
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QComboBox,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QStatusBar)
from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput)
from pydub import AudioSegment
from ui.clickable_slider import ClickableSlider
from tts.xtts_engine import generate_xtts, get_available_speakers
from workers.tts_worker import TTSWorker

class MainWindow(QMainWindow):
       
    def __init__(self):
        super().__init__()
        
        ## Window Settings
        self.setWindowTitle("Text-To-Speech AI Studio")
        self.resize(1200, 700)
        self.setMinimumSize(1000, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.set_status("Ready")

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

         # Character Count
        self.character_label = QLabel("0 characters")
        left_layout.addWidget(self.character_label) 

        self.text_input.textChanged.connect(
        self.update_character_count
        )

        # Generate Button
        self.generate_button = QPushButton(
            "🎙 GENERATE SPEECH"
        )
        self.generate_button.clicked.connect(self.generate_speech)
        left_layout.addWidget(self.generate_button)

        # Audio Player 
        audio_layout = QVBoxLayout()
        controls_layout = QHBoxLayout()

        self.play_button = QPushButton("▶")
        self.pause_button = QPushButton("⏸")
        self.stop_button = QPushButton("⏹")
        self.audio_slider = ClickableSlider(Qt.Horizontal)
        self.duration_label = QLabel("00:00 / 00:00")
        self.duration_label.setAlignment(Qt.AlignCenter)

        controls_layout.addStretch()
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addStretch()

        audio_layout.addLayout(controls_layout)
        audio_layout.addWidget(self.audio_slider)
        audio_layout.addWidget(self.duration_label)

        left_layout.addLayout(audio_layout)

        self.hide_audio_controls()

        ''' Settings Section '''
        settings_title = QLabel("Settings")
        right_layout.addWidget(settings_title)
        settings_title.setStyleSheet(
            "font-size: 16px;"
            "font-weight: bold;"
        )

        # Engine Selection
        self.engine_label = QLabel("Engine")

        self.engine_combo = QComboBox()
        self.engine_combo.addItems([
            "XTTS v2",
            "F5-TTS"
        ])
        right_layout.addWidget(self.engine_label)
        right_layout.addWidget(self.engine_combo)

        # Language Selection
        self.language_label = QLabel("Language")

        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "English",
            "Hindi"
        ])
        right_layout.addWidget(self.language_label)
        right_layout.addWidget(self.language_combo)

        # Voice Mode Selection
        self.voice_label = QLabel("Voice Mode")

        self.voice_combo = QComboBox()
        self.voice_combo.addItems([
            "Default Voice",
            "Voice Cloning"
        ])
        right_layout.addWidget(self.voice_label)
        right_layout.addWidget(self.voice_combo)

        # Default Voice Selection

        self.default_voice_label = QLabel("Voice")
        self.default_voice_combo = QComboBox()
        self.default_voice_combo.addItems(get_available_speakers())

        right_layout.addWidget(self.default_voice_label)
        right_layout.addWidget(self.default_voice_combo)
        self.default_voice_label.hide()
        self.default_voice_combo.hide()

        # Reference Audio Upload     
        self.upload_label = QLabel("Reference Audio")
        self.upload_button = QPushButton(
            "Select Audio File"
        )
        self.selected_file_label = QLabel(
            "No file selected"
        )

        self.reference_audio_path = None

        right_layout.addWidget(self.upload_label)
        right_layout.addWidget(self.upload_button)
        right_layout.addWidget(self.selected_file_label)
        self.upload_label.hide()
        self.upload_button.hide()
        self.selected_file_label.hide()

        self.upload_button.clicked.connect(
            self.select_audio_file
        )

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()

        self.player.setAudioOutput(self.audio_output)

        self.play_button.clicked.connect(self.play_audio)
        self.pause_button.clicked.connect(self.pause_audio)
        self.stop_button.clicked.connect(self.stop_audio)
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.player.playbackStateChanged.connect(self.handle_playback_state)
        self.audio_slider.sliderMoved.connect(self.seek_audio)

        self.toggle_sections()

        # Output Format
        self.output_label = QLabel("Output Format")

        self.output_combo = QComboBox()
        self.output_combo.addItems([
            "MP3",
            "WAV",
            "FLAC",
            "OGG"
        ])
        right_layout.addWidget(self.output_label)
        right_layout.addWidget(self.output_combo)
        right_layout.addStretch()

        # Download Button
        self.download_button = QPushButton("Download Output")
        right_layout.addWidget(self.download_button)
        right_layout.addSpacing(10)
        self.hide_download_button()

        self.generated_audio_path = None
        self.download_button.clicked.connect(self.download_audio)

        # UI Connections
        self.engine_combo.currentTextChanged.connect(
            self.toggle_sections
        )

        self.voice_combo.currentTextChanged.connect(
            self.toggle_sections
        )

        self.upload_button.clicked.connect(
            self.select_audio_file
        )


    ''' Methods for MainWindow class '''

    def toggle_sections(self):

        engine = self.engine_combo.currentText()
        voice_mode = self.voice_combo.currentText()

        # F5-TTS
        if engine == "F5-TTS":

            self.language_label.hide()
            self.language_combo.hide()

            self.default_voice_label.hide()
            self.default_voice_combo.hide()

            self.upload_label.show()
            self.upload_button.show()
            self.selected_file_label.show()

            # F5 requires reference audio,
            # so force Voice Cloning mode.
            if voice_mode != "Voice Cloning":

                self.voice_combo.blockSignals(True)

                self.voice_combo.setCurrentText(
                    "Voice Cloning"
                )

                self.voice_combo.blockSignals(False)

        # XTTS v2
        else:

            self.language_label.show()
            self.language_combo.show()

            if voice_mode == "Voice Cloning":

                self.upload_label.show()
                self.upload_button.show()
                self.selected_file_label.show()

                self.default_voice_label.hide()
                self.default_voice_combo.hide()

            else:

                self.upload_label.hide()
                self.upload_button.hide()
                self.selected_file_label.hide()

                self.default_voice_label.show()
                self.default_voice_combo.show()
                
    def update_character_count(self):
        text = self.text_input.toPlainText()
        count = len(text)
        self.character_label.setText(f"{count} characters")

    def select_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Reference Audio",
            "",
            "Audio Files (*.wav *.mp3 *.flac)"
        )

        if file_path:
            self.reference_audio_path = file_path
            file_name = file_path.split("/")[-1]
            self.upload_button.setText(f"✓ {file_name}")
            self.selected_file_label.setText(f"Selected: {file_name}")
            
    def show_audio_controls(self):
        self.play_button.show()
        self.pause_button.show()
        self.stop_button.show()
        self.audio_slider.show()
        self.duration_label.show()

    def hide_audio_controls(self):
        self.play_button.hide()
        self.pause_button.hide()
        self.stop_button.hide()
        self.audio_slider.hide()
        self.duration_label.hide()

    def show_download_button(self):
        self.download_button.show()

    def hide_download_button(self):
        self.download_button.hide()

    def generate_speech(self):
        
        text = self.text_input.toPlainText()
        if not text.strip():
            QMessageBox.warning(
                self,
                "No Text Entered",
                "Please enter some text to convert into speech."
            )
            return
        
        engine = self.engine_combo.currentText()
        language = self.language_combo.currentText()
        language_map = {
            "English": "en",
            "Hindi": "hi"
        }

        xtts_language = language_map[language]

        voice_mode = self.voice_combo.currentText()

        selected_speaker = self.default_voice_combo.currentText()

        if voice_mode == "Voice Cloning" and self.reference_audio_path is None:
            QMessageBox.warning(
                self,
                "Missing Reference Audio",
                "Voice cloning requires a reference audio file.\n\nPlease select one and try again."
            )
            return

        output_format = self.output_combo.currentText()

        print(f"Text: {text}")
        print(f"Engine: {engine}")
        print(f"Language: {language}")
        print(f"Voice Mode: {voice_mode}")
        print(f"Output Format: {output_format}")

        if voice_mode == "Voice Cloning":
            print(f"Reference Audio: {self.reference_audio_path}")
        else:
            print("Reference Audio: Not Required")

        self.set_status("Generating speech...")
        QApplication.processEvents()

        audio_path = "output/generated_audio_test1.wav"
        
        self.thread = QThread()
        self.worker = TTSWorker(
            text=text,
            engine=engine,
            language=xtts_language,
            voice_mode=voice_mode,
            output_path=audio_path,
            speaker_wav=self.reference_audio_path,
            speaker=selected_speaker
        )
        self.worker.moveToThread(self.thread)
        # Thread starts the worker
        self.thread.started.connect(self.worker.run)

        # Worker signals
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)

        # Cleanup
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.generate_button.setEnabled(False)
        self.thread.start()

    def on_generation_finished(self, audio_path):

        self.generated_audio_path = audio_path
        self.load_audio(audio_path)
        self.show_audio_controls()
        self.show_download_button()
        self.set_status("Speech generated successfully.")
        self.reset_status()
        self.generate_button.setEnabled(True)

    def on_generation_error(self, message):
        QMessageBox.critical(
            self,
            "Generation Error",
            message
        )

        self.set_status("Generation failed.")
        self.reset_status()
        self.generate_button.setEnabled(True)
            
    def set_status(self, message):
        self.status_bar.showMessage(
            f"Application Status : {message}"
        )

    def play_audio(self):
        self.player.play()

    def pause_audio(self):
        self.player.pause()

    def stop_audio(self):
        self.player.stop()

    def load_audio(self, audio_path):
        self.player.stop()

        # Clear the previous media source
        self.player.setSource(QUrl())

        # Load the new file
        self.player.setSource(QUrl.fromLocalFile(audio_path))

        self.audio_slider.setValue(0)
        self.set_status("Audio loaded successfully.")

    def update_duration(self, duration):
                
        self.audio_slider.setMaximum(duration)

        total_duration = QTime(
            0,
            duration // 60000,
            (duration // 1000) % 60
        )

        self.duration_label.setText(
            f"00:00 / {total_duration.toString('mm:ss')}"
        )

    def update_position(self, position):
        self.audio_slider.setValue(position)

        current_time = QTime(
            0,
            position // 60000,
            (position // 1000) % 60
        )

        total_duration = QTime(
            0,
            self.player.duration() // 60000,
            (self.player.duration() // 1000) % 60
        )

        self.duration_label.setText(
            f"{current_time.toString('mm:ss')} / "
            f"{total_duration.toString('mm:ss')}"
        )

    def seek_audio(self, position):
        self.player.setPosition(position)
    
    def handle_playback_state(self, state):

        if state == QMediaPlayer.PlayingState:
            self.set_status("Playing audio...")

        elif state == QMediaPlayer.PausedState:
            self.set_status("Audio paused.")
            self.reset_status()

        elif state == QMediaPlayer.StoppedState:

            if self.player.position() == self.player.duration():
                self.set_status("Playback finished.")
                self.set_status("Audio stopped.")
                self.reset_status()

    def reset_status(self, delay=3000):

        QTimer.singleShot(
            delay,
            lambda: self.set_status("Ready")
        )

    def export_audio(
        self,
        output_path,
        output_format
    ):
        try:
            audio = AudioSegment.from_file(
                self.generated_audio_path
            )

            audio.export(
                output_path,
                format=output_format
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Error",
                f"Failed to export audio.\n\n{e}"
            )
        
    def download_audio(self):

        if self.generated_audio_path is None:
                QMessageBox.warning(
                    self,
                    "No Audio Available",
                    "Please generate speech before downloading."
                )
                return

        selected_format = self.output_combo.currentText().lower()

        default_name = f"generated_audio.{selected_format}"

        file_filter = (
            f"{selected_format.upper()} Files "
            f"(*.{selected_format})"
        )

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Audio As",
            default_name,
            file_filter
        )

        if not file_path:
            return

        self.export_audio(
            file_path,
            selected_format)
        self.set_status("Audio saved successfully.")
        self.reset_status()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())