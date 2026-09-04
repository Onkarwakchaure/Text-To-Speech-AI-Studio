from TTS.api import TTS


tts_model = None


def get_xtts_model():

    global tts_model

    if tts_model is None:

        print("Loading XTTS v2 Model...")

        tts_model = TTS(
            "tts_models/multilingual/multi-dataset/xtts_v2"
        )

        print("XTTS v2 Loaded.")

    return tts_model


def generate_xtts(
    text,
    language,
    output_path,
    speaker="Ana Florence",
    speaker_wav=None
):

    model = get_xtts_model()

    print("Speaker WAV:", speaker_wav)

    if speaker_wav:

        model.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=speaker_wav,
            language=language
        )

    else:

        model.tts_to_file(
            text=text,
            file_path=output_path,
            speaker=speaker,
            language=language
        )

    return output_path


def get_available_speakers():

    model = get_xtts_model()

    return list(
        model.synthesizer.tts_model.speaker_manager.name_to_id
    )