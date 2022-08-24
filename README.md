# **Arcweb**

An svg score generator in arcaea


## Routes

| route | arg                  | interface            | example                       |
| ----- | -------------------- | -------------------- | ----------------------------- |
| /     | -                    | recently played song | /                             |
| /best | song and difficulty* | best score           | /best?song=nhelv&difficulty=1 |

```
*song is for songid in arcaea , can be found in songlist
*difficulty is for short name or full name of difficulties
	 "future" "ftr" "2" are acceptable
```

## Deploy to vercel

Fork this repository and import it from [vercel](https://vercel.com/)

![img](guide/ConfigureProject.png)

Then configure your project:

Set `FRAMEWORK PRESET` to `Other`

Add `Environment Variables`

```
host = "xxxxxx" # for ArcaeaUnlimitedApi
token = "xxxxxx" # for ArcaeaUnlimitedApi
usercode = "xxxxxx" # your user code in Arcaea
timezone = "xxxxxx" # [optional] Asia/Shanghai for default
```

Click `Deploy `and wait for building
