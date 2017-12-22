import json

with open('player.json') as file:
    player = json.load(file)
    print (player) 
    print ("Player's name = ",player["name"])

with open('warriors_player.json', "w") as file:
    player = {}
    player["name"] = "Curry"
    player["age"] = 28
    player["championship"] = [2014, 2016]
    json.dump(player, file, indent=4)