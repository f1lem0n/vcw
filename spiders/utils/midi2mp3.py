# Prerequisites: timidity, ffmpeg

from pathlib import Path
from sys import argv
import subprocess

try:
    files = Path(argv[1]).iterdir()
    output_dir = Path(argv[2]).absolute()
except IndexError:
    print("Usage: python3 midi2mp3.py <input_directory> <output_directory>")
    exit(1)
log = ""
try:
    for f in files:
        if Path(f).suffix != ".mid":
            continue
        if Path(output_dir / f"{f.stem}.mp3").exists():
            continue
        print(f"Converting {f.name} to wav...")
        proc1 = subprocess.run(
            f"timidity \"{f}\" -OwS2 -o \"{output_dir / f.stem}.wav\"",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        log += proc1.stdout.decode("latin-1")
        print(f"Converting {f.stem}.wav to mp3...")
        proc2 = subprocess.run(
            f"ffmpeg -i \"{output_dir / f.stem}.wav\" -vn -ar 44100 -ac 2 -b:a 192k \"{output_dir / f.stem}.mp3\"",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        log += proc2.stderr.decode("latin-1")
        print("Removing wav file...\n")
        Path(output_dir / f"{f.stem}.wav").unlink()
except KeyboardInterrupt:
    Path(output_dir / f"{f.stem}.wav").unlink()
    Path(output_dir / f"{f.stem}.mp3").unlink()
    print("\nKeyboard interrupt detected. Exiting...")
    exit(1)
with open(output_dir / "log.txt", "w") as f:
    f.write(log)