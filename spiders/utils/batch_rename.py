from pathlib import Path
from sys import argv

try:
    filenames = Path(argv[1]).iterdir()
except IndexError:
    print("Usage: python3 batch_rename.py <directory>")
    exit(1)
for fn in filenames:
    print("Renaming:", fn)
    old_fn = fn
    fn = str(fn).replace("..", ".")
    fn = fn.replace(",.", ".")
    fn = fn.replace(" -.", ".")
    fn = fn.replace("--", "-")
    fn = fn.replace("  ", " ")
    fn = fn.replace(" - ", "-")
    fn = fn.replace("-", " - ")
    fn = fn.replace(" ?", "?")
    fn = fn.replace(".midi", ".mid")
    Path(old_fn).rename(fn)
    print("Done!")