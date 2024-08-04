import re
from random import randrange
import queue
import json
from os.path import join

words = []
users = {}
config = {}

def load_words():
    global words, config

    def has_cyrillic(text):
        return bool(re.search('[а-яА-Я]', text))

    file = open("words")
    unsorted = []

    for line in file.readlines():
        line_words = line.split()[:-1]
        unsorted.append({"key": line_words[0], "rus": [], "eng": []})

        for i in range(1, len(line_words)):
            if has_cyrillic(line_words[i]):
                unsorted[-1]["rus"] = " ".join(line_words[i:]).split(", ")
                unsorted[-1]["eng"] = " ".join([wrd for wrd in line_words[1:i] if not ")" in wrd and not "(" in wrd]).split(", ")
                break

    for word in unsorted:
        words.insert(randrange(0, len(words) + 1), word)

    with open(join("support", "config.json")) as file:
        config = json.load(file)


class User:
    words = {}
    now_word = ""
    now_lang = "eng"
    known_words = {"rus": [], "eng":[]}
    lang_changed = False
    id = ""

    def __init__(self, id) -> None:
        self.id = str(id)
        self.words = {"rus": queue.Queue(), "eng": queue.Queue()}

        if not self.id in config:
            for el in words:
                self.words["rus"].put(el["key"])
                self.words["eng"].put(el["key"])
        else:
            for el in words:
                if not el["key"] in config[self.id]["rus"]:
                    self.words["rus"].put(el["key"])
                if not el["key"] in config[self.id]["eng"]:
                    self.words["eng"].put(el["key"])
            self.known_words = config[self.id]


    def get_next(self):
        if self.lang_changed:
            self.lang_changed = False
            self.now_lang = "rus" if self.now_lang == "eng" else "eng"

        if self.words[self.now_lang].empty():
            return ""
        self.now_word = self.words[self.now_lang].get()
        for word in words:
            if word["key"] == self.now_word:
                return word[self.now_lang]


    def guess_word(self, guess):
        if not guess:
            self.words[self.now_lang].put(self.now_word)
        else:
            self.known_words[self.now_lang].append(self.now_word)

    def get_correct(self):
        trans_lang = "rus" if self.now_lang == "eng" else "eng"
        for word in words:
            if word["key"] == self.now_word:
                return word[trans_lang]
        return []
    
    def change_lang(self):
        self.lang_changed = True

    def save(self):
        config[self.id] = self.known_words
        with open(join("support", "config.json"), "w") as file:
            json.dump(config, file, indent=2)

    def get_known(self):
        rus = ""
        eng = ""
        lenght_rus = len(self.known_words["rus"])
        lenght_eng = len(self.known_words["eng"])

        for word in words:
            if lenght_rus + lenght_eng == 0: break
            if word["key"] in self.known_words["rus"]:
                rus += "\n" + ", ".join(word["rus"])
                lenght_rus -= 1
            if word["key"] in self.known_words["eng"]:
                eng += "\n" + ", ".join(word["eng"])
                lenght_eng -= 1

        return rus, eng
