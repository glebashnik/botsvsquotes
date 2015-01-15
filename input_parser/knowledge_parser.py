__author__ = 'alm'
# parsing the knowledge parser for Tony's NOC file

from cc_pattern import noc
from input_parser.parser import file_parser
import random
from random import randint

class KB_parser:

    def __init__(self):
        self.rows = noc.parse_rows(noc.NOC)
        self.people = file_parser()
        self.character_data = self.get_fictional()
        self.people_data = self.get_people()

    def get_people_from_kb(self, people):

        result = []
        for character in people:
            #print character
            for row in self.rows:
                if character == row["Character"]:
                    result.append(row)

        return result

    def get_fictional(self):
        '''
        fictional characters
        :return:
        '''
        return self.get_people_from_kb(self.people.movie_characters.keys())

    def get_people(self):
        '''
        real people
        :return:
        '''
        return self.get_people_from_kb(self.people.people.keys())

    def random_manager(self):
        count = len(self.people_data)
        return self.people_data[randint(0,count-1)]

    def random_players(self, count):
        size = len(self.character_data)
        result = []
        consumed = []
        for i in random.sample(range(0, size-1),count):
            result.append(self.character_data[i])
        return result

    def all_players(self, characters):
        return self.get_people_from_kb(characters)


if __name__ == "__main__":

    k = KB_parser()
    print "Got game manager: "+k.random_manager()["Character"]
    n = 3
    #print "Got "+str(n)+" players: "+str(k.random_players(3))
    print
    print "Got "+str(n)+" players:"
    #for k.ge
    '''
    for player in k.random_players(3):
        #print player["Character"]
        for feature in player:
            print "\t"+feature+": "+player[feature]
    '''


