import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab, ImageFont, ImageDraw, Image, ImageTk
import time
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
from googletrans import Translator
from functools import partial
import numpy
import random
import os

# Download tesseract and copy the path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

class Text:
    class CreateToolTip(object):
        def __init__(self, widget, text='widget info'):
            self.waittime = 100  # milliseconds
            self.wraplength = 150  # pixels
            self.widget = widget
            self.text = text
            self.widget.bind("<Enter>", self.enter)
            self.widget.bind("<Leave>", self.leave)
            self.widget.bind("<ButtonPress>", self.leave)
            self._id = None
            self.tw = None
        def enter(self, event=None):
            self.schedule()
        def leave(self, event=None):
            self.unschedule()
            self.hidetip()
        def schedule(self):
            self.unschedule()
            self._id = self.widget.after(self.waittime, self.showtip)
        def unschedule(self):
            _id = self._id
            self._id = None
            if _id:
                self.widget.after_cancel(_id)
        def showtip(self, event=None):
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 20
            # creates a toplevel window
            self.tw = Toplevel(self.widget)
            # Leaves only the label and removes the app window
            self.tw.wm_overrideredirect(True)
            self.tw.wm_geometry("+%d+%d" % (x, y))
            label = Label(self.tw, text=self.text, justify='left', background="white",relief='solid', borderwidth=1, wraplength=self.wraplength)
            label.pack(ipadx=1)
        def hidetip(self):
            tw = self.tw
            self.tw = None
            if tw:
                tw.destroy()

# UI
    def __init__(self, text):
        self.oriLangua = "Chinese"
        self.resultLangua = "Chinese"
        self.frame = LabelFrame(app, text="Language", width=260, height=100)
        self.frame.place(x=30, y=50)
        self.radio_buttons = list()
        radio_buttons_tool_tips = ("Mandarin","English","Japanese")
        for i, language in enumerate(("Chinese", "English", "Japanese")):
            btn = Radiobutton(self.frame, text=language, value=i + 1, command=partial(self.from_langua, language), variable=0)
            btn.place(x=10, y=int(i)*25)
            self.CreateToolTip(btn, radio_buttons_tool_tips[i])
            btn.deselect()
            self.radio_buttons.append(btn)
        self.radio_buttons[0].select()

        self.frame2 = LabelFrame(app, text="Language", width=260, height=100)
        self.frame2.place(x=400, y=50)
        self.radio_buttons2 = list()
        for j, language2 in enumerate(("Chinese", "English", "Japanese")):
            btn2 = Radiobutton(self.frame2, text=language2, value=j + 1, command=partial(self.to_langua, language2), variable=1)
            btn2.place(x=10, y=int(j) * 25)
            self.CreateToolTip(btn2, radio_buttons_tool_tips[j])
            btn2.deselect()
            self.radio_buttons2.append(btn2)
        self.radio_buttons2[0].select()

        self.message = Label(app, text="to")
        self.message.place(x=340, y=90)

        self.buttons = Button(app, text="Image", width=13, height=2, command=self.imageFile)
        self.buttons.place(x=30, y=200)

        self.transbtn = Button(app, text="Translate", width=10, height=1, command=self.translateAll)
        self.transbtn.place(x=30, y=260)
        self.transbtn['state'] = DISABLED

        self.clearbtn = Button(app, text="Clear", width=10, height=1, command=self.clearAll)
        self.clearbtn.place(x=130, y=260)
        self.clearbtn['state']=DISABLED

        self.oriFrame = LabelFrame(app, text="", width=310, height=200)
        self.oriFrame.place(x=30, y=300)

        self.resultFrame = LabelFrame(app, text="", width=310, height=200)
        self.resultFrame.place(x=350, y=300)

# Selected Language
    def from_langua(self, language):
        self.oriLangua = language
        print(self.oriLangua)

    def to_langua(self, language):
        self.resultLangua = language
        print(self.resultLangua)

    def theLanguage(self):
        if self.oriLangua == "Chinese" and self.resultLangua == "Chinese":
            ori = 'zh-cn'
            res = 'zh-cn'
            self.Trans(ori, res)
        elif self.oriLangua == "English" and self.resultLangua == "Chinese":
            ori = 'en'
            res = 'zh-cn'
            self.Trans(ori, res)
        elif self.oriLangua == "Japanese" and self.resultLangua == "Chinese":
            ori = 'ja'
            res = 'zh-cn'
            self.Trans(ori, res)
        elif self.oriLangua == "Chinese" and self.resultLangua == "English":
            ori = 'zh-cn'
            res = 'en'
            self.Trans(ori, res)
        elif self.oriLangua == "English" and self.resultLangua == "English":
            ori = 'en'
            res = 'en'
            self.Trans(ori, res)
        elif self.oriLangua == "Japanese" and self.resultLangua == "English":
            ori = 'ja'
            res = 'en'
            self.Trans(ori, res)
        elif self.oriLangua == "Chinese" and self.resultLangua == "Japanese":
            ori = 'zh-cn'
            res = 'ja'
            self.Trans(ori, res)
        elif self.oriLangua == "English" and self.resultLangua == "Japanese":
            ori = 'en'
            res = 'ja'
            self.Trans(ori, res)
        elif self.oriLangua == "Japanese" and self.resultLangua == "Japanese":
            ori = 'ja'
            res = 'ja'
            self.Trans(ori, res)


# Translate Button
    def translateAll(self):
        self.transbtn['state'] = DISABLED
        self.clearbtn['state'] = NORMAL
        self.theLanguage()

    def clearAll(self):
        self.transbtn['state'] = NORMAL
        self.clearbtn['state'] = DISABLED
        orignalMsg.destroy()
        resultMsg.destroy()

# Chinese Translate
    def Trans(self, ori, res):
        global orignalMsg
        global resultMsg
        translator = Translator()
        ori = ori
        res = res

        result = self.result
        self.chinese = translator.translate(result, src=ori, dest=res)
        orignalMsg = Label(self.oriFrame, text=self.result)
        orignalMsg.place(x=10, y=10)
        resultMsg = Label(self.resultFrame, text=self.chinese.text)
        resultMsg.place(x=10, y=10)

# Choose Image from file
    def imageFile(self):
        filename = filedialog.askopenfile(initialdir="/", title="Select Image", filetype=(("jpeg", "*.jpg"), ("All Files", "*.*")))
        filename = filename.name.split('/').pop()
        fileLabel = Label(app, text=filename)
        fileLabel.place(x=260, y=210)
        if(fileLabel.cget("text") is None):
            print("nothing")
        else:
            self.transbtn['state'] = NORMAL
        self.scanImage(filename)

# Scan Image
    def scanImage(self, image):
        img = cv2.imread(image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if(self.oriLangua == "Chinese"):
            self.result = pytesseract.image_to_string(img, lang="chi_sim")
            print(self.result)
        elif(self.oriLangua == "English"):
            self.result = pytesseract.image_to_string(img, lang="eng")
            print(self.result)
        elif (self.oriLangua == "Japanese"):
            self.result = pytesseract.image_to_string(img, lang="jpn")
            print(self.result)


def on_closing():
    if messagebox.askokcancel("Quit", "Quit Program?"):
        os._exit(0)
if __name__ == '__main__':
    app = Tk()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.title("Text Detection")
    app.geometry("693x545")
    app.resizable(False, False)
    Text(app)
    app.mainloop()