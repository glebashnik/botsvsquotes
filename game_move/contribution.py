from scorer import similarity_score
from cards import cards



def score_contributions(quoter_contr, player_contr, max_or_min):
    
    """
    args:
    type(quoter_contr): str
    type(player_contr): list
    """    
    
    result_list = []
    
    for c in player_contr:
        result_list.append(similarity_score(quoter_contr, c))

    if max_or_min == "max":
        res = ''.join(max(result_list))
    else:
        res = ''.join(min(result_list))

    return res


def score_player(quoter, player_name, data_set):
    
    return [
            {
             ( quoter['name'], fills[0], "filler" ): score_contributions( quoter['filler'], fills[1], "min" ),
             ( quoter['name'], ctxt[0], "context" ): score_contributions( quoter['context'], ctxt[1], "max" )
             }
            for ctxt,fills in data_set
            if ctxt[0] == player_name
            ]



if __name__ == '__main__':
    
    #player_type = "fictional"
    #quoter_type = "real"
    
    import os

    player_name = "Don Corleone"
    quoter_name = "Stephen Hawking"

    test_quoter = {
              "name": "vader", 
              "context":"Don't underestimate the power of _", 
              "filler":"the Force"}
    
    # Load data
    black_card_file = os.path.join("..\\cards","fictional_black_cards.json")
    white_card_file = os.path.join("..\\cards","fictional_white_cards.json")
    black_card_dict = cards.load_cards_dict(black_card_file)
    white_card_dict = cards.load_cards_dict(white_card_file)
    data_set = zip(black_card_dict.items(), white_card_dict.items())

    print score_player(test_quoter, player_name, data_set)
    
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


