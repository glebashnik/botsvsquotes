# Black card - quote with the blank.
# White card - proposed filling for the quote in the black card.
# Czar - the character with the black card, also the one who selects a winner
# Players - all the other characters except czar

import random
from time import sleep

from cards.io import load_character_names, load_character_cards
from input_parser.knowledge_parser import KB_parser
from sim.player_similarity import Sim
from tweet import post_tweet, reply_tweet, get_replies
from twitter.wnsim import match_cards


def select_czar(characters):
    return random.choice(characters)

# Knowledge
def select_players(czar, candidates):
    czar_profile = kb.get_people_from_kb([czar])[0]
    players_profiles = kb.get_people_from_kb(candidates)
    selected_players_profiles = character_sim.choose_players_random(czar_profile, players_profiles, 5)
    return [p["Character"] for p in selected_players_profiles]
    #return random.sample(candidates, 5)


def select_czar_card(czar_cards):
    czar_cards = [card for card in czar_cards if len(card.black_string()) < 110]
    return random.choice(czar_cards)

# Similarity based on wordnet here
def select_player_card(czar_card, player_cards):
    return max(player_cards, key=lambda c: match_cards(czar_card, c))
    #return random.choice(players_cards)


def select_winner(czar, czar_card, selected_players_cards):
    return max(selected_players_cards.keys(), key=lambda p: match_cards(czar_card, selected_players_cards[p]))
    #return random.choice(selected_players_cards.keys())

"""
def select_winner_from_replies(reply_id, czar, selected_czar_card, selected_players_cards):
    import difflib

    winner_announcement = [", nice one!", ", that's absolutely tremendous!", ]
    bad_stuff = [", ohh come on!", ", you suck!", ", next time try to use your imagination.", ", you could better than that."]

    bot_replies, user_replies = get_replies(reply_id)
    winner = ""
    
    if user_replies == {}:
        print "user_replies is empty"
        selected_players = dict((player,selected_players_cards[player]) for player in bot_replies.keys())
        winner = select_winner(czar, selected_czar_card, selected_players)
    else:
        print "user_replies is full" 
        print user_replies 
        czar_quote=selected_czar_card.black_string().lower().strip()

        max_ratio = 0
        for user, quote in user_replies.iteritems():
            seq=difflib.SequenceMatcher(a=czar_quote, b=quote.lower().strip())
            seq_ratio = seq.ratio()
            
            if seq_ratio < 0.5:
                reply_tweet(user + ": " + random.choice(bad_stuff), reply_id)
                sleep(5)
                continue
            else:
                if seq_ratio > max_ratio:
                    winner = user
                    max_ratio = seq_ratio
        
        if max_ratio == 0:
            winner = select_winner(czar, selected_czar_card, selected_players)

    reply_tweet(czar + ": " + winner + random.choice(winner_announcement), reply_id)
    tweet = czar + ": " + selected_czar_card.black_string().replace("___", "[" + selected_czar_card.white_string() + "]")
    tweet = tweet.split(":")[1]
    reply_tweet(czar + ": What I meant was: " + tweet, reply_id)
"""
if __name__ == '__main__':
    kb = KB_parser()
    character_sim = Sim()
    characters = load_character_names()
    tweet_delay = 300
    reply_delay = 10
    winner_announcement = [", nice one!", ", that's absolutely tremendous!", ", not bad!", ", fantastic!", ", that's evil, but I like it!", ", good on you!", ", I don't really see the point, but it's better than everybody else."]

    while 1:
        try:
            print "playing"
            czar = select_czar(characters)
            players = [character for character in characters if czar != character]
            selected_players = select_players(czar, players)

            czar_cards = load_character_cards(czar)
            players_cards = {player: load_character_cards(player) for player in selected_players}

            selected_czar_card = select_czar_card(czar_cards)
            selected_players_cards = {player: select_player_card(selected_czar_card, players_cards)
                                      for player, players_cards in players_cards.iteritems()}

            print "twitting..."
            reply_id = post_tweet(czar + ": " + selected_czar_card.black_string())
            
            sleep(reply_delay)

            for player, selected_player_card in selected_players_cards.iteritems():
                reply_tweet(
                    player + ": " + selected_czar_card.black_string()
                    .replace("___", "[" + selected_player_card.white_string().lower() + "]"),
                    reply_id)

                sleep(reply_delay)
            """
            print "selecting a winner"
            sleep(20)
            select_winner_from_replies(reply_id, czar, selected_czar_card, selected_players_cards)            
            
            """
            winner = select_winner(czar, selected_czar_card, selected_players_cards)
            reply_tweet(czar + ": " + winner + random.choice(winner_announcement), reply_id)
            tweet = czar + ": " + selected_czar_card.black_string().replace("___", "[" + selected_czar_card.white_string() + "]")
            tweet = tweet.split(":")[1]
            reply_tweet(czar + ": The original was: " + tweet, reply_id)
            print "sleeping ..."
            sleep(tweet_delay)
        except Exception as e:
            print "failing"
            print e
            print 
            pass
            


