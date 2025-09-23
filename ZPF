import os
import platform
import random
import time
from colorama import Fore, Style, init
init(autoreset=True)

# ----------------------------
# Utility
# ----------------------------
def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def slow_print(text, delay=0.02):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def choose(prompt, options):
    while True:
        slow_print(prompt)
        for key, desc in options.items():
            slow_print(f"[{key}] {desc}")
        choice = input("> ").strip().lower()
        clear_screen()
        if choice in options:
            return choice
        slow_print("Invalid entry.")

# ----------------------------
# Data
# ----------------------------
LOCATIONS = ["Forest", "Lake", "Nuclear Plant", "Shack"]

# Fishing species pools by category (merged/extended from C++)
FISH_POOLS = {
    "common": [
        "Catfish", "Smallmouth Bass", "Crappie", "Bluegill", "Sunfish"
    ],
    "rare": [
        "Largemouth Bass", "Walleye", "Gar", "Pike", "Turtle",
        "Mutant Catfish", "Brook Trout"
    ],
    "epic": [
        "Sturgeon", "Paddlefish", "Brown Trout", "Muskellunge"
    ],
    "legendary": [
        "Zombie Fish", "Mighty Bluegill"
    ],
}

# Weapon shop (name, weapon_mod_damage, cost)
WEAPONS = [
    ("Knife", 1, 5),
    ("Machete", 2, 10),
    ("Axe", 3, 20),
    ("Pistol", 4, 40),
    ("SMG", 5, 80),
    ("Shotgun", 6, 100),
    ("AR-15", 7, 160),
    ("Sniper", 8, 200),
    ("Brass Knuckles", 9, 250),
    ("Spiked Bat", 10, 400),
]

# Rod shop (name, rod_luck, cost)
RODS = [
    ("Common Rod", 1, 5),
    ("Sturdy Rod", 2, 20),
    ("Premium Rod", 3, 50),
    ("Deep Sea Rod", 4, 100),
    ("Jody Barrs Rod", 5, 250),
]

# Armor / consumables (name, type, value, cost)
ARMOR = [
    ("Medkit", "heal", 2, 5),
    ("Nurse Aimees Power Kit", "fullheal", 0, 25),
    ("Ollies Leather Coat", "maxhp", 1, 50),
    ("Tactical Kerpants", "maxhp", 2, 100),
    ("Clemuratan Helmet", "maxhp", 3, 150),
]

FOOD = [
    ("Sage Cookies", 2, 6),
    ("Mrs Sierras Pasta", 4, 10),
    ("Chicky-fi-laa", 6, 16),
    ("Missy's Cookbook", "cookbook", 50),  # sets cookbook flag
]

# Sell values per category (C++ update)
SELL_VALUES = {
    "common": 3,
    "rare": 5,
    "epic": 7,
    "legendary": 18,
}

# Crafting per C++ update: (name, wood, stone, parts, weapon_mod or None, isBoat)
CRAFT = [
    ("Knife",       2,  3,  0, 1, False),
    ("Machete",     3,  7,  0, 2, False),
    ("Pistol",      5, 10, 10, 4, False),
    ("SMG",        10, 15, 15, 6, False),
    ("Shotgun",    15, 20, 20, 7, False),
    ("Boat",       75, 50, 20, None, True),
]

