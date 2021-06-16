import json
from aiohttp import request

BASE = "https://www.codewars.com/api/v1/users/"


class Warrior:
    def __init__(self, data):
        content = json.loads(data)

        self.name = content["name"]
        self.username = content["username"]
        self.honor = content["honor"]
        self.clan = content["clan"]
        self.position = content["leaderboardPosition"]
        self.completed = content["codeChallenges"]["totalCompleted"]
        self.rank = content["ranks"]["overall"]["name"]
        print("[+] Obtained",self.username)


async def get_warrior(username):
    async with request("GET", f"https://www.codewars.com/api/v1/users/{username}") as res:

        if res.status == 200:
            print("[+]", res.status)
            bio = await res.text()
            return Warrior(bio)
        else:
            print("[-]", res.status)
