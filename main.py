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

# Fishing species pools by category
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
    ("Knife", 1, 5, False),
    ("Machete", 2, 10, False),
    ("Axe", 3, 20, False),
    ("Pistol", 4, 40, False),
    ("SMG", 5, 80, False),
    ("Shotgun", 6, 100, False),
    ("AR-15", 7, 160, False),
    ("Sniper", 8, 200, False),
    ("Brass Knuckles", 9, 250, False),
    ("Spiked Bat", 10, 400, False),
]

# Rod shop (name, rod_luck, cost)
RODS = [
    ("Common Rod", 1, 5, False),
    ("Sturdy Rod", 2, 20, False),
    ("Premium Rod", 3, 50, False),
    ("Deep Sea Rod", 4, 100, False),
    ("Jody Barrs Rod", 5, 250, True),
]

# Armor / consumables (name, type, value, cost)
ARMOR = [
    ("Medkit", "heal", 2, 5, False),
    ("Nurse Aimees Power Kit", "fullheal", 0, 25, False),
    ("Ollies Leather Coat", "maxhp", 1, 50, True),
    ("Tactical Kerpants", "maxhp", 2, 100, False),
    ("Clemuratan Helmet", "maxhp", 3, 150, False),
]

FOOD = [
    ("Sage Cookies", 2, 6, False),
    ("Mrs Sierras Pasta", 4, 10, False),
    ("Chicky-fi-laa", 6, 16, False),
    ("Missy's Cookbook", "cookbook", 50, True),  # sets cookbook flag
]

# Sell values per category
SELL_VALUES = {
    "common": 2.50,
    "rare": 5.00,
    "epic": 8.25,
    "legendary": 18.00,
}

