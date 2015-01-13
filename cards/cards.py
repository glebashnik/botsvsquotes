import json
from input_parser.parser import file_parser
from pattern.text.en import parsetree


def extract_cards(quote):
    black_cards = []
    white_cards = []
    parsed = parsetree(quote, chunks=True)

    for sentence in parsed:
        for chunk in sentence.chunks:
            if chunk.type == "NP":
                white_cards.append(chunk.string)

                before = sentence.slice(0, chunk.start).string
                after = sentence.slice(chunk.stop, len(sentence)).string
                black_card = before + " ___ " + after
                black_cards.append(black_card)

    return black_cards, white_cards


def extract_cards_dict(quotes_dict):
    black_cards_dict = {}
    white_cards_dict = {}

    for name, quotes in quotes_dict.iteritems():
        black_cards_dict[name] = []
        white_cards_dict[name] = []

        for quote in quotes:
            black_cards, white_cards = extract_cards(quote)
            black_cards_dict[name].extend(black_cards)
            white_cards_dict[name].extend(white_cards)

    return black_cards_dict, white_cards_dict


def load_cards_dict(path):
    with open(path, 'r') as infile:
        return json.load(infile)

if __name__ == '__main__':
    quotes = file_parser()

    (fictional_black_cards, fictional_white_cards) = extract_cards_dict(quotes.movie_characters)

    with open('fictional_black_cards.json', 'w') as outfile:
        json.dump(fictional_black_cards, outfile)

    with open('fictional_white_cards.json', 'w') as outfile:
        json.dump(fictional_white_cards, outfile)

    (nonfictional_black_cards, nonfictional_white_cards) = extract_cards_dict(quotes.people)

    with open('nonfictional_black_cards.json', 'w') as outfile:
        json.dump(nonfictional_black_cards, outfile)

    with open('nonfictional_white_cards.json', 'w') as outfile:
        json.dump(nonfictional_white_cards, outfile)

    print load_cards_dict('fictional_black_cards.json')