import re

# Represents both black and white cards.
# text is a parsed quote
# sentence_index and chunk_index point to the filling.
class Card:
    def __init__(self, text, sentence_index, chunk_index):
        self.text = text
        self.sentence_index = sentence_index
        self.chunk_index = chunk_index

        self.sentence = text.sentences[sentence_index]
        self.chunk = self.sentence.chunks[chunk_index]

    # String with the blank for the black card
    def black_string(self):
        before_sentences = self.text.sentences[0:self.sentence_index]
        before_sentences_string = " ".join([sentence.string for sentence in before_sentences])

        after_sentences = self.text.sentences[self.sentence_index + 1:]
        after_sentences_string = " ".join([sentence.string for sentence in after_sentences])

        before = self.sentence.slice(0, self.chunk.start).string
        after = self.sentence.slice(self.chunk.stop, len(self.sentence)).string
        string = before_sentences_string + " " + before + " ___ " + after + " " + after_sentences_string
        return re.sub(r'\s([?.!;:,"](?:\s|$))', r'\1', string.replace(" '", "'")).strip()

    # String for the filling in the white card
    def white_string(self):
        return self.chunk.string

    def context_chunks(self):
        return [chunk for chunk in self.sentence.chunks if chunk != self.chunk]

    def context_words(self):
        return [[word for word in chunk.words] for chunk in self.context_chunks()]