# ----------------------------
# Player
# ----------------------------
class Player:
    def __init__(self):
        # Core stats
        self.max_health = 8
        self.health = 8
        self.hunger = 10

        # Stat system (split into base + gear mods)
        self.base_luck = 0
        self.rod_luck = 0      # from rod
        self.base_damage = 1
        self.weapon_mod = 0    # from weapon

        # Economy & resources
        self.money = 10
        self.wood = 0
        self.stone = 0
        self.machineparts = 0

        # Gear / Inventory
        self.fishingrod = "Stick And String"
        self.weapon = "Fists"
        self.armor_items = []
        self.fish_list = []  # list of fish names
        self.fish_counts = {"common": 0, "rare": 0, "epic": 0, "legendary": 0}

        # Flags
        self.cookbook = False
        self.name = ""
        self.location = "Forest"
        self.turns = 0
        self.hasboat = False

    @property
    def total_luck(self):
        return self.base_luck + self.rod_luck

    @property
    def total_damage(self):
        return self.base_damage + self.weapon_mod

    def stats(self):
        print(f"\nNAME: {self.name}")
        print(f"HEALTH: {self.health}/{self.max_health}")
        print(f"DAMAGE: {self.total_damage} (base {self.base_damage} + weapon {self.weapon_mod})")
        print(f"LUCK: {self.total_luck} (base {self.base_luck} + rod {self.rod_luck})")
        print(f"HUNGER: {self.hunger}")
        print(f"MONEY: {self.money}")
        print(f"WOOD: {self.wood}")
        print(f"STONE: {self.stone}")
        print(f"MACHINE PARTS: {self.machineparts}")
        print(f"FISHING ROD: {self.fishingrod}")
        print(f"WEAPON: {self.weapon}")
        print(f"ARMOR: {', '.join(self.armor_items) if self.armor_items else 'None'}")
        print(f"FISH: {', '.join(self.fish_list) if self.fish_list else 'None'}\n")

    def update_stats(self):
        self.hunger = min(self.hunger, 10)
        self.health = min(self.health, self.max_health)
        if self.hunger < 0:
            self.hunger = 0
            self.health -= 1
            slow_print("You are starving! -1 HP")

# ----------------------------
# Character creation
# ----------------------------
def character_creation(player: Player):
    slow_print("\nWelcome to Zombie Pro Fisher - Byte Sized!")
    time.sleep(1)
    slow_print("\n--- Character Customization ---\n")

    eye = choose("Choose eye color:", {
        "1": "Blue (+2 luck)",
        "2": "Brown (+1 damage)",
        "3": "Green (+2 max health)"
    })
    if eye == "1": player.base_luck += 2
    elif eye == "2": player.base_damage += 1
    elif eye == "3": player.max_health += 2

    hair = choose("Choose hair color:", {
        "1": "Blonde (+2 luck)",
        "2": "Brown (+1 damage)",
        "3": "Black (+2 max health)"
    })
    if hair == "1": player.base_luck += 2
    elif hair == "2": player.base_damage += 1
    elif hair == "3": player.max_health += 2

    size = choose("Choose size:", {
        "1": "Short (+2 luck)",
        "2": "Tall (+1 damage)",
        "3": "Medium (+2 max health)"
    })
    if size == "1": player.base_luck += 2
    elif size == "2": player.base_damage += 1
    elif size == "3": player.max_health += 2

    player.name = input("Now, what is your hero's name? ")
    player.health = player.max_health

    slow_print("\nStarting your journey now! Here are your stats:")
    player.stats()

    player.location = random.choice(LOCATIONS)
    slow_print("\nSPAWNING CHARACTER...")
    time.sleep(2)
    slow_print(f"You arrive at the {player.location.upper()}.")

# ----------------------------
# Encounters / Actions
# ----------------------------
def zombie_encounter(player: Player):
    if player.location == "Shack":
        return False

    spawn_roll = random.randint(0, 10)
    risky = (spawn_roll >= 9 and player.location != "Shack") or (spawn_roll >= 6 and player.location == "Nuclear Plant")
    if not risky:
        return False

    zombie_hp = random.randint(5, 15)
    slow_print("\nZOMBIE ENCOUNTER!")
    while zombie_hp > 0 and player.health > 0:
        print(f"Zombie HP: {zombie_hp} | Your HP: {player.health}")
        action = choose("What do you do?", {"1": "Attack", "2": "Run away"})
        if action == "1":
            dmg = random.randint(0, 4) + player.total_damage
            slow_print(f"You hit the zombie for {dmg}!")
            zombie_hp -= dmg
            if zombie_hp <= 0:
                reward = random.randint(1, 15)
                slow_print(f"You killed the zombie! You got ${reward}.")
                player.money += reward
                break
            z_dmg = random.randint(0, 8)
            slow_print(f"The zombie hits you for {z_dmg}!")
            player.health -= z_dmg
        else:
            escape = random.randint(0, 20) + int(player.total_luck * 1.5)
            if escape >= 12:
                slow_print("You successfully got away!")
                break
            else:
                slow_print("The zombie caught up to you!")
                z_dmg = random.randint(0, 5)
                slow_print(f"The zombie hits you for {z_dmg}!")
                player.health -= z_dmg

    if player.health <= 0:
        weeks = player.turns // 7
        days = player.turns % 7
        slow_print(f"\nYOU DIED\nYou lasted {weeks} week(s) and {days} day(s). ({player.turns} turns). Not bad!")
        return True
    return False

