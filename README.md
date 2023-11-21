# 🎥 Video Creation Workflow (VCW)
> Workflow for automatically creating and uploading randomized music playlist videos to YouTube

## Disclaimer
This workflow DOES NOT provide all the necessary tools to create libraries needed to run it.

## Prerequisites

- conda >= 23.5.0
- git

## Setup

1. Clone this repository: `git clone https://github.com/f1lem0n/vcw.git`
2. After cloning `cd` into the repository root directory and execute ALL the following commands from within it
3. Create conda environment: `conda env create -f envs/vcw.yaml`
4. You will need to create your own `workflow/configs/params.yaml` file like so:
```
yt_account: <channel_name>          # it does not have to be exactly like on YouTube,
                                    # it is just used for creating and using auth files

upload: True                        # choose if you want to upload the video after creating it

working_dir: <path/to/working/dir>  # working dir should have a structure as described below

target_length: <length>             # target video length in seconds
                                    # e.g 3600 will result in video of length ABOUT 1 h
```

HOW THE WORKING DIRECTORY SHOULD BE STRUCTURED INITIALLY:

```
working_dir
└── input
    ├── audio
    │   └── some_audio.mp3
    ├── images
    │   └── some_image.jpg
    ├── soundfonts
    │   └── some_soundfont.sf2
    ├── description_template.txt
    ├── keywords.txt
    └── titles.txt
```

Remember to put `{tracklist}` keyword into your description template
as this will be used to create a custom description for the video containing the tracklist.

## Usage

After activating vcw environment (`conda activate vcw`), view help:
```
$ python vcw.py -h
Usage: vcw.py [OPTIONS] COMMAND [ARGS]...

    VCW is an automated tool for music playlist video creation

  Options:
    -h, --help  Show this message and exit.

  Commands:
    clean   Clean all redundant files
    run     Run VCW
    upload  Upload last video to YouTube
```

You can view more detailed help for every command by executing it with `-h` flag.

## Spiders

❗Most of the spiders are WORK IN PROGRESS, therefore they are not available yet.

Spiders are used to scrape the web for data (midis, mp3s, videos, pictures).
Because spiders are not part of the workflow but an additional tools for data collection,
they are not straightforward to use and require some programming knowledge.
To use spiders you will need to set up the Scrapy environment: `conda env create -f envs/scrapy.yaml`.
There are several utility scripts available at `spiders/utils`.
You can use them by executing them with Python. Please note that some need additional dependencies.

For more information please refer to [Scrapy documentation](https://docs.scrapy.org/en/latest/).
