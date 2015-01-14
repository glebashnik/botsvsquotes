from pattern.vector import Document
from pattern.vector import distance
from pattern.text.en import sentiment, wordnet
import pandas as pd
from os import path

from nltk.stem.snowball import SnowballStemmer
stemmer_stem = SnowballStemmer("english").stem


def similarity_score(s1, s2):

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
    anew = pd.read_csv(
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
    input_dataframe = pd.DataFrame.from_records(input_list, columns=["word"])
    
    for df in input_dataframe:
        
        # Stem and lowercase words in df
        df['word'].apply(lambda x: ''.join(u'%s' % stemmer_stem(x).lower()))
        


if __name__ == '__main__':
    contxt1 = "Don't underestimate the power of _"
    fill1 = "the Force".split(" ")
    contxt2 = "A man who doesn't spend time with _ can never be a real man."
    fill2 = "his family".split(" ")
    
    anew = load_anew_sentiment_scores()
    
    print anew_sentiment_score(anew, fill1)

