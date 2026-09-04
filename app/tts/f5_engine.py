import time

from f5_tts.api import F5TTS


f5_model = None


def get_f5_model():

    global f5_model

    if f5_model is None:

        print("Loading F5-TTS Model...")

        load_start = time.perf_counter()

        f5_model = F5TTS()

        load_end = time.perf_counter()

        print(
            f"F5-TTS Loaded in "
            f"{load_end - load_start:.2f} seconds."
        )

    return f5_model


def generate_f5tts(
    text,
    reference_audio,
    output_path,
    reference_text="",
    speed=1.0,
    remove_silence=False
):

    model = get_f5_model()

    result = model.infer(
        ref_file=reference_audio,
        ref_text=reference_text,
        gen_text=text,
        speed=speed,
        remove_silence=remove_silence,
        file_wave=output_path,
    )

    return output_path