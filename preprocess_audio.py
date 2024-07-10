import os
from pydub import AudioSegment

def preprocess_audio(audio_folder, output_format='mp3', bitrate='96k'):
    for filename in os.listdir(audio_folder):
        file_path = os.path.join(audio_folder, filename)
        if filename.endswith(('.m4a', '.opus')):
            try:
                audio = AudioSegment.from_file(file_path)
                output_path = f"{os.path.splitext(file_path)[0]}.{output_format}"
                audio.export(output_path, format=output_format, bitrate=bitrate)
                print(f"Converted {filename} to {output_format} with bitrate {bitrate}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")