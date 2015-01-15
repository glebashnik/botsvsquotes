import random

from cards.io import load_character_cards, load_character_names


def select_players(parser, s, n=3):
    # choose manager
    manager = parser.random_manager()

    #chose other players
    players = s.choose_players_random(manager, load_character_names(), n)
    manager = manager["Character"]

    return manager, players


"""
def make_selection(black_cards, white_cards, n=3):
    white_cards_num = random.sample(range(0, len(white_cards)), n)
    white_cards_selection = dict([(white_cards.keys()[i], white_cards[white_cards.keys()[i]]) for i in white_cards_num])
    
    black_cards_num = random.randint(0, len(black_cards)-1)
    black_cards_name = black_cards.keys()[black_cards_num]
    black_cards_selection = dict([(black_cards_name, black_cards[black_cards_name])])
    
    return black_cards_selection, white_cards_selection
"""


def combine_quotes(bc_selection, wc_selection):
    bc_name = bc_selection.keys()[0]
    bc_quote = bc_selection[bc_name][random.randint(0, len(bc_selection[bc_name]) - 1)]
    question = {bc_name: bc_quote}

    answers = {}
    for person, quotes in wc_selection.iteritems():
        quote = quotes[random.randint(0, len(quotes) - 1)]
        answers[person] = bc_quote.replace("___", quote.lower())

    return question, answers


def post_to_twitter(question, answers, time_start=5, time_end=10):
    from tweet import post_tweet, reply_tweet

    main_name = question.keys()[0]
    main_quote = question[main_name]
    tweet = main_name + ": " + main_quote + " #codecampCC"
    reply_id = post_tweet(tweet)
    print reply_id
    print tweet
    sleep(random.randrange(time_start, time_end))

    names = []
    for name, quote in answers.iteritems():
        tweet = name + ": " + main_quote.replace("___", "[" + quote + "]")
        reply_tweet(tweet, reply_id)
        print tweet
        names.append(name)
        sleep(random.randrange(time_start, time_end))

    # rand_name = names[random.randint(0, len(names)-1)]
    #tweet = main_name + ": " + rand_name + " is the one that I like the most. Others are stupid."
    #reply_tweet(tweet, reply_id)
    #print tweet
    #print
    return reply_id


def post_to_console(question, answers, time_start=0, time_end=1):
    main_name = question.keys()[0]
    quote = question[main_name]
    print main_name + ": " + quote + " #codecampCC"
    sleep(random.randrange(time_start, time_end))

    names = []
    for name, quote in answers.iteritems():
        print name + ": " + quote
        names.append(name)
        sleep(random.randrange(time_start, time_end))


def evaluate_quotes(reply_id):
    from tweet import get_replies

    bot_replies, user_replies = get_replies(reply_id)
    return bot_replies, user_replies




if __name__ == '__main__':
    from time import sleep
    #from input_parser.knowledge_parser import KB_parser
    #from sim.player_similarity import Sim

    print "Hello! I am waking up... its such a lovely morning!"
    print

    print "Parser loading ..."
    #parser = KB_parser()
    print "done!"

    print "Simillarity loading ..."
    #simillarity = Sim()
    print "done!"

    # black_cards1, black_cards2, white_cards1, white_cards2 = read_dataset()

    while 1:
        # if bool(random.getrandbits(1)):
        #     print "nonfictional vs fictional characters"
        #     black_cards, white_cards = black_cards1, white_cards1
        # else:
        #     print "fictional vs nonfictional characters"
        #     black_cards, white_cards = black_cards2, white_cards2

        manager, players = select_players(parser, simillarity)
        print manager, players

        manager_card = random.choice(load_character_cards(manager))
        players_cards = {player: load_character_cards(player) for player in players}
        selected_player_cards = {}

        for player, player_cards in players_cards.iteritems():
            selected_player_cards[player] = select_filler(manager_card, player_cards)

        sleep(10)
        #bc_selection, wc_selection = make_selection(parser, simillarity, black_cards, white_cards)
        #question, answers = combine_quotes(bc_selection, wc_selection)

        reply_id = post_to_twitter(
            {manager: manager_card.black_string()},
            {player: card.white_string() for player, card in selected_player_cards.iteritems()})
        #sleep(20)
        #reply_id = post_to_console(question, answers)
        #sleep(5)

        #bot_replies, user_replies = evaluate_quotes(reply_id)
        #print bot_replies, user_replies
        #sleep(60)



        
        



















    