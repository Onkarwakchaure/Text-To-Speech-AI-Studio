from PySide6.QtCore import QObject, Signal

from tts.xtts_engine import generate_xtts
from tts.f5_engine import generate_f5tts


class TTSWorker(QObject):

    finished = Signal(str)
    error = Signal(str)

    def __init__(
        self,
        engine,
        text,
        language,
        voice_mode,
        output_path,
        speaker_wav=None,
        speaker=None,
        speed=1.0,
        reference_text="",
        remove_silence=False
    ):
        
        super().__init__()

        self.engine = engine
        self.text = text
        self.language = language
        self.voice_mode = voice_mode
        self.output_path = output_path
        self.speaker_wav = speaker_wav
        self.speaker = speaker
        self.speed = speed
        self.reference_text = reference_text
        self.remove_silence = remove_silence

    def run(self):

        try:

            # XTTS v2

            if self.engine == "XTTS v2":

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

            # F5-TTS

            elif self.engine == "F5-TTS":

                generate_f5tts(
                    text=self.text,
                    reference_audio=self.speaker_wav,
                    output_path=self.output_path,
                    speed=self.speed,
                    reference_text=self.reference_text,
                    remove_silence=self.remove_silence
                )

            # Unknown engine

            else:

                raise ValueError(
                    f"Unsupported TTS engine: {self.engine}"
                )

            self.finished.emit(self.output_path)

        except Exception as e:

            self.error.emit(str(e))