def forage(player: Player):
    if player.location == "Nuclear Plant":
        slow_print("You're not sure there's anything safe to eat here...")
        # Stranger (Hudson) encounter (as per C++ flow)
        if random.randint(0, 10) == 5:
            slow_print("\nYou search through the maze of Seqouyah Power Plant.")
            slow_print("Upon approaching a janitor's closet, you hear someone.")
            slow_print("You carefully open the door. To your surprise, it's a man in withered clothes.")
            slow_print("His eyes are bloodshot and his hair grows in patches. He shivers and stares you in the eyes.")

            c1 = choose("STRANGER: A-Are you here... for... for me...?", {
                "1": "Who are you?",
                "2": "What are you doing here?",
                "3": "Kill it."
            })
            if c1 == "3":
                slow_print("Without a second thought you put an end to the hoodlum's life. +$10")
                player.money += 10
                return
            if c1 == "1":
                slow_print("STRANGER: Ker... ker something... Kerhuddy? Krudson? It's been... so long. I was looking for the code!")
            else:
                slow_print("STRANGER: I came after the meltdown. It's all gone. The code. The numbers. They were supposed to be here!")

            c2 = choose("What do you do?", {
                "1": "Code?",
                "2": "So where is it?",
                "3": "Kill him."
            })
            if c2 == "3":
                slow_print("Without a second thought you put an end to the hoodlum's life. +$10")
                player.money += 10
                return
            if c2 == "1":
                slow_print("STRANGER: Hahaha! The code! But, of course, you can't see it. You're not awakened!")
            else:
                slow_print("STRANGER: Hahaha! You think you're worthy of finding it? The eyes of the unawakened will NEVER find it! NEVER!")

            c3 = choose("What do you do?", {
                "1": "How do I become... awakened?",
                "2": "Good luck on your search.",
                "3": "Enough of this. Kill him."
            })
            if c3 == "3":
                slow_print("Without a second thought you put an end to the hoodlum's life. +$10")
                player.money += 10
                return
            if c3 == "2":
                slow_print("STRANGER: I-Its here... somewhere! The code! Hahaha!")
                return

            # Milk / Sugar
            final_choice = choose("Choose:", {"1": "The milk.", "2": "The sugar."})
            if final_choice == "1":
                slow_print("You choke down a vial of solid white liquid. Your vision blurs... you feel... awakened.")
                slow_print("Luck +5, Damage +2")
                player.base_luck += 5
                player.base_damage += 2
            else:
                slow_print("You sniff a bag of harsh white powder. Your eyes burn... yet you feel... awakened.")
                slow_print("Luck +2, Damage +5")
                player.base_luck += 2
                player.base_damage += 5
        return

    if player.location == "Shack":
        slow_print("Mr. Hutchinson tells you to stop snooping around in his shop.")
        return

    # Normal forage (C++ thresholds w/ cookbook effect)
    player.hunger -= 1
    result = random.randint(-10, 32) + int(player.total_luck * 1.8)
    if result <= 0:
        slow_print("You found nothing.")
    elif (1 <= result <= 10 and not player.cookbook) or (0 <= result <= 5 and player.cookbook):
        hp_loss = random.randint(1, 3)
        player.health -= hp_loss
        slow_print(f"Yuck! You ate something you shouldn't have. -{hp_loss} HP.")
    elif (11 <= result <= 20 and not player.cookbook) or (6 <= result <= 20 and player.cookbook):
        slow_print("You found some nuts and berries. +2 Hunger")
        player.hunger += 2
    elif 21 <= result <= 25:
        slow_print("You're not sure what you found, but the geiger counter didn't beep. +3 Hunger.")
        player.hunger += 3
    elif 26 <= result <= 30:
        slow_print("You trapped some local fauna and ate a well-cooked meal. +4 Hunger.")
        player.hunger += 4
    elif 31 <= result <= 40:
        slow_print("You found unexpired canned food. +5 Hunger.")
        player.hunger += 5

