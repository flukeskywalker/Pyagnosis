from __future__ import print_function, division, unicode_literals
import threading
import inspect

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class InspectorWindow(object):
    def __init__(self, objects, parent_inspector_window=None):
        if parent_inspector_window is None:
            self.main_win = tk.Tk()
        else:
            self.main_win = tk.Toplevel(master=parent_inspector_window.main_win)

        self.main_win.geometry("640x480")

        self.listbox = tk.Listbox(master=self.main_win, font="Courier")
        self.scroller = tk.Scrollbar(master=self.main_win, command=self.listbox.yview, orient="vertical")
        self.hscroller = tk.Scrollbar(master=self.main_win, command=self.listbox.xview, orient="horizontal")
        self.listbox.configure(yscrollcommand=self.scroller.set)
        self.listbox.configure(xscrollcommand=self.hscroller.set)

        self.listbox.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.scroller.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.hscroller.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.main_win.columnconfigure(0, weight=1)
        self.main_win.rowconfigure(0, weight=1)

        self.listbox.bind("<Return>", self.listbox_enter)

        maxlen = max([len(x) for x in objects.keys()])
        for varname in sorted(objects, key=str.lower):
            varvalue = objects[varname]
            self.listbox.insert(tk.END, varname.ljust(maxlen) + "  |  " + str(varvalue))

        if parent_inspector_window is None:
            self.main_win.mainloop()

    def listbox_enter(self, *whatever):
        print("yo")

class Inspector(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        iw = InspectorWindow(globals())


def test():
    #iw = InspectorWindow(globals())
    i = Inspector()
    i.start()
    print(raw_input('Whazzuuuup'))
    #i.join()


if __name__ == "__main__":
    test()