from JSON.songlist import *

DIFFICULTIES = ["Past", "Present", "Future", "Beyond"]


class Difficulty:
    def __init__(self, key, raw: Difficulty):
        self.key = key
        self.rating = raw.rating / 10

    def __str__(self):
        return f"{self.key} ({self.rating})"


class Song:
    def __init__(self, raw: SongListElement):
        self.song_name = raw.difficulties[0].name_en
        self.song_id = raw.song_id
        self.difficulties = []
        for index in range(len(raw.difficulties)):
            self.difficulties.append(Difficulty(
                DIFFICULTIES[index], raw.difficulties[index]))

    def __str__(self):
        return self.song_name
