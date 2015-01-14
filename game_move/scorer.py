from pattern.vector import Document
from pattern.vector import distance
from pattern.text.en import sentiment, wordnet
import pandas
from os import path
import string

from gensim.models import Word2Vec

from nltk.stem.snowball import SnowballStemmer
stemmer_stem = SnowballStemmer("english").stem



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
    
    result_dict_contexts = {}
    result_dict_fillers = {}
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
      
    tmp_quoter_context = " ".join(uncontract(utt).lower() for utt in quoter_utt[0].split(" "))
    # Clean up punctuation characters
    tmp_quoter_context = "".join(char for char in tmp_quoter_context if char not in exclude)
    # Construct lists of words for quoter contexts
    tmp_quoter_context_list = [i for i in tmp_quoter_context.split(" ") if i]

    tmp_player_contexts_list = [
                               " ".join(uncontract(utt.lower())
                                    for utt in pl_utt[0].split(" ")) 
                               for pl_utt in player_utt_list
                               ]

    tmp_quoter_filler = " ".join(uncontract(utt).lower() for utt in quoter_utt[1].split(" "))
    # Clean up punctuation characters
    tmp_quoter_filler = "".join(char for char in tmp_quoter_filler if char not in exclude)
    # Construct lists of words for quoter contexts
    tmp_quoter_filler_list = [i for i in tmp_quoter_filler.split(" ") if i]

    tmp_player_fillers_list = [
                               " ".join(uncontract(utt.lower()) 
                                    for utt in pl_utt[1].split(" ")) 
                               for pl_utt in player_utt_list
                               ]

    for pl_utt in tmp_player_contexts_list:
        
        # Clean up punctuation characters
        pl_utt = "".join(char for char in pl_utt if char not in exclude)
        
        # Construct lists of words for player
        pl_utt_list = [i for i in pl_utt.split(" ") if i]

        res = 0.0
        try:
            res = trained_model.n_similarity(tmp_quoter_context_list, pl_utt_list)
        except:
            res = -1
        result_dict_contexts[(quoter_utt[0], pl_utt)] = res
    
    for pl_utt in tmp_player_fillers_list:

        # Clean up punctuation characters
        pl_utt = "".join(char for char in pl_utt if char not in exclude)
        
        # Construct lists of words for player
        pl_utt_list = [i for i in pl_utt.split(" ") if i]

        res = 0.0
        try:
            res = trained_model.n_similarity(tmp_quoter_filler_list, pl_utt_list)
        except:
            res = -1
        result_dict_fillers[(quoter_utt[1], pl_utt)] = res
         
    return result_dict_contexts, result_dict_fillers
    


def gensim_similarity_score_phraselist(quoter_utt, player_utt_list, trained_model):
    
    result_dict = {}
    
    def uncontract(s):
        return s[0:-2]+" not" if "n't" in s else s
      
    tmp_quoter_utt = " ".join(uncontract(utt).lower() 
                                    for utt in quoter_utt.split(" "))
    tmp_player_utt_list = [
                           " ".join(uncontract(utt).lower() 
                                    for utt in pl_utt.split(" ")) 
                           for pl_utt in player_utt_list
                           ]

    for pl_utt in tmp_player_utt_list:
        result_dict[(quoter_utt, pl_utt)] = trained_model.n_similarity(tmp_quoter_utt.split(" "), pl_utt.split(" "))

    return result_dict 
    

def gensim_similarity_score_wordlist(str_list1, str_list2, trained_model):
    
    results_dict = {}
    
    for s1 in str_list1:
        for s2 in str_list2:
            results_dict[trained_model.similarity(s1, s2)] = (s1,s2) 

    return results_dict


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


def load_anew_sentiment_scores():
    
    # Load anew scores
    anew = pandas.read_csv(
                       path.join("res","anew.csv"), 
                       usecols=[
                                    'Word','V.Mean.Sum','V.SD.Sum','V.Rat.Sum',
                                    'A.Mean.Sum','A.SD.Sum','A.Rat.Sum','D.Mean.Sum',
                                    'D.SD.Sum','D.Rat.Sum']
                       )

    anew = anew.drop_duplicates()

    anew.columns = [
                    'Word','VMeanSum','VSDSum',
                    'VRatSum','AMeanSum',
                    'ASDSum','ARatSum',
                    'DMeanSum','DSDSum','DRatSum'
                    ]

    return anew


def anew_sentiment_score(scores, input_list):
    
    ## Initialise a pandas DataFrame, with a single column for "word"
    input_dataframe = pandas.DataFrame.from_records(input_list, columns=["word"])
    print input_dataframe
    
    for df in input_dataframe:
        
        # Stem and lowercase words in df
        df['word'].apply(lambda x: ''.join(u'%s' % stemmer_stem(x).lower()))
        


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



