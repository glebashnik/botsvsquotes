import os

from cards.card import Card
from cards.io import save_cards
from pattern.text.en import parsetree


def is_filler(chunk):
    return chunk.type == "NP" and \
           len(chunk.string) > 3 and \
           chunk.head.type == "NN"


def extract_cards(quote):
    cards = []

    text = parsetree(quote)

    for sentence_index, sentence in enumerate(text.sentences):
        for chunk_index, chunk in enumerate(sentence.chunks):
            if is_filler(chunk):
                cards.append(Card(text, sentence_index, chunk_index))

    return cards


def by_character(cards):
    cards_by_character = {}

    for card in cards:
        cards_by_character.setdefault(card.character, []).append(card)

    return cards_by_character


if __name__ == '__main__':
    quotes_path = "../quotes/data/processed/"

    for file_name in os.listdir(quotes_path):
        print file_name

        with open(quotes_path + file_name) as r:
            cards = []

            for quote in r.readlines():
                cards.extend(extract_cards(quote.strip()))

            if len(cards) > 0:
                save_cards(cards, "data/" + file_name.replace(".txt", ".csv"))