key_A = { "type": "key", "name": "yellow" }
key_B = { "type": "key", "name": "pink" }
key_C = { "type": "key", "name": "blue" }
key_D = { "type": "key", "name": "green" }

door_A = { "type": "item", "name": "yellow door", "description": "", "keys": [] }
door_B = { "type": "item", "name": "pink door", "description": "", "keys": []  }
door_C = { "type": "item", "name": "blue door", "description": "", "keys": []  }
door_D = { "type": "item", "name": "green door", "description": "", "keys": []  }

item_couch = { "type": "item", "name": "couch", "keys": [], "description": "There's a funky smelling couch... You can only find a cat toy underneath it." }
item_piano = { "type": "item", "name": "piano", "keys": [key_A], "description": "A grand piano with a yellow key inside of it!" }
item_queen_bed = { "type": "item", "name": "queen bed", "keys": [key_B], "description": "A cozy queen bed. Underneath it you find a box with a small pink key inside of it!" }
item_double_bed = { "type": "item", "name": "double bed", "keys": [key_C], "description": "A spacious double bed. Inside of the pillowcase you see the ouline of a key... it's a blue key!" }
item_dresser = { "type": "item", "name": "dresser", "keys": [key_D], "description": "You can see a small dresser with some clothes inside of it and an antique-looking green key hidden in the second drawer."}
item_dining_table = { "type": "item", "name": "dining table", "keys": [], "description": "A large dining table with a runner on top of it." }

room_game = { "type": "room", "name": "Game Room", "items": [item_couch, item_piano, door_A], "doors": [] }
room_bedroom_1 = { "type": "room", "name": "Bedroom 1", "items": [item_queen_bed, door_A, door_B, door_C], "doors": [] }
room_bedroom_2 = { "type": "room", "name": "Bedroom 2", "items": [item_double_bed, item_dresser, door_B], "doors": [] }
room_living_room = { "type": "room", "name": "Living Room", "items": [item_dining_table, door_C, door_D], "doors": [] }
room_outside = { "type": "room", "name": "Outside", "items": [], "doors": [] }

room_transitions = {
    "yellow door": [
        { "key": key_A, "from": room_game, "to": room_bedroom_1 },
        { "key": key_A, "from": room_bedroom_1, "to": room_game }
    ],
    "pink door": [
        { "key": key_B, "from": room_bedroom_1, "to": room_bedroom_2 },
        { "key": key_B, "from": room_bedroom_2, "to": room_bedroom_1 }
    ],
    "blue door": [
        { "key": key_C, "from": room_bedroom_1, "to": room_living_room },
        { "key": key_C, "from": room_living_room, "to": room_bedroom_1 }
    ],
    "green door": [
        { "key": key_D, "from": room_living_room, "to": room_outside },
        { "key": key_D, "from": room_outside, "to": room_living_room }
    ]
}

game_state = { "current_room": room_game, "inventory": [], "target_room": room_outside }

def wait_for_choice(info, error = "Invalid choice", choices = [item['name'] for item in game_state["current_room"]["items"]]):
    while True:
        choice = input(f"{info} ({', '.join(choices)}) ").strip().lower()
        if choice in choices: return choice
        else: print(error)

def examine_item(item):

    """
    The examine_item(item) function allows the player to examine a specific item in the room.
    It prints the description of the item and, if the item contains any keys,
    it adds them to the player's inventory and informs the player of this.
    """
    # print description of the item
    print(f"You examine the {item['name']}.")
    if "door" in item['name'].lower(): open_door(item)
    else: print(f"{item['description']}")

    # add key to inventory
    for key in item["keys"]:
        if key not in game_state["inventory"]:
            print(f"A {key['name']} {key['type']} has been added to your inventory.")
            game_state["inventory"].append(key)

def examine_item_prompt():
    """

    """
    # accepts choice of item player wants to examine
    item_names = [item["name"] for item in game_state["current_room"]["items"]]
    item_choice = wait_for_choice("Which item would you like to examine?", "Uh oh. You must be confused. Please choose between the items in the room.", item_names)

    # examine the chosen item
    for item in game_state["current_room"]["items"]:
        if item["name"] == item_choice: examine_item(item)

def open_door(door):

  """
  The open_door function attempts to open a door in the current room if the player has the required key.
  It checks the player’s inventory for a key that matches the door and ensures that the door can transition from the current room to another room.
  If the player has the correct key, they are moved to the connected room;
  otherwise, the function informs them that the door cannot be opened.
  Parameters:

  game_state (dictionary): The current state of the game, including the player's current room and their inventory.
  door (dictionary): The door the player is trying to open, containing details like its name (color).
  Returns: None (the function directly updates the game_state if the door is opened, or prints a message if not).

  """

  # check if a key in the inventory can transition from one room to the other
  for transition in room_transitions[door["name"]]:
    if transition["key"] in game_state["inventory"] and transition["from"] == game_state["current_room"]:
        game_state["current_room"] = transition["to"]
        print(f"You open the door and enter {game_state['current_room']['name']}.")
        return
  print("You can't open that door.")

def start():
    # prompt the player with yes/no to ask whether they want to continue playing
    """
    The start() function initializes the Escape Room game. It begins by prompting the player with a yes/no choice to
    confirm if they want to play the game. If they choose "no," the game ends immediately.
    If they choose "yes,", player is automatically exploring the room and the main game loop starts to ask
    the player to examine items or doors until they successfully exit the house and win the game.
    """
    start = wait_for_choice("Welcome to the Escape Room Game! Do you want to start playing?", "I'm sorry, I didn't understand that. Please answer with 'yes' or 'no'.", ["yes", "no"])
    if start == "no":
        print("Alright. Bye!")
        return

    print("Suddenly, you find yourself waking up on an unfamiliar couch, in an eerie house devoid of windows.\nYour memory fails to provide any explanation about how you ended up here, or what transpired previously. You can sense an imminent threat lurking somewhere - your gut tells you to escape the house immediately!\nYou look around and realize you’re in a game room.\n\n'What should I do?' you ponder.")
    # main game loop: keep asking for input until the player reaches outside
    while game_state["current_room"] != room_outside:
        item_names = [item['name'] for item in game_state["current_room"]["items"]]
        print(f"You are in the {game_state['current_room']['name']}.\nHere you can see the following items: {', '.join(item_names)}.")
        examine_item_prompt()

    print("Congratulations! You have escaped the room!")

try:
    start()
except KeyboardInterrupt:
    print("\n\nGoodbye! Thanks for playing!")
