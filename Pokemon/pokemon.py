import random
import pickle

class Move:
    def __init__(self, name, mtype, power, accuracy, category, effect=None):
        self.name = name
        self.mtype = mtype
        self.power = power
        self.accuracy = accuracy
        self.category = category
        self.effect = effect

    def apply_effect(self, target):
        if self.effect:
            self.effect(target)

class Pokémon:
    def __init__(self, name, ptype, health, attack, defense, special_attack, special_defense, speed, level, experience, moves, is_wild=False):
        self.name = name
        self.ptype = ptype
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.level = level
        self.experience = experience
        self.moves = moves
        self.is_wild = is_wild

    def attack_opponent(self, opponent, move):
        if random.random() > move.accuracy:
            print(f"{self.name}'s attack missed!")
            return 0
        damage = self.calculate_damage(opponent, move)
        opponent.take_damage(damage)
        move.apply_effect(opponent)
        return damage

    def calculate_damage(self, opponent, move):
        if move.category == 'physical':
            attack = self.attack
            defense = opponent.defense
        elif move.category == 'special':
            attack = self.special_attack
            defense = opponent.special_defense
        else:
            raise ValueError("Invalid move category")

        # Simple damage calculation
        base_damage = (attack * move.power) / (defense + 10)
        return max(1, int(base_damage))

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
            print(f"{self.name} has fainted!")

    def gain_experience(self, exp):
        self.experience += exp
        while self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 5
        self.health = self.max_health
        self.attack += 2
        self.defense += 2
        self.special_attack += 2
        self.special_defense += 2
        print(f"{self.name} leveled up to level {self.level}!")

    def learn_move(self, move):
        self.moves.append(move)

    def get_stat(self, stat):
        return getattr(self, stat, "Invalid stat")

class Trainer:
    def __init__(self, name, team, inventory=None, badges=None):
        self.name = name
        self.team = team
        self.inventory = inventory if inventory is not None else []
        self.badges = badges if badges is not None else []

    def catch_pokemon(self, wild_pokemon):
        print(f"\nWild {wild_pokemon.name} appeared!")
        print(f"Type: {wild_pokemon.ptype}")
        print(f"Health: {wild_pokemon.health}")
        print(f"Attack: {wild_pokemon.attack}")
        print(f"Defense: {wild_pokemon.defense}")
        print(f"Speed: {wild_pokemon.speed}")
        print("Choose a Pokéball to use:")
        print("1: Pokéball (Catch Rate: 50%)")
        print("2: Great Ball (Catch Rate: 70%)")
        print("3: Ultra Ball (Catch Rate: 90%)")

        choice = input("Enter the number of your choice: ")
        catch_rates = {"1": 0.5, "2": 0.7, "3": 0.9}
        if choice in catch_rates:
            if random.random() < catch_rates[choice]:
                self.team.append(wild_pokemon)
                print(f"Congratulations! You caught {wild_pokemon.name}!")
            else:
                print(f"Sorry, {wild_pokemon.name} escaped!")
        else:
            print("Invalid choice! The Pokémon escaped.")

    def use_item(self, item, target):
        if item in self.inventory:
            item.use(target)
            self.inventory.remove(item)
        else:
            print("Item not found in inventory!")

    def battle(self, opponent):
        while self.team and opponent.team:
            print(f"\n{self.team[0].name} vs {opponent.team[0].name}")
            while self.team[0].health > 0 and opponent.team[0].health > 0:
                move = random.choice(self.team[0].moves)
                damage = self.team[0].attack_opponent(opponent.team[0], move)
                print(f"{self.team[0].name} used {move.name} and did {damage} damage!")
                if opponent.team[0].health > 0:
                    opp_move = random.choice(opponent.team[0].moves)
                    opp_damage = opponent.team[0].attack_opponent(self.team[0], opp_move)
                    print(f"{opponent.team[0].name} used {opp_move.name} and did {opp_damage} damage!")
                else:
                    print(f"{opponent.team[0].name} fainted!")
                    self.team[0].gain_experience(opponent.team[0].level * 5)
                    opponent.team.pop(0)
                    break

            if self.team[0].health <= 0:
                print(f"{self.team[0].name} fainted!")
                self.team.pop(0)

        if self.team:
            print(f"{self.name} won the battle!")
            self.badges.append(opponent.badges[0])
            print(f"Received {opponent.badges[0]} badge!")
        else:
            print(f"{opponent.name} won the battle!")

