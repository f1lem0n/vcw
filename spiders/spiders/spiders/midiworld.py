from pathlib import Path
import os

import scrapy


class MidiworldSpider(scrapy.Spider):
    name = "midiworld"
    allowed_domains = ["midiworld.com"]
    artists = [
        "Bach",
        "Bartok",
        "Beethoven",
        "Brahms",
        "Byrd",
        "Chopin",
        "Haydn",
        "Handel",
        "Hummel",
        "Liszt",
        "Mendelssohn",
        "Mozart",
        "Rachmaninov",
        "Scarlatti",
        "Schumann",
        "Scriabin",
        "Shostakovich",
        "Tchaikovsky",
    ]

    def start_requests(self):
        urls = [
            f"https://www.midiworld.com/{artist.lower()}.htm"
            for artist in self.artists
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Get all MIDI URLs and names
        midi_urls = response.xpath("//div[@id='page']//li/a/@href").getall()
        midi_names = response.xpath("//div[@id='page']//li/a/text()").getall()

        # Create appropriate curl commands and run them to download MIDIs
        artist = response.url.split("/")[-1].split(".")[0]
        formatted_midi_names = []
        for mn in midi_names:
            if "[" in mn:
                mn = mn.split("[")[0]
            elif "(" in mn:
                mn = mn.split("(")[0]
            mn = mn.strip()
            mn = mn.replace('"', "")
            mn = f"{artist.title()}, {mn}"
            mn = mn.replace("/", " ")
            formatted_midi_names.append(mn)
        midi_for_curl = zip(midi_urls, formatted_midi_names)
        for url, name in midi_for_curl:
            if not Path(f"output/midis/{name}.mid").exists():
                cmd = (f"curl {url} -o \"output/midis/{name}.mid\"")
                print(cmd)
                os.system(cmd)
