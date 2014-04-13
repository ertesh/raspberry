from tkinter import *
from tkinter import ttk

class SimpleGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Feet to Meters")
        self.addInitialFrame()

    def clickRecord(self, *args):
        self.textField.insert(END, 'record\n')
    
    def clickGo(self, *args):
        self.textField.insert(END, 'go\n')

    def addInitialFrame(self):
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        self.textField = Text(mainframe, height=5)
        self.textField.grid(column=1, columnspan=2, row=1)
        ttk.Button(mainframe, text="Record", command=self.clickRecord).grid(column=1, row=2, sticky=N)
        ttk.Button(mainframe, text="Go", command=self.clickGo).grid(column=2, row=2, sticky=S)
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    gui = SimpleGUI()
    gui.run()