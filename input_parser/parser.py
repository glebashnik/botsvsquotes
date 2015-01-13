__author__ = 'alm'

class file_parser:

    _CHAR_FILE = "../data/characters_famous_lines.txt"
    _PEOPLE_FILE = "../data/people_famous_lines.txt"

    def __init__(self):
        self.movie_characters = {}
        self.people = {}
        self.load_files()

    def load_files(self):
        self.movie_characters = self.load_file(self._CHAR_FILE)
        self.people = self.load_file(self._PEOPLE_FILE)

    def load_file(self, file):
        result = {}

        characters = open(file, 'r')
        person = ""
        for line in characters.readlines():
            if line.startswith('#'): #person
                person = line.split('#')[1].strip()
                result[person] = []
            else: # assuming lines after character introduced
                result[person].append(line.rstrip())

        return result

if __name__ == "__main__":

    f = file_parser()
    print f.people
    print f.movie_characters






