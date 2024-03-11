# kontruktor, käivitamine,
import time


class GameTime:
    def __init__(self, lbl_time):
        self.__lbl_time = lbl_time
        self.__counter = 0  # aeg hakkab 0-iga peale
        self.__running = False

    @property
    def counter(self):
        return self.__counter
    # Et saaks ajale ligi ja andmebaasi kirjutada

    def update(self):
        if self.__running:
            if self.__counter == 0:
                display = '00:00:00'
            else:
                # kui aeg läheb käima
                # https://www.studytonight.com/python-howtos/how-to-convert-seconds-to-hours-minutes-and-seconds-in-python
                display = time.strftime('%H:%M:%S', time.gmtime(self.__counter))  # hetke manguaeg

            self.__lbl_time['text'] = display
            self.__lbl_time.after(1000, self.update)
            self.__counter += 1
            # mujal vaja start, stop ja reset

    def start(self):
        self.__running = True
        self.update()

    def stop(self):
        self.__running = False

    def reset(self):
        self.__counter = 0
        self.__lbl_time['text'] = '00:00:00'





