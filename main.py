import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams
rcParams['text.usetex'] = True
rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

rcParams["font.family"] = "Latin Modern Roman"
matplotlib.use('TkAgg')


def center(win):  # Esta clase se encarga de centrar ventanas
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


# Esta clase genera ventanas emergentes especificamente para ingresos de datos para la multiplicacion escalar
class Popup(object):
    def __init__(self, master):
        top = self.top = ttk.Toplevel(master)
        top.geometry("400x200")
        center(top)
        self.value = None
        self.title = ttk.Label(top, text="Ingrese un escalar")
        self.title.pack()
        self.e = ttk.Entry(top)
        self.e.pack()
        self.content = ttk.Frame(top, padding=10)
        self.content.pack(fill=X, expand=YES)

        self.option = ttk.IntVar()

        self.content_child = ttk.Frame(self.content, padding=10)
        self.content_child.pack()

        self.rdbtn1 = ttk.Radiobutton(self.content_child, text='Matriz uno', variable=self.option, value=1)
        self.rdbtn1.grid(row=0, column=0, padx=10, pady=10)

        self.rdbtn2 = ttk.Radiobutton(self.content_child, text='Matriz dos', variable=self.option, value=2)
        self.rdbtn2.grid(row=0, column=1, padx=10, pady=10)

        self.b = ttk.Button(self.content_child, text='Continuar', command=self.cleanup, style=SUCCESS)
        self.b.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()


