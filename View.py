from tkinter import *
from tkinter import ttk
import tkinter.font as font
from datetime import datetime
import time
from PIL import ImageTk, Image  # PIP install Pillow

class View(Tk):
    def __init__(self, controller, model):
        super().__init__()  # käitub nagu põhiaken
        self.__controller = controller
        self.__model = model

        # Kirjastiilid
        self.__big_font = font.Font(family='Courier', size=20, weight='bold')
        self.__default_font = font.Font(family='Verdana', size=12)
        self.__default_bold = font.Font(family='Verdana', size=12, weight='bold')

        # Põhiakna parameetrid
        self.__width = 555
        self.__height = 200
        self.title('Poomismäng')
        self.center(self, self.__width, self.__height)

        # kolm frame'i
        self.__frame_top, self.__frame_bottom, self.__frame_image = self.create_frames()

        # loome 4 nuppu
        self.__btn_new, self.__btn_cancel, self.__btn_send = self.create_buttons()
        # tekitame meetodi nuppude loomise funktsioonile
        # edetabeli nupp ei muutu

        # piltide kuvamine - viimane pilt esimesena
        self.__image = ImageTk.PhotoImage(Image.open(self.__model.image_files[len(self.__model.image_files) - 1]))
        self.__lbl_image = None

        # loome 4 silti
        self.__lbl_error, self.__lbl_time, self.__lbl_result = self.create_labels()

        # Sisestuskast teisel moel
        self.__char_input = Entry(self.__frame_top, justify='center', font=self.__default_font)
        self.__char_input['state'] = DISABLED
        self.__char_input.grid(row=1, column=1, padx=5, pady=2, sticky=EW)

        # Enter klahvi funktsionaalsus
        self.bind('<Return>', lambda event: self.__controller.btn_send_click())

    @property
    def btn_new(self):
        return self.__btn_new

    @property
    def btn_cancel(self):
        return self.__btn_cancel

    @property
    def btn_send(self):
        return self.__btn_send

    @property
    def char_input(self):
        return self.__char_input

    @property
    def lbl_time(self):
        return self.__lbl_time

    @property
    def lbl_result(self):
        return self.__lbl_result

    @property
    def lbl_error(self):
        return self.__lbl_error

    def main(self):
        self.mainloop()

    # ekraani laius, mis jagatakse 2 ja koordinaatidega pannakse keskele, tulemus täisarvuna
    @staticmethod
    def center(win, w, h):
        x = int((win.winfo_screenwidth() / 2) - (w / 2))
        y = int((win.winfo_screenheight() / 2) - (h / 2))
        win.geometry(f'{w}x{h}+{x}+{y}')

    def create_frames(self):
        top = Frame(self, height=50)
        bottom = Frame(self)
        image = Frame(top, bg='white', height=130, width=130)

        top.pack(fill=BOTH)
        bottom.pack(expand=True, fill=BOTH)
        image.grid(row=0, column=3, rowspan=4, padx=5, pady=5)
        # topi peale pandud asjad on gridiga
        # alguses pildikastike vasakul, kuna muud sisu pole
        return top, bottom, image

    def create_buttons(self):
        new = Button(self.__frame_top, text='Uus mäng', font=self.__default_font,
                     command=self.__controller.btn_new_click)
        cancel = Button(self.__frame_top, text='Loobu', font=self.__default_font, state=DISABLED,
                        command=self.__controller.btn_cancel_click)
        send = Button(self.__frame_top, text='Saada', font=self.__default_font,
                      command=self.__controller.btn_send_click, state=DISABLED)
        (Button(self.__frame_top, text='Edetabel',
               font=self.__default_font, command=self.__controller.button_scoreboard_click).
         grid(row=0, column=1, padx=5, pady=2, sticky=EW))

        new.grid(row=0, column=0, padx=5, pady=2, sticky=EW)
        cancel.grid(row=0, column=2, padx=5, pady=2, sticky=EW)
        send.grid(row=1, column=2, padx=5, pady=2, sticky=EW)
        return new, cancel, send

    def create_labels(self):
        # Entry label ei muutu kunagi
        (Label(self.__frame_top, text='Sisesta täht', anchor='w', font=self.__default_bold).
         grid(row=1, column=0, padx=5, pady=2, sticky=EW))
        error = Label(self.__frame_top, text='Vigased tähed', anchor='w', font=self.__default_bold)
        lbl_time = Label(self.__frame_top, text='00:00:00', font=self.__default_font)
        result = Label(self.__frame_bottom, text='Mängime'.upper(), font=self.__big_font)

        # kolm järgnevat labelit
        error.grid(row=2, column=0, columnspan=3, padx=5, pady=2, sticky=EW)
        lbl_time.grid(row=3, column=0, columnspan=3, padx=5, pady=2, sticky=EW)
        result.pack(padx=5, pady=2)  # pack, kuna on eraldi frame'i peal

        # Pildi paigutamine
        self.__lbl_image = Label(self.__frame_image, image=self.__image)
        self.__lbl_image.pack()

        return error, lbl_time, result

    def create_scoreboard_window(self):
        top = Toplevel(self)
        top.title('Edetabel')
        top_w = 500
        top_h = 180
        top.resizable(False, False)
        top.grab_set()  # Alumist akent klikkida ei saa
        top.focus()

        frame = Frame(top)
        frame.pack(fill=BOTH, expand=True)
        self.center(top, top_w, top_h)

        return frame

    def draw_scoreboard(self, frame, data):
        # argumedid sisse frame ja data ehk andmed, mis saab kontrollerist
        if len(data) > 0:  # kontrollib andmete olemasolu
            # Tabeli vaade
            my_table = ttk.Treeview(frame)

            # vertikaalne kerimisriba
            vsb = ttk.Scrollbar(frame, orient=VERTICAL, command=my_table.yview)
            vsb.pack(side=RIGHT, fill=Y)  # täitmine paremal, ülevalt alla
            my_table.configure(yscrollcommand=vsb.set)

            # Veergude id
            my_table['columns'] = ('name', "word", "missing", "seconds", "date_time")

            # Veergude seaded
            my_table.column('#0', width=0, stretch=NO)
            my_table.column('name', anchor='w', width=100)
            my_table.column('word', anchor='w', width=100)
            my_table.column('missing', anchor='w', width=100)
            my_table.column('seconds', anchor='center', width=100)
            my_table.column('date_time', anchor='center', width=100)

            # Tabeli päis (nähtav)
            my_table.heading('#0', text='', anchor='center')
            my_table.heading('name', text='Nimi', anchor='center')
            my_table.heading('word', text='Valed tähed', anchor='center')
            my_table.heading('missing', text='Sõna', anchor='center')
            my_table.heading('seconds', text='Kestvus', anchor='center')
            my_table.heading('date_time', text='Mängitud', anchor='center')

            # lisa info tabelisse
            x = 0
            for p in data:
                # aeg tuleb formaatida, et andmbaasi ja rakenduse aeg samad
                dt = datetime.strptime(p.time, '%Y-%m-%d %H:%M:%S').strftime('%Y.%m.%Y %T')
                sec = time.strftime('%T', time.gmtime(p.seconds))
                my_table.insert(parent='', index='end', iid=str(x), text='',
                                values=(p.name, p.word, p.missing, sec, dt))
                #  aega muudetakse iga kord, sest info on erinev

                x += 1

            my_table.pack(expand=True, fill=BOTH)

        # Muudame nuppude kasutamist
    def change_image(self, image_id ):  # pildi id = vigade number
        self.__image = ImageTk.PhotoImage(Image.open(self.__model.image_files[image_id]))
        self.__lbl_image.configure(image=self.__image)
        self.__lbl_image.image = self.__image






















