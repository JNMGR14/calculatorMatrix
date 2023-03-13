import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import numpy as np


class Calculator(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=10, **kwargs)
        ttk.Style().configure("TButton", font="TkFixedFont 12")
        self.pack(fill=X)

        self.input_variableF = ttk.StringVar()
        self.input_variableC = ttk.StringVar()

        self.input_variableF.set('0')
        self.input_variableC.set('0')

        self.mt1 = []
        self.mt2 = []
        self.frames = []

        if "bootstyle" in kwargs:
            self.bootstyle = kwargs.pop("bootstyle")
        else:
            self.bootstyle = None
            self.create_title_display()
            self.create_gen_pad()

    def create_title_display(self):
        digits = ttk.Label(
            master=self,
            font="TkFixedFont 14",
            text="Calculadora de matrices",
            bootstyle=self.bootstyle
        )
        digits.pack(pady=30)

    def create_gen_pad(self):
        container = ttk.Frame(master=self, padding=20, bootstyle=self.bootstyle)
        container.pack(fill=X, expand=YES)
        matrix = [
            "Ingrese filas:",
            self.input_variableF,
            "Ingrese columnas:",
            self.input_variableC,
        ]
        for j, textL in enumerate(matrix):
            container.columnconfigure(j, weight=1)
            container.rowconfigure(j, weight=1)
            if j % 2 == 0:
                lab = self.create_label(master=container, text=textL)
                lab.grid(row=0, column=j, sticky=EW, padx=10)
            else:
                entr = self.create_entry(master=container, obj=textL)
                entr.grid(row=0, column=j, sticky=EW, padx=10)

        cont = ttk.Frame(master=self, padding=2, bootstyle=self.bootstyle)
        cont.pack(fill=X, expand=YES)
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)
        btn = self.create_button(master=cont, text="Crear matrices")
        btn.grid(row=1, column=0, sticky=NS, padx=10)

    def create_operations_pad(self):
        container = ttk.Frame(master=self, padding=20, bootstyle=self.bootstyle)
        container.pack(fill=X, expand=YES)
        matrix = [
            "Suma de matrices",
            "Resta de matrices",
            "Multiplicacion escalar de matrices ",
            "Multiplicacion de matrices",
        ]

        for j, textL in enumerate(matrix):
            container.columnconfigure(j, weight=1)
            container.rowconfigure(j, weight=1)
            btn = self.create_button(master=container, text=textL)
            btn.grid(row=0, column=j, sticky=EW, padx=10)

    @staticmethod
    def create_entry(obj, master):
        return ttk.Entry(
            master=master,
            bootstyle=INFO,
            textvariable=obj
        )

    @staticmethod
    def create_label(master, text):
        return ttk.Label(
            master=master,
            text=text,
            bootstyle=INFO
        )

    def create_button(self, master, text):
        return ttk.Button(
            master=master,
            text=text,
            bootstyle=SECONDARY,
            command=lambda x=text: self.on_button_pressed(x),
            padding=8,
        )

    def on_button_pressed(self, txt):
        if txt in "Crear matrices":
            self.create_matrix()

    def create_matrix(self):
        x = int(self.input_variableC.get())
        y = int(self.input_variableF.get())

        for i in self.frames:
            i.destroy()
            self.mt1.clear()
            self.mt2.clear()

        main_cont = ttk.Frame(master=self, padding=20, bootstyle=self.bootstyle)
        main_cont.pack(fill=BOTH, expand=YES)

        mat0 = ttk.Frame(master=main_cont, padding=20, bootstyle=self.bootstyle)
        mat0.pack(side=RIGHT)
        mat1 = ttk.Frame(master=main_cont, padding=20, bootstyle=self.bootstyle)
        mat1.pack(side=LEFT)

        self.frames.append(main_cont)

        d = [[np.random.randint(-100, 100) for _ in range(x)] for _ in range(y)]
        for g in range(len(d)):
            for c in range(len(d[g])):
                e = ttk.Entry(mat0, width=3, justify='center')
                e.grid(row=g, column=c)
                e.insert(END, '{}'.format(d[g][c]))
                self.mt1.append(e)

        x = [[np.random.randint(-100, 100) for _ in range(x)] for _ in range(y)]
        for g in range(len(x)):
            for c in range(len(x[g])):
                e = ttk.Entry(mat1, width=3, justify='center')
                e.grid(row=g, column=c)
                e.insert(END, '{}'.format(x[g][c]))
                self.mt2.append(e)

        self.create_operations_pad()


if __name__ == "__main__":
    app = ttk.Window(
        title="Calculadora",
        themename="solar",
        size=(1850, 925),
        resizable=(True, True),
    )
    Calculator(app)
    app.mainloop()
