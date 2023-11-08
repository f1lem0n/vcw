from pathlib import Path
import random
import sys


def create_description(
    template_path: Path, tracklist_path: Path, description_path: Path
) -> None:
    """Create a description of the video."""
    with open(template_path, "r") as template_file:
        template = template_file.read()
    with open(tracklist_path, "r") as tracklist_file:
        tracklist = tracklist_file.read()
    description = template.format(tracklist=tracklist)
    with open(description_path, "w") as description_file:
        description_file.write(description)
    print("SUCCESS: Description created.")


def choose_title(titles_path, title_path):
    """Choose a title for the video."""
    with open(titles_path, "r") as titles_file:
        titles = titles_file.readlines()
    if 0 < len(titles) < 20:
        print("WARNING: Less than 20 titles left.")
    elif len(titles) == 0:
        print("ERROR: No titles left.")
        exit(1)
    title = random.choice(titles)
    titles.remove(title)
    with open(titles_path, "w") as titles_file:
        titles_file.writelines(titles)
    with open(title_path, "w") as title_file:
        title_file.write(title)
    print("SUCCESS: Title chosen.")


if __name__ == "__main__":
    template_path = Path(sys.argv[1])
    tracklist_path = Path(sys.argv[2])
    titles_path = Path(sys.argv[3])
    description_path = Path(sys.argv[4])
    title_path = Path(sys.argv[5])
    create_description(template_path, tracklist_path, description_path)
    choose_title(titles_path, title_path)
