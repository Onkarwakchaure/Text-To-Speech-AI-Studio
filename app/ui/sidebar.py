from PySide6.QtCore import QSize, Qt, Signal, QPropertyAnimation
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton
)

class Sidebar(QWidget):

    page_changed = Signal(str)

    EXPANDED_WIDTH = 140
    COLLAPSED_WIDTH = 40

    def __init__(self):
        super().__init__()

        self.is_expanded = False

        self.setFixedWidth(
            self.COLLAPSED_WIDTH
        )

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            4, 4, 4, 4
        )

        self.layout.setSpacing(4)

        self.setLayout(self.layout)

        # Collapse / Expand button
        self.toggle_button = QPushButton()

        self.toggle_button.setIcon(
            QIcon("app/assets/icons/menu.svg")
        )

        self.toggle_button.setIconSize(
            QSize(20, 20)
        )

        self.toggle_button.setFixedHeight(40)

        self.layout.addWidget(
            self.toggle_button
        )

        # TTS Studio title
        self.title_button = QPushButton(
            "TTS Studio"
        )

        font = self.title_button.font()
        font.setPointSize(12)
        font.setBold(True)
        self.title_button.setFont(font)
        self.title_button.setFixedHeight(40)

        self.layout.addWidget(
            self.title_button
        )

        # Generate button
        self.generate_button = QPushButton(
            "Generate"
        )

        self.generate_button.setIcon(
            QIcon("app/assets/icons/generate.svg")
        )

        self.generate_button.setIconSize(
            QSize(20, 20)
        )

        font = self.generate_button.font()
        font.setPointSize(12)
        self.generate_button.setFont(font)

        self.generate_button.setFixedHeight(40)

        self.layout.addWidget(
            self.generate_button
        )

        # History button
        self.history_button = QPushButton(
            "History"
        )

        self.history_button.setIcon(
            QIcon("app/assets/icons/history.svg")
        )

        self.history_button.setIconSize(
            QSize(20, 20)
        )

        font = self.history_button.font()
        font.setPointSize(12)
        self.history_button.setFont(font)

        self.history_button.setFixedHeight(40)

        self.layout.addWidget(
            self.history_button
        )

        self.layout.addStretch()

        # Borderless navigation buttons
        button_style = """
            QPushButton {
                border: none;
                background: transparent;
                padding: 2px;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 20);
                border-radius: 6px;
            }
        """
        
        self.title_button.setStyleSheet(
            button_style
        )
        
        self.toggle_button.setStyleSheet(
            button_style
        )

        self.generate_button.setStyleSheet(
            button_style
        )

        self.history_button.setStyleSheet(
            button_style
        )

        # Animation
        self.animation = QPropertyAnimation(
            self,
            b"minimumWidth"
        )

        self.animation.setDuration(250)

        # Signals
        self.toggle_button.clicked.connect(
            self.expand_sidebar
        )

        self.title_button.clicked.connect(
            self.collapse_sidebar
        )

        self.generate_button.clicked.connect(
            lambda: self.page_changed.emit(
                "generate"
            )
        )

        self.history_button.clicked.connect(
            lambda: self.page_changed.emit(
                "history"
            )
        )

        # Start collapsed
        self.title_button.hide()

        self.toggle_button.show()

        self.generate_button.setText(
            ""
        )

        self.history_button.setText(
            ""
        )

    def collapse_sidebar(self):

        if not self.is_expanded:
            return

        self.is_expanded = False

        self.animation.stop()

        self.animation.setStartValue(
            self.width()
        )

        self.animation.setEndValue(
            self.COLLAPSED_WIDTH
        )

        self.animation.start()

        # Hide title
        self.title_button.hide()

        self.toggle_button.setFixedSize(40, 40)
        self.generate_button.setFixedSize(40, 40)
        self.history_button.setFixedSize(40, 40)

        # Show menu button
        self.toggle_button.show()

        # Icons only
        self.generate_button.setText(
            ""
        )

        self.history_button.setText(
            ""
        )

    def expand_sidebar(self):

        if self.is_expanded:
            return

        self.is_expanded = True

        self.animation.stop()

        self.animation.setStartValue(
            self.width()
        )

        self.animation.setEndValue(
            self.EXPANDED_WIDTH
        )

        self.animation.start()

        # Hide menu button
        self.toggle_button.hide()

        # Show title
        self.title_button.show()

        # Full labels
        self.generate_button.setText(
            "Generate"
        )

        self.history_button.setText(
            "History"
        )

        self.toggle_button.setMinimumSize(0, 0)
        self.toggle_button.setMaximumSize(16777215, 16777215)

        self.generate_button.setMinimumSize(0, 0)
        self.generate_button.setMaximumSize(16777215, 16777215)

        self.history_button.setMinimumSize(0, 0)
        self.history_button.setMaximumSize(16777215, 16777215)