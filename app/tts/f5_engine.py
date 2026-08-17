import time

from f5_tts.api import F5TTS

print("Loading F5-TTS Model...")

load_start = time.perf_counter()

f5_model = F5TTS()

load_end = time.perf_counter()

print(
    f"F5-TTS Loaded in "
    f"{load_end - load_start:.2f} seconds."
)

def generate_f5tts(
    text,
    reference_audio,
    output_path,
    reference_text="",
    speed=1.0
):
    result = f5_model.infer(
        ref_file=reference_audio,
        ref_text=reference_text,
        gen_text=text,
        speed=speed,
        file_wave=output_path,
    )

    return output_path