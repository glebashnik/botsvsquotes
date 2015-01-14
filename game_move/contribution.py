from scorer import gensim_similarity_score_full
from cards import card
from os import path
import operator
import string 

from gensim.models import Word2Vec
from cards.io import load_cards_dict
from numpy import character



class Contribution(object):
    
    def __init__(self, path_to_model, player_name, player_data):
        self.traind_model = self.load_model(path_to_model)
        self.player_ref = player_name
        self.player_data_set = player_data
        self.player_full_list = [
                                 ctxts_fills 
                                 for ctxt,fills in self.player_data_set
                                 for ctxts_fills in zip(ctxt[1], fills[1])
                                 if ctxt[0] == self.player_ref
                                 ]

    
    def load_model(self, path_to_model):
        return Word2Vec.load(trained_medium_model_path)


    def score_contributions(self, quoter_contrib, player_contrib):
        
        """
        args:
        type(quoter_contr): str
        type(player_contr): list
        """    

        return gensim_similarity_score_full(quoter_contrib, player_contrib, self.traind_model)


    def score_player(self, quoter):
        
        return {
                quoter['name']: self.score_contributions( [quoter['context'], quoter['filler']], self.player_full_list )
                }

    
    def humourise(self, contrs_object):
        
        plyrs_scores_dict = {}        
        exclude = set(string.punctuation)
        
        def uncontract(s):
            res = ""
            if "n't" in s:
                res = s[0:-3]+" not"
            elif "'m" in s:
                res = s[0:-2]+" am"
            else:
                res = s
            return res
        
        def minmax(val1, val2):
            return min(val1, val2), max(val1, val2)
    
        for plyr in self.player_full_list:
            (ctx,fill) = plyr
            
            ctx = " ".join(uncontract(c).lower() for c in ctx.split(" "))
            # Clean up punctuation characters
            ctx = "".join(char for char in ctx if char not in exclude)
            # Construct lists of words
            ctx = " ".join([i for i in ctx.split(" ") if i])
            
            fill = " ".join(uncontract(c).lower() for c in fill.split(" "))
            # Clean up punctuation characters
            fill = "".join(char for char in fill if char not in exclude)
            # Construct lists of words
            fill = " ".join([i for i in fill.split(" ") if i])

            for contr in contrs_object.items():
                for c_k1,c_v1 in contr[1][0].items():
                    for f_k2,f_v2 in contr[1][1].items():
                        if ctx in c_k1[1].strip(" "):
                            if fill in f_k2[1].strip(" "):
                                plyrs_scores_dict[(ctx,fill)] = (c_v1,f_v2)
        
        min_f = sorted(plyrs_scores_dict.items(), key=operator.itemgetter(1), reverse=True)
        
        return min_f[0][0][1]

    
    def printer(self, quoter_info, contrs_object):
        print "Quoter:",test_quoter["name"]
        print "Context:",test_quoter["context"]
        for contr in contrs_object.items():
            print "\nPlayer contexts:"
            for k,v in contr[1][0].items():
                print k[1],"=",v
            print "\nPlayer fills:"
            for k,v in contr[1][1].items():
                print k[1],"=",v


if __name__ == '__main__':
    
    #player_type = "fictional"
    #quoter_type = "real"
    
    player_name = "Adam Sandler"
    quoter_name = "Aristotle"

    test_quoter = {
              "name": "vader", 
              "context":"Don't underestimate the power of _", 
              "filler":"the Force"}
    
    # Load data
    card_dict = load_cards_dict()
    black_cards = {character: [card.black_string() for card in cards] for character, cards in card_dict.iteritems()}
    white_cards = {character: [card.white_string() for card in cards] for character, cards in card_dict.iteritems()}
    data_set = zip(black_cards.items(), white_cards.items())    

    # Load models
    trained_medium_model_path = path.join("E:\Dropbox\Data\WordVecModels","w2v_103.model")
    trained_medium_model = Word2Vec.load(trained_medium_model_path)
    #trained_big_model_path = path.join("E:\Dropbox\Data\WordVecModels","1-billion-word-language-modeling-benchmark-r13output.bin.gz")
    #trained_big_model = Word2Vec.load_word2vec_format(trained_big_model_path, binary=True)
    
    contrs = Contribution(trained_medium_model_path, player_name, data_set)
    scoring_results = contrs.score_player(test_quoter)
    
    # Print results
    #contrs.printer(test_quoter, scoring_results)

    # Humourise
    print "Vader poses the quote:",test_quoter["context"]
    print player_name,"replies with:",contrs.humourise(scoring_results)

    
"""
Testing:

    test_player_name = "corleone"
    test_players = [
               {
               "name": "corleone", 
               "quotes":[
                         {"context":"A man who doesn't spend time with _ can never be a real man.", "filler":"his family"}
                         ]
               },
               {
               "name": "batman", 
               "quotes": [
                          {"context": "You're not _", "filler": "the devil"}
                          ]
               }
              ] 
    test_res = [
           {
           "contexts": score_contexts(quotes["context"], test_quoter["context"]),
           "fillers": score_fillers(quotes["filler"], test_quoter["filler"])
           }
           for player in test_players
           for quotes in player["quotes"]
           if test_player_name == player["name"]
           ]
    #print test_res

"""