def fishing(player: Player):
    # C++-style fishing: 0..95 + total_luck*2.5
    player.hunger -= 1
    roll = random.randint(0, 95) + int(player.total_luck * 2.5)

    if roll <= 40:
        slow_print("You didn't catch any fish today...")
        return
    elif 41 <= roll <= 70:
        category = "common"
    elif 71 <= roll <= 85:
        category = "rare"
    elif 86 <= roll <= 95:
        category = "epic"
    else:  # >=96
        category = "legendary"

    species = random.choice(FISH_POOLS[category])
    slow_print(f"You caught a {species}!")
    player.fish_list.append(species)
    player.fish_counts[category] += 1

def gather(player: Player, resource: str):
    amount = random.randint(0, 5)
    slow_print(f"You gathered {amount} pieces of {resource}.")
    if resource == "wood":
        player.wood += amount
    elif resource == "stone":
        player.stone += amount
    elif resource == "machinery":
        player.machineparts += amount
    player.hunger -= 1

# ----------------------------
# Shop (overhauled)
# ----------------------------
def shop(player: Player):
    hutchinson_dialogues = [
        "It's good to see a friendly face. Here's my shop.",
        "Welcome back, old timer!",
        f"Hittin' the lakes already, are we {player.name}?",
        f"Ahh, {player.name}, glad to see you're safe and well!",
        "My tackle is the best in town! Glad the youngins are getting into the spirit of fishing!"
    ]
    slow_print(f"Mr Hutchinson greets you with a warm nod and a gruffy smile. {random.choice(hutchinson_dialogues)}")

    while True:
        action = choose("What would you like to do?", {
            "1": "Buy weapons",
            "2": "Buy/sell fishing goods",
            "3": "Armor Shop",
            "4": "Craft",
            "5": "Sage Snack Shack",
            "6": "Goodbye"
        })

        # Weapons
        if action == "1":
            slow_print("WEAPON SHOP:")
            for idx, (name, mod, cost) in enumerate(WEAPONS, start=1):
                slow_print(f"[{idx}] {name:<22} +{mod} DMG  - ${cost}")
            slow_print(f"[0] Go Back")
            choice = input("> ").strip()
            if choice == "0":
                continue
            try:
                i = int(choice) - 1
                name, mod, cost = WEAPONS[i]
            except:
                slow_print("Invalid choice.")
                continue
            if player.money >= cost:
                player.weapon = name
                player.weapon_mod = mod
                player.money -= cost
                slow_print(f"You bought {player.weapon}! (Weapon mod +{mod})")
            else:
                slow_print("Not enough money.")

        # Fishing goods
        elif action == "2":
            # compute cashout
            cc = player.fish_counts
            total_cash = (
                cc["common"] * SELL_VALUES["common"] +
                cc["rare"] * SELL_VALUES["rare"] +
                cc["epic"] * SELL_VALUES["epic"] +
                cc["legendary"] * SELL_VALUES["legendary"]
            )
            slow_print("FISHING GOODS:")
            for idx, (name, rluck, cost) in enumerate(RODS, start=1):
                slow_print(f"[{idx}] {name:<18} +{rluck} Luck - ${cost}")
            slow_print(f"[s] Sell your fish (+${total_cash})")
            slow_print("[0] Goodbye")
            slow_print(f"You currently have: {', '.join(player.fish_list) if player.fish_list else 'None'}")

            choice = input("> ").strip().lower()
            if choice == "0":
                continue
            elif choice == "s":
                if player.fish_list:
                    player.money += total_cash
                    slow_print(f"MR. HUTCHINSON: Nice work! You made ${total_cash} for this sale!")
                    player.fish_list.clear()
                    for k in player.fish_counts:
                        player.fish_counts[k] = 0
                else:
                    slow_print("You have no fish to sell.")
            else:
                try:
                    i = int(choice) - 1
                    name, rluck, cost = RODS[i]
                except:
                    slow_print("Invalid choice.")
                    continue
                if player.money >= cost:
                    player.fishingrod = name
                    player.rod_luck = rluck
                    player.money -= cost
                    slow_print(f"You bought {player.fishingrod}! (Rod luck +{rluck})")
                else:
                    slow_print("Not enough money.")

        # Armor
        elif action == "3":
            slow_print("ARMOR AND PROTECTION:")
            for idx, (name, typ, value, cost) in enumerate(ARMOR, start=1):
                if typ == "heal": desc = f"Restore {value} HP"
                elif typ == "fullheal": desc = "Restore full HP"
                else: desc = f"+{value} Max HP"
                slow_print(f"[{idx}] {name:<25} {desc:<18} - ${cost}")
            slow_print("[0] Goodbye")

            choice = input("> ").strip()
            if choice == "0":
                continue
            try:
                i = int(choice) - 1
                name, typ, val, cost = ARMOR[i]
            except:
                slow_print("Invalid choice.")
                continue
            if player.money < cost:
                slow_print("Not enough money.")
                continue

            if typ == "heal":
                player.health = min(player.health + val, player.max_health)
            elif typ == "fullheal":
                player.health = player.max_health
            elif typ == "maxhp":
                player.max_health += val
                player.health += val
                player.armor_items.append(name)
            player.money -= cost
            slow_print(f"You bought {name}!")

        # Craft (C++ costs)
        elif action == "4":
            slow_print("CRAFTABLE ITEMS:")
            for idx, (name, w, s, p, mod, isBoat) in enumerate(CRAFT, start=1):
                if isBoat:
                    slow_print(f"[{idx}] {name:<10} {w} wood, {s} stone, {p} machine parts")
                else:
                    slow_print(f"[{idx}] {name:<10} {w} wood, {s} stone, {p} machine parts  -> +{mod} DMG")
            slow_print("[0] Goodbye")
            choice = input("> ").strip()
            if choice == "0":
                continue
            try:
                i = int(choice) - 1
                name, w, s, p, mod, isBoat = CRAFT[i]
            except:
                slow_print("Invalid choice.")
                continue

            if player.wood >= w and player.stone >= s and player.machineparts >= p:
                player.wood -= w
                player.stone -= s
                player.machineparts -= p
                if isBoat:
                    player.hasboat = True
                    slow_print("Distant horizons draw near. You've crafted a boat!")
                else:
                    player.weapon = name
                    player.weapon_mod = mod
                    slow_print(f"You successfully crafted a {name}! (Weapon mod +{mod})")
            else:
                slow_print("Not enough resources to craft that.")

        # Food
        elif action == "5":
            slow_print("SAGE SNACK SHACK:")
            for idx, (name, val, cost) in enumerate(FOOD, start=1):
                if name == "Missy's Cookbook":
                    desc = "Lessens chance of foraging poisonous food"
                    slow_print(f"[{idx}] {name:<22} {desc} - ${cost}")
                else:
                    slow_print(f"[{idx}] {name:<22} +{val} Hunger - ${cost}")
            slow_print("[0] Goodbye")

            choice = input("> ").strip()
            if choice == "0":
                continue
            try:
                i = int(choice) - 1
                name, val, cost = FOOD[i]
            except:
                slow_print("Invalid choice.")
                continue
            if player.money < cost:
                slow_print("Not enough money.")
                continue
            if name == "Missy's Cookbook":
                player.cookbook = True
            else:
                player.hunger += val
            player.money -= cost
            slow_print(f"You bought {name}!")

        else:
            slow_print("MR HUTCHINSON: Thanks for checking out my shop!")
            break

