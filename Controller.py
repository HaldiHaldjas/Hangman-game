from GameTime import GameTime
from Model import Model
from View import View
from tkinter import simpledialog


class Controller:
    def __init__(self, db_name=None):  # Kui andmebaasil on nimi, kasutab seda, kui ei, siis None

        self.__view = View()  # self - fail, kus me praegu oleme
        self.__model = Model(self.__view)

        # siin loodud controllerit kasutame ka Views!
        if db_name is not None:  # kui DB nimi on olemas
            self.__model.database = db_name
        # mänguaja objekt
        self.__game_time = GameTime(self.__view.lbl_time)
        #  print(self.__model.database) käsurealt käivitamiseks


    def main(self):
        self.__view.main()

    # kutsume nupu kliki valja
    def button_scoreboard_click(self):
        window = self.__view.create_scoreboard_window()
        data = self.__model.read_data_from_database()
        self.__view.draw_scoreboard(window, data)

        # kui mäng lõppeb või alustatakse uuesti
    def buttons_no_game(self):
        self.__view.btn_new['state'] = 'normal'
        self.__view.btn_cancel['state'] = 'disabled'
        self.__view.btn_send['state'] = 'disabled'
        self.__view.char_input.delete(0, 'end')  # Kustutab sisestuskasti sisu
        self.__view.char_input['state'] = 'disabled'


    #  Mängu algus
    def buttons_to_game(self):
        self.__view.btn_new['state'] = 'disabled'
        self.__view.btn_cancel['state'] = 'normal'
        self.__view.btn_send['state'] = 'normal'
        self.__view.char_input['state'] = 'normal'
        self.__view.char_input.focus()

    # funktsioon uuele mängule
    def btn_new_click(self):
        self.buttons_to_game()  # Nupud aktiivseks
        # aja reset ja restart
        self.__game_time.reset()
        self.__game_time.start()
        self.__view.change_image(0)
        self.__model.play()
        self.__view.lbl_result['text'] = self.__model.guess
        self.__view.lbl_error['text'] = "Vigased tähed"



        # TODO Mängu pilt muuda esimeseks (ISESESIVALT TUNNIS KOHE) - tehtud
        # TODO Seadista mudelis uus mäng. Juhuslik sõna andmebaasist vaja kätte saada - tehtud
        # TODO Näita äraarvatavat sõna aga iga tähe asemel on allkriips. Kirjastiil on big_font
        # TODO Veateadete label muuda tekst "Vigased tähed:"



    def btn_cancel_click(self):
        self.__game_time.stop()  # Aeg seisma
        self.buttons_no_game()
        self.__view.change_image(len(self.__model.image_files) - 1)
        self.__view.lbl_result['text'] = 'Mängime!'.upper()

    def btn_send_click(self):
        guess = self.__model.play(self.__view.char_input())
        self.__view.lbl_result['text'] = "".join(self.__model.letters)
        self.__view.lbl_error['text'] = "Vigased tähed!"
        self.__view.change_image(self.__model.tries_list)

    def game_over(self):
        if self.__model.guessed:
            name = simpledialog.askstring("Mäng on läbi! Sisesta enda nimi: ")
            if name:
                self.__model.save_score(name, self.__game_time.counter)



        # TODO Loe sisestuskastist saadud info ja suuna mudelisse infot töötlema
        # TODO Muuda teksti tulemus aknas (äraarvatav sõna)
        # TODO Muuda teksti Vigased tähed
        # TODO Tühjenda sisestuskast (ISESEISVALT TUNNIS KOHE)
        # TODO KUI on vigu tekkinud, muuda alati vigade tekst punaseks ning näita vastavalt veanumbrile õiget pilti
        # TODO on mäng läbi. MEETOD siin samas klassis.

    # eraldi meetod
    # TODO Kontrollida kas mäng on läbi.# TODO JAH puhul peata mänguaeg
    # TODO Seadista nupud õigeks (meetod juba siin klassis olemas)
    # TODO Küsi mängija nime (simpledialog.askstring)
    # TODO Saada sisestatud mängija nimi ja mängu aeg sekundites mudelisse kus toimub kogu muu tegevus kasutajanimega
    # mänguaeg on muutujas self.__game_time.counter


"""
sisestuskastist huvitab vaid esimene märk. 
Võrdlemise hetkel peavad mõlemad olema ühtemoodi väikesed.
iga vale märgi korral peab vigade arv kasvama. 
"""





