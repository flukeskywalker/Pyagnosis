from __future__ import print_function, division, unicode_literals
import threading
import inspect

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class BasePyagnosisWindow(object):
    def __init__(self, master=None, title=None, globals=globals(), locals=locals(), message=''):
        if master is None:
            self.main_win = tk.Tk()
            self.needs_mainloop = True
        else:
            if isinstance(master, BasePyagnosisWindow):
                master = master.main_win
            self.main_win = tk.Toplevel(master=master)
            self.needs_mainloop = False
        if title is None:
            title = "Pyagnosis"
        self.main_win.wm_title(title)

        self.globals = globals
        self.locals = locals

        self.main_win.geometry("640x480")

        currentrow = 0

        self.listlabel = tk.Label(master=self.main_win, text="The list:")
        self.listlabel.grid(row=currentrow, column=0, sticky=tk.W+tk.E)

        currentrow += 1

        self.fieldlist = tk.Listbox(master=self.main_win, font=("Courier", 10))
        self.fieldlist_scroller = tk.Scrollbar(master=self.main_win, command=self.fieldlist.yview, orient="vertical")
        self.fieldlist.grid(row=currentrow, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.fieldlist_scroller.grid(row=currentrow, column=1, sticky=tk.N+tk.S)
        self.fieldlist.bind("<Return>", self.fieldlist_enter)
        self.fieldlist.bind("<Double-Button-1>", self.fieldlist_enter)
        self.main_win.rowconfigure(currentrow, weight=1)

        currentrow += 1

        self.fieldlist_hscroller = tk.Scrollbar(master=self.main_win, command=self.fieldlist.xview, orient="horizontal")
        self.fieldlist_hscroller.grid(row=currentrow, column=0, sticky=tk.W+tk.E)
        self.fieldlist.configure(yscrollcommand=self.fieldlist_scroller.set)
        self.fieldlist.configure(xscrollcommand=self.fieldlist_hscroller.set)

        currentrow += 1

        self.evallabel = tk.Label(master=self.main_win, text="Eval area:")
        self.evallabel.grid(row=currentrow, column=0, sticky=tk.W+tk.E)

        currentrow += 1

        self.evalentry = tk.Entry(master=self.main_win)
        self.evalentry.grid(row=currentrow, column=0, sticky=tk.W+tk.E)
        self.evalentry.bind("<Return>", self.evalentry_enter)

        currentrow += 1

        self.evaltext = tk.Text(master=self.main_win, height=5)
        self.evaltext_scroller = tk.Scrollbar(master=self.main_win, command=self.evaltext.yview, orient="vertical")
        self.evaltext.grid(row=currentrow, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.evaltext_scroller.grid(row=currentrow, column=1, sticky=tk.N+tk.S)
        self.evaltext.configure(yscrollcommand=self.evaltext_scroller.set)
        self.evaltext.insert('1.0', message + '\n')
        self.main_win.rowconfigure(currentrow, weight=0)

        self.main_win.columnconfigure(0, weight=1)


    def fieldlist_enter(self, *whatever):
        x = self.fieldlist.get(self.fieldlist.curselection()[0])
        self.evalentry.delete(0, tk.END)
        self.evalentry.insert(0, x.split("|")[0].strip())
        self.evalentry_enter()

    def evalentry_enter(self, *whatever):
        cmd = self.evalentry.get()
        self.evaltext.insert(tk.END, str(eval(cmd, self.globals, self.locals)) + '\n')
        self.evaltext.yview_pickplace("end")

    def show(self):
        if self.needs_mainloop:
            self.main_win.mainloop()


class ScopePyagnosisWindow(BasePyagnosisWindow):
    def __init__(self, master=None, title=None, globals=globals(), locals=locals(), message=''):
        BasePyagnosisWindow.__init__(self, master=master, title=title, globals=globals, locals=locals, message=message)
        objects = dict(globals.items() + locals.items()) 
        maxlen = max([len(x) for x in objects.keys()])
        for varname in sorted(objects, key=str.lower):
            varvalue = objects[varname]
            self.fieldlist.insert(tk.END, varname.ljust(maxlen) + "  |  " + str(varvalue))
    
class ObjectPyagnosisWindow(BasePyagnosisWindow):
    def __init__(self, master=None, title=None, globals=globals(), locals=locals(), message='', target=None):
        attrnames = dir(target)
        if target is None or len(attrnames) == 0:
            pass
        else:
            objects = {}
            for attrname in attrnames:
                objects[attrname] = getattr(target, attrname)
                locals[attrname] = objects[attrname]
            BasePyagnosisWindow.__init__(self, master=master, title=title, globals=globals, locals=locals, message=message)
            maxlen = max([len(x) for x in objects.keys()])
            for varname in sorted(objects, key=str.lower):
                varvalue = objects[varname]
                self.fieldlist.insert(tk.END, varname.ljust(maxlen) + "  |  " + str(varvalue))
    

def test1():
    a = 1
    b = 2
    mywin = ScopePyagnosisWindow(message='Check this out', locals=locals(), globals=globals())
    mywin.show()

def test2():
    class X:
        a = 1
        b = 2 
        def f(self):
            pass
    mywin = ObjectPyagnosisWindow(message='Inspecting an object', locals=locals(), target=X())
    mywin.show()

if __name__ == "__main__":
    test1()
    test2()

