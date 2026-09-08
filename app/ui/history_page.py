import json
import os
from datetime import datetime
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QScrollArea,
)


class HistoryCard(QFrame):

    def __init__(
        self,
        text,
        engine,
        timestamp
    ):
        super().__init__()

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
            14, 7, 14, 7
        )

        layout.setSpacing(4)

        self.setLayout(layout)

        # Top row
        top_layout = QHBoxLayout()

        top_layout.setSpacing(8)

        # Generated text
        self.text_label = QLabel(text)

        self.text_label.setWordWrap(True)

        self.text_label.setStyleSheet(
            "font-size: 14px;"
        )

        top_layout.addWidget(
            self.text_label,
            1
        )

        # Play button
        self.play_button = QPushButton()

        self.play_button.setIcon(
            QIcon("app/assets/icons/play.svg")
        )

        self.play_button.setIconSize(
            QSize(24, 24)
        )

        self.play_button.setFixedSize(
            40, 40
        )

        self.play_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                background: transparent;
                font-size: 18px;
                padding: 0px;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 20);
                border-radius: 6px;
            }
            """
        )

        top_layout.addWidget(
            self.play_button,
            0,
            Qt.AlignVCenter
        )

        # More button
        self.more_button = QPushButton()

        self.more_button.setIcon(
            QIcon("app/assets/icons/More.svg")
        )

        self.more_button.setIconSize(
            QSize(24, 24)
        )

        self.more_button.setFixedSize(
            40, 40
        )

        self.more_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                background: transparent;
                font-size: 20px;
                padding: 0px;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 20);
                border-radius: 6px;
            }
            """
        )

        top_layout.addWidget(
            self.more_button,
            0,
            Qt.AlignVCenter
        )

        layout.addLayout(
            top_layout
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

        layout.addWidget(
            self.info_label
        )


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()

        self.history_entries = []
        self.history_file = "data/history.json"
        self.load_history()

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

    def add_history_entry(
        self,
        text,
        engine,
        timestamp
    ):

        self.history_entries.append(
            {
                "text": text,
                "engine": engine,
                "timestamp": timestamp
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
                entry["timestamp"]
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
                    "timestamp": entry["timestamp"].isoformat()
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

            self.refresh_history()

        except Exception as e:

            print(
                f"Could not load history: {e}"
            )