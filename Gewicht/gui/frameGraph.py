from tkinter import *
import tkinter as tk
from tkinter import ttk

from gui.frameSuper import FrameSuper


class GraphFrame(FrameSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)