class Calculator(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=10, **kwargs)
        ttk.Style().configure("TButton", font="TkFixedFont 12")
        self.pack(fill=X)

        self.input_variableF = ttk.StringVar()
        self.input_variableC = ttk.StringVar()

        self.is_btn_created = False

        self.mt0 = []  # Arreglo de objetos de tipo Entry con los elementos de cada matriz
        self.mt1 = []  # Arreglo de objetos de tipo Entry con los elementos de cada matriz
        self.mt2 = []  # Arreglo de objetos de tipo Entry con los elementos de cada matriz

        self.textMatrix = np.empty([2, 2])

        self.symbolArit = ttk.Label()  # Variable para el simbolo de operacion

        self.frames = []  # Arreglo con contenedores principales
        self.frame_results = [ttk.Frame()]  # Arreglo con contenedores principales
        self.frames_child = []  # Arreglo con contenedores hijos de los contenedores principales
        self.buttons = []  # Arreglo con panel de controles de operaciones

        self.objet_pop = None  # Objeto para controlar las pop up

        if "bootstyle" in kwargs:  # Determinante de estilo
            self.bootstyle = kwargs.pop("bootstyle")
        else:
            self.bootstyle = None
            self.create_title_display()
            self.create_gen_pad()

    def create_title_display(self):  # Creador del titulo de la ventana
        digits = ttk.Label(
            master=self,
            font="TkFixedFont 14",
            text="Calculadora de matrices",
            bootstyle=self.bootstyle
        )
        digits.pack(pady=30)

    def create_gen_pad(self):  # Generador del panel principal de ingreso de datos
        container = ttk.Frame(master=self, padding=20, bootstyle=self.bootstyle)  # Frame contenedor del panel
        container.pack(fill=X, expand=YES)  # Caracteristicas del panel
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
            "Multiplicacion escalar de matrices",
            "Multiplicacion de matrices",
        ]

        for j, textL in enumerate(matrix):
            container.columnconfigure(j, weight=1)
            container.rowconfigure(j, weight=1)
            btn = self.create_button(master=container, text=textL)
            btn.grid(row=0, column=j, sticky=EW, padx=10)
            self.buttons.append(btn)

        self.buttons.append(container)
        self.is_btn_created = True

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

    def create_matrix(self):
        x = int(self.input_variableC.get())
        y = int(self.input_variableF.get())

        self.reset_elements()

        main_cont = ttk.Frame(master=self, padding=20, bootstyle=self.bootstyle)  # Contenedor principal de las matrices
        main_cont.pack(fill=X, expand=YES)

        main_cont.columnconfigure(0, weight=1)
        main_cont.rowconfigure(0, weight=1)
        mat0 = ttk.Frame(master=main_cont, padding=20, bootstyle=self.bootstyle)  # Matriz uno
        mat0.grid(row=0, column=0, padx=10)
        self.frames_child.append(mat0)

        main_cont.columnconfigure(1, weight=1)
        main_cont.rowconfigure(0, weight=1)
        label_simbol = ttk.Frame(master=main_cont, padding=4, bootstyle=self.bootstyle)
        label_simbol.grid(row=0, column=1, padx=10)
        labl = ttk.Label(master=label_simbol, text="?", font="TkFixedFont 33")
        labl.grid(row=0, column=1)
        self.frames_child.append(label_simbol)
        self.symbolArit = labl

        main_cont.columnconfigure(2, weight=1)
        main_cont.rowconfigure(0, weight=1)
        mat1 = ttk.Frame(master=main_cont, padding=20, bootstyle=self.bootstyle)  # Matriz dos
        mat1.grid(row=0, column=2, padx=10)
        self.frames_child.append(mat1)

        main_cont.columnconfigure(3, weight=1)
        main_cont.rowconfigure(0, weight=1)
        label_equals = ttk.Frame(master=main_cont, padding=4, bootstyle=self.bootstyle)
        label_equals.grid(row=0, column=3, padx=10)
        lable = ttk.Label(master=label_equals, text="=", font="TkFixedFont 33")
        lable.grid(row=0, column=3)
        self.frames_child.append(label_equals)

        main_cont.columnconfigure(4, weight=1)
        main_cont.rowconfigure(0, weight=1)
        mat2 = ttk.Frame(master=main_cont, padding=20, bootstyle=self.bootstyle)  # Matriz tres
        mat2.grid(row=0, column=4, padx=10)
        self.frames_child.append(mat2)

        self.frames.append(main_cont)  # Se almacena para la posterior reutilizacion

        d = [[np.random.randint(-99, 99) for _ in range(x)] for _ in range(y)]
        for g in range(len(d)):
            for c in range(len(d[g])):
                e = ttk.Entry(mat0, width=3, justify='center')
                e.grid(row=g, column=c, padx=2, pady=2)
                e.insert(END, '{}'.format(d[g][c]))
                e.configure(state="readonly")
                self.mt0.append(e)

        x = [[np.random.randint(-99, 99) for _ in range(x)] for _ in range(y)]
        for g in range(len(x)):
            for c in range(len(x[g])):
                e = ttk.Entry(mat1, width=3, justify='center')
                e.grid(row=g, column=c, padx=2, pady=2)
                e.insert(END, '{}'.format(x[g][c]))
                e.configure(state="readonly")
                self.mt1.append(e)

        for g in range(len(d)):
            for c in range(len(d[g])):
                e = ttk.Entry(mat2, width=3, justify='center')
                e.grid(row=g, column=c, padx=2, pady=2)
                e.insert(END, "0")
                e.configure(state="readonly")
                self.mt2.append(e)

        self.create_operations_pad()

    @staticmethod
    def graph(self, ax, canvas):
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        tmptext = self.bmatrix(self, self.textMatrix)
        tmptext = "$" + tmptext + "$"
        ax.clear()
        ax.text(0.5 * (left + right), 0.5 * (bottom + top), tmptext, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=15, family='Latin Modern Roman')
        canvas.draw()

    @staticmethod
    def bmatrix(self, a):
        """Returns a LaTeX bmatrix

        :a: numpy array
        :returns: LaTeX bmatrix as a string
        """
        if len(a.shape) > 2:
            raise ValueError('bmatrix can at most display two dimensions')
        lines = str(a).replace('[', '').replace(']', '').splitlines()
        rv = [r'C_{'+str(self.input_variableF.get().replace(" ", "")) + r"\times " + (self.input_variableC.get().replace(" ", ""))+r'} = \begin{bmatrix}']
        rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
        rv += [r'\end{bmatrix}']
        print(''.join(rv).replace("'", ''))
        return ''.join(rv).replace("'", '')

    def adition_matrix(self):
        self.reset_matrix_position()
        incr = 0
        text_sum_array = []
        self.symbolArit.configure(text="+")
        for z in range(0, int(self.input_variableF.get())):
            aux = []
            for y in range(0, int(self.input_variableC.get())):
                e = self.mt2[incr]
                e.configure(state="normal", width=4)
                e.delete(0, END)
                e.insert(END, '{}'.format(int(self.mt0[incr].get()) + int(self.mt1[incr].get())))
                e.configure(state="readonly")
                aux.append("("+str(self.mt0[incr].get()) + "+(" + str(self.mt1[incr].get())+"))")
                incr += 1
            text_sum_array.append(aux)
        self.textMatrix = np.array(text_sum_array)
        self.generate_result()

    def sustraction_matrix(self):
        self.reset_matrix_position()
        incr = 0
        text_sum_array = []
        self.symbolArit.configure(text="-")
        for z in range(0, int(self.input_variableF.get())):
            aux = []
            for y in range(0, int(self.input_variableC.get())):
                e = self.mt2[incr]
                e.configure(state="normal", width=4)
                e.delete(0, END)
                e.insert(END, '{}'.format(int(self.mt0[incr].get()) - int(self.mt1[incr].get())))
                e.configure(state="readonly")
                aux.append("("+str(self.mt0[incr].get()) + "-(" + str(self.mt1[incr].get())+"))")
                incr += 1
            text_sum_array.append(aux)
        self.textMatrix = np.array(text_sum_array)
        self.generate_result()

    def scalar_matrix(self):
        self.popup()
        escalar = int(self.entry_value())
        matrix_selected = int(self.entry_rbtn_value())

        text_sum_array = []
        incr = 0

        self.symbolArit.configure(text="x                  " + str(escalar))
        for z in range(0, int(self.input_variableF.get())):
            aux = []
            for y in range(0, int(self.input_variableC.get())):
                e = self.mt2[incr]
                e.configure(state="normal", width=4)
                e.delete(0, END)
                if matrix_selected == 1:
                    locate = self.frames_child[0]
                    locate.grid(row=0, column=0, padx=10)

                    e.insert(END, '{}'.format(int(self.mt0[incr].get()) * escalar))
                    aux.append("("+str(self.mt0[incr].get()) + "*" + str(escalar)+")")
                    k = self.frames_child[2]
                    k.grid_forget()
                else:
                    locate = self.frames_child[2]
                    locate.grid(row=0, column=0, padx=10)

                    e.insert(END, '{}'.format(int(self.mt1[incr].get()) * escalar))
                    aux.append("("+str(self.mt1[incr].get()) + "*" + str(escalar)+")")
                    k = self.frames_child[0]
                    k.grid_forget()
                e.configure(state="readonly")
                incr += 1
            text_sum_array.append(aux)

        self.textMatrix = np.array(text_sum_array)
        self.generate_result()

    def matrix_multiplication(self):
        self.reset_matrix_position()

        self.symbolArit.configure(text="x")

        sum_content = 0

        reformat_matrix0 = []
        reformat_matrix1 = []

        incr = 0
        for z in range(0, int(self.input_variableF.get())):
            temp_arr = []
            for y in range(0, int(self.input_variableC.get())):
                temp_arr.append(self.mt0[incr])
                incr += 1
            reformat_matrix0.append(temp_arr)

        incr = 0
        for z in range(0, int(self.input_variableF.get())):
            temp_arr1 = []
            for y in range(0, int(self.input_variableC.get())):
                temp_arr1.append(self.mt1[incr])
                incr += 1
            reformat_matrix1.append(temp_arr1)

        reformat_matrix0 = np.array(reformat_matrix0)
        reformat_matrix1 = np.array(reformat_matrix1)

        if reformat_matrix0.shape[1] == reformat_matrix1.shape[0]:
            incr = 0
            c = np.zeros((reformat_matrix0.shape[0], reformat_matrix1.shape[1]), dtype=int)
            for row in range(int(self.input_variableF.get())):
                for col in range(int(self.input_variableC.get())):
                    for elt in range(len(reformat_matrix1)):
                        sum_content += int(reformat_matrix0[row, elt].get()) * int(reformat_matrix1[elt, col].get())
                    c[row, col] = sum_content
                    self.mt2[incr].configure(state="normal", width=6)
                    self.mt2[incr].delete(0, END)
                    self.mt2[incr].insert(END, sum_content)
                    self.mt2[incr].configure(state="readonly", width=6)
                    incr += 1
                    sum_content = 0
        else:
            toast = ToastNotification(
                title="Error",
                message="Esta operacion no puede ser realizada por asimetria",
                position=(0, 50, "se"),
                alert=True,
                duration=5000,
                bootstyle=DANGER
            )
            toast.show_toast()  # display the Toast Notification

    def generate_result(self):
        self.frame_results[0].destroy()
        self.frame_results.clear()

        main_res_cont = ttk.Frame(master=self, padding=20)  # Contenedor principal de las matrices
        main_res_cont.pack(fill=X, expand=YES)

        self.frame_results.append(main_res_cont)

        fig = matplotlib.figure.Figure(figsize=(20, 20), dpi=72)
        ax = fig.add_subplot(111)

        canvas = FigureCanvasTkAgg(fig, master=main_res_cont)
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        canvas.tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        self.graph(self, ax, canvas)

    def on_button_pressed(self, txt):
        if txt in "Crear matrices":
            self.create_matrix()
        elif txt in "Suma de matrices":
            self.adition_matrix()
        elif txt in "Resta de matrices":
            self.sustraction_matrix()
        elif txt in "Multiplicacion escalar de matrices":
            self.scalar_matrix()
        elif txt in "Multiplicacion de matrices":
            self.matrix_multiplication()

    def popup(self):
        self.objet_pop = Popup(self.master)
        self.master.wait_window(self.objet_pop.top)

    def entry_value(self):
        return self.objet_pop.value

    def entry_rbtn_value(self):
        return self.objet_pop.option.get()

    def reset_matrix_position(self):
        locate = self.frames_child[0]
        locate.grid(row=0, column=0, padx=10)
        locate = self.frames_child[2]
        locate.grid(row=0, column=2, padx=10)

    def reset_elements(self):
        for btns in self.buttons:
            btns.destroy()

        for i in self.frames:
            i.destroy()
            self.buttons.clear()

        for m in self.frames_child:
            m.destroy()

        self.buttons.clear()
        self.frames.clear()
        self.frames_child.clear()
        self.mt0.clear()
        self.mt1.clear()
        self.mt2.clear()


if __name__ == "__main__":
    app = ttk.Window(
        title="Calculadora",
        themename="darkly",
        size=(1050, 525),
        resizable=(True, True),
    )
    app.state("zoomed")
    center(app)
    Calculator(app)
    app.mainloop()
