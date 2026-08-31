from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
)


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(
            20, 20, 20, 20
        )
        layout.setSpacing(12)

        self.setLayout(layout)

        # Page title
        title = QLabel("History")

        title.setStyleSheet(
            "font-size: 20px;"
            "font-weight: bold;"
        )

        layout.addWidget(title)

        # Search history
        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search history..."
        )

        layout.addWidget(
            self.search_input
        )

        # History list
        self.history_list = QListWidget()

        layout.addWidget(
            self.history_list
        )