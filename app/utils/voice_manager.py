import os
import shutil


class VoiceManager:

    def __init__(self):

        self.voices_directory = os.path.join(
            os.path.expanduser("~"),
            "TextToSpeechAIStudio",
            "voices"
        )

        os.makedirs(
            self.voices_directory,
            exist_ok=True
        )

    def save_voice(self, name, source_audio_path):

        file_extension = os.path.splitext(
            source_audio_path
        )[1]

        destination_path = os.path.join(
            self.voices_directory,
            f"{name}{file_extension}"
        )

        shutil.copy2(
            source_audio_path,
            destination_path
        )

        return destination_path

    def get_saved_voices(self):

        if not os.path.exists(
            self.voices_directory
        ):
            return []

        voices = []

        for file_name in os.listdir(
            self.voices_directory
        ):

            file_path = os.path.join(
                self.voices_directory,
                file_name
            )   

            if os.path.isfile(file_path):

                voices.append(
                    os.path.splitext(file_name)[0]
                )

        voices.sort()

        return voices

    def get_voice_path(self, name):

        for file_name in os.listdir(
            self.voices_directory
        ):

            file_path = os.path.join(
                self.voices_directory,
                file_name
            )

            if os.path.isfile(file_path):

                voice_name = os.path.splitext(
                    file_name
                )[0]

                if voice_name == name:
                    return file_path

        return None

    def update_voice(self, name, source_audio_path):

        existing_path = self.get_voice_path(name)

        if existing_path is None:
            return None

        file_extension = os.path.splitext(
            source_audio_path
        )[1]

        new_path = os.path.join(
            self.voices_directory,
            f"{name}{file_extension}"
        )

        if existing_path != new_path:
            os.remove(existing_path)

        shutil.copy2(
            source_audio_path,
            new_path
        )

        return new_path

    def rename_voice(self, old_name, new_name):

        existing_path = self.get_voice_path(
            old_name
        )

        if existing_path is None:
            return None

        file_extension = os.path.splitext(
            existing_path
        )[1]

        new_path = os.path.join(
            self.voices_directory,
            f"{new_name}{file_extension}"
        )

        if os.path.exists(new_path):
            return None

        os.rename(
            existing_path,
            new_path
        )

        return new_path

    def delete_voice(self, name):

        voice_path = self.get_voice_path(name)

        if voice_path is None:
            return False

        os.remove(voice_path)

        return True