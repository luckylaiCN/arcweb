from utils.html import *
from utils.auth import *
from utils.svgGenerator import *
from JSON.songlist import *
from JSON.account import *

import os
import base64
import requests
import datetime
import pytz
import traceback
import time
import io

from typing import List

from urllib import parse
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import make_response
from flask import send_file


def pprint(*arg, **kwargs):
    print(*arg, **kwargs)


timezone = os.environ.get("timezone", "Asia/Shanghai")
py_timezone = pytz.timezone(timezone)
utc = pytz.timezone("UTC")


def do_nothing():
    return None


class ExceptionHandler:
    def __init__(self):
        self.last = ""
        self.timestamp = 0

    def record(self):
        self.last = traceback.format_exc()
        self.timestamp = int(time.time() * 1e3)

    def get_last_exception(self):
        return {
            "exception": self.last,
            "time": self.timestamp
        }

def date_from(timestamp):
    time0 = datetime.datetime.utcfromtimestamp(
            timestamp / 1000)
    utc_time = datetime.datetime(time0.year, time0.month, time0.day,
                                    time0.hour, time0.minute, time0.second, time0.microsecond, tzinfo=utc)
    datetime_zoned = utc_time.astimezone(py_timezone)
    now = datetime.datetime.now().astimezone(py_timezone)
    delta = now - datetime_zoned
    time_str = datetime_zoned.strftime("%Y.%m.%d %H:%M:%S") + "  ("
    if int(delta.days) > 0 :
        return time_str + str(int(delta.days)) + " D)"
    if delta.seconds > 3600:
        return time_str + str(int(delta.seconds / 3600)) + " H)"
    if delta.seconds > 60:
        return time_str + str(int(delta.seconds / 60)) + " M)"
    return time_str + str(int(delta.seconds)) + " S)"