class Item:
    def __init__(self, name, itype, effect):
        self.name = name
        self.itype = itype
        self.effect = effect

    def use(self, target):
        self.effect(target)

def save_game(trainer):
    with open('savefile.pkl', 'wb') as f:
        pickle.dump(trainer, f)
    print("Game saved!")

def load_game():
    try:
        with open('savefile.pkl', 'rb') as f:
            trainer = pickle.load(f)
        print("Game loaded!")
        return trainer
    except FileNotFoundError:
        print("No saved game found.")
        return None

# Sample Moves
scratch = Move(name="Scratch", mtype="physical", power=40, accuracy=0.9, category="physical")
tackle = Move(name="Tackle", mtype="physical", power=40, accuracy=0.9, category="physical")
ember = Move(name="Ember", mtype="special", power=40, accuracy=0.9, category="special", effect=lambda target: print(f"{target.name} might be burned!"))

# Sample Pokémon
charmander = Pokémon(name="Charmander", ptype="Fire", health=39, attack=52, defense=43, special_attack=60, special_defense=50, speed=65, level=5, experience=0, moves=[scratch, ember])
bulbasaur = Pokémon(name="Bulbasaur", ptype="Grass", health=45, attack=49, defense=49, special_attack=65, special_defense=65, speed=45, level=5, experience=0, moves=[tackle])
squirtle = Pokémon(name="Squirtle", ptype="Water", health=44, attack=48, defense=65, special_attack=50, special_defense=64, speed=43, level=5, experience=0, moves=[tackle])
pikachu = Pokémon(name="Pikachu", ptype="Electric", health=35, attack=55, defense=40, special_attack=50, special_defense=50, speed=90, level=5, experience=0, moves=[scratch])

# Sample Trainers
gary = Trainer(name="Gary", team=[squirtle], badges=["Boulder Badge"])

def main():
    print("Welcome to the Pokémon game!")
    print("Choose your starter Pokémon:")
    starters = {"1": charmander, "2": bulbasaur, "3": squirtle, "4": pikachu}
    for key, pokemon in starters.items():
        print(f"{key}: {pokemon.name}")

    choice = input("Enter the number of your choice: ")
    if choice in starters:
        player_trainer = Trainer(name="Player", team=[starters[choice]], inventory=[], badges=[])
    else:
        print("Invalid choice, defaulting to Charmander.")
        player_trainer = Trainer(name="Player", team=[charmander], inventory=[], badges=[])

    while True:
        print("\nMenu:")
        print("1: Battle Gary")
        print("2: Catch a wild Pokémon")
        print("3: Use an item")
        print("4: Save game")
        print("5: Load game")
        print("6: Exit")

        option = input("Choose an option: ")

        if option == "1":
            player_trainer.battle(gary)
        elif option == "2":
            wild_pokemon = random.choice([charmander, bulbasaur, squirtle, pikachu])
            player_trainer.catch_pokemon(wild_pokemon)
        elif option == "3":
            if player_trainer.inventory:
                item = player_trainer.inventory[0]  # Use the first item in inventory
                print(f"Using item: {item.name}")
                player_trainer.use_item(item, player_trainer.team[0])
            else:
                print("No items in inventory!")
        elif option == "4":
            save_game(player_trainer)
        elif option == "5":
            loaded_trainer = load_game()
            if loaded_trainer:
                player_trainer = loaded_trainer
        elif option == "6":
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
