import json
import os
from datetime import datetime
from PySide6.QtCore import (
    Qt,
    QSize,
    QPropertyAnimation,
    QEasingCurve,
    QParallelAnimationGroup
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMenu,
    QMessageBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QScrollArea,
    QGraphicsOpacityEffect
)


class HistoryCard(QFrame):

    def __init__(
        self,
        text,
        engine,
        language,
        voice_mode,
        voice,
        reference_audio,
        f5_speed,
        f5_reference_text,
        f5_remove_silence,
        timestamp,
        audio_path,
        download_callback,
        use_text_callback,
        delete_callback
    ):
        super().__init__()

        self.audio_path = audio_path
        self.language = language
        self.voice_mode = voice_mode
        self.voice = voice
        self.reference_audio = reference_audio
        self.f5_speed = f5_speed
        self.f5_reference_text = f5_reference_text
        self.f5_remove_silence = f5_remove_silence
        self.download_callback = download_callback
        self.use_text_callback = (use_text_callback)
        self.text = text
        self.timestamp = timestamp
        self.delete_callback = (delete_callback)
        self.setObjectName("historyCard")
        self.setCursor(
            Qt.PointingHandCursor
        )
        self.setStyleSheet(
            """
            QFrame#historyCard {
                background: rgba(255, 255, 255, 8);
                border: 1px solid rgba(255, 255, 255, 18);
                border-radius: 10px;
            }

            QFrame#historyCard:hover {
                background: rgba(255, 255, 255, 14);
            }

            QLabel {
                background: transparent;
                border: none;
            }

            QPushButton {
                border: none;
                background: transparent;
                border-radius: 6px;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 20);
            }
            """
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            14, 6, 14, 6
        )

        layout.setSpacing(4)

        self.setLayout(layout)

        # Main horizontal layout
        main_layout = QHBoxLayout()

        main_layout.setSpacing(8)

        # Left side
        left_layout = QVBoxLayout()

        left_layout.setSpacing(4)

        # Generated text
        self.text_label = QLabel(text)

        self.text_label.setWordWrap(True)

        self.text_label.setStyleSheet(
            "font-size: 14px;"
        )

        left_layout.addWidget(
            self.text_label
        )

        # Metadata
        time_text = timestamp.strftime(
            "%I:%M %p"
        ).lstrip("0")

        self.info_label = QLabel(
            f"{engine}  ·  {time_text}"
        )

        self.info_label.setStyleSheet(
            """
            color: #aaaaaa;
            font-size: 12px;
            """
        )

        left_layout.addWidget(
            self.info_label
        )

        main_layout.addLayout(
            left_layout,
            1
        )

        # Right side buttons
        button_layout = QHBoxLayout()

        button_layout.setSpacing(2)

        # Play button
        self.play_button = QPushButton()

        self.play_button.setIcon(
            QIcon("app/assets/icons/play.svg")
        )

        self.play_button.setIconSize(
            QSize(20, 20)
        )

        self.play_button.setFixedSize(
            36, 36
        )
        self.play_button.clicked.connect(
            self.play_audio
        )
        button_layout.addWidget(
            self.play_button
        )

        # More button
        self.more_button = QPushButton()

        self.more_button.setIcon(
            QIcon("app/assets/icons/More.svg")
        )

        self.more_button.setIconSize(
            QSize(20, 20)
        )

        self.more_button.setFixedSize(
            36, 36
        )

        self.more_button.clicked.connect(
            self.show_more_menu
        )

        button_layout.addWidget(
            self.more_button
        )

        main_layout.addLayout(
            button_layout,
            0
        )

        layout.addLayout(
            main_layout
        )

        # Details section
        self.details_frame = QFrame()

        self.details_frame.setVisible(
            False
        )

        self.details_frame.setMaximumHeight(
            0
        )

        self.details_opacity = (
            QGraphicsOpacityEffect(
                self.details_frame
            )
        )

        self.details_opacity.setOpacity(
            0
        )

        self.details_frame.setGraphicsEffect(
            self.details_opacity
        )

        self.details_expanded = False

        self.details_layout = QVBoxLayout()

        self.details_layout.setContentsMargins(
            0, 8, 0, 4
        )

        self.details_layout.setSpacing(
            4
        )

        self.details_frame.setLayout(
            self.details_layout
        )

        layout.addWidget(
            self.details_frame
        )

        # Details content
        self.add_detail_row(
            "Engine",
            engine
        )

        if engine == "XTTS v2":

            self.add_detail_row(
                "Language",
                language
            )

            self.add_detail_row(
                "Voice Mode",
                voice_mode
            )

            self.add_detail_row(
                "Voice",
                voice
            )

        elif engine == "F5-TTS":

            self.add_detail_row(
                "Voice Mode",
                voice_mode
            )

            if reference_audio:
                self.add_detail_row(
                    "Reference Audio",
                    os.path.basename(
                        reference_audio
                    )
                )

            self.add_detail_row(
                "Speed",
                f"{f5_speed:.2f}"
            )

            self.add_detail_row(
                "Reference Text",
                f5_reference_text
                if f5_reference_text
                else "None"
            )

            self.add_detail_row(
                "Remove Silence",
                "Yes"
                if f5_remove_silence
                else "No"
            )
    def add_detail_row(
        self,
        label,
        value
    ):
        row = QHBoxLayout()

        row.setSpacing(8)

        label_widget = QLabel(
            label
        )

        label_widget.setStyleSheet(
            """
            color: #aaaaaa;
            font-size: 12px;
            """
        )

        value_widget = QLabel(
            str(value)
        )

        value_widget.setWordWrap(
            True
        )

        value_widget.setStyleSheet(
            """
            font-size: 12px;
            """
        )

        row.addWidget(
            label_widget
        )

        row.addWidget(
            value_widget,
            1
        )

        self.details_layout.addLayout(
            row
        )

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.show_details()

        super().mousePressEvent(
            event
        )

    def play_audio(self):

        if not self.audio_path:
            return

        if not os.path.exists(
            self.audio_path
        ):
            return

        os.startfile(
            os.path.abspath(
                self.audio_path
            )
        )

    def show_more_menu(self):
        menu = QMenu(self)

        download_action = menu.addAction("Download")
        details_action = menu.addAction("Details")
        use_text_action = menu.addAction("Use Text Again")
        delete_action = menu.addAction("Delete")

        action = menu.exec(
            self.more_button.mapToGlobal(
                self.more_button.rect().bottomLeft()
            )
        )

        if action == download_action:
            self.download_audio()

        elif action == details_action:
            self.show_details()

        elif action == use_text_action:
            self.use_text_again()

        elif action == delete_action:
            self.delete_history()   

    def show_details(self):

        self.details_expanded = (
            not self.details_expanded
        )

        if hasattr(
            self,
            "details_animation"
        ):
            self.details_animation.stop()

        self.details_frame.setVisible(
            True
        )

        start_height = (
            self.details_frame.maximumHeight()
        )

        start_opacity = (
            self.details_opacity.opacity()
        )

        if self.details_expanded:

            end_height = (
                self.details_frame.layout()
                .sizeHint()
                .height()
            )

            end_opacity = 1.0

        else:

            end_height = 0
            end_opacity = 0.0

        height_animation = (
            QPropertyAnimation(
                self.details_frame,
                b"maximumHeight"
            )
        )

        height_animation.setDuration(
            500
        )

        height_animation.setStartValue(
            start_height
        )

        height_animation.setEndValue(
            end_height
        )

        height_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        opacity_animation = (
            QPropertyAnimation(
                self.details_opacity,
                b"opacity"
            )
        )

        opacity_animation.setDuration(
            350
        )

        opacity_animation.setStartValue(
            start_opacity
        )

        opacity_animation.setEndValue(
            end_opacity
        )

        opacity_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        self.details_animation = (
            QParallelAnimationGroup(
                self
            )
        )

        self.details_animation.addAnimation(
            height_animation
        )

        self.details_animation.addAnimation(
            opacity_animation
        )

        self.details_animation.finished.connect(
            self.on_details_animation_finished
        )

        self.details_animation.start()


    def on_details_animation_finished(self):

        if not self.details_expanded:

            self.details_frame.setVisible(
                False
            )

    def download_audio(self):

        if not self.audio_path:
            return

        if not os.path.exists(
            self.audio_path
        ):
            return

        self.download_callback(
            self.audio_path
        )

    def use_text_again(self):

        self.use_text_callback(
            self.text
        )

    def delete_history(self):

        message_box = QMessageBox(
            QMessageBox.Question,
            "Delete History",
            "Are you sure you want to delete this history entry?",
            QMessageBox.Yes | QMessageBox.No,
            self
        )

        yes_button = message_box.button(
            QMessageBox.Yes
        )

        no_button = message_box.button(
            QMessageBox.No
        )

        yes_button.setFixedSize(
            80, 32
        )

        no_button.setFixedSize(
            80, 32
        )

        yes_button.setStyleSheet(
            """
            QPushButton {
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 6px;
                background: transparent;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 15);
            }
            """
        )

        no_button.setStyleSheet(
            """
            QPushButton {
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 6px;
                background: transparent;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 15);
            }
            """
        )

        button_box = message_box.layout()

        button_box.setAlignment(
            Qt.AlignCenter
        )

        button_box.setSpacing(
            12
        )

        result = message_box.exec()

        if result == QMessageBox.Yes:

            self.delete_callback(
                self.timestamp
            )

