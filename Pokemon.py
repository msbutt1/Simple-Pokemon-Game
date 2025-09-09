import random

class Attack:
    def __init__(self, name: str, power: int):
        self.name = name
        self.power = power

    def __str__(self):
        return f"{self.name} (Power: {self.power})"

class Pokemon:
    def __init__(self, name, attack, defense, max_health, current_health, attacks):
        self.name = name
        self.attack_stat = attack
        self.defense = defense
        self.max_health = max_health
        self.current_health = current_health
        self.attacks = attacks  # List[Attack]

    def __str__(self):
        return f"{self.name} (HP: {self.current_health}/{self.max_health})"

    def lose_health(self, lost_health):
        if lost_health > 0:
            self.current_health = max(0, self.current_health - lost_health)

    def is_alive(self):
        return self.current_health > 0

    def revive(self):
        self.current_health = self.max_health
        print(f"{self.name} was revived to full health!")

    def choose_attack(self, is_player=False):
        if is_player:
            print(f"\nChoose an attack for {self.name}:")
            for i, atk in enumerate(self.attacks, start=1):
                print(f"{i}. {atk}")
            while True:
                try:
                    choice = int(input("Enter attack number (1-4): "))
                    if 1 <= choice <= len(self.attacks):
                        return self.attacks[choice - 1]
                except ValueError:
                    pass
                print("Invalid choice. Try again.")
        else:
            return random.choice(self.attacks)

    def perform_attack(self, other, attack):
        luck = random.uniform(0.8, 1.2)
        # Optionally factor user's attack stat a little to differentiate species
        base = attack.power + max(0, (self.attack_stat - 70) // 5)
        damage = round(base * luck)
        print(f"{self.name} uses {attack.name} on {other.name} for {damage} damage!")

        if damage > other.defense:
            lost_health = damage - other.defense
            other.lose_health(lost_health)
            print(f"{other.name} loses {lost_health} HP. ({other.current_health}/{other.max_health})")
        else:
            print(f"{other.name} blocked the attack!")

def read_pokemon_from_file(filename: str):
    pokemons = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()[1:]  # skip header
    for line in lines:
        parts = line.strip().split("|")
        if len(parts) < 8:
            # Skip malformed lines
            continue
        name, attack, defense, health = parts[0], int(parts[1]), int(parts[2]), int(parts[3])
        moves = []
        for move_str in parts[4:8]:
            if ":" in move_str:
                move_name, power = move_str.rsplit(":", 1)
                try:
                    moves.append(Attack(move_name, int(power)))
                except ValueError:
                    continue
        if len(moves) < 4:
            # Fill any missing moves with simple defaults
            defaults = [Attack("Tackle", 40), Attack("Headbutt", 70), Attack("Body Slam", 85), Attack("Hyper Beam", 150)]
            moves += defaults[:4-len(moves)]
        pokemons.append(Pokemon(name, attack, defense, health, health, moves))
    return pokemons

def pick_two_distinct(pokemons):
    p1 = random.choice(pokemons)
    p2 = random.choice(pokemons)
    while p2 is p1:
        p2 = random.choice(pokemons)
    return p1, p2

def main():
    print("Loading Pokémon and moves...")
    pokemons = read_pokemon_from_file("all_pokemon.txt")

    player, opponent = pick_two_distinct(pokemons)
    print(f"\nYour Pokémon: {player}")
    print(f"Opponent's Pokémon: {opponent}")

    round_num = 1
    while player.is_alive() and opponent.is_alive():
        print(f"\n--- Round {round_num} ---")
        atk = player.choose_attack(is_player=True)
        player.perform_attack(opponent, atk)
        if not opponent.is_alive():
            print(f"{opponent.name} fainted! You win!")
            break

        opp_atk = opponent.choose_attack(is_player=False)
        opponent.perform_attack(player, opp_atk)
        if not player.is_alive():
            print(f"{player.name} fainted! You lose!")
            break

        round_num += 1

if __name__ == "__main__":
    main()