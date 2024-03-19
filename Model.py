import glob
import sqlite3
from datetime import datetime

from Score import Score


class Model:
    def __init__(self):
        self.__database = 'databases/hangman_words_ee.db'  # Andmebaas
        self.__image_files = glob.glob('images/*.png')  # List, mis sisaldab pilte
        # self.__correct_letters = ['_'] * len(self.__word)
        self.__word = ''
        self.__typed_letters = []
        self.__wrong_guesses = 0
        self.__wrong_letters = []
        self.__correct_letters = []

    @property
    def database(self):
        return self.__database

    @property
    def image_files(self):
        return self.__image_files

    @property
    def word(self):
        return self.__word

    @property
    def typed_letters(self):
        return self.__typed_letters

    @property
    def wrong_letters(self):
        return self.__wrong_letters

    @property
    def wrong_guesses(self):
        return self.__wrong_guesses

    @property
    def correct_letters(self):
        return self.__correct_letters

    @database.setter
    def database(self, value):
        self.__database = value

    def read_scores_from_database(self):
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            sql = 'SELECT * FROM scores ORDER BY seconds;'
            cursor = connection.execute(sql)
            data = cursor.fetchall()  # lae kõik andmed
            score_result = []
            for row in data:
                score_result.append(Score(row[1], row[2], row[3], row[4], row[5]))
            return score_result
            # nimi, aeg, , , sekundid

        except sqlite3.Error as error:
            print(f'Viga andmebaasiga ühendumisel ({self.__database}): {error}')

        finally:
            if connection:
                connection.close()

            # seadistab uue mängu
    def new_game(self):
        self.__wrong_guesses = 0
        self.__typed_letters = []
        # self.__correct_letters = []
        self.__wrong_letters = []
        self.__word = self.read_words_from_database()
        self.__correct_letters = len(self.__word) * '_'
        print(self.__word)
        # self.__correct_letters = list("_" * len(self.__random_word))

    def read_words_from_database(self):
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            # loeb andmebaasist eestikeelseid sõnu
            cursor = connection.cursor()
            cursor.execute('SELECT word FROM words order by random() limit 1;')
            word = cursor.fetchone()[0]
            cursor.close()
            return word
        except sqlite3.Error as error:
            print(f'Viga andmebaasiga ühendumisel ({self.__database}): {error}')

        finally:
            # tehakse alati
            if connection:
                connection.close()

        # Meetod mis seadistab uue mängu
    def process_player_input(self, text):
        if text:
            guess = text[0].strip().lower()
            self.__typed_letters.append(guess)
            word_letters = list(self.__word.lower())
            if guess in word_letters:
                for index, letter in enumerate(word_letters):
                    if guess == letter:
                        self.__correct_letters = list(self.correct_letters)
                        self.__correct_letters[index] = guess
            else:
                self.__wrong_guesses += 1
                if guess in self.__typed_letters and guess not in self.__wrong_letters:
                    self.__wrong_letters.append(guess)
                    print("valed tahed: ", self.__wrong_letters)

    @staticmethod
    def list_to_string(char_list):
        return ', '.join(str(char_list))

    def add_player_score(self, name, game_time):
        name = name.strip()
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connection = None
        wrong = "".join(self.list_to_string(char_list=self.__wrong_letters).upper())
        wrong_filtered = ''
        for char in wrong:
            if char.isalpha():
                wrong_filtered += char
        print("wrong", wrong)
        print("wrong_filtered", wrong_filtered)
        try:
            connection = sqlite3.connect(self.__database)
            sql = 'INSERT INTO scores (name, missing, word, seconds, date_time) VALUES (?, ?, ?, ?, ?);'
            # print(sql)
            cursor = connection.cursor()
            cursor.execute(sql, (
                name,
                self.list_to_string(wrong_filtered),
                self.__word,
                game_time,
                today))
            connection.commit()
        except sqlite3.Error as error:
            print(f'Viga andmebaasiga {self.__database} ühendamisel: {error}')
        finally:
            if connection:
                connection.close()
