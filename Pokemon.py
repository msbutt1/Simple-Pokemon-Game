import random
import pygame
import sys

# ======================
# Game Data Classes
# ======================
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

    def choose_attack(self, is_player=False):
        if not is_player:
            return random.choice(self.attacks)

    def perform_attack(self, other, attack):
        luck = random.uniform(0.8, 1.2)
        base = attack.power + max(0, (self.attack_stat - 70) // 5)
        damage = round(base * luck)
        if damage > other.defense:
            lost_health = damage - other.defense
            other.lose_health(lost_health)
            return f"{self.name} uses {attack.name}! {other.name} lost {lost_health} HP!"
        else:
            return f"{self.name} uses {attack.name}, but {other.name} blocked it!"


def read_pokemon_from_file(filename: str):
    pokemons = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()[1:]  # skip header
    for line in lines:
        parts = line.strip().split("|")
        if len(parts) < 8:
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
            defaults = [
                Attack("Tackle", 40),
                Attack("Headbutt", 70),
                Attack("Body Slam", 85),
                Attack("Hyper Beam", 150),
            ]
            moves += defaults[: 4 - len(moves)]
        pokemons.append(Pokemon(name, attack, defense, health, health, moves))
    return pokemons


def pick_two_distinct(pokemons):
    p1 = random.choice(pokemons)
    p2 = random.choice(pokemons)
    while p2 is p1:
        p2 = random.choice(pokemons)
    return p1, p2


# ======================
# Pygame UI Functions
# ======================
def draw_ui(screen, font, player, opponent, message, buttons, retry_button=None):
    screen.fill((200, 220, 255))  # background

    # --- Pokémon placeholders ---
    player_rect = pygame.Rect(100, 350, 150, 150)
    opponent_rect = pygame.Rect(550, 150, 150, 150)
    pygame.draw.rect(screen, (255, 0, 0), player_rect)  # player
    pygame.draw.rect(screen, (0, 0, 255), opponent_rect)  # opponent

    # --- Top HP bars ---
    bar_width = 300
    bar_height = 20

    # Player HP bar (top-left)
    pygame.draw.rect(screen, (0, 0, 0), (50, 50, bar_width, bar_height), 2)  # border
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (50, 50, bar_width * player.current_health / player.max_health, bar_height),
    )
    screen.blit(
        font.render(
            f"{player.name} HP: {player.current_health}/{player.max_health}", True, (0, 0, 0)
        ),
        (50, 25),
    )

    # Opponent HP bar (top-right)
    pygame.draw.rect(screen, (0, 0, 0), (450, 50, bar_width, bar_height), 2)  # border
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (450, 50, bar_width * opponent.current_health / opponent.max_health, bar_height),
    )
    screen.blit(
        font.render(
            f"{opponent.name} HP: {opponent.current_health}/{opponent.max_health}",
            True,
            (0, 0, 0),
        ),
        (450, 25),
    )

    # --- Message text ---
    text_surface = font.render(message, True, (0, 0, 0))
    screen.blit(text_surface, (50, 550))

    # --- Attack buttons ---
    for rect, label in buttons:
        pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        text = font.render(label, True, (0, 0, 0))
        screen.blit(text, (rect.x + 5, rect.y + 5))

    # --- Retry button if battle ended ---
    if retry_button:
        pygame.draw.rect(screen, (255, 255, 200), retry_button)
        pygame.draw.rect(screen, (0, 0, 0), retry_button, 2)
        text = font.render("Retry", True, (0, 0, 0))
        screen.blit(text, (retry_button.x + 20, retry_button.y + 5))

    pygame.display.flip()
    return player_rect, opponent_rect


def make_attack_buttons(player):
    buttons = []
    for i, atk in enumerate(player.attacks):
        rect = pygame.Rect(400, 350 + i * 50, 200, 40)
        buttons.append((rect, atk.name))
    return buttons


def animate_attack(screen, attacker_rect, target_rect, color):
    """Simple projectile animation"""
    for i in range(10):
        x = attacker_rect.centerx + (target_rect.centerx - attacker_rect.centerx) * i // 10
        y = attacker_rect.centery + (target_rect.centery - attacker_rect.centery) * i // 10
        pygame.draw.circle(screen, color, (x, y), 15)
        pygame.display.flip()
        pygame.time.delay(40)


# ======================
# Game Loop
# ======================
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pokémon Battle")
    font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    pokemons = read_pokemon_from_file("all_pokemon.txt")

    # Initial setup
    player, opponent = pick_two_distinct(pokemons)
    message = f"A wild {opponent.name} appeared!"
    buttons = make_attack_buttons(player)
    retry_button = None
    turn = "player"
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button and retry_button.collidepoint(event.pos):
                    # Restart battle
                    player, opponent = pick_two_distinct(pokemons)
                    message = f"A wild {opponent.name} appeared!"
                    buttons = make_attack_buttons(player)
                    retry_button = None
                    turn = "player"

                elif turn == "player":
                    for rect, label in buttons:
                        if rect.collidepoint(event.pos):
                            chosen_attack = next(a for a in player.attacks if a.name == label)
                            msg = player.perform_attack(opponent, chosen_attack)
                            message = msg
                            turn = "opponent"

        # Opponent's turn automatically
        if turn == "opponent" and opponent.is_alive():
            pygame.time.delay(800)
            opp_attack = opponent.choose_attack()
            msg = opponent.perform_attack(player, opp_attack)
            message = msg
            turn = "player"

        # Check win/lose
        if not opponent.is_alive() and not retry_button:
            message = f"{opponent.name} fainted! You win!"
            buttons = []
            retry_button = pygame.Rect(350, 500, 100, 40)

        elif not player.is_alive() and not retry_button:
            message = f"{player.name} fainted! You lose!"
            buttons = []
            retry_button = pygame.Rect(350, 500, 100, 40)

        # Draw everything
        player_rect, opponent_rect = draw_ui(
            screen, font, player, opponent, message, buttons, retry_button
        )

        clock.tick(30)


if __name__ == "__main__":
    main()
