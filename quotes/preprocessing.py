import os

last_character = ""

for raw_file_name in os.listdir("data/raw"):
    quotes = []

    with open("data/raw/" + raw_file_name) as r:
        lines = r.readlines()

        for line in lines:
            if line.find("http") == -1 and line.find("*") == -1 and line.find("{{") == -1 \
                    and 120 >= len(line) > 40 and line.find("<") == -1 and line.find("\\x") == -1:
                quotes.append(line)

    if len(quotes) > 0:
        with open("data/processed/" + raw_file_name.replace("clean_", ""), 'w') as w:
            for quote in quotes:
                w.write(quote)