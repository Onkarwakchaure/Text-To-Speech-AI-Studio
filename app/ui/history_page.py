import json
import os
from datetime import datetime
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMenu,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QScrollArea,
    QFileDialog
)


class HistoryCard(QFrame):

    def __init__(
        self,
        text,
        engine,
        timestamp,
        audio_path
    ):
        super().__init__()

        self.audio_path = audio_path
        self.setObjectName("historyCard")

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

        download_action = menu.addAction(
            "Download"
        )

        action = menu.exec(
            self.more_button.mapToGlobal(
                self.more_button.rect().bottomLeft()
            )
        )

        if action == download_action:
            self.download_audio()

    def download_audio(self):

        if not self.audio_path:
            return

        if not os.path.exists(
            self.audio_path
        ):
            return

        extension = os.path.splitext(
            self.audio_path
        )[1].lower()

        if extension == ".mp3":
            file_filter = "MP3 Files (*.mp3)"

        elif extension == ".wav":
            file_filter = "WAV Files (*.wav)"

        else:
            file_filter = "Audio Files (*.*)"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Audio",
            os.path.basename(
                self.audio_path
            ),
            file_filter
        )

        if not file_path:
            return

        with open(
            self.audio_path,
            "rb"
        ) as source:

            with open(
                file_path,
                "wb"
            ) as destination:

                destination.write(
                    source.read()
                )
                
class HistoryPage(QWidget):

    def __init__(self, export_audio_callback):
        super().__init__()

        self.export_audio_callback = export_audio_callback

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
        timestamp,
        audio_path
    ):

        self.history_entries.append(
            {
                "text": text,
                "engine": engine,
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
                entry["timestamp"],
                entry.get("audio_path", "")
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