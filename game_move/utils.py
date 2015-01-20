# -*- coding: utf-8 -*-

"""
Some NLP tools.

* NLG:
  (1) Surface realisation
      (a) Tool for handling case sensitive pronouns, 
          ensuring for case form is correctly matches 
          the larger context in which they occur. 
      (b) Tool for handling names (i.e. retains capitalisation
          patterns for names).
      (c) TODO: create a tool for handling compounds.
  (2) Some miscellaneous tools, mostly helper functions for the scorer.
"""


import re, string
from pattern.text.en import parsetree, parser

# Create a list of characters to remove from output
## TODO: Possible way of ignoring hyphens (to properly render compounds, etc): 
### re.sub("-","",string.punctuation+unicode("”", 'utf-8'))
exclude = string.punctuation+unicode("”", 'utf-8')



"""
Various one-off tools for cleaning up surface forms
"""

def uncontract(s):
    res = ""
    if "n't" in s.lower():
        res = s[0:-3]+" not"
    elif "'m" in s.lower():
        res = s[0:-2]+" am"
    else:
        res = s
    return res


def prep_quote(quote_list):
    
    res = " ".join(uncontract(utt) for utt in quote_list.split(" "))
    # Clean up punctuation characters
    res = "".join(char for char in res if char not in set(exclude))
    # Construct lists of words for quote contexts
    res_list = [i for i in res.split(" ") if i]

    return res_list


def prep_plyr_ctxts_fills(plyr_list):

    ctxt = [
            " ".join(
                     uncontract(utt)
                     for utt in pl_utt[1].split(" ")
                     )
            for pl_utt in plyr_list
            ]
    
    fill = [
            " ".join(
                     uncontract(utt)
                     for utt in pl_utt[1].split(" ")
                     )
            for pl_utt in plyr_list
            ]

    return ctxt, fill


def prep_plyr_contr(plyr_utt):
    
    # Clean up punctuation characters
    pl_utt = "".join(char for char in plyr_utt if char not in set(exclude))
        
    # Construct lists of words for player
    return [i for i in pl_utt.split(" ") if i]



