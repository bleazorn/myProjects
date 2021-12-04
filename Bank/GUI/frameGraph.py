from tkinter import *

from tkcalendar import DateEntry
from babel.numbers import *
from GUI.frameSuper import FrameSuper

from datetime import date
from dateutil.relativedelta import relativedelta


class GraphSuper(FrameSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

    def create(self):
        pass