class ArcController:
    song_list_update_time : int
    song_list: List[SongListElement]
    song_id_difficulties_dict: dict

    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.header = {
            "User-Agent": self.token,
            "Authorization": f"Bearer {self.token}"
        }
        self.session = requests.session()
        self.song_list = []
        self.song_id_difficulties_dict = {}
        self.songs_html = []
        self.song_list_update_time = 0
        self.get_song_list()

    def get(self, ispublic=True, *arg, **kwargs):
        headers = {}
        if not ispublic:
            headers.update(self.header)
        response = self.session.get(headers=headers, *arg, **kwargs)
        return response

    def get_json(self, ispublic=True, *arg, **kwargs):
        try:
            response = self.get(ispublic, *arg, **kwargs)
            return response.json()
        except:
            return {}

    def get_content(self, ispublic=True, *arg, **kwargs):
        try:
            response = self.get(ispublic, *arg, **kwargs)
            return response.content
        except:
            return b''

    def u(self, uri):
        return self.url + uri

    def get_song_asset(self, song_id, difficulty):
        return self.get_content(url=self.u(f"assets/song?songid={song_id}&difficulty={difficulty}"), ispublic=False)

    def get_song_preview(self, song_id, difficulty):
        return self.get_content(url=self.u(f"assets/preview?songid={song_id}&difficulty={difficulty}"), ispublic=False)

    def get_song_list(self):
        response = self.get_json(url=self.u("song/list"))
        if response is None:
            return
        status_code = response["status"]
        if status_code:
            pprint(f"[get_song_list] Got status code {status_code}")
            return
        content = response["content"]
        self.song_list = song_list_from_dict(content["songs"])
        self.song_id_difficulties_dict = {}
        for item in self.song_list:
            self.song_id_difficulties_dict[item.song_id] = item.difficulties
            self.songs_html.append(Song(item))
        self.songs_html.sort(key=lambda x: x.song_name)
        self.song_list_update_time = time.time()
        return self.song_list

    def check_update(self):
        if time.time() - self.song_list_update_time > 86400:
            self.get_song_list()

    def get_user_by_code(self, uid):
        self.check_update()
        response: dict = self.get_json(url=self.u(
            f"user/info?usercode={uid}"), ispublic=False)
        return response.get("content")

    def get_user_best(self, uid, song_id, difficulty):
        self.check_update()
        response: dict = self.get_json(ispublic=False, url=self.u(
            f"user/best?usercode={uid}&songid={song_id}&difficulty={difficulty}"))
        return response.get("content")

    def get_song_asset_api(self, song_id, difficulty : str):
        return self.get_song_asset(song_id, difficulty.lower())

    def get_song_preview_api(self,song_id, difficulty:str):
        return self.get_song_preview(song_id, difficulty.lower())

    def get_user_best40(self, uid):
        self.check_update()
        response: dict = self.get_json(ispublic=False, url=self.u(
            f"user/best30?usercode={uid}&overflow=9"))
        return response.get("content")

    def get_user_best40_api(self,uid):
        result = self.get_user_best40(uid)
        content = account_best40_from_dict(result)
        
        b40 = content.best30_list[:]
        b40.extend(content.best30_overflow)
        resp = []
        for song in b40:
            info : Difficulty = self.song_id_difficulties_dict[song.song_id][song.difficulty]
            resp.append({
                "id" : song.song_id,
                "name" : info.name_en,
                "difficulty" : str(song.difficulty),
                "diff" : ["PST","PRS","FTR","BYD"][song.difficulty],
                "time_from" : date_from(song.time_played),
                "result" : {
                    "score" : song.score,
                    "shiny" : song.shiny_perfect_count,
                    "perfect" : song.perfect_count,
                    "far" : song.near_count,
                    "lost" : song.miss_count,
                },
                "rating":{
                    "full" : info.rating / 10,
                    "obtained" : round(song.rating,2)
                }
            })
        return resp

    def update_list_now(self):
        return self.get_song_list()


    def generate_recent_svg(self, uid):
        response = self.get_user_by_code(uid)
        this_account: Account = account_from_dict(response)
        recent_play_song = this_account.recent_score[0]
        song_id = recent_play_song.song_id
        song_info: List[Difficulty] = self.song_id_difficulties_dict[song_id]
        difficulty_info = song_info[recent_play_song.difficulty]
        score = recent_play_song.score
        shiny_perfect_count = recent_play_song.shiny_perfect_count
        perfect_count = recent_play_song.perfect_count
        near_count = recent_play_song.near_count
        miss_count = recent_play_song.miss_count
        difficulty_level = difficulty_info.rating / 10
        difficulty = ["Past", "Present", "Future",
                      "Beyond"][recent_play_song.difficulty]
        rating = this_account.account_info.rating
        username = this_account.account_info.name
        songname = difficulty_info.name_en
        illustration_b64 = base64.b64encode(self.get_song_asset(
            song_id, recent_play_song.difficulty)).decode()
        playptt = "%.3f" % (recent_play_song.rating)
        time0 = datetime.datetime.utcfromtimestamp(
            recent_play_song.time_played / 1000)
        utc_time = datetime.datetime(time0.year, time0.month, time0.day,
                                     time0.hour, time0.minute, time0.second, time0.microsecond, tzinfo=utc)
        datetime_zoned = utc_time.astimezone(py_timezone)
        playtime = datetime_zoned.strftime("%Y.%m.%d %H:%M:%S")
        return gen_svg(illustration_b64, rating, username, score, songname, difficulty, difficulty_level, shiny_perfect_count, perfect_count, near_count, miss_count, playtime, playptt)

    def generate_best_svg(self, uid, song_id, difficulty):
        response = self.get_user_best(uid, song_id, difficulty)
        this_account: AccountBest = account_best_from_dict(response)
        recent_play_song = this_account.record
        song_id = recent_play_song.song_id
        song_info: List[Difficulty] = self.song_id_difficulties_dict[song_id]
        difficulty_info = song_info[recent_play_song.difficulty]
        score = recent_play_song.score
        shiny_perfect_count = recent_play_song.shiny_perfect_count
        perfect_count = recent_play_song.perfect_count
        near_count = recent_play_song.near_count
        miss_count = recent_play_song.miss_count
        difficulty_level = difficulty_info.rating / 10
        difficulty = ["Past", "Present", "Future",
                      "Beyond"][recent_play_song.difficulty]
        rating = this_account.account_info.rating
        username = this_account.account_info.name
        songname = difficulty_info.name_en
        illustration_b64 = base64.b64encode(self.get_song_asset(
            song_id, recent_play_song.difficulty)).decode()
        playptt = "%.3f" % (recent_play_song.rating)
        time0 = datetime.datetime.utcfromtimestamp(
            recent_play_song.time_played / 1000)
        utc_time = datetime.datetime(time0.year, time0.month, time0.day,
                                     time0.hour, time0.minute, time0.second, time0.microsecond, tzinfo=utc)
        datetime_zoned = utc_time.astimezone(py_timezone)
        playtime = datetime_zoned.strftime("%Y.%m.%d %H:%M:%S")
        return gen_svg(illustration_b64, rating, username, score, songname, difficulty, difficulty_level, shiny_perfect_count, perfect_count, near_count, miss_count, playtime, playptt)


