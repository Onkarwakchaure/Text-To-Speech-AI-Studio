import os, sys
from PySide6.QtCore import Qt, QUrl, QTime, QTimer, QThread
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
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
    QStatusBar,
    QDoubleSpinBox,
    QGroupBox,
    QInputDialog,
    QMenu,
    QStackedWidget
    )
from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput)
from pydub import AudioSegment
from ui.clickable_slider import ClickableSlider
from tts.xtts_engine import get_available_speakers
from workers.tts_worker import TTSWorker
from utils.settings_manager import SettingsManager
from utils.voice_manager import VoiceManager
from ui.voice_combo_box import VoiceComboBox
from ui.sidebar import Sidebar
from ui.history_page import HistoryPage
from datetime import datetime

class MainWindow(QMainWindow):
       
    def __init__(self):
        super().__init__()

        # Initialize Settings Manager
        self.settings_manager = SettingsManager()

        # Initialize Voice Manager
        self.voice_manager = VoiceManager()
        
        # voice mode state variables
        self.xtts_voice_mode = "Default Voice"
        self.f5_forced_voice_mode = False

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

        self.sidebar = Sidebar()

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # TTS page
        self.tts_page = QWidget()
        self.tts_page.setLayout(left_layout)

        # History page
        self.history_page = HistoryPage()

        # Page stack
        self.page_stack = QStackedWidget()

        self.page_stack.addWidget(
            self.tts_page
        )

        self.page_stack.addWidget(
            self.history_page
        )

        main_layout.addWidget(
            self.sidebar
        )

        main_layout.addWidget(
            self.page_stack,
            3
        )

        main_layout.addLayout(
            right_layout,
            1
        )

        self.sidebar.page_changed.connect(
            self.change_page
        )

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

        speakers = get_available_speakers()
        speakers.sort()

        self.default_voice_combo.addItems(speakers)

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

        # Save Reference Voice

        self.save_voice_button = QPushButton(
            "Save Voice"
        )

        self.saved_voices_label = QLabel(
            "Saved Reference Voices"
        )

        self.saved_voices_combo = VoiceComboBox()
        self.saved_voices_combo.rightClicked.connect(
            self.show_voice_context_menu
        )

        self.save_voice_button.hide()
        self.saved_voices_label.hide()
        self.saved_voices_combo.hide()

        self.save_voice_button.clicked.connect(
            self.save_reference_voice
        )

        right_layout.addWidget(
            self.upload_label
        )
        right_layout.addWidget(
            self.upload_button
        )
        right_layout.addWidget(
            self.selected_file_label
        )
        
        right_layout.addWidget(
            self.save_voice_button
        )

        right_layout.addWidget(
            self.saved_voices_label
        )

        right_layout.addWidget(
            self.saved_voices_combo
        )
        self.upload_label.hide()
        self.upload_button.hide()
        self.selected_file_label.hide()

        self.upload_button.clicked.connect(
            self.select_audio_file
        )
        self.saved_voices_combo.textActivated.connect(
            self.select_saved_voice
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

        ''' F5-TTS Settings '''

        # Advanced Settings Group Box

        self.advanced_settings = QGroupBox("Advanced Settings")
        self.advanced_settings.setCheckable(True)
        self.advanced_settings.setChecked(False)

        advanced_layout = QVBoxLayout()

        # F5 Speed
        self.f5_speed_label = QLabel("Speed")

        self.f5_speed_spinbox = QDoubleSpinBox()
        self.f5_speed_spinbox.setRange(0.5, 1.5)
        self.f5_speed_spinbox.setSingleStep(0.1)
        self.f5_speed_spinbox.setValue(0.9)

        advanced_layout.addWidget(self.f5_speed_label)
        advanced_layout.addWidget(self.f5_speed_spinbox)

        # F5 Reference Text

        self.f5_reference_text_label = QLabel("Reference Text")
        self.f5_reference_text = QTextEdit()
        self.f5_reference_text.setPlaceholderText(
            "Optional — enter text spoken in reference audio..."
        )
        self.f5_reference_text.setFixedHeight(80)

        advanced_layout.addWidget(self.f5_reference_text_label)
        advanced_layout.addWidget(self.f5_reference_text)

        self.advanced_settings.setLayout(advanced_layout)

        right_layout.addWidget(self.advanced_settings)

        self.advanced_settings.toggled.connect(
            self.toggle_advanced_settings
        )

        # F5 Remove Silence
        self.f5_remove_silence = QCheckBox("Remove Silence")

        advanced_layout.addWidget(
            self.f5_remove_silence
        )

        # Download Button
        right_layout.addStretch()

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

        self.load_settings()
        self.load_saved_voices()
        self.toggle_sections()

    ''' Methods for MainWindow class '''

    def change_page(self, page):

        if page == "generate":

            self.page_stack.setCurrentWidget(
                self.tts_page
            )

        elif page == "history":

            self.page_stack.setCurrentWidget(
                self.history_page
            )

    def toggle_sections(self):

        engine = self.engine_combo.currentText()
        voice_mode = self.voice_combo.currentText()
        
        if engine == "XTTS v2" and voice_mode != "Voice Cloning":
            self.xtts_voice_mode = voice_mode

        if engine == "F5-TTS":
            self.advanced_settings.show()
        else:
            self.advanced_settings.hide()

        if engine == "F5-TTS":
            self.f5_speed_label.show()
            self.f5_speed_spinbox.show()
        else:
            self.f5_speed_label.hide()
            self.f5_speed_spinbox.hide()

        # F5-TTS
        if engine == "F5-TTS":

            self.language_label.hide()
            self.language_combo.hide()

            self.default_voice_label.hide()
            self.default_voice_combo.hide()

            self.upload_label.show()
            self.upload_button.show()
            self.selected_file_label.show()

            self.saved_voices_label.show()
            self.saved_voices_combo.show()

            # F5 requires reference audio,
            # so force Voice Cloning mode.
            if voice_mode != "Voice Cloning":

                self.voice_combo.blockSignals(True)

                self.voice_combo.setCurrentText(
                    "Voice Cloning"
                )

                self.voice_combo.blockSignals(False)

                self.f5_forced_voice_mode = True

        # XTTS v2
        else:

            if self.f5_forced_voice_mode:

                self.voice_combo.blockSignals(True)

                self.voice_combo.setCurrentText(
                    self.xtts_voice_mode
                )

                self.voice_combo.blockSignals(False)

                self.f5_forced_voice_mode = False

                voice_mode = self.xtts_voice_mode

            self.language_label.show()
            self.language_combo.show()

            if voice_mode == "Voice Cloning":

                self.upload_label.show()
                self.upload_button.show()
                self.selected_file_label.show()

                self.default_voice_label.hide()
                self.default_voice_combo.hide()

                self.saved_voices_label.show()
                self.saved_voices_combo.show()

            else:

                self.upload_label.hide()
                self.upload_button.hide()
                self.selected_file_label.hide()

                self.default_voice_label.show()
                self.default_voice_combo.show()

                self.saved_voices_label.hide()
                self.saved_voices_combo.hide()
                
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

        if not file_path:
            return

        # Check that the file exists
        if not os.path.isfile(file_path):
            QMessageBox.warning(
                self,
                "Invalid Audio File",
                "The selected audio file could not be found."
            )
            return

        try:
            # Try loading the audio to verify that it is readable
            audio = AudioSegment.from_file(file_path)

            # Check that the audio actually contains data
            if len(audio) == 0:
                raise ValueError("The audio file is empty.")

        except Exception:
            QMessageBox.warning(
                self,
                "Invalid Audio File",
                "The selected audio file could not be read.\n\n"
                "Please choose a valid WAV, MP3, or FLAC file."
            )
            return

        # File is valid
        self.reference_audio_path = file_path
        file_name = os.path.basename(file_path)
        duration_seconds = len(audio) / 1000

        self.upload_button.setText(
            f"✓ {file_name}"
        )

        self.selected_file_label.setText(
            f"Selected: {file_name} | "
            f"Duration: {duration_seconds:.1f} sec"
        )
        self.save_voice_button.show()

    def save_reference_voice(self):

        if self.reference_audio_path is None:
            QMessageBox.warning(
                self,
                "No Reference Audio",
                "Please select a reference audio file first."
            )
            return

        voice_name, ok = QInputDialog.getText(
            self,
            "Save Reference Voice",
            "Voice Name:"
        )

        if not ok:
            return

        voice_name = voice_name.strip()

        if not voice_name:
            QMessageBox.warning(
                self,
                "Invalid Voice Name",
                "Please enter a name for the saved voice."
            )
            return

        # Check for duplicate names
        existing_voices = self.voice_manager.get_saved_voices()

        if voice_name.lower() in [
            name.lower()
            for name in existing_voices
        ]:
            QMessageBox.warning(
                self,
                "Voice Already Exists",
                f"A saved voice named '{voice_name}' already exists."
            )
            return

        try:

            self.voice_manager.save_voice(
                voice_name,
                self.reference_audio_path
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Save Voice Error",
                f"Failed to save the reference voice.\n\n{e}"
            )
            return

    # Add the new voice to the list
        self.saved_voices_combo.addItem(
            voice_name
        )

        self.saved_voices_combo.setCurrentText(
            voice_name
        )

        # Show saved voices section
        self.saved_voices_label.show()
        self.saved_voices_combo.show()

        # Hide Save Voice button after saving
        self.save_voice_button.hide()

        self.set_status(
            f"Reference voice '{voice_name}' saved."
        )
        self.reset_status()

    def load_saved_voices(self):

        self.saved_voices_combo.clear()

        saved_voices = self.voice_manager.get_saved_voices()

        if not saved_voices:
            self.saved_voices_label.hide()
            self.saved_voices_combo.hide()
            return

        self.saved_voices_combo.addItems(
            saved_voices
        )

        self.saved_voices_label.show()
        self.saved_voices_combo.show()

    def select_saved_voice(self, voice_name):

        voice_path = self.voice_manager.get_voice_path(
            voice_name
        )

        if voice_path is None:
            return

        self.reference_audio_path = voice_path

        file_name = os.path.basename(voice_path)

        audio = AudioSegment.from_file(
            voice_path
        )

        duration_seconds = len(audio) / 1000

        self.upload_button.setText(
            f"✓ {file_name}"
        )

        self.selected_file_label.setText(
            f"Selected: {file_name} | "
            f"Duration: {duration_seconds:.1f} sec"
        )

        self.save_voice_button.hide()

    def show_voice_context_menu(self, voice_name, global_position):

        if not voice_name:
            return

        menu = QMenu(self)

        update_action = menu.addAction("Update Voice")
        rename_action = menu.addAction("Rename Voice")
        delete_action = menu.addAction("Delete Voice")

        action = menu.exec(
            global_position
        )

        if action == update_action:
            self.update_saved_voice(voice_name)

        elif action == rename_action:
            self.rename_saved_voice(voice_name)

        elif action == delete_action:
            self.delete_saved_voice(voice_name)
            
    def update_saved_voice(self, voice_name):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select New Reference Audio",
            "",
            "Audio Files (*.wav *.mp3 *.flac *.ogg)"
        )

        if not file_path:
            return

        try:
            audio = AudioSegment.from_file(
                file_path
            )

            duration_seconds = len(audio) / 1000

            if duration_seconds <= 0:
                QMessageBox.warning(
                    self,
                    "Invalid Audio",
                    "The selected audio file is empty."
                )
                return

        except Exception as e:

            QMessageBox.warning(
                self,
                "Invalid Audio",
                f"Could not read the selected audio file.\n\n{e}"
            )
            return

        try:

            updated_path = self.voice_manager.update_voice(
                voice_name,
                file_path
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Update Voice Error",
                f"Failed to update '{voice_name}'.\n\n{e}"
            )
            return

        if updated_path is None:
            QMessageBox.warning(
                self,
                "Voice Not Found",
                f"The saved voice '{voice_name}' could not be found."
            )
            return

        # If this voice is currently selected,
        # update the active reference audio.
        if (
            self.saved_voices_combo.currentText()
            == voice_name
        ):

            self.reference_audio_path = updated_path

            file_name = os.path.basename(
                updated_path
            )

            self.upload_button.setText(
                f"✓ {file_name}"
            )

            self.selected_file_label.setText(
                f"Selected: {file_name} | "
                f"Duration: {duration_seconds:.1f} sec"
            )

        self.load_saved_voices()

        self.saved_voices_combo.setCurrentText(
            voice_name
        )

        self.set_status(
            f"Reference voice '{voice_name}' updated."
        )

        self.reset_status()

    def rename_saved_voice(self, old_name):

        was_active = (
            self.saved_voices_combo.currentText()
            == old_name
        )

        new_name, ok = QInputDialog.getText(
            self,
            "Rename Reference Voice",
            "New Voice Name:",
            text=old_name
        )

        if not ok:
            return

        new_name = new_name.strip()

        if not new_name:
            QMessageBox.warning(
                self,
                "Invalid Voice Name",
                "Please enter a name for the saved voice."
            )
            return

        if new_name.lower() == old_name.lower():
            return

        existing_voices = self.voice_manager.get_saved_voices()

        if new_name.lower() in [
            name.lower()
            for name in existing_voices
        ]:
            QMessageBox.warning(
                self,
                "Voice Already Exists",
                f"A saved voice named '{new_name}' already exists."
            )
            return

        renamed_path = self.voice_manager.rename_voice(
            old_name,
            new_name
        )

        if renamed_path is None:
            QMessageBox.warning(
                self,
                "Rename Failed",
                f"Could not rename '{old_name}'."
            )
            return

        self.load_saved_voices()

        self.saved_voices_combo.setCurrentText(
            new_name
        )

        if was_active:
            self.reference_audio_path = renamed_path

            file_name = os.path.basename(
                renamed_path
            )

            self.upload_button.setText(
                f"✓ {file_name}"
            )
            
        self.set_status(
            f"Reference voice '{old_name}' renamed to '{new_name}'."
        )

        self.reset_status()

    def delete_saved_voice(self, voice_name):

        reply = QMessageBox.question(
            self,
            "Delete Reference Voice",
            f"Are you sure you want to delete "
            f"the saved voice '{voice_name}'?\n\n"
            "This will remove the saved reference audio.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        was_active = (
            self.saved_voices_combo.currentText()
            == voice_name
        )

        deleted = self.voice_manager.delete_voice(
            voice_name
        )

        if not deleted:
            QMessageBox.warning(
                self,
                "Delete Failed",
                f"Could not delete '{voice_name}'."
            )
            return

        self.load_saved_voices()

        if was_active:

            self.reference_audio_path = None

            self.upload_button.setText(
                "Select Audio File"
            )

            self.selected_file_label.setText(
                "No file selected"
            )

        self.set_status(
            f"Reference voice '{voice_name}' deleted."
        )

        self.reset_status()
        
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

        if self.advanced_settings.isChecked():

            f5_speed = self.f5_speed_spinbox.value()

            f5_reference_text = (
                self.f5_reference_text
                .toPlainText()
                .strip()
            )

            f5_remove_silence = (
                self.f5_remove_silence.isChecked()
            )

        else:

            f5_speed = 1.0
            f5_reference_text = ""
            f5_remove_silence = False

        print(f"Text: {text}")
        print(f"Engine: {engine}")
        print(f"Language: {language}")
        print(f"Voice Mode: {voice_mode}")
        print(f"Output Format: {output_format}")
        print(f"F5 Speed: {f5_speed}")
        print(f"F5_remove_silence: {f5_remove_silence}")

        if voice_mode == "Voice Cloning":
            print(f"Reference Audio: {self.reference_audio_path}")
        else:
            print("Reference Audio: Not Required")

        self.set_status("Generating speech...")
        QApplication.processEvents()

        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        audio_path = (
            f"output/generated_{timestamp}.wav"
        )

        self.thread = QThread()
        self.worker = TTSWorker(
            text=text,
            engine=engine,
            language=xtts_language,
            voice_mode=voice_mode,
            output_path=audio_path,
            speaker_wav=self.reference_audio_path,
            speaker=selected_speaker,
            speed=f5_speed,
            reference_text=f5_reference_text,
            remove_silence=f5_remove_silence
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

    def toggle_advanced_settings(self, checked):

        self.f5_speed_label.setVisible(checked)
        self.f5_speed_spinbox.setVisible(checked)

        self.f5_reference_text_label.setVisible(checked)
        self.f5_reference_text.setVisible(checked)

        self.f5_remove_silence.setVisible(checked)

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
    
    def load_settings(self):

        self.engine_combo.setCurrentText(
            self.settings_manager.load(
                "engine",
                "XTTS v2"
            )
        )

        self.language_combo.setCurrentText(
            self.settings_manager.load(
                "language",
                "English"
            )
        )

        self.voice_combo.setCurrentText(
            self.settings_manager.load(
                "voice_mode",
                "Default Voice"
            )
        )

        self.default_voice_combo.setCurrentText(
            self.settings_manager.load(
                "speaker",
                "Ana Florence"
            )
        )

        self.output_combo.setCurrentText(
            self.settings_manager.load(
                "output_format",
                "MP3"
            )
        )

        self.f5_speed_spinbox.setValue(
            float(
                self.settings_manager.load(
                    "f5_speed",
                    0.9
                )
            )
        )

        self.f5_reference_text.setPlainText(
            self.settings_manager.load(
                "f5_reference_text",
                ""
            )
        )

        remove_silence = self.settings_manager.load(
            "f5_remove_silence",
            False
        )

        if isinstance(remove_silence, str):
            remove_silence = remove_silence.lower() == "true"

        self.f5_remove_silence.setChecked(
            remove_silence
        )

        advanced_settings = self.settings_manager.load(
            "advanced_settings",
            False
        )

        if isinstance(advanced_settings, str):
            advanced_settings = advanced_settings.lower() == "true"

        self.advanced_settings.setChecked(
            advanced_settings
        )
    
    def save_settings(self):

        self.settings_manager.save(
            "engine",
            self.engine_combo.currentText()
        )

        self.settings_manager.save(
            "language",
            self.language_combo.currentText()
        )

        self.settings_manager.save(
            "voice_mode",
            self.voice_combo.currentText()
        )

        self.settings_manager.save(
            "speaker",
            self.default_voice_combo.currentText()
        )

        self.settings_manager.save(
            "output_format",
            self.output_combo.currentText()
        )

        self.settings_manager.save(
            "f5_speed",
            self.f5_speed_spinbox.value()
        )

        self.settings_manager.save(
            "f5_reference_text",
            self.f5_reference_text.toPlainText()
        )

        self.settings_manager.save(
            "f5_remove_silence",
            self.f5_remove_silence.isChecked()
        )

        self.settings_manager.save(
            "advanced_settings",
            self.advanced_settings.isChecked()
        )

    def closeEvent(self, event):

        self.save_settings()

        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())