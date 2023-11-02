import pathlib
import sys
import random

from mutagen.mp3 import MP3
from pydub import AudioSegment


def get_files_to_combine(
    audio_path: pathlib.Path, target_length: int
) -> list[pathlib.Path]:
    """
    get list of audio files to combine
    """
    try:
        audio_files = list(audio_path.iterdir())
        files_to_combine = []
        total_length = 0
        while total_length < target_length:
            audio_file = random.choice(audio_files)
            print("processing:", audio_file.absolute())
            audio_length = MP3(audio_file).info.length
            total_length += audio_length
            files_to_combine.append(audio_file)
            audio_files.remove(audio_file)  # avoid duplicates
    except IndexError:
        print("ERROR: Not enough unique audio files to reach target length.")
        exit(1)
    return files_to_combine


def combine_files(
    files_to_combine: list[pathlib.Path], output_path: pathlib.Path
) -> None:
    combined_audio = AudioSegment.empty()
    for file in files_to_combine:
        audio = AudioSegment.from_mp3(file)
        combined_audio += audio
    combined_audio.export(output_path, format="mp3")


if __name__ == "__main__":
    # assign args from command line
    audio_path = pathlib.Path(sys.argv[1]).absolute()
    target_length = int(sys.argv[2])
    output_path = pathlib.Path(sys.argv[3]).absolute()
    files_to_combine = get_files_to_combine(audio_path, target_length)
    combine_files(files_to_combine, output_path)
    print("SUCCESS: Combined audio files.")
