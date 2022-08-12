from JSON.songlist import song_list_from_dict,SongListElement,Difficulty
from JSON.account import account_from_dict,Account
from utils.svgGenerator import gen_svg
from typing import List

import os
import base64
import requests

from dotenv import load_dotenv
project_folder = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(project_folder, 'env_conf'))

from flask import Flask

def pprint(*arg,**kwargs):
    print(*arg,**kwargs)

class ArcBot:
    song_list : List[SongListElement]
    song_id_difficulties_dict : dict
    def __init__(self,url,token):
        self.url = url 
        self.token = token
        self.header = {
            "User-Agent" : self.token
        }
        self.session = requests.session()
        self.song_list = []
        self.song_id_difficulties_dict = {}

    def get(self,ispublic=True,*arg,**kwargs):
        headers = {}
        if not ispublic:
            headers.update(self.header)
        response = self.session.get(headers=headers,*arg,**kwargs)
        return response

    def get_json(self,ispublic=True,*arg,**kwargs):
        try:
            response = self.get(ispublic,*arg,**kwargs)
            return response.json()
        except:
            return None

    def get_content(self,ispublic=True,*arg,**kwargs):
        try:
            response = self.get(ispublic,*arg,**kwargs)
            return response.content
        except:
            pass
        
    def u(self,uri):
        return self.url + uri

    def get_song_asset(self,song_id,difficulty):
        return self.get_content(url = self.u(f"assets/song?songid={song_id}&difficulty={difficulty}"))

    def get_song_list(self):
        response = self.get_json(url = self.u("song/list"))
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
        return self.song_list

    def get_user_by_code(self,uid):
        response = self.get_json(url = self.u(f"user/info?usercode={uid}"),ispublic=False)
        return response.get("content")

    def generate_recent_svg(self,uid):
        if len(self.song_list) == 0:
            self.get_song_list()
        response = self.get_user_by_code(uid)
        account : Account = account_from_dict(response)
        recent_play_song = account.recent_score[0]
        song_id = recent_play_song.song_id
        song_info : List[Difficulty] = self.song_id_difficulties_dict[song_id]
        difficulty_info = song_info[recent_play_song.difficulty]
        score = recent_play_song.score
        shiny_perfect_count = recent_play_song.shiny_perfect_count
        perfect_count = recent_play_song.perfect_count
        near_count = recent_play_song.near_count
        miss_count = recent_play_song.miss_count
        difficulty_level = difficulty_info.rating / 10
        difficulty = ["Past","Present","Future","Beyond"][recent_play_song.difficulty]
        rating = account.account_info.rating
        username = account.account_info.name
        songname = difficulty_info.name_en
        illustration_b64 = base64.b64encode(self.get_song_asset(song_id,recent_play_song.difficulty)).decode()
        return gen_svg(illustration_b64,rating,username,score,songname,difficulty,difficulty_level,shiny_perfect_count,perfect_count,near_count,miss_count)

url = os.environ["host"]
token = os.environ["token"]
usercode = os.environ["usercode"]
app = Flask(__name__)
handler = ArcBot(url,token)

@app.route("/")
def index():
    svg = handler.generate_recent_svg(usercode)
    return app.response_class(svg,mimetype="image/svg+xml")

if __name__ == "__main__":
    app.run()