# Crafting (name, wood, stone, machine parts, weapon_mod or None, isBoat)
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
        self.max_health = 10
        self.health = 10
        self.hunger = 10
        self.xp = 0

        # Attributes (max 10 each)
        self.grit = 0   #  +1.5 dodge per point
        self.muscle = 0  # +0.5 base damage per point
        self.nature = 0  # +0.5 foraging luck per point
        self.brains = 0  # +1.5% xp gain per point
        self.charm = 0  # +1.5% more money from fish sale per point

        # Class bonuses (only one can be true)
        self.is_scavenger = False #  +15% foraging luck
        self.is_angler    = False #  +10% fishing luck
        self.is_mechanic  = False #  -25% crafting resource costs
        self.is_hunter    = False #  +10% combat damage
        self.is_medic     = False #  Gauze heals 2–4 HP
        self.is_trader    = False #  +10% money from all sources
        self.is_brawler   = False #  +15 dodge chance
        self.is_farmer    = False #  +2 Hunger restored from foraging
        self.is_captain   = False #  +3 Skill points
        self.is_scientist = False #  +10% XP gain

        # Stat system (split into base + gear mods)
        self.base_luck = 0
        self.rod_luck = 0      # from rod
        self.base_damage = 1
        self.weapon_mod = 0    # from weapon
        self.dodge = 0
        self.dodge_mod = 0     # from armor

        # Economy & resources
        self.money = 10
        self.wood = 0
        self.stone = 0
        self.machineparts = 0
        self.xp_until_level = 10

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
    
    @property
    def total_dodge(self):
        return self.dodge + self.dodge_mod
    
    def statscore(self):
        print(f"\n{self.name}: HP {self.health}/{self.max_health} || HUNGER: {self.hunger} || XP: {self.xp}/{self.xp_until_level} || ${self.money}")
        print(f"LOCATION: {self.location} || DAY: {(self.turns // 3) + 1} || TIME: {['Morning', 'Noon', 'Night'][self.turns % 3]}")
        print("________________________________________________________________")

    def stats(self):
        print(f"\nNAME: {self.name}")
        print(f"HEALTH: {self.health}/{self.max_health}")
        print(f"DAMAGE: {self.total_damage} (base {self.base_damage} + weapon {self.weapon_mod})")
        print(f"LUCK: {self.total_luck} (base {self.base_luck} + rod {self.rod_luck})")
        print(f"HUNGER: {self.hunger}")
        print(f"XP: {self.xp}/{self.xp_until_level}")
        print(f"DODGE: {self.total_dodge} (base {self.dodge} + armor {self.dodge_mod})")
        print("\n--- ATTRIBUTES ---")
        print(f"GRIT: {self.grit} (+{self.grit * 1.5} Dodge)")
        print(f"MUSCLE: {self.muscle} (+{self.muscle * 0.5} Base Damage)")
        print(f"NATURE: {self.nature} (+{self.nature * 0.5} Foraging Luck)")
        print(f"BRAINS: {self.brains} (+{self.brains * 1.5}% XP Gain)")
        print(f"CHARM: {self.charm} (+{self.charm * 1.5}% Money Gain)")

    def inventory(self):
        print(f"MONEY: {self.money}")
        print(f"WOOD: {self.wood}")
        print(f"STONE: {self.stone}")
        print(f"MACHINE PARTS: {self.machineparts}")
        print(f"FISHING ROD: {self.fishingrod}")
        print(f"WEAPON: {self.weapon}")
        print(f"ARMOR: {', '.join(self.armor_items) if self.armor_items else 'None'}")
        print(f"FISH: {', '.join(self.fish_list) if self.fish_list else 'None'}\n")

    def almanac(self):
        print("\n--- FISH ALMANAC ---")
        for category, species in FISH_POOLS.items():
            print(f"\n{category.upper()} FISH:")
            for fish in species:
                caught = " (caught)" if fish in self.fish_list else ""
                print(f" - {fish}{caught}")
        print()
        print("\n--- ZOMBIE ALMANAC ---")
        for enemy in ENEMIES:
            abilities = []
            if enemy.is_buster: abilities.append("Explosive!")
            if enemy.is_grappler: abilities.append("Will Grapple!")
            ability_str = f" ({', '.join(abilities)})" if abilities else ""
            print(f" - {enemy.name}{ability_str}: HP {enemy.hp_min}-{enemy.hp_max}, DMG {enemy.dmg_min}-{enemy.dmg_max}, Dodge Target {enemy.dodge_target}, Flee DC {enemy.flee_dc}")



    def update_stats(self):
        self.hunger = min(self.hunger, 10)
        self.health = min(self.health, self.max_health)
        if self.hunger < 0:
            self.hunger = 0
            self.health -= 1
            slow_print("You are starving! -1 HP")


from dataclasses import dataclass
import random

@dataclass
class EnemyType:
    name: str
    hp_min: int
    hp_max: int
    dmg_min: int
    dmg_max: int
    reward_min: int
    reward_max: int
    dodge_target: int   
    flee_dc: int
      # --- special abilities ---
    is_buster: bool = False
    is_grappler: bool = False

ZOMBIE  = EnemyType(name="Zombie",  hp_min=5, hp_max=11, dmg_min=1, dmg_max=5, reward_min=1,  reward_max=5, dodge_target=60, flee_dc=12, is_grappler=False, is_buster=False)
SCRAMBLER  = EnemyType(name="Scrambler",  hp_min=4, hp_max=9, dmg_min=2, dmg_max=6, reward_min=1,  reward_max=5, dodge_target=80, flee_dc=15, is_grappler=False, is_buster=False)
BRUTE = EnemyType(name="Brute", hp_min=13, hp_max=21, dmg_min=5, dmg_max=9, reward_min=1,  reward_max=5, dodge_target=45, flee_dc=10, is_grappler=False, is_buster=False)
BUSTER = EnemyType(name="Buster", hp_min=2, hp_max=5, dmg_min=6, dmg_max=17, reward_min=1,  reward_max=5, dodge_target=90, flee_dc=13, is_buster=True, is_grappler=False)
CRAWLER = EnemyType(name="Crawler", hp_min=4, hp_max=8, dmg_min=2, dmg_max=4, reward_min=1,  reward_max=5, dodge_target=60, flee_dc=9, is_grappler=True, is_buster=False)

