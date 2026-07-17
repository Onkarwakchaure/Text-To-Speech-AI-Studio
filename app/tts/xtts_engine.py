from TTS.api import TTS
import os

tts_model = TTS(
    "tts_models/multilingual/multi-dataset/xtts_v2"
)

def generate_xtts(
    text,
    language,
    output_path,
    speaker_wav=None
):

    if speaker_wav:
        tts_model.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=speaker_wav,
            language=language
        )

    else:
        tts_model.tts_to_file(
            text=text,
            file_path=output_path,
            speaker="Ana Florence",
            language=language
        )

    return output_path
