import random

def read_dataset():
    from cards.cards import load_cards_dict

    dataset_path = "cards/"
    black_cards1 = load_cards_dict(dataset_path + 'nonfictional_black_cards.json')
    white_cards1 = load_cards_dict(dataset_path + 'fictional_white_cards.json')

    black_cards2 = load_cards_dict(dataset_path + 'fictional_black_cards.json')
    white_cards2 = load_cards_dict(dataset_path + 'nonfictional_white_cards.json')

    return black_cards1, black_cards2, white_cards1, white_cards2

def make_selection(black_cards, white_cards, n=3):
    white_cards_num = random.sample(range(0, len(white_cards)), n)
    white_cards_selection = dict([(white_cards.keys()[i], white_cards[white_cards.keys()[i]]) for i in white_cards_num])
    
    black_cards_num = random.randint(0, len(black_cards)-1)
    black_cards_name = black_cards.keys()[black_cards_num]
    black_cards_selection = dict([(black_cards_name, black_cards[black_cards_name])])
    
    return black_cards_selection, white_cards_selection

def combine_quotes(bc_selection, wc_selection):
    bc_name = bc_selection.keys()[0]
    bc_quote = bc_selection[bc_name][random.randint(0, len(bc_selection[bc_name])-1)]
    question = {bc_name: bc_quote}

    answers = {}
    for person, quotes in wc_selection.iteritems():
        quote = quotes[random.randint(0, len(quotes)-1)]
        answers[person] = bc_quote.replace("___", quote).lower()

    return question, answers

def post_to_twitter(question, answers, time_start=5, time_end=10):
    from tweet import post_tweet, reply_tweet
    
    main_name = question.keys()[0]
    quote = question[main_name]
    reply_id = post_tweet(main_name + ": " + quote + " #codecampCC")
    sleep(random.randrange(time_start, time_end))
    
    names = []
    for name, quote in answers.iteritems():
        reply_tweet(name + ": " + quote, reply_id)
        names.append(name)
        sleep(random.randrange(time_start, time_end))

    rand_name = names[random.randint(0, len(names)-1)]
    reply_tweet(main_name + ": " + rand_name + " is the one that I like the most. Others are stupid.", reply_id)

def post_to_console(question, answers, time_start=5, time_end=10):  
    main_name = question.keys()[0]
    quote = question[main_name]
    print main_name + ": " + quote + " #codecampCC"
    sleep(random.randrange(time_start, time_end))
    
    names = []
    for name, quote in answers.iteritems():
        print name + ": " + quote
        names.append(name)
        sleep(random.randrange(time_start, time_end))

    rand_name = names[random.randint(0, len(names)-1)]
    print main_name + ": " + rand_name + " is the one that I like the most. Others are stupid."
    print

if __name__ == '__main__':
    from time import sleep

    black_cards1, black_cards2, white_cards1, white_cards2 = read_dataset()

    while 1:
        if random.random() > random.random():
            print "nonfictional vs fictional characters"
            black_cards, white_cards = black_cards1, white_cards1
        else:
            print "fictional vs nonfictional characters"
            black_cards, white_cards = black_cards2, white_cards2

        bc_selection, wc_selection = make_selection(black_cards, white_cards)
        question, answers = combine_quotes(bc_selection, wc_selection)
        #post_to_twitter(question, answers)
        #sleep(60)
        
        post_to_console(question, answers)
        sleep(5)

        
        



















    