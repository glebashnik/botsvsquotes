import random
from time import sleep

from cards.io import load_character_names, load_character_cards
from input_parser.knowledge_parser import KB_parser
from sim.player_similarity import Sim
from tweet import post_tweet, reply_tweet
from twitter.wnsim import match_cards


def select_czar(characters):
    return random.choice(characters)


kb = KB_parser()
character_sim = Sim()


def select_players(czar, candidates):
    czar_profile = kb.get_people_from_kb([czar])[0]
    candidate_profiles = kb.get_people_from_kb(candidates)
    player_profiles = character_sim.choose_players_random(czar_profile, candidate_profiles, 5)
    return [p["Character"] for p in player_profiles]
    #return random.sample(candidates, 5)


def select_czar_card(czar_cards):
    return random.choice(czar_cards)


def select_player_card(czar_card, player_cards):
    return max(player_cards, key=lambda c: match_cards(czar_card, c))
    #return random.choice(players_cards)


def select_winner(czar, czar_card, selected_players_cards):
    return max(selected_players_cards.keys(), key=lambda p: match_cards(czar_card, selected_players_cards[p]))
    #return random.choice(selected_players_cards.keys())

if __name__ == '__main__':
    while 1:
        try:
            print "playing"
            characters = load_character_names()
            czar = select_czar(characters)
            candidates = [character for character in characters if czar != character]
            players = select_players(czar, candidates)

            czar_cards = load_character_cards(czar)
            players_cards = {player: load_character_cards(player) for player in players}

            selected_czar_card = select_czar_card(czar_cards)
            selected_players_cards = {player: select_player_card(selected_czar_card, players_cards)
                                      for player, players_cards in players_cards.iteritems()}
            winner = select_winner(czar, selected_czar_card, selected_players_cards)

            print "twitting"
            sleep(10)
            reply_id = post_tweet(czar + ": " + selected_czar_card.black_string())

            sleep(10)

            for player, selected_player_card in selected_players_cards.iteritems():
                reply_tweet(
                    player + ": " + selected_czar_card.black_string()
                    .replace("___", "[" + selected_player_card.white_string() + "]"),
                    reply_id)
                sleep(10)

            reply_tweet(czar + ": " + winner + ", nice one!", reply_id)

            print "waiting"
            sleep(1800)
        except:
            print "failing"