from enum import Enum
from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, Callable, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

@dataclass
class Difficulty:
    name_en: str
    name_jp: str
    artist: str
    bpm: str
    bpm_base: float
    set: str
    set_friendly: str
    time: int
    side: int
    world_unlock: bool
    remote_download: bool
    bg: str
    date: int
    version: str
    difficulty: int
    rating: int
    note: int
    chart_designer: str
    jacket_designer: str
    jacket_override: bool
    audio_override: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Difficulty':
        assert isinstance(obj, dict)
        name_en = from_str(obj.get("name_en"))
        name_jp = from_str(obj.get("name_jp"))
        artist = from_str(obj.get("artist"))
        bpm = from_str(obj.get("bpm"))
        bpm_base = from_float(obj.get("bpm_base"))
        set = from_str(obj.get("set"))
        set_friendly = obj.get("set_friendly")
        time = from_int(obj.get("time"))
        side = from_int(obj.get("side"))
        world_unlock = from_bool(obj.get("world_unlock"))
        remote_download = from_bool(obj.get("remote_download"))
        bg = from_str(obj.get("bg"))
        date = from_int(obj.get("date"))
        version = from_str(obj.get("version"))
        difficulty = from_int(obj.get("difficulty"))
        rating = from_int(obj.get("rating"))
        note = from_int(obj.get("note"))
        chart_designer = from_str(obj.get("chart_designer"))
        jacket_designer = from_str(obj.get("jacket_designer"))
        jacket_override = from_bool(obj.get("jacket_override"))
        audio_override = from_bool(obj.get("audio_override"))
        return Difficulty(name_en, name_jp, artist, bpm, bpm_base, set, set_friendly, time, side, world_unlock, remote_download, bg, date, version, difficulty, rating, note, chart_designer, jacket_designer, jacket_override, audio_override)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name_en"] = from_str(self.name_en)
        result["name_jp"] = from_str(self.name_jp)
        result["artist"] = from_str(self.artist)
        result["bpm"] = from_str(self.bpm)
        result["bpm_base"] = to_float(self.bpm_base)
        result["set"] = from_str(self.set)
        result["set_friendly"] = from_str(self.set_friendly)
        result["time"] = from_int(self.time)
        result["side"] = from_int(self.side)
        result["world_unlock"] = from_bool(self.world_unlock)
        result["remote_download"] = from_bool(self.remote_download)
        result["bg"] = from_str(self.bg)
        result["date"] = from_int(self.date)
        result["version"] = from_str(self.version)
        result["difficulty"] = from_int(self.difficulty)
        result["rating"] = from_int(self.rating)
        result["note"] = from_int(self.note)
        result["chart_designer"] = from_str(self.chart_designer)
        result["jacket_designer"] = from_str(self.jacket_designer)
        result["jacket_override"] = from_bool(self.jacket_override)
        result["audio_override"] = from_bool(self.audio_override)
        return result


@dataclass
class SongListElement:
    song_id: str
    difficulties: List[Difficulty]
    alias: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'SongListElement':
        assert isinstance(obj, dict)
        song_id = from_str(obj.get("song_id"))
        difficulties = from_list(Difficulty.from_dict, obj.get("difficulties"))
        alias = from_list(from_str, obj.get("alias"))
        return SongListElement(song_id, difficulties, alias)

    def to_dict(self) -> dict:
        result: dict = {}
        result["song_id"] = from_str(self.song_id)
        result["difficulties"] = from_list(lambda x: to_class(Difficulty, x), self.difficulties)
        result["alias"] = from_list(from_str, self.alias)
        return result


def song_list_from_dict(s: Any) -> List[SongListElement]:
    return from_list(SongListElement.from_dict, s)


def song_list_to_dict(x: List[SongListElement]) -> Any:
    return from_list(lambda x: to_class(SongListElement, x), x)


# generated from app.quicktype.io