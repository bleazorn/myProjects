from tkinter import *
import tkinter as tk
from tkinter import ttk

from gui.frameSuper import frameSuper


class GraphFrame(frameSuper):
    def __init__(self, parent, data, loc=None):
        row = 0
        col = 0
        if loc and type(loc) is tuple and len(loc) == 2:
            row = loc[0]
            col = loc[1]
