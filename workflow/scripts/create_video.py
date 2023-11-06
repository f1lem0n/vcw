from pathlib import Path
import random
import sys
from PIL import Image

from moviepy.editor import VideoFileClip, AudioFileClip


def get_random_image(images_path: Path) -> Path:
    """
    Get a random image from the images directory, check if it's 16:9 and if it is,
    then rescale it to 4k resolution, and if not crop the image to 16:9
    (max width, centered vertically) and then rescale it to 4k
    """
    image_files = list(images_path.iterdir())
    if 20 > len(image_files) > 0:
        print("WARNING: You have less than 20 images in your images directory.")
    elif len(image_files) == 0:
        print("ERROR: You have no images left in your images directory.")
        sys.exit(1)
    image_path = random.choice(image_files).absolute()
    image = Image.open(image_path)

    width, height = image.size
    aspect_ratio = width / height

    if abs(aspect_ratio - 16 / 9) < 0.01:  # if the image is approximately 16:9
        image = image.resize((3840, 2160))  # rescale to 4k
    else:
        new_height = width / 16 * 9
        top = (height - new_height) / 2
        image = image.crop((0, top, width, top + new_height))  # crop to 16:9
        image = image.resize((3840, 2160))  # rescale to 4k

    image.save(image_path)

    return image_path


def create_video(
    image: Path, music_path: Path, framerate: int, output_path: Path
) -> None:
    """
    Create a video from a random image and an audio file
    """
    audio_clip = AudioFileClip(str(music_path))
    video_clip = VideoFileClip(str(image))
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
    selected_image.unlink()
