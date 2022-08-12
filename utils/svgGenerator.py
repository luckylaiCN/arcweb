import os
import base64

file_dir = os.path.dirname(os.path.abspath(__file__))
mod_svg_path = os.path.join(file_dir,"mod.svg")
with open(mod_svg_path) as f:
    mod_svg = f.read()

rating_keys = ["0","1","2","3","4","5","6","7","off"]
rating_frames = {}
for key in rating_keys:
    with open(os.path.join(file_dir,"ptt",f"rating_{key}.png"),"rb") as f:
        rating_frames[key] = base64.b64encode(f.read()).decode()

def get_rating(ptt):
    if ptt == -1:
        return "off"
    ptt /= 100
    if ptt < 3:
        return "0"
    elif 3 <= ptt < 7:
        return "1"
    elif 7 <= ptt < 10:
        return "2"
    elif 10 <= ptt < 11:
        return "3"
    elif 11 <= ptt < 12:
        return "4"
    elif 12 <= ptt < 12.5:
        return "5"
    elif 12.5 <= ptt < 13:
        return "6"
    else:
        return "7"

def get_difficulty(diff):
    if diff < 9:
        return str(int(diff))
    elif int(diff * 10) % 10 >= 7:
        return str(int(diff))+'+'
    else :
        return str(int(diff))


def get_score_formatted(score):
    full = str(score).rjust(8,'0')[-8:]
    return f"{full[:2]}'{full[2:5]}'{full[5:8]}"

def gen_svg(illustration_base64,ptt,username,score,songName,difficulty,difficulty_level,shiny_perfect_count,perfect_count,near_count,miss_count):
    result = mod_svg.format(
        illustration = "data:image/jpeg;base64," + illustration_base64,
        ratingFrame = "data:image/png;base64," + rating_frames[get_rating(ptt)],
        ratingScore = "" if ptt==-1 else str(format("%.2f"%(ptt/100))),
        username = username,
        Score = get_score_formatted(score),
        songName = songName,
        difficulty = f"{difficulty} {get_difficulty(difficulty_level)}",
        pureCount = f"{perfect_count}(+{shiny_perfect_count})",  
        farCount = near_count,
        lostCount = miss_count,
    )
    return result
