from PySide6.QtCore import QSettings


class SettingsManager:

    def __init__(self):
        self.settings = QSettings(
            "Onkar Wakchaure",
            "TextToSpeechAIStudio"
        )

    def save(self, key, value):
        self.settings.setValue(key, value)
        self.settings.sync()

    def load(self, key, default=None):
        return self.settings.value(key, default)

    def remove(self, key):
        self.settings.remove(key)
        self.settings.sync()

    def clear(self):
        self.settings.clear()
        self.settings.sync()