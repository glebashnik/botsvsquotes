import os
from cards.card import Card
from pattern.db import CSV, encode_utf8
from pattern.text import Text


def save_cards(cards, path):
    csv = CSV()

    for card in cards:
        csv.append((card.text.xml, card.sentence_index, card.chunk_index))

    csv.save(path)


def load_cards(path):
    csv = CSV.load(path)
    cards = []

    for text_xml, sentence_index, chunk_index in csv:
        text = Text.from_xml(encode_utf8(text_xml))
        card = Card(text, int(sentence_index), int(chunk_index))
        cards.append(card)

    return cards


def file_name_to_character_name(file_name):
    return file_name.replace(".csv", "").replace("'", '"').replace("_", " ")


def load_cards_dict(path="cards/data"):
    character_dict = {}

    for file_name in os.listdir(path):
        character = file_name_to_character_name(file_name)
        cards = load_cards(path + "/" + file_name)

        character_dict[character] = []

        for card in cards:
            character_dict[character].append(card)

    return character_dict


def load_character_names(path="cards/data"):
    return [file_name_to_character_name(file_name) for file_name in os.listdir(path)]


def load_character_cards(character_name, path="cards/data/"):
    return load_cards(path + character_name.replace(" ", "_").replace('"', "'") + ".csv")


if __name__ == '__main__':
    characters = load_character_names()

#    with open("characters.txt", "w") as w:
#        for character in characters:
#            w.write(character + "\n")

    print characters

    cards = load_character_cards("Alan Partridge")

    for card in cards:
        print card.black_string()
        print card.white_string()
        print