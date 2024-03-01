
couch = {
    "name": "couch",
    "type": "furniture",
}

door_a = {
    "name": "door a",
    "type": "door",
}
door_d = {
    "name": "door d",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

piano = {
    "name": "piano",
    "type": "furniture",
}

game_room = {
    "name": "game room",
    "type": "room",
}

outside = {
  "name": "outside"
}

bedroom_1= {
    "name": "bedroom 1",
    "type":"room",
}

queen_bed= {
    "name": "Queen Bed",
    "type":"furniture",
}

door_b = {
    "name": "door b",
    "type": "door",
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

door_c = {
    "name": "door c",
    "type": "door",
}

living_room= {
    "name": "living room",
    "type":"room",
} 

dining_table= {
    "name": "dining table",
    "type":"furniture",
}

bedroom_2 = {"name": "bedroom 2",
            "type": "room",
            }

double_bed = {"name": "double bed",
             "type" : "furniture",
             }
dresser = {"name" : "dresser",
          "type" : "furniture"}

key_c = {"name" : "Key to Door C",
        "type" : "key",
        "target": door_c,}
key_d = {"name" : "Key to Door D",
        "type" : "key",
        "target": door_d,}

all_rooms = [game_room, bedroom_1,bedroom_2, living_room, outside]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related

object_relations = {
    "game room": [couch, piano, door_a],
    "piano": [key_a],
    "outside": [door_a],
    "door a": [game_room, bedroom_1],
    "double bed" : [key_c],
    "dresser" : [key_d],
    "door b" : [bedroom_1, bedroom_2],
    "bedroom 1" : [door_a, queen_bed,door_b, door_c],
    "bedroom 2": [door_b, double_bed, dresser],
    "living room": [door_d,dining_table],
    "door d": [living_room, outside],
    "queen bed": [key_b],
    "door c":[bedroom_1,living_room],
}


INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside}

import random
from pygame import mixer

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"])

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        
        print("Congrats! You escaped the room!\n\n")
        print("""""
                             ,@@@@@@@,
       ,,,.   ,@@@@@@/@@,  .oo8888o.
    ,&%%&%&&%,@@@@@/@@@@@@,8888\88/8o
   ,%&\%&&%&&%,@@@\@@@/@@@88\88888/88'
   %&&%&%&/%&&%@@\@@/ /@@@88888\88888'
   %&&%/ %&%%&&@@\ V /@@' `88\8 `/88'
   `&%\ ` /%&'    |.|        \ '|8'
       |o|        | |         | |
       |.|        | |         | |
jgs \\/ ._\//_/__/  ,\_//__\\/.  \_//__/_
              """)
        mixer.init()
        mixer.music.load("sounds/outside.mp3")
        mixer.music.play()
    else:
        print("You are now in " + room["name"] + "\n")
        intended_action = input("What would you like to do? Type 'explore' or 'examine'? ").strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine? ").strip())
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()

def encounter_joker():

    print("You encounter the joker! He wants to kill you!\n")
   
    random_number = random.randint(1, 10)
    if random_number <= 7:
        print("You defeated the joker and you continue playing!" )
        return "win"
    else:
        print(f"The joker defeats you. He pushes you back.")
        return "lose"

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items) + "\n\n")

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    for item in object_relations[current_room["name"]]:
        if(item["name"].lower() == item_name.lower()):
            output = "You examine " + item_name + ".\n"
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have.\n"
                    next_room = get_next_room_of_door(item, current_room)
                    mixer.init()
                    mixer.music.load("sounds/squeaky_door.mp3")
                    mixer.music.play()
                    print(""" ______________
|\ ___________ /|
| |  /|,| |   | |
| | |,x,| |   | |
| | |,x,' |   | |
| | |,x   ,   | |
| | |/    |%==| |
| |    /] ,   | |
| |   [/ ()   | |
| |       |   | |
| |       |   | |
| |       |   | |
| |      ,'   | |
| |   ,'      | |
|_|,'_________|_| )""")
                else:
                    output += "It is locked but you don't have the key.\n"
            elif(item["type"] == "furniture"):
                if(item["name"].lower() == "queen bed"):
                    output += """You examine the Queen Bed.\n
           
            ___
        ,-""___""-.
       .;""'| |`"":.
       || | | | | ||
       ||_|_|_|_|_||
      //          /|
     /__         //|
 ,-""___""-.    //||
.;""'| |`"":.  //
||/| | | | || //
||_|_|_|_|_||//
||_________||/
||         ||
''         ''"""
                    output += "You lift the pillow and find the a key underneath it..\n\n" """
                        8 8          ,o.                                              
                       d8o8azzzzzzzzd   b                                      
                                     `o'                                       
                                                  """
                    mixer.init()
                    mixer.music.load("sounds/found.mp3")
                    mixer.music.play() 
                    key_found = key_b  
                    game_state["keys_collected"].append(key_found)
                    output += f"You found {key_found['name']}.\n"
                elif(item["name"] == "piano"):
                    output += "Here's a riddle for you:\n"
                    output += "Named after a snake, but not found in the wild,\n"
                    output += "My syntax and features leave programmers beguiled.\n"
                    output += "From data manipulation to web development's reign,\n"
                    output += """In the coding world, I effortlessly sustain.\n
          _ _ _
      _ -       - _ _ _ _ _
  _ -                       \\
 -                     _  -||
|                _  -       ||
|          _  -        \     ||
|    _  -                    \||
|_-_______________________________\\
|                                  |
|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
||----------------------------------|   
||              || ||              ||
[]              `UUU'              []"""
                    print(output)  
                    answer = input("What am I? ").strip().lower()
                    if answer == "python":
                        output = "Correct! You found the key to door a..\n\n" """
                        8 8          ,o.                                              
                       d8o8azzzzzzzzd   b                                      
                                     `o'                                       
                                                  """
                        mixer.init()
                        mixer.music.load("sounds/found.mp3")
                        mixer.music.play() 
                        item_found = object_relations[item["name"]].pop()
                        game_state["keys_collected"].append(item_found)     
                    else:
                        output = "Incorrect answer. You continue exploring the room.\n"
                elif item["name"].lower() == "double bed":
                    output += "Here's a riddle for you:\n"
                    output += "I store key-value pairs, a treasure trove indeed,\n"
                    output += "Accessing information with remarkable speed.\n"
                    output += "Whether words or numbers, I hold them with care,\n"
                    output += """In the world of programming, I'm quite rare.\n 
            ___
        ,-""___""-.
       .;""'| |`"":.
       || | | | | ||
       ||_|_|_|_|_||
      //          /|
     /__         //|
 ,-""___""-.    //||
.;""'| |`"":.  //
||/| | | | || //
||_|_|_|_|_||//
||_________||/
||         ||
''         ''"""""
                    print(output)
                    answer = input("What am I? ").strip().lower()
                    if answer == "function":
                        output += "Correct! You found the key to door c..\n\n" """
                        8 8          ,o.                                              
                       d8o8azzzzzzzzd   b                                      
                                     `o'                                       
                                                  """
                        mixer.init()
                        mixer.music.load("sounds/found.mp3")
                        mixer.music.play()
                        item_found = object_relations[item["name"]].pop()
                        game_state["keys_collected"].append(item_found)  
                    else:
                        output += "Incorrect answer. You continue exploring the room.\n"
                elif item["name"] == "dresser":
                    output += "Here's a riddle for you:\n"
                    output += """I am a delicious way of representing data.
     __________
   /          /|
 /__________/  |
 |________ |   |
 /_____  /||   |    
|".___."| ||   |
|_______|/ |   |
 || .___."||  /
 ||_______|| /
 |_________|/ """
                    print(output)
                    answer = input("What am I? ").strip().lower()
                    if answer == "pie chart":
                        output += "Correct! You found the key to door d..\n\n" """
                        8 8          ,o.                                              
                       d8o8azzzzzzzzd   b                                      
                                     `o'                                       
                                                  """
                        mixer.init()
                        mixer.music.load("sounds/found.mp3")
                        mixer.music.play()
                        item_found = object_relations[item["name"]].pop()
                        game_state["keys_collected"].append(item_found)
                else:
                    output += f"You examine the {item['name']}. There isn't anything interesting about it.\n"
                break
                
    if not output:
        output = "The item you requested is not found in the current room.\n"
    
    print(output)
    
    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        result = encounter_joker()
        mixer.init()
        mixer.music.load("sounds/joker.mp3")
        mixer.music.play()
        if result == "win":
            play_room(next_room)
        else:
            play_room(current_room)
            
    else:
        play_room(current_room)

game_state = INIT_GAME_STATE.copy()

start_game()