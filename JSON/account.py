from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class AccountInfo:
    code: int
    name: str
    user_id: int
    is_mutual: bool
    is_char_uncapped_override: bool
    is_char_uncapped: bool
    is_skill_sealed: bool
    rating: int
    join_date: int
    character: int

    @staticmethod
    def from_dict(obj: Any) -> 'AccountInfo':
        assert isinstance(obj, dict)
        code = int(from_str(obj.get("code")))
        name = from_str(obj.get("name"))
        user_id = from_int(obj.get("user_id"))
        is_mutual = from_bool(obj.get("is_mutual"))
        is_char_uncapped_override = from_bool(obj.get("is_char_uncapped_override"))
        is_char_uncapped = from_bool(obj.get("is_char_uncapped"))
        is_skill_sealed = from_bool(obj.get("is_skill_sealed"))
        rating = from_int(obj.get("rating"))
        join_date = from_int(obj.get("join_date"))
        character = from_int(obj.get("character"))
        return AccountInfo(code, name, user_id, is_mutual, is_char_uncapped_override, is_char_uncapped, is_skill_sealed, rating, join_date, character)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_str(str(self.code))
        result["name"] = from_str(self.name)
        result["user_id"] = from_int(self.user_id)
        result["is_mutual"] = from_bool(self.is_mutual)
        result["is_char_uncapped_override"] = from_bool(self.is_char_uncapped_override)
        result["is_char_uncapped"] = from_bool(self.is_char_uncapped)
        result["is_skill_sealed"] = from_bool(self.is_skill_sealed)
        result["rating"] = from_int(self.rating)
        result["join_date"] = from_int(self.join_date)
        result["character"] = from_int(self.character)
        return result


