import random
from cards.io import load_character_cards


def pick_winner(czar, czar_card, participants, participant_cards):
    return random.choice(participants)

if __name__ == '__main__':
    czar = "Adolf Hitler"
    participants = ["Richard Dawkins", "Robin Williams"]
    pick_winner("Adolf Hitler", load_character_cards())