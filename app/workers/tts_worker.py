from PySide6.QtCore import QObject, Signal
from tts.xtts_engine import generate_xtts


class TTSWorker(QObject):

    finished = Signal(str)
    error = Signal(str)

    def __init__(
        self,
        text,
        language,
        voice_mode,
        output_path,
        speaker_wav=None,
        speaker=None
    ):
        
        super().__init__()

        self.text = text
        self.language = language
        self.voice_mode = voice_mode
        self.output_path = output_path
        self.speaker_wav = speaker_wav
        self.speaker = speaker

    def run(self):
        try:

            if self.voice_mode == "Voice Cloning":
                generate_xtts(
                    text=self.text,
                    language=self.language,
                    output_path=self.output_path,
                    speaker_wav=self.speaker_wav
                )

            else:
                generate_xtts(
                    text=self.text,
                    language=self.language,
                    output_path=self.output_path,
                    speaker=self.speaker
                )

            self.finished.emit(self.output_path)

        except Exception as e:
            self.error.emit(str(e))