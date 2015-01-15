from pattern.text import sentiment
from pattern.text.en import wordnet


def match_words(word1, word2):
    try:
        synset1 = wordnet.synsets(word1.lemma)[0]
        synset2 = wordnet.synsets(word2.lemma)[0]
        return wordnet.similarity(synset1, synset2)
    except:
        return 0


def match_chunks(words1, words2):
    return sum([max([match_words(w1, w2) for w1 in words1]) for w2 in words2])


def match_cards(czar_card, player_card):
    context_sim = match_chunks(czar_card.context_words(), player_card.chunk.words)
    chunk_sim = match_chunks(czar_card.chunk.words, player_card.chunk.words)

    czar_sentiment, _ = sentiment(czar_card.text)
    player_sentiment, _ = sentiment(player_card.text)

    return abs(czar_sentiment - player_sentiment) + context_sim - chunk_sim