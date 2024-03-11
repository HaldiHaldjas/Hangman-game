import glob
import random
import sqlite3
from datetime import datetime

from Score import Score


class Model:
    def __init__(self, view):
        self.__view = view
        self.__database = 'databases/hangman_words_ee.db'  # Andmebaas
        self.__database_en = 'databases/hangman_words_en.db'  # Ingliskeelne andmebaas
        # pip install Pillow - piltidega majandamiseks
        self.__image_files = glob.glob('images/*.png')  # List, mis sisaldab pilte

        # TODO juhuslik sõna
        self.__guess = []
        self.__word = []
        self.__tries = []
        self.__letter = []
        self.__guessed = False
        # TODO kõik sisestatud tähed (List)
        # TODO vigade lugeja (s.h. pildi id + muutuja)
        # TODO kasutaja leitud tähed (visuaal muidu on seal allkriips, mis tähed leitud, mis asendatud.
        # allkriips pole veel arvatud.
        # getterid tuleb teha
        # Mänguga seotud muutujad



    @property
    def database(self):
        return self.__database

    @property
    def database_en(self):
        return self.__database_en

    # getter piltide saamiseks
    @property
    def image_files(self):
        return self.__image_files

    @property
    def words_list(self):
        return self.__word

    @property
    def tries_list(self):
        return self.__tries

    @property
    def letters(self):
        return self.__letter

    @property
    def guess(self):
        return self.__guess

    def guessed_word(self):
        return self.__guessed

    @database.setter
    def database(self, value):
        self.__database = value

    @database.setter
    def database_en(self, value):
        self.__database_en = value

    def read_data_from_database(self):
        """
        Loeb andmebaasi tabeli edetabeli kirjeid
        :return:
        See on ametlik dokumentatsioon
        """

        connection = None
        connection_en = None

        try:
            connection = sqlite3.connect(self.__database)
            #  sql = 'SELECT * FROM scores ORDER BY seconds;'
            #  cursor = connection.execute(sql)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM scores ORDER BY seconds;')
            data = cursor.fetchall()  # lae kõik andmed
            #  kontroller sellest datast aru ei saa, kontrolleril ligipääs puudub, andmbebaasist saadud info pannakse listi.
            score_result = []
            for row in data:
                score_result.append(Score(row[1], row[2], row[3], row[4], row[5]))
                # nimi, aeg, , , sekundid

            # loeb andmebaasist eestikeelseid sõnu
            cursor.execute('SELECT word FROM words;')
            words_list = [row[0] for row in cursor.fetchall()]
            print(words_list)
            word = random.choice(words_list)

            # loeb andmebaasist inglisekeelseid sõnu
            connection_en = sqlite3.connect(self.__database_en)
            cursor_en = connection_en.cursor()
            cursor_en.execute('SELECT word FROM words')
            words_list_en = [row[0] for row in cursor_en.fetchall()]
            connection_en.close()
            print(words_list_en)
            word_en = random.choice(words_list_en)
            print(word_en)
            return score_result, word.upper(), word_en.upper()

        except sqlite3.Error as error:
            print(f'Viga andmebaasiga ühendumisel ({self.__database} or {self.__database_en}): {error}')

        finally:
            # tehakse alati
            if connection:
                connection.close()
            if connection_en:
                connection_en.close()

        # Meetod mis seadistab uue mängu
    def play(self):
        self.__guess = self.__view.char_input()
        word = self.read_data_from_database()
        # word_en = self.read_data_from_database()
        guessed_letters = []
        guessed_words = []
        word_complete = "_" * len(word)
        self.__guessed = False
        tries = 12
        while not self.__guessed and tries > 0:
            # guess view failist
            guess = self.__view.get_guess()
            # sisestuse kontroll
            if len(guess) == 1 and guess.isalpha():
                # kui mängija on tähte juba arvanud
                if guess in guessed_letters:
                    print("Sa oled seda tähte juba pakkunud", guess)
                    # kui tähte pole selles sõnas, jääb mänguvõimalusi vähemaks, liidetakse arvatud tähtede listi.
                elif guess not in word:
                    print(guess, "ei ole selles sõnas.")
                    tries -= 1
                    guessed_letters.append(guess)
                    # kui täht on õige, lisab arvatud tähtede listi
                else:
                    print("Tubli!", guess, "on sõnas olemas.")
                    guessed_letters.append(guess)
                    word_as_list = list(word_complete)
                    indices = [i for i, letter in enumerate(word) if letter == guess]
                    # asendab alakriipsud tähtedega
                    for index in indices:
                        word_as_list[index] = guess
                    word_complete = "".join(word_as_list)
                    if "_" not in word_complete:
                        guessed = True
            # kui mängija sisestab sõna, kontrollib vastavust - sama pikkus, abc
            elif len(guess) == len(word) and guess.isalpha():
                if guess in guessed_words:
                    print("Sa oled seda sõna juba pakkunud", guess)
                elif guess != word:
                    print(guess, "ei ole õige sõna.")
                    tries -= 1
                    guessed_words.append(guess)
                else:
                    self.__guessed = True
                    word_complete = word
                    print("Tubli!", guess, "ongi õige sõna!")

            else:
                print("Vigane sisestus!")

            # näita mängu hetkeiseisu
            self.__view.display_game_status(word_complete, guessed_letters, tries)

        if self.__guessed == True:
            print("Palju õnne, õige sõna ongi ", word)
        else:
            print("Mäng on läbi! Sul ei õnnestunud sõna ära arvata! Õige sõna oli ", word)
            self.__view.game_over()

    def save_score(self, name, game_time):
        name = name.strip()
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO scores (name, word, missing, seconds, date_time) VALUES (?, ?, ?, ?, ?)"
            connection.execute(sql, (name, self.__word, self.__letter, game_time, today))
            connection.commit()
        except sqlite3.Error as error:
            print('Viga andmebaasiga ühendumisel: {error}')
        finally:
            if connection:
                connection.close()


    # TODO Seadistab uue sõna äraarvamiseks


        # TODO Seadistab mõningate muutujate algväärtused (vaata ___init__ kolme viimast TODO. Neljas muutuja on eelmine
        # rida)
        # TODO Seadistab ühe muutuja nii et iga tähe asemel paneb allkiriipsu mida näidata aknas äraarvatavas sõnas (LIST)

        # TODO Meetod mis seadistab juhusliku sõna muutujasse
        # TODO Teeb andmebaasi ühenduse ja pärib sealt ühe juhusliku sõna ning kirjutab selle muutujasse

        # TODO kasutaja siestuse kontroll (Vaata COntrolleris btn_send_click esimest TODO)
        # TODO Kui on midagi sisestatud võta sisestusest esimene märk (me saame sisestada pika teksti aga esimene täht on
        # oluline!)
        # TODO Kui täht on otsitavas sõnas, siis asneda tulemuses allkriips õige tähega.
        # TODO kui tähte polnud, siis vigade arv kasvab +1 ning lisa vigane täht eraldi listi

        # TODO Meetod mis tagastab vigaste tähtede listi asemel tulemuse stringina. ['A', 'B', 'C'] => A, B, C

        # TODO Meetod mis lisab mängija ja tema aja andmebaasi (Vaata Controlleris viimast TODO rida)
        # TODO Võtab hetke/jooksva aja kujul AAAA-KK-PP TT:MM:SS (Y-m-d H:M:S)
        # TODO Kui kasutaja sisestas nime, siis eemalda algusest ja lõpust tühikud
        # TODO Tee andmebaasi ühendus ja lisa kirje tabelisse scores. Salvesta andmed tabelis ja sulge ühendus.



