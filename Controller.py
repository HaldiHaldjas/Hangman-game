from tkinter import simpledialog

from GameTime import GameTime
from Model import Model
from View import View


class Controller:
    def __init__(self, db_name=None):
        self.__model = Model()
        self.__view = View(self, self.__model)
        if db_name is not None:
            self.__model.database = db_name
        self.__game_time = GameTime(self.__view.lbl_time)
        #  print(self.__model.database) käsurealt käivitamiseks

    def main(self):
        self.__view.main()

    # kutsume nupu kliki valja
    def button_scoreboard_click(self):
        window = self.__view.create_scoreboard_window()
        data = self.__model.read_scores_from_database()
        self.__view.draw_scoreboard(window, data)
        print(data)

    # I - kui mäng kuvatakse või alustatakse uuesti
    def buttons_no_game(self):
        self.__view.btn_new['state'] = 'normal'
        self.__view.btn_cancel['state'] = 'disabled'
        self.__view.btn_send['state'] = 'disabled'
        self.__view.char_input.delete(0, 'end')  # Kustutab sisestuskasti sisu
        self.__view.char_input['state'] = 'disabled'
        self.__view.change_image(0)

    #  II -
    def buttons_game(self):
        self.__view.btn_new['state'] = 'disabled'
        self.__view.btn_cancel['state'] = 'normal'
        self.__view.btn_send['state'] = 'normal'
        self.__view.char_input['state'] = 'normal'
        self.__view.char_input.focus()

    # III - Mängu algus nupp "Uus mäng"
    def btn_new_click(self):
        self.buttons_game()  # Nupud aktiivseks
        # aja reset ja restart
        self.__game_time.reset()
        self.__game_time.start()

        self.__model.new_game()
        word_length = len(self.__model.word)
        initial_text = '_' * word_length
        self.__view.lbl_result['text'] = self.__model.correct_letters
        self.__view.lbl_error.config(text="")
        self.__view.change_image(0)
        # self.game_over()

    # IV - "Loobu" nupp
    def btn_cancel_click(self):
        self.__game_time.stop()  # Aeg seisma
        self.__view.change_image(-1)
        self.buttons_no_game()
        self.__view.lbl_result.config['text'] = 'Mängime!'.upper()

    # V - "Saada" nupp
    def btn_send_click(self):
        input_value = self.__view.char_input.get()
        self.__model.process_player_input(input_value)
        self.__view.char_input.delete(0, 'end')
        self.__view.lbl_result['text'] = "".join(self.__model.correct_letters).upper()
        # self.__view.lbl_error['text'] = f'Vigased tähed {self.__model.list_to_string(self.__model.wrong_letters)}'
        self.__view.lbl_error['text'] = f'Vigased tähed {self.__model.list_to_string(input_value)}'
        if self.__model.wrong_guesses > 0:
            self.__view.lbl_result['fg'] = 'red'
        self.__view.change_image(self.__model.wrong_guesses)
        self.game_over()

    def game_over(self):
        input = self.__view.char_input.get()
        game_over = False
        game_guessed = False
        if self.__model.word.lower() == self.__model.list_to_string(input):
        # if self.__model.word.lower() == self.__model.list_to_string(self.__correct_letters):
            game_guessed = True
            game_over = True

        if game_over:
            self.__game_time.stop()
            self.buttons_no_game()
            if game_guessed:
                name = simpledialog.askstring('Mäng läbi', 'Mäng läbi! \nSisesta mängija nimi:')
                if name:
                    self.__model.add_player_score(name, self.__game_time.counter)
        # if "".join(self.__model.correct_letters) == self.__model.word:
        #     self.btn_cancel_click()
        #     self.__view.show_message()
        #     self.__view.game_over()