def make_cache_response(response, age=86400):
    response = make_response(response)
    response.headers["Cache-Control"] = "public, max-age=" + str(age)
    return response


url = os.environ["host"]
token = os.environ["token"]
usercode = os.environ["usercode"]
auth_key = os.environ["auth"]

app = Flask(__name__)
arc_handler = ArcController(url, token)
exception_handler = ExceptionHandler()
auth_handler = AuthController(auth_key, usercode)

@app.route("/image/recent")
def route_recent():
    request_user = auth_handler.get_id(request.args.get("s", "default"))
    svg = arc_handler.generate_recent_svg(request_user),
    return app.response_class(svg, mimetype="image/svg+xml")


@app.route("/log")
def route_log():
    return jsonify(exception_handler.get_last_exception())


@app.route("/image/best")
def route_best():
    request_user = auth_handler.get_id(request.args.get("s", "default"))
    svg = arc_handler.generate_best_svg(
        request_user, request.args.get("song"), request.args.get("difficulty"))
    return app.response_class(svg, mimetype="image/svg+xml")

@app.route("/")
@app.route("/pages/songlist")
def route_songlist():
    return render_template(
        "songs.html", data=arc_handler.songs_html, s=request.args.get("s", "default"))


@app.route("/pages/song/<req_type>")
def route_song(req_type):
    subfix = req_type + "?" + parse.urlencode(request.args)
    return render_template(
        "song.html",subfix=subfix,s=request.args.get("s", "default")
    )


@app.route("/asset/illustration/<song_id>/<difficulty>")
def route_illustration(song_id, difficulty):
    result = arc_handler.get_song_asset_api(song_id, difficulty)
    return make_cache_response(send_file(
        io.BytesIO(result),
        mimetype="image/jpeg"
    ),129600)

@app.route("/pages/best30")
@app.route("/pages/best40")
def route_best40():
    request_user = auth_handler.get_id(request.args.get("s", "default"))
    data = arc_handler.get_user_best40_api(request_user)
    return render_template("best40.html",data=data,s=request.args.get("s", "default"))


@app.errorhandler(500)
def server_error(error):
    return app.response_class(svg_503, mimetype="image/svg+xml")

@app.route("/image/preview")
def route_preview():
    song_id = request.args.get("song")
    difficulty = request.args.get("difficulty")
    result = arc_handler.get_song_preview_api(song_id, difficulty)
    return make_cache_response(send_file(
        io.BytesIO(result),
        mimetype="image/png"
    ),129600)

@app.route("/admin/update")
def update_songlist():
    return jsonify(arc_handler.update_list_now())


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.run()
