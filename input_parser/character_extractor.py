__author__ = 'alm'

'''
replacement for old parser: parser the characters and
their quotes from the text files
'''

from cards import io
from random import randint
import random
from cc_pattern import noc
from sim.player_similarity import Sim

def get_random_captain():
    noc_character_data = noc.parse_rows(noc.NOC)
    count = len(noc_character_data)
    captain =  noc_character_data[randint(0,count-1)]
    return captain

def get_players():
    '''
    take names from quote data and get the corresponding noc character
    :return:
    '''
    noc_character_data = noc.parse_rows(noc.NOC)
    people = io.load_character_names()

    noc_selected = []

    for character in noc_character_data:
        name = character["Character"]
        if name in people:
            #print "got ", name
            noc_selected.append(character)

    return noc_selected

def get_random_players(players, count):

    result = []

    indices = random.sample(range(0, len(players)),count)
    for i in indices:
        #print players[i]["Character"]
        result.append(players[i]["Character"])

    return result


if __name__ == "__main__":

    captain = get_random_captain()
    players = get_players()
    #print captain
    #r_players = get_random_players(get_players(),5)
    #print r_players

    s = Sim()
    s.choose_players_random(captain, players, 5)