@dataclass
class RecentScore:
    score: int
    health: int
    rating: float
    song_id: str
    modifier: int
    difficulty: int
    clear_type: int
    best_clear_type: int
    time_played: int
    near_count: int
    miss_count: int
    perfect_count: int
    shiny_perfect_count: int

    @staticmethod
    def from_dict(obj: Any) -> 'RecentScore':
        assert isinstance(obj, dict)
        score = from_int(obj.get("score"))
        health = from_int(obj.get("health"))
        rating = from_float(obj.get("rating"))
        song_id = from_str(obj.get("song_id"))
        modifier = from_int(obj.get("modifier"))
        difficulty = from_int(obj.get("difficulty"))
        clear_type = from_int(obj.get("clear_type"))
        best_clear_type = from_int(obj.get("best_clear_type"))
        time_played = from_int(obj.get("time_played"))
        near_count = from_int(obj.get("near_count"))
        miss_count = from_int(obj.get("miss_count"))
        perfect_count = from_int(obj.get("perfect_count"))
        shiny_perfect_count = from_int(obj.get("shiny_perfect_count"))
        return RecentScore(score, health, rating, song_id, modifier, difficulty, clear_type, best_clear_type, time_played, near_count, miss_count, perfect_count, shiny_perfect_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["score"] = from_int(self.score)
        result["health"] = from_int(self.health)
        result["rating"] = to_float(self.rating)
        result["song_id"] = from_str(self.song_id)
        result["modifier"] = from_int(self.modifier)
        result["difficulty"] = from_int(self.difficulty)
        result["clear_type"] = from_int(self.clear_type)
        result["best_clear_type"] = from_int(self.best_clear_type)
        result["time_played"] = from_int(self.time_played)
        result["near_count"] = from_int(self.near_count)
        result["miss_count"] = from_int(self.miss_count)
        result["perfect_count"] = from_int(self.perfect_count)
        result["shiny_perfect_count"] = from_int(self.shiny_perfect_count)
        return result


@dataclass
class Account:
    account_info: AccountInfo
    recent_score: List[RecentScore]

    @staticmethod
    def from_dict(obj: Any) -> 'Account':
        assert isinstance(obj, dict)
        account_info = AccountInfo.from_dict(obj.get("account_info"))
        recent_score = from_list(RecentScore.from_dict, obj.get("recent_score"))
        return Account(account_info, recent_score)

    def to_dict(self) -> dict:
        result: dict = {}
        result["account_info"] = to_class(AccountInfo, self.account_info)
        result["recent_score"] = from_list(lambda x: to_class(RecentScore, x), self.recent_score)
        return result


def account_from_dict(s: Any) -> Account:
    return Account.from_dict(s)


def account_to_dict(x: Account) -> Any:
    return to_class(Account, x)

@dataclass
class Record:
    score: int
    health: int
    rating: float
    song_id: str
    modifier: int
    difficulty: int
    clear_type: int
    best_clear_type: int
    time_played: int
    near_count: int
    miss_count: int
    perfect_count: int
    shiny_perfect_count: int

    @staticmethod
    def from_dict(obj: Any) -> 'Record':
        assert isinstance(obj, dict)
        score = from_int(obj.get("score"))
        health = from_int(obj.get("health"))
        rating = from_float(obj.get("rating"))
        song_id = from_str(obj.get("song_id"))
        modifier = from_int(obj.get("modifier"))
        difficulty = from_int(obj.get("difficulty"))
        clear_type = from_int(obj.get("clear_type"))
        best_clear_type = from_int(obj.get("best_clear_type"))
        time_played = from_int(obj.get("time_played"))
        near_count = from_int(obj.get("near_count"))
        miss_count = from_int(obj.get("miss_count"))
        perfect_count = from_int(obj.get("perfect_count"))
        shiny_perfect_count = from_int(obj.get("shiny_perfect_count"))
        return Record(score, health, rating, song_id, modifier, difficulty, clear_type, best_clear_type, time_played, near_count, miss_count, perfect_count, shiny_perfect_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["score"] = from_int(self.score)
        result["health"] = from_int(self.health)
        result["rating"] = to_float(self.rating)
        result["song_id"] = from_str(self.song_id)
        result["modifier"] = from_int(self.modifier)
        result["difficulty"] = from_int(self.difficulty)
        result["clear_type"] = from_int(self.clear_type)
        result["best_clear_type"] = from_int(self.best_clear_type)
        result["time_played"] = from_int(self.time_played)
        result["near_count"] = from_int(self.near_count)
        result["miss_count"] = from_int(self.miss_count)
        result["perfect_count"] = from_int(self.perfect_count)
        result["shiny_perfect_count"] = from_int(self.shiny_perfect_count)
        return result


@dataclass
class AccountBest:
    account_info: AccountInfo
    record: Record

    @staticmethod
    def from_dict(obj: Any) -> 'AccountBest':
        assert isinstance(obj, dict)
        account_info = AccountInfo.from_dict(obj.get("account_info"))
        record = Record.from_dict(obj.get("record"))
        return AccountBest(account_info, record)

    def to_dict(self) -> dict:
        result: dict = {}
        result["account_info"] = to_class(AccountInfo, self.account_info)
        result["record"] = to_class(Record, self.record)
        return result


def account_best_from_dict(s: Any) -> AccountBest:
    return AccountBest.from_dict(s)


def account_best_to_dict(x: AccountBest) -> Any:
    return to_class(AccountBest, x)


@dataclass
class Best30:
    best_clear_type: int
    clear_type: int
    difficulty: int
    health: int
    miss_count: int
    modifier: int
    near_count: int
    perfect_count: int
    rating: float
    score: int
    shiny_perfect_count: int
    song_id: str
    time_played: int

    @staticmethod
    def from_dict(obj: Any) -> 'Best30':
        assert isinstance(obj, dict)
        best_clear_type = from_int(obj.get("best_clear_type"))
        clear_type = from_int(obj.get("clear_type"))
        difficulty = from_int(obj.get("difficulty"))
        health = from_int(obj.get("health"))
        miss_count = from_int(obj.get("miss_count"))
        modifier = from_int(obj.get("modifier"))
        near_count = from_int(obj.get("near_count"))
        perfect_count = from_int(obj.get("perfect_count"))
        rating = from_float(obj.get("rating"))
        score = from_int(obj.get("score"))
        shiny_perfect_count = from_int(obj.get("shiny_perfect_count"))
        song_id = from_str(obj.get("song_id"))
        time_played = from_int(obj.get("time_played"))
        return Best30(best_clear_type, clear_type, difficulty, health, miss_count, modifier, near_count, perfect_count, rating, score, shiny_perfect_count, song_id, time_played)

    def to_dict(self) -> dict:
        result: dict = {}
        result["best_clear_type"] = from_int(self.best_clear_type)
        result["clear_type"] = from_int(self.clear_type)
        result["difficulty"] = from_int(self.difficulty)
        result["health"] = from_int(self.health)
        result["miss_count"] = from_int(self.miss_count)
        result["modifier"] = from_int(self.modifier)
        result["near_count"] = from_int(self.near_count)
        result["perfect_count"] = from_int(self.perfect_count)
        result["rating"] = to_float(self.rating)
        result["score"] = from_int(self.score)
        result["shiny_perfect_count"] = from_int(self.shiny_perfect_count)
        result["song_id"] = from_str(self.song_id)
        result["time_played"] = from_int(self.time_played)
        return result


@dataclass
class AccountBest40:
    account_info: AccountInfo
    best30_avg: float
    best30_list: List[Best30]
    best30_overflow: List[Best30]
    recent10_avg: float

    @staticmethod
    def from_dict(obj: Any) -> 'AccountBest40':
        assert isinstance(obj, dict)
        account_info = AccountInfo.from_dict(obj.get("account_info"))
        best30_avg = from_float(obj.get("best30_avg"))
        best30_list = from_list(Best30.from_dict, obj.get("best30_list"))
        best30_overflow = from_list(Best30.from_dict, obj.get("best30_overflow"))
        recent10_avg = from_float(obj.get("recent10_avg"))
        return AccountBest40(account_info, best30_avg, best30_list, best30_overflow, recent10_avg)

    def to_dict(self) -> dict:
        result: dict = {}
        result["account_info"] = to_class(AccountInfo, self.account_info)
        result["best30_avg"] = to_float(self.best30_avg)
        result["best30_list"] = from_list(lambda x: to_class(Best30, x), self.best30_list)
        result["best30_overflow"] = from_list(lambda x: to_class(Best30, x), self.best30_overflow)
        result["recent10_avg"] = to_float(self.recent10_avg)
        return result


def account_best40_from_dict(s: Any) -> AccountBest40:
    return AccountBest40.from_dict(s)
# generated from app.quicktype.io