class HistoryPage(QWidget):

    def __init__(
        self,
        export_audio_callback,
        use_text_callback,
        release_audio_callback
    ):
        super().__init__()

        self.export_audio_callback = export_audio_callback
        self.use_text_callback = (
            use_text_callback
        )
        self.release_audio_callback = (
            release_audio_callback
        )
        self.history_entries = []
        self.history_file = "data/history.json"

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            20, 20, 20, 20
        )

        main_layout.setSpacing(12)

        self.setLayout(
            main_layout
        )

        # Page title
        title = QLabel("History")

        title.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            """
        )

        main_layout.addWidget(
            title
        )

        # Search
        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search history..."
        )

        main_layout.addWidget(
            self.search_input
        )

        # Scroll area
        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_area.setFrameShape(
            QFrame.NoFrame
        )

        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }
            """
        )

        # History container
        self.history_container = QWidget()

        self.history_layout = QVBoxLayout()

        self.history_layout.setContentsMargins(
            0, 4, 0, 4
        )

        self.history_layout.setSpacing(
            6
        )

        self.history_container.setLayout(
            self.history_layout
        )

        self.scroll_area.setWidget(
            self.history_container
        )

        main_layout.addWidget(
            self.scroll_area
        )

        self.load_history()

    def add_history_entry(
        self,
        text,
        engine,
        language,
        voice_mode,
        voice,
        reference_audio,
        f5_speed,
        f5_reference_text,
        f5_remove_silence,
        timestamp,
        audio_path
    ):
        
        self.history_entries.append(
            {
                "text": text,
                "engine": engine,
                "language": language,
                "voice_mode": voice_mode,
                "voice": voice,
                "reference_audio": reference_audio,
                "f5_speed": f5_speed,
                "f5_reference_text": f5_reference_text,
                "f5_remove_silence": f5_remove_silence,
                "timestamp": timestamp,
                "audio_path": audio_path
            }
        )

        self.save_history()
        
        self.history_entries.sort(
            key=lambda entry: entry["timestamp"],
            reverse=True
        )

        self.refresh_history()

    def refresh_history(self):

        # Remove existing widgets
        while self.history_layout.count():

            item = self.history_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        current_date = None

        for index, entry in enumerate(
            self.history_entries
        ):

            timestamp = entry["timestamp"]

            entry_date = timestamp.date()

            # Date group
            if entry_date != current_date:

                current_date = entry_date

                date_label = QLabel(
                    self.format_date(
                        timestamp
                    )
                )

                date_label.setStyleSheet(
                    """
                    font-size: 14px;
                    font-weight: bold;
                    color: #dddddd;
                    padding-top: 12px;
                    padding-bottom: 8px;
                    """
                )

                self.history_layout.addWidget(
                    date_label
                )

            # History card
            card = HistoryCard(
                entry["text"],
                entry["engine"],
                entry.get("language", ""),
                entry.get("voice_mode", ""),
                entry.get("voice", ""),
                entry.get("reference_audio"),
                entry.get("f5_speed", 1.0),
                entry.get("f5_reference_text", ""),
                entry.get("f5_remove_silence", False),
                entry["timestamp"],
                entry.get("audio_path", ""),
                self.export_audio_callback,
                self.use_text_callback,
                self.delete_history_entry
            )

            self.history_layout.addWidget(
                card
            )

        self.history_layout.addStretch()

    def format_date(self, timestamp):

        today = timestamp.today().date()

        if timestamp.date() == today:
            return "Today"

        if (
            timestamp.date()
            == today.fromordinal(
                today.toordinal() - 1
            )
        ):
            return "Yesterday"

        return timestamp.strftime(
            "%B %d, %Y"
        ).replace(
            " 0",
            " "
        )
    
    def save_history(self):

        os.makedirs("data", exist_ok=True)

        data = []

        for entry in self.history_entries:

            data.append(
                {
                    "text": entry["text"],
                    "engine": entry["engine"],
                    "language": entry.get("language", ""),
                    "voice_mode": entry.get("voice_mode", ""),
                    "voice": entry.get("voice", ""),
                    "reference_audio": entry.get("reference_audio"),
                    "f5_speed": entry.get("f5_speed", 1.0),
                    "f5_reference_text": entry.get(
                        "f5_reference_text",
                        ""
                    ),
                    "f5_remove_silence": entry.get(
                        "f5_remove_silence",
                        False
                    ),
                    "timestamp": entry["timestamp"].isoformat(),
                    "audio_path": entry.get("audio_path", "")
                }
            )

        with open(
            self.history_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def load_history(self):

        if not os.path.exists(
            self.history_file
        ):
            return

        try:

            with open(
                self.history_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            for entry in data:

                entry["language"] = entry.get(
                    "language",
                    ""
                )

                entry["voice_mode"] = entry.get(
                    "voice_mode",
                    ""
                )

                entry["voice"] = entry.get(
                    "voice",
                    ""
                )

                entry["reference_audio"] = entry.get(
                    "reference_audio",
                    None
                )

                entry["f5_speed"] = entry.get(
                    "f5_speed",
                    1.0
                )

                entry["f5_reference_text"] = entry.get(
                    "f5_reference_text",
                    ""
                )

                entry["f5_remove_silence"] = entry.get(
                    "f5_remove_silence",
                    False
                )

                entry["timestamp"] = (
                    datetime.fromisoformat(
                        entry["timestamp"]
                    )
                )

            self.history_entries = data

            self.history_entries.sort(
                key=lambda entry: entry["timestamp"],
                reverse=True
            )

            self.refresh_history()

        except Exception as e:

            print(
                f"Could not load history: {e}"
            )

    def delete_history_entry(
        self,
        timestamp
    ):

        audio_path = None

        for entry in self.history_entries:

            if entry["timestamp"] == timestamp:

                audio_path = entry.get(
                    "audio_path",
                    ""
                )

                break

        if audio_path:

            self.release_audio_callback(
                audio_path
            )
            
        # Delete audio file first
        if audio_path:

            if os.path.exists(
                audio_path
            ):

                try:

                    os.remove(
                        audio_path
                    )

                except Exception as e:

                    QMessageBox.warning(
                        self,
                        "Could Not Delete Audio",
                        "The audio file is currently "
                        "being used by another "
                        "application.\n\n"
                        "Please close the audio player "
                        "and try deleting this history "
                        "entry again."
                    )

                    print(
                        f"Could not delete audio file: {e}"
                    )

                    return

        # Remove history entry only after
        # audio deletion succeeds
        self.history_entries = [
            entry
            for entry in self.history_entries
            if entry["timestamp"] != timestamp
        ]

        self.save_history()

        self.refresh_history()