"""
More comprehensive surface modifications, for the player fillers.
"""
class Surface_Tweaker(object):
    
    def __init__(self, player_filler, quote_context, quote_filler):
        self.player_filler = player_filler
        self.quote_context = quote_context
        self.quote_filler = quote_filler
        self.PATTERN_LEXICON = parser.lexicon

        # Collection of case sensitive personal pronouns in English
        self.CASE_SENSITIVE_PRON_DICT = {
                                    1: {
                                        "s": {
                                              "subj":"i",
                                              "obj":"me"
                                              },
                                        "p": {
                                              "subj:":"we",
                                              "obj":"us"
                                              }
                                        },
                                    3: {
                                        "s_m": {
                                                "subj":"he",
                                                "obj":"him"
                                                },
                                        "s_f": {
                                                "subj":"she",
                                                "obj":"her"
                                                },
                                        "p": {
                                              "subj":"they",
                                              "obj":"them"
                                              }
                                        }
                                    }
        
        # Convert dictionary to lists, one each for 1st person vs. 3rd person pronouns
        PRON_DICT2LIST_1 = [ d.values() for d in self.CASE_SENSITIVE_PRON_DICT[1].values() ]
        self.PRON_LIST_1 = [ e for ent in PRON_DICT2LIST_1 for e in ent ]
        PRON_DICT2LIST_3 = [ d.values() for d in self.CASE_SENSITIVE_PRON_DICT[3].values() ]
        self.PRON_LIST_3 = [ e for ent in PRON_DICT2LIST_3 for e in ent ]
                
        # Determine role of filler
        self.role = self.filler_role(self.quote_context, self.quote_filler)
                
        
    # Make output form
    def make_filler(self):

        res = self.handle_names(
                                parsetree(self.player_filler)
                                )
        res = self.handle_case_sensitive_pronoun( 
                                                 parsetree(res), 
                                                 self.role
                                                 )
        # TODO: at the moment, we can end up with examples like "characterbuilding",
        ## which is an unhyphenated compound
        #res = self.detect_compounds(
        #                           parsetree(res)
        #                           )
        
        return res


    # Work out semantic role for the player's filler, based on the quote filler 
    def filler_role(self, quote_context, quote_filler):
        for sent in parsetree(re.sub("_+", quote_filler, quote_context), relations=True):
            for c in sent.constituents(pnp=True):
                if quote_filler in c.string:
                    if c.role=="Subj":
                        return "Subj" 
                    else:
                        return "NonSubj" #Including objects of prepositions 
        return
    
    
    # Handler function for the case sensitive pronouns
    def handle_case_sensitive_pronoun(self, filler_parsetree, role):
    
        res = []
    
        for s in filler_parsetree:
            for c in s:#.constituents(pnp=True):
                if (c.string in set(exclude)):
                    pass#remove punctuation
                elif (c.type=="PRP") or (c.type=="NN" and c.string=="i"):
                    if (c.string in self.PRON_LIST_1):
                        if role == "Subj":#switch to subject case
                            if c.string.lower() == "i": 
                                res.append(c.string.upper())
                            elif c.string.lower() == "me": 
                                res.append(self.CASE_SENSITIVE_PRON_DICT[1]["s"]["subj"])
                        elif role == "NonSubj":#switch to non-subject case
                            if c.string.lower() == "i": 
                                res.append(self.CASE_SENSITIVE_PRON_DICT[1]["s"]["obj"])
                            elif c.string.lower() == "me":
                                res.append(c.string.lower())
                    elif (c.string in self.PRON_LIST_3):
                        if role == "Subj":#switch to subject case
                            if c.string.lower() == "he": 
                                res.append(c.string.lower())
                            elif c.string.lower() == "him": 
                                res.append(self.CASE_SENSITIVE_PRON_DICT[3]["s_m"]["subj"])
                            if c.string.lower() == "she": 
                                res.append(c.string.lower())
                            elif c.string.lower() == "her": 
                                res.append(self.CASE_SENSITIVE_PRON_DICT[3]["s_f"]["subj"])
                            if c.string.lower() == "they": 
                                res.append(c.string.lower())
                            elif c.string.lower() == "them": 
                                res.append(self.CASE_SENSITIVE_PRON_DICT[3]["p"]["subj"])
                        elif role == "NonSubj":#switch to non-subject case
                            if c.string.lower() == "he": 
                                res.append(self.CASE_SENSITIVE_PRON_DICT[3]["s_m"]["obj"])
                            elif c.string.lower() == "him": 
                                res.append(c.string.lower())
                            if c.string.lower() == "she": 
                                res.append(self.CASE_SENSITIVE_PRON_DICT[3]["s_f"]["obj"])
                            elif c.string.lower() == "her": 
                                res.append(c.string.lower())
                            if c.string.lower() == "they": 
                                res.append(self.CASE_SENSITIVE_PRON_DICT[3]["p"]["obj"])
                            elif c.string.lower() == "them": 
                                res.append(c.string.lower())
                    else:
                        res.append(c.string)
                else: 
                    res.append(c.string)
        
        # Remove null entries in list of words 
        res = [r for r in res if r]
        return " ".join("%s" % r for r in res)


    def handle_names(self, filler_parsetree):
        
        res = []
        
        for s in filler_parsetree:
            for c in s:#.constituents(pnp=True):
                if (c.string in set(exclude)):
                    pass#remove punctuation
                elif (c.type=="NNP"):
                    res.append(c.string[0].upper() + c.string[1:])
                else:
                    res.append(c.string.lower())
        
        # Remove null entries in list of words 
        res = [r for r in res if r]
        return " ".join("%s" % r for r in res)


#    def detect_compounds(self, filler_parsetree):
#        
#        res = []
#        
#        for s in filler_parsetree:
#            for c in s:#.constituents(pnp=True):
#                start = 0
#                for idx in range(len(c.string)+1):
#                    check = c.string[start:idx]
#                    for k,v in parser.lexicon.items():
#                        if (len(k)>2) and (check == k):
#                            print k,v
#                            start = idx
#                            idx = -1



if __name__ == '__main__':
    
    print Surface_Tweaker("characterbuilding", "all you need is __", "love").make_filler()

