from app.tts.f5_engine import generate_f5tts, f5_model
import time

reference_audio = "E:\\Projects\\Text-To-Speech-AI-Desktop\\F5_TTS\\reference_audio\\Aria.mp3"

print("Transcribing reference audio...\n")

transcribe_start = time.perf_counter()

text = f5_model.transcribe(reference_audio)

transcribe_end = time.perf_counter()

print("=" * 50)
print("TRANSCRIPTION")
print("=" * 50)

print(text)

print(f"\nTime: {transcribe_end - transcribe_start:.2f} seconds")

print("=" * 50)
print("Generating Speech...")
print("=" * 50)
generate_start = time.perf_counter()

generate_f5tts(
    text="But I don't want to jump there yet. Let's first confirm this refactor works exactly as expected.",
    reference_audio=reference_audio,
    output_path="output4.wav",
    reference_text="",
    speed=1.0
)

generate_end = time.perf_counter()
print(f"\nTime: {generate_end - generate_start:.2f} seconds")

print("\nAudio saved successfully!")

print(f"\n Total Time: {generate_end - transcribe_start:.2f} seconds")
