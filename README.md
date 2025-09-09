# Pokémon Battle Simulator (Python)

A simple text-based Pokémon battle simulator written in Python.  
Pick your Pokémon, choose from their moves, and battle against a randomly chosen opponent!

---

## Features

- Loads Pokémon stats and moves from `all_pokemon.txt`
- Each Pokémon has:
  - **Attack, Defense, Health** stats
  - **Four moves** (semi-accurate to their type/fandom, with realistic power values)
- Player selects moves each round
- Opponent chooses randomly
- Battles continue until one Pokémon faints

---

---

## How to Play

1. Clone/download the repository.
2. Make sure you have **Python 3.8+** installed.
3. Run the game from your terminal:

   ```bash
   python Pokemon.py
4. Example flow:
    -The game randomly assigns you a Pokémon and your opponent.
    -On your turn, choose a move (1–4).
    -Moves deal damage based on their power and your Pokémon’s Attack stat.
    -The battle ends when one Pokémon faints.

Example Gameplay:

Your Pokémon: Bulbasaur (HP: 45/45)
Opponent's Pokémon: Charmander (HP: 39/39)

--- Round 1 ---
Choose an attack for Bulbasaur:
1. Vine Whip (Power: 45)
2. Energy Ball (Power: 90)
3. Ice Beam (Power: 90)
4. Solar Beam (Power: 120)
Enter attack number: 1
Bulbasaur uses Vine Whip on Charmander for 52 damage!
Charmander loses 9 HP. (30/39)
...

Future Improvements:
-Add type effectiveness (Water > Fire, Fire > Grass, etc.)
-Add status effects (paralysis, burn, poison)
-Add multiplayer mode (two players taking turns)
-Improve/Add AI for opponent move choice

License:
This project is provided for educational and personal use.
Pokémon and Pokémon character names are trademarks of Nintendo, Game Freak, and The Pokémon Company.
This project is fan-made and not affiliated with or endorsed by Nintendo.