ENEMIES = [ZOMBIE, SCRAMBLER, BRUTE, BUSTER, CRAWLER]
 
def run_combat(player, enemy: EnemyType):
    rng = random
    zombie_hp = rng.randint(enemy.hp_min, enemy.hp_max)

    combat_dodge = False   # +20 to THIS enemy attack if you repositioned
    grappled = False       # while True, you can't flee or reposition

    slow_print(f"\n{enemy.name.upper()} ENCOUNTER!")
    while zombie_hp > 0 and player.health > 0:
        print(f"{enemy.name.upper()} HP: {zombie_hp} | Your HP: {player.health}")

        # ---------- action menu (block flee/reposition if grappled) ----------
        actions = {"1": "Attack", "3": "Distract", "4": "Use Gauze"}
        if not grappled:
            actions["2"] = "Reposition (+20 Dodge)"
            actions["5"] = "Flee"
        action = choose("What do you do?", dict(sorted(actions.items())))

        # -------------------- your turn --------------------
        if action == "1": # Attacking
            dmg = rng.randint(0, 4) + player.total_damage
            slow_print(f"You hit the {enemy.name.upper()} for {dmg}!")
            zombie_hp -= dmg
            if zombie_hp <= 0:
                reward = rng.randint(enemy.reward_min, enemy.reward_max)
                if reward > 0:
                    slow_print(f"You killed the {enemy.name.upper()}! You got ${reward}.")
                    player.money += reward
                else:
                    slow_print(f"You killed the {enemy.name.upper()}!")
                return "won"

        elif action == "2":  # Reposition
            if grappled:
                slow_print("You're grappled! You can't reposition this turn.")
            else:
                combat_dodge = True
                slow_print("\nYou reposition yourself, bracing for an attack. +20 Dodge.")

        elif action == "3":  # Distract
            slow_print("not ready yet")

        elif action == "4":  # Use Gauze
            if "Gauze" in player.armor_items:
                heal = rng.randint(1, 3)
                player.health = min(player.health + heal, player.max_health)
                player.armor_items.remove("Gauze")
                slow_print(f"You use a piece of Gauze to heal yourself. +{heal} HP.")
            else:
                slow_print("You don't have any Gauze!")

        elif action == "5":  # Flee
            if grappled:
                slow_print("You're grappled! You can't flee this turn.")
            else:
                escape = rng.randint(0, 20) + int(player.total_luck * 1.5)
                if escape >= enemy.flee_dc:
                    slow_print("You successfully got away!")
                    return "escaped"
                else:
                    slow_print(f"The {enemy.name.upper()} caught up to you!")

        # -------------------- enemy turn --------------------
        z_dmg = rng.randint(enemy.dmg_min, enemy.dmg_max)
        dodge_roll = rng.randint(0, 100) + player.total_dodge + (20 if combat_dodge else 0)
        dodged = (dodge_roll >= enemy.dodge_target)

        if dodged:
            slow_print(f"You dodged the {enemy.name.upper()}'s attack!")
            if enemy.is_grappler and grappled:
                slow_print("You break free from the grapple!")
                grappled = False
        else:
            slow_print(f"The {enemy.name.upper()} hits you for {z_dmg}!")
            player.health -= z_dmg
            if player.health <= 0:
                slow_print("You collapse...")
                return "dead"
            if enemy.is_grappler:
                grappled = True
                slow_print("The zombie has grappled you! You cannot reposition or flee until it misses an attack.")

        if enemy.is_buster:
            slow_print(f"It busted everywhere!")
            if player.health <= 0:
                slow_print(" You couldn't handle the juice...")
            else:
                return "escaped"

        combat_dodge = False

    return "dead" if player.health <= 0 else "won"

# ----------------------------
# Character creation
# ----------------------------
def character_creation(player: Player):
    slow_print("Welcome to Zombie Pro Fisher - Byte Sized!")
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
# Encounters
# ----------------------------

