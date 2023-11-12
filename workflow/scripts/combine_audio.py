from datetime import timedelta
from pathlib import Path
import sys
import random

from mutagen.mp3 import MP3
from pydub import AudioSegment, effects


def get_tracklist_record(audio_file, total_length):
    """
    get tracklist record from audio file
    """
    timestamp = str(timedelta(seconds=total_length)).split(".")[0]
    title = Path(audio_file).stem
    tracklist_record = f"{timestamp} {title}"
    return tracklist_record


def get_files_to_combine(audio_path: Path, target_length: int) -> list[Path]:
    """
    get list of audio files to combine
    """
    try:
        audio_files = list(audio_path.iterdir())
        tracklist = []
        files_to_combine = []
        total_length = 0
        while total_length < target_length:
            audio_file = random.choice(audio_files)
            print("processing:", audio_file.absolute())
            audio_length = MP3(audio_file).info.length
            files_to_combine.append(audio_file)
            tracklist.append(get_tracklist_record(audio_file, total_length))
            audio_files.remove(audio_file)  # avoid duplicates
            total_length += audio_length + 2
    except IndexError:
        print("ERROR: Not enough unique audio files to reach target length.")
        exit(1)
    return files_to_combine, tracklist


def combine_files(files_to_combine: list[Path], output_path: Path) -> None:
    combined_audio = AudioSegment.empty() + AudioSegment.silent(duration=2000)
    for file in files_to_combine:
        audio = AudioSegment.from_mp3(file)
        combined_audio += audio + AudioSegment.silent(duration=2000)
    normalized_audio = effects.normalize(combined_audio)
    normalized_audio.export(output_path, format="mp3")


if __name__ == "__main__":
    # assign args from command line
    audio_path = Path(sys.argv[1]).absolute()
    target_length = int(sys.argv[2])
    audio_output = Path(sys.argv[3]).absolute()
    tracklist_output = Path(sys.argv[4]).absolute()
    # combine files and get tracklist
    files_to_combine, tracklist = get_files_to_combine(
        audio_path, target_length
    )
    with open(tracklist_output, "w") as f:
        f.write("\n".join(tracklist))
    combine_files(files_to_combine, audio_output)
    print("SUCCESS: Combined audio files.")
