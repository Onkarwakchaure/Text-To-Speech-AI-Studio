from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

manager = tts.synthesizer.tts_model.speaker_manager

print("Number of speakers:")
print(manager.num_speakers)

print("\nName to ID:")
print(type(manager.name_to_id))
print(manager.name_to_id)