# ----------------------------
# Main loop
# ----------------------------
def main():
    player = Player()
    character_creation(player)

    while player.health > 0:
        player.turns += 1
        player.update_stats()

        if zombie_encounter(player):
            break

        print("\nWhat would you like to do?")
        options = {"1": "Forage", "2": "Change location", "3": "Check stats"}

        if player.location == "Forest":
            options.update({"4": "Gather wood", "5": "Watch birds"})
        elif player.location == "Lake":
            options.update({"4": "Go fishing", "5": "Gather rocks"})
            if player.hasboat:
                options.update({"6": "Sail away..."})
        elif player.location == "Nuclear Plant":
            options.update({"4": "Gather machine parts", "5": "Listen to echoes"})
        elif player.location == "Shack":
            options.update({"4": "Interact with Mr. Hutchinson", "5": "Rest by the fire"})

        choice = choose("Choose an action:", options)

        if choice == "1":
            forage(player)

        elif choice == "2":
            locs = {"1": "Forest", "2": "Lake", "3": "Nuclear Plant", "4": "Shack"}
            loc_choice = choose("Where would you like to go? Traveling is dangerous and takes time.", {
                "1": "FOREST", "2": "LAKE", "3": "NUCLEAR PLANT", "4": "SHACK"
            })
            newloc = locs[loc_choice]
            if newloc == player.location:
                slow_print("You can't travel to a place you're already at.")
            else:
                player.location = newloc
                slow_print(f"You travel to the {player.location}.")

        elif choice == "3":
            player.stats()

        elif choice == "4":
            if player.location == "Forest":
                gather(player, "wood")
            elif player.location == "Lake":
                fishing(player)
            elif player.location == "Nuclear Plant":
                gather(player, "machinery")
            elif player.location == "Shack":
                shop(player)

        elif choice == "5":
            if player.location == "Forest":
                event = random.randint(1, 4)
                if event == 1:
                    slow_print("The birds are lively today. +1 HP.")
                    player.health = min(player.health + 1, player.max_health)
                elif event == 2:
                    slow_print("There are only a few birds today. You find peace in solitude.")
                elif event == 3:
                    slow_print("No birds today. It's quiet and eerie. -1 Damage.")
                    player.base_damage = max(1, player.base_damage - 1)
                elif event == 4:
                    slow_print("You see large birds. +1 luck, -1 Hunger.")
                    player.base_luck += 1
                    player.hunger -= 1

            elif player.location == "Lake":
                gather(player, "stone")

            elif player.location == "Nuclear Plant":
                event = random.randint(1, 4)
                if event == 1:
                    slow_print("You hear the humming of a machine. It gives you hope. +1 HP.")
                    player.health = min(player.health + 1, player.max_health)
                elif event == 2:
                    slow_print("You hear water dripping in the dark corridors.")
                elif event == 3:
                    slow_print("You hear zombie screeches in the distant maze. It scares you.")
                    player.base_damage = max(1, player.base_damage - 1)
                elif event == 4:
                    slow_print("You hear metal drop in the distance. It's your lucky day. +$1.")
                    player.money += 1

            elif player.location == "Shack":
                slow_print("The fire reminds you of home.")

        elif choice == "6" and player.location == "Lake" and player.hasboat:
            slow_print("After weeks of survival...")
            b1 = choose("A) Board the boat...\nB) No -- your work here isn't finished.",
                        {"a": "Board the boat", "b": "Stay"})
            if b1 == "a":
                slow_print("...And many zombies slain...")
                b2 = choose("A) ...And set sail...\nB) No -- your work here isn't finished.",
                            {"a": "Set sail", "b": "Stay"})
                if b2 == "a":
                    slow_print("... You finally embark. As the ruins of Seqouyah fade into the distance and the calm wake splashes your hull, anywhere is better than here.")
                    weeks = player.turns // 7
                    days = player.turns % 7
                    slow_print(f"You escaped after surviving for {weeks} week(s) and {days} day(s). ({player.turns} turns). Congratulations!!")
                    return

    slow_print("\nGame Over. Thanks for playing!")

if __name__ == "__main__":
    main()
