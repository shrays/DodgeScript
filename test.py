
print('=======')
import requests
from requests.api import request
username = "Shrasfdsgd"
out = str(requests.get("https://api.mojang.com/users/profiles/minecraft/" + username).content)
print('out' + out)
if len(str(out)) == 3:
    print('yeet')
else:
    uuid = out[out.find("id\":") + 5:out.find("\"", out.find("id\":") + 5)]

    key = '324ddd0c-2350-435d-9610-eb4fd6f1ec9d'

    player = requests.get('https://api.hypixel.net/player?uuid=' + uuid + '&key=' + key).json()
    deaths = int(player["player"]["stats"]["Bedwars"]["final_deaths_bedwars"])
    kills = int(player["player"]["stats"]["Bedwars"]["final_kills_bedwars"])
    print(round(kills/deaths, 2))
#324ddd0c-2350-435d-9610-eb4fd6f1ec9d
#final_deaths_bedwars
#final_kills_bedwars
#four_four_final_deaths_bedwars