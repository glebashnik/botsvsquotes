

def read_dataset():
    from cards.cards import load_cards_dict

    dataset_path = "cards/"
    black_cards = load_cards_dict(dataset_path + 'nonfictional_black_cards.json')
    white_cards = load_cards_dict(dataset_path + 'fictional_white_cards.json')
    return black_cards, white_cards

def make_selection(black_cards, white_cards, n=3):
    import random
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
        answers[person] = bc_quote.replace("___", quote)

    return question, answers

def post_to_twitter(question, answers):
    from tweet import post_tweet
    import random
    
    main_name = question.keys()[0]
    quote = question[main_name]
    post_tweet(main_name + ": " + quote + " #codecampCC")
    
    names = []
    for name, quote in answers.iteritems():
        post_tweet(name + ": " + quote)
        names.append(name)
        sleep(5)

    rand_name = names[random.randint(0, len(names)-1)]
    post_tweet(main_name + ": " + rand_name + " is the one I like the most. Others are stupid.")

if __name__ == '__main__':
    from time import sleep
    

    black_cards, white_cards = read_dataset()

    while 1:
        bc_selection, wc_selection = make_selection(black_cards, white_cards)
        question, answers = combine_quotes(bc_selection, wc_selection)
        post_to_twitter(question, answers)



        #print "black_cards", bc_selection.keys()
        #print "white_cards", wc_selection.keys()
        #print 

        sleep(60)
        



















    