def zombie_encounter(player):
    if player.location == "Shack":
        return False

    spawn = random.randint(0, 10)
    risky = (spawn >= 8 and player.location != "Shack") or (spawn >= 6 and player.location == "Nuclear Plant")
    if not risky:
        return False
    
    enemy = random.choice(ENEMIES)

    result = run_combat(player, enemy)
    if result == "dead":
        return True
    return False

#----------------------------------------------------------

def forage(player: Player):
    if player.location == "Nuclear Plant":
        slow_print("You're not sure there's anything safe to eat here...")
        player.hunger -= 1
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
            final_choice = choose("Choose:", {"1": "The juice.", "2": "The sugar."})
            if final_choice == "1":
                slow_print("You choke down a vial of solid purple liquid. Your vision blurs... you feel... awakened.")
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
        slow_print("Mr. Hutchinson politely tells you there's nothing to forage here.")
        return

    # Normal forage
    player.hunger -= 1
    result = random.randint(-10, 32) + int(player.total_luck * 1.8)
    if result <= 0:
        slow_print("You found nothing.")
    elif (1 <= result <= 10 and not player.cookbook) or (0 <= result <= 5 and player.cookbook):
        hp_loss = random.randint(1, 3)
        player.health -= hp_loss
        slow_print(f"Yuck! You ate something you shouldn't have. -{hp_loss} HP.")
    elif (11 <= result <= 20 and not player.cookbook) or (6 <= result <= 20 and player.cookbook):
        slow_print("You found some nuts and berries. +1 Hunger")
        player.hunger += 2
    elif 21 <= result <= 25:
        slow_print("You're not sure what you found, but the geiger counter didn't beep. +2 Hunger.")
        player.hunger += 3
    elif 26 <= result <= 30:
        slow_print("You found unexpired canned food. +3 Hunger.")
        player.hunger += 4
    elif 31 <= result <= 40:
        slow_print("You trapped some local fauna and ate a well-cooked meal. +4 Hunger.")
        player.hunger += 5

def fishing(player: Player):
    player.hunger -= 1
    roll = random.randint(0, 100) + int(player.total_luck * 2.5)

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
        "\n HUTCHINSON: It's good to see a friendly face. Here's my shop.",
        "\n HUTCHINSON: Welcome back, old timer!",
        f"\n HUTCHINSON: Hittin' the lakes already, are we {player.name}?",
        f"\n HUTCHINSON: Ahh, {player.name}, glad to see you're safe and well!",
        "\n HUTCHINSON: My tackle is the best in town! Glad the youngins are getting into the spirit of fishing!",
        "\n HUTCHINSON: I've been around these parts a long time. Seen a lot of things... some good, some bad.",
        "\n HUTCHINSON: No zombie apocalypse will stop me from hitting the lakes!",
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

        # Crafting
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
    clear_screen()
    player = Player()
    character_creation(player)

    while player.health > 0:
        player.turns += 1
        player.update_stats()
        weeks = player.turns // 7
        days = player.turns // 3

        if zombie_encounter(player):
            break

        player.statscore()

        print("\nWhat would you like to do?")
        options = {"1": "Forage", "2": "Change location", "3": "Open Inventory"}

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
            while True:
                inv_choice = choose("\n--- INVENTORY MENU ---", {
                "1": "View Stats",
                "2": "View Bag",
                "3": "View Almanac",
                "4": "Go Back"
                })

                if inv_choice == "1":
                    player.stats()
                elif inv_choice == "2":
                    player.inventory()
                elif inv_choice == "3":
                    player.almanac()
                elif inv_choice == "4":
                    break

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

    slow_print("\nGame Over. You survived for:")
    slow_print(f"{weeks % 4} week(s), and {days % 7} day(s). ({player.turns} turns).")
    slow_print("\nThanks for playing Zombie Pro Fisher - Byte Sized!")

if __name__ == "__main__":
    main()