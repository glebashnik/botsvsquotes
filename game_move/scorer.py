# -*- coding: utf-8 -*-

from pattern.vector import Document
from pattern.text.en import sentiment, wordnet
from os import path
import string
import utils
from gensim.models import Word2Vec

# Create a list of characters to remove from output
## TODO: Possible way of ignoring hyphens (to properly render compounds, etc): 
### re.sub("-","",string.punctuation+unicode("”", 'utf-8'))
exclude = string.punctuation+unicode("”", 'utf-8')



def gensim_similarity_score_full(quoter_utt, player_utt_list, trained_model):

    """
    args:
    type(quoter_utt) = (context, filler)
    type(player_utt_list) = list of (context, filler)
    type(trained_model) = gensim.models.Word2Vec instance
    
    returns tuple of dictionaries: 
        (1) (each quoter's and player's contexts): similarity score
        (2) (each quoter's and player's fillers): similarity score
    """
    
    contexts_dict = {}
    fillers_dict = {}

    # Clean up punctuation characters
    # Construct lists of words for quote contexts
    tmp_quoter_context_list = utils.prep_quote(quoter_utt[0])
    
    # Clean up punctuation characters
    # Construct lists of words for quote contexts
    tmp_quoter_filler_list = utils.prep_quote(quoter_utt[1])

    # Construct lists of words for player contexts and fillers
    tmp_player_contexts_list, tmp_player_fillers_list = utils.prep_plyr_ctxts_fills(player_utt_list)

    for pl_utt in tmp_player_contexts_list:
        
        # Clean up punctuation characters
        # Construct lists of words for player
        pl_utt_list = utils.prep_plyr_contr(pl_utt)

        res = 0.0
        try:
            res = trained_model.n_similarity(tmp_quoter_context_list, pl_utt_list)
        except:
            res = -1
        contexts_dict[(quoter_utt[0], pl_utt)] = res
    
    for pl_utt in tmp_player_fillers_list:

        # Clean up punctuation characters
        # Construct lists of words for player
        pl_utt_list = utils.prep_plyr_contr(pl_utt)

        res = 0.0
        try:
            res = trained_model.n_similarity(tmp_quoter_filler_list, pl_utt_list)
        except:
            res = -1
        fillers_dict[(quoter_utt[1], pl_utt)] = res
         
    return contexts_dict, fillers_dict



if __name__ == '__main__':
    quoter_contxt1 = "Don't underestimate the power of _"
    quoter_fill = "the Force"
    quoter_full = [quoter_contxt1, quoter_fill]
    contxt2 = "A man who doesn't spend time with _ can never be a real man."
    player_full_list = [
                        ("A man who doesn't spend time with his family can never be a real man.", "his family"),
                        ("Why do I deserve your generosity", "your generosity"), 
                        ("I'm gonna make him an offer he can't refuse.", "an offer he can't refuse"), 
                        ("You can act like a man! What's the matter with you?", "a real man")
                        ]

    #anew = load_anew_sentiment_scores()
    
    #anew_sentiment_score(anew, fill1)
    
    #trained_medium_model_path = path.join("E:\Dropbox\Data\WordVecModels","w2v_103.model")
    #trained_medium_model = Word2Vec.load(trained_medium_model_path)
    trained_big_model_path = path.join("E:\Dropbox\Data\WordVecModels","1-billion-word-language-modeling-benchmark-r13output.bin.gz")
    trained_big_model = Word2Vec.load_word2vec_format(trained_big_model_path, binary=True)
    
    #print gensim_similarity_score_phraselist(quoter_fill, player_fill_list, trained_model)
    (ctxts,fills) = gensim_similarity_score_full(quoter_full, player_full_list, trained_big_model)
    print "Contexts:"
    print "Quoter:",ctxts.items()[0][0][0]
    print "Player:"
    for k,v in ctxts.items():
        print k[1],"=",v
    print "\n"
    print "Fillers:"
    print "Quoter:",fills.items()[0][0][0]
    print "Player:"
    for k,v in fills.items():
        print k[1],"=",v


"""
BELOW ARE SOME EARLIER ATTEMPTS AT SIMILARITY FUNCTIONS, SHOULD EVENTUALLY BE DELETED.


def gensim_similarity_score_phraselist(quoter_utt, player_utt_list, trained_model):
    
    result_dict = {}
    
#    def uncontract(s):
#        return s[0:-2]+" not" if "n't" in s.lower() else s
      
    tmp_quoter_utt = " ".join(utils.uncontract(utt) 
                                    for utt in quoter_utt.split(" "))
    tmp_player_utt_list = [
                           " ".join(utils.uncontract(utt).lower() 
                                    for utt in pl_utt.split(" ")) 
                           for pl_utt in player_utt_list
                           ]

    for pl_utt in tmp_player_utt_list:
        result_dict[(quoter_utt, pl_utt)] = trained_model.n_similarity(tmp_quoter_utt.split(" "), pl_utt.split(" "))

    return result_dict 
    

def gensim_similarity_score_wordlist(str_list1, str_list2, trained_model):

    return {
            trained_model.similarity(s1, s2):(s1,s2)
            for s1 in str_list1
            for s2 in str_list2
            }


def pattern_similarity_score(s1, s2):

    d1 = Document(s1)#, type="rabbit")
    d2 = Document(s2)#, type="rabbit")
    
    #result = distance(d1.vector, d2.vector, method="euclidean")
    #result = distance(d1.vector, d2.vector, method="cosine")
    result = d1.similarity(d2) # (1 - cosine distance)
    result = "{0:.10f}".format(result)#round(res,10))
    
    return result


def wordnet_similarity_score(s1, s2):
    
    w_sim1 = wordnet.synsets(s1)[0]
    w_sim2 = wordnet.synsets(s2)[0]
    
    result = wordnet.similarity(w_sim1, w_sim2)
    result = "{0:.10f}".format(result)
    
    return result


def pattern_sentiment_score(s):
    
    return sentiment(s)
"""