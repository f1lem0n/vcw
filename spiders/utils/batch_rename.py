from pathlib import Path
from sys import argv

try:
    filenames = Path(argv[1]).absolute().iterdir()
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
    fn = fn.replace("_ ", ", ")
    fn = fn.replace("J. S. Bach", "Bach")
    fn = fn.replace("P. I. Tchaikovsky", "Tchaikovsky")
    fn = fn.replace("W. A. Mozart", "Mozart")
    fn = fn.replace(".midi", ".mid")
    Path(old_fn).rename(fn)
    print("Done!")
