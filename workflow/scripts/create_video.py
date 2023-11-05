from pathlib import Path
import random
import sys

from moviepy.editor import VideoFileClip, AudioFileClip


def get_random_image(images_path: Path) -> Path:
    """
    Get a random image from the images directory
    """
    image_files = list(images_path.iterdir())
    return random.choice(image_files).absolute()


def create_video(
    image: Path, music_path: Path, framerate: int, output_path: Path
) -> None:
    """
    Create a video from a random image and an audio file
    """
    video_clip = VideoFileClip(str(image))
    audio_clip = AudioFileClip(str(music_path))
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(str(output_path))


if __name__ == "__main__":
    # assign args from command line
    images_path = Path(sys.argv[1]).absolute()
    music_path = Path(sys.argv[2]).absolute()
    framerate = int(sys.argv[3])
    output_path = Path(sys.argv[4]).absolute()

    selected_image = get_random_image(images_path)
    create_video(selected_image, music_path, framerate, output_path)
