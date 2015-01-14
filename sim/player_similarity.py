__author__ = 'alm'

from input_parser.knowledge_parser import KB_parser
from gensim.models import *
from random import randint
import random
import numpy as np
import sys
import math
import operator

class Sim:
    POS = ("Positive Talking Points", True) # True --> comma-separated word-values in the field
    NEG = ("Negative Talking Points", True)
    WEAR = ("Seen Wearing", True)
    DO = ("Typical Activity", True)
    WEAPON = ("Weapon of Choice", True)
    GENRE = ("Genres", True)
    CAT = ("Category", True)

    W2V_SMALL = "../data/w2v_7.model"
    W2V_MEDIUM = "../data/w2v_103.model"
    W2V_BIG = "/home/alm/data/w2v-googlenews-corpus/GoogleNews-vectors-negative300.bin.gz"

    def __init__(self):
        #self.w2v = Word2Vec.load(self.W2V_SMALL) # word2vec model
        self.w2v = Word2Vec.load(self.W2V_MEDIUM)
        #self.w2v = Word2Vec.load_word2vec_format(self.W2V_BIG, binary=True)
        self.values_used = []
        self.values_used_features = {}

    def sim_val(self, player1, player2):
        result = self.sim(player1, player2)
        for feature in result.keys():
            if result[feature] == -1:
                del result[feature]

        return np.mean(result.values())

    def sim_avg(self, input):
        for feature in input.keys():
            if input[feature] == -1:
                del input[feature]

        return np.mean(input.values())

    def sim_cat_values(self, player1, player2, categories):
        result = self.sim_cat(player1, player2, categories)
        for feature in result.keys():
            if result[feature] == -1:
                del result[feature]

        return np.mean(result.values())

    def sim_cat(self, player1, player2, categories):
        return self.compare(player1, player2, categories)

    def sim(self, player1, player2):
        '''
        similarity function between two players based on w2v model measures the distance
        between the words found from the features of the players
        :param player1: dict of features of player 1
        :param player2: dict of features of player 2
        :return:
        '''

        return self.compare(player1, player2, [self.POS[0], self.NEG[0], self.CAT[0]])


    def compare(self, player1, player2, features):

        #print "Player 1:", player1["Character"]
        #print "Player 2:", player2["Character"]

        result = {}

        for feature in features:
            arr1 = player1.get(feature).split(",")
            arr2 = player2.get(feature).split(",")
            #print "FEATURE: "+feature
            sim_val = self.distance(arr1, arr2)
            self.values_used_features[feature]= self.values_used
            #print "SIMILARITY: "+str(sim_val)
            result[feature] = sim_val

        return result

    def distance(self, arr1, arr2):

        dists = []
        self.values_used = []

        for val in arr1: # all-all comparison of words + average
            val = val.lower()
            for val2 in arr2:
                val2 = val2.lower()
                try:
                    #print val+" <---> "+ val2+": "+str(self.w2v.similarity(val, val2))
                    dists.append(self.w2v.similarity(val, val2))
                    self.values_used = [(val,val2)]
                except:
                    #print val +" or "+val2+" not found"
                    pass

        if dists:
            return np.mean(dists)
        else:
            return -1

    def choose_players_random(self, manager, players, count):
        '''
        * choose randomly a feature to utilize
        * choose also similarity / dissimilarity aspect
        * TODO: fiction / non-fiction?

        :param manager: the game master, one with the template
        :param players: the player set
        :return:
        '''


        features = [self.POS[0], self.CAT[0], self.GENRE[0], self.NEG[0]]
        mname = manager["Character"]
        print mname +" is choosing players..."
        selected_features = []

        flen = len(features) # no of features
        f_count = randint(1, flen) # no of features to select
        for i in random.sample(range(0, flen),f_count):
            selected_features.append(features[i])

        print mname +" says: looking for following features: "+str(selected_features)

        pos = bool(random.getrandbits(1))
        
        if pos:
            print mname +" says: looking for "+str(count)+" players similar to me"
        else:
            print mname +" says: looking for "+str(count)+" players different than me"

        loop = 0
        player_sim_index =  {}
        print "PLAYERS", str(players)
        for candidate in players:
            similarity = self.sim_cat_values(manager, candidate, selected_features)
            if math.isnan(similarity):
                similarity = -1
            player_sim_index[loop] = similarity
            loop += 1
        sorted_index = sorted(player_sim_index.items(), key=operator.itemgetter(1))
        result = []

        print "COUNT NEG ", str(count*-1)
        if pos:
            print "--> POS"
            for tuple in sorted_index[count*-1:]:
                #print "TUPLE", tuple
                result.append(players[tuple[0]])
        else:
            print "--> NEG"
            for tuple in sorted_index[:count]:
                #print "TUPLE", tuple
                result.append(players[tuple[0]])

        for player in result:
            print player["Character"]


if __name__ == "__main__":
    k = KB_parser()
    n = 2
    #print "Got "+str(n)+" players: "+str(k.random_players(3))
    #for k.ge

    s = Sim()

    manager = k.random_manager()

    s.choose_players_random(manager, k.all_players(), n)
    sys.exit(0)

    for i in range(1,10):
        players = k.random_players(n)
        sim_values = s.sim(players[0], players[1])
        print "-----------------"
        print "SIM: " +str(sim_values)
        print "VALUES USED: "+str(s.values_used_features)
        print "SIMILARITY: " + str(s.sim_avg(sim_values))
        print "-----------------"

