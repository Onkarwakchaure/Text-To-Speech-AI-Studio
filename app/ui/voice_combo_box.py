from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtWidgets import QComboBox


class VoiceComboBox(QComboBox):

    rightClicked = Signal(str, object)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.view().viewport().installEventFilter(
            self
        )

    def mousePressEvent(self, event):

        if event.button() == Qt.RightButton:

            voice_name = self.currentText()

            if voice_name:
                global_position = self.mapToGlobal(
                    event.position().toPoint()
                )

                self.rightClicked.emit(
                    voice_name,
                    global_position
                )

            return

        super().mousePressEvent(event)

    def eventFilter(self, watched, event):

        if (
            watched == self.view().viewport()
            and event.type() == QEvent.MouseButtonPress
            and event.button() == Qt.RightButton
        ):

            index = self.view().indexAt(
                event.position().toPoint()
            )

            if index.isValid():

                voice_name = self.itemText(
                    index.row()
                )

                global_position = self.view().viewport().mapToGlobal(
                    event.position().toPoint()
                )

                self.rightClicked.emit(
                    voice_name,
                    global_position
                )

            return True

        return super().eventFilter(
            watched,
            event
        )