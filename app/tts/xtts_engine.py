from TTS.api import TTS
import os

tts_model = TTS(
    "tts_models/multilingual/multi-dataset/xtts_v2"
)

def generate_xtts(
    text,
    language,
    output_path,
    speaker="Ana Florence",
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
            speaker=speaker,
            language=language
        )

    return output_path

def get_available_speakers():
    return list(tts_model.synthesizer.tts_model.speaker_manager.name_to_id)