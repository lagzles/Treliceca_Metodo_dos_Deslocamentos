from tkinter import *  
from tkinter import messagebox, filedialog
import geometria_001 as geo
import os
import matplotlib.pyplot as plt
import rigidez_001 as rig

n_vaos = 0
steeldeck_str = ''

cumeeira = None
nos_objetos = []
barras_objetos = []
lista_vaos = []


def find_in_grid(frame, row, column):
    for children in frame.children.values():
        info = children.grid_info()
        try:
            if info['row'] == (row) and info['column'] == (column):
                return children
        except:
            a = 1
    return None


class Calculo:

    def __init__(self, master,
                 nos_objetoss, barras_objetoss,
                 cumeeiraa, vaos):
        self.master = master
        master.title('Calculo Treliças')
        ss = 0
        global nos_objetos
        global barras_objetos
        global cumeeira
        global lista_vaos

        nos_objetos = nos_objetoss
        barras_objetos = barras_objetoss
        cumeeira = cumeeiraa
        lista_vaos = vaos
        
        self.master.geometry("810x750")
       
        self.container_topo = Frame(self.master)
        self.container_topo.grid(row=1, column=1)
##        self.container_topo.place(x=15, y=15)

        self.container_meio = Frame(self.master)
        self.container_meio.grid(row=2, column=1)

##        self.container_baixo = Frame(self.master, width=500, height=400)
##        self.container_baixo.grid(row=3, column=1)

        self.container_baixo = VerticalScrolledFrame(self.master, width=500, height=400)
        self.container_baixo.grid(row=3, column=1)
        
####        self.canvas_barras = Canvas(self.container_baixo, width=500, height=400, scrollregion=(0,0,800,800))
####
####        self.hbar=Scrollbar(self.container_baixo, orient=HORIZONTAL)
####        self.hbar.pack(side=BOTTOM, fill=X)
####        self.hbar.config(command=self.canvas_barras.xview)
####
####        self.vbar=Scrollbar(self.container_baixo, orient=VERTICAL)
####        self.vbar.pack(side=RIGHT, fill=Y)
####        self.vbar.config(command=self.canvas_barras.yview)
####
####        self.canvas_barras.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
####        self.canvas_barras.pack(side=LEFT,expand=True, fill=BOTH)
##        self.canvas_barras.pack(side=LEFT,expand=False) ## ,fill=BOTH)
        
        #################################################################### 
        ####################################################################
        self.canvas_projecao = Canvas(self.container_topo, width=780,
                                      height=200, bd=0, highlightthickness=3,
                                      relief='ridge')
        self.canvas_projecao.grid(row=1, column=0)

        self.desenhar_canvas('')

        #################################################################### 
        ####################################################################

        self.botao_completo = Button(self.container_meio,
                                   text='Completo',
                                   command=lambda : self.mostrar_barras(''))
        self.botao_completo.config(width=25)
        self.botao_completo.grid(row=1, column = 0)

        self.botao_banzos = Button(self.container_meio,
                                   text='Banzos',
                                   command=lambda : self.mostrar_barras('banzo'))
        self.botao_banzos.config(width=25)
        self.botao_banzos.grid(row=1, column = 1)
        
        self.botao_montantes = Button(self.container_meio,
                                   text='Montantes',
                                   command=lambda : self.mostrar_barras('montante'))
        self.botao_montantes.config(width=25)
        self.botao_montantes.grid(row=1, column = 2)
        
        self.botao_diagonais = Button(self.container_meio,
                                   text='Diagonais',
                                   command=lambda : self.mostrar_barras('diagonal'))
        self.botao_diagonais.config(width=25)
        self.botao_diagonais.grid(row=1, column = 3)

    
    def desenhar_canvas(self, tipo):
        master = self.master

        global nos_objetos
        global barras_objetos
        global cumeeira
     
        # desenho da viga treliçada
        can = self.canvas_projecao
        mult = 0.9 * (800 / barras_objetos[-1].nf.x)
        pe_direito = barras_objetos[0].ni.y

        dh = cumeeira * 3 / 100 + 3
        hi = 100 + dh*0.5*mult
        
        can.delete('all')
        c = 0
        
        for b in barras_objetos:
            c +=1
            if b.tipo == tipo or tipo == '':
##                c +=1
                xi = 30 + b.ni.x*mult
                yi = hi - (b.ni.y - pe_direito)*mult
                
                xf = 30 + b.nf.x*mult
                yf = hi - (b.nf.y - pe_direito)*mult
                
                can.create_line([xi, yi],
                                [xf, yf],
                                fill="black", width=1)
                if tipo != '':                    
                    can.create_text((xi+xf)/2, (yi+yf)/2, font="Times 7",
                                    text=c, fill="red")
                    if tipo != 'banzo':
                        can.create_text(xi+mult, yi, font="Times 7",
                                        text=int(b.ni.id), fill="blue")
                        can.create_text(xf+mult, yf, font="Times 6",
                                        text=int(b.nf.id), fill="blue")
            
                # desenhar apoios
                if b.ni.fy == "x":# or b.nf.fy == "x":
                    can.create_line([xi - mult*.5, yi + mult], [xi, yi],
                                    fill="blue", width=1)
                    can.create_line([xi + mult*.5, yi + mult], [xi, yi],
                                    fill="blue", width=1)
                    can.create_line([xi + mult*.5, yi + mult], [xi - mult*.5, yi + mult],
                                    fill="blue", width=1)
                elif b == barras_objetos[-2]:
                    can.create_line([xf - mult*.5, yf + mult], [xf, yf],
                                    fill="blue", width=1)
                    can.create_line([xf + mult*.5, yf + mult], [xf, yf],
                                    fill="blue", width=1)
                    can.create_line([xf + mult*.5, yf + mult], [xf - mult*.5, yf + mult],
                                    fill="blue", width=1)

    def mostrar_barras(self, tipo):
        master = self.master

        global nos_objetos
        global barras_objetos
        global cumeeira
        self.desenhar_canvas(tipo)
        barras = []
        
        for b in barras_objetos:
            if b.tipo == tipo:
                barras.append(b)
        r = 1
        c = 1
        for j in range(len(barras_objetos)):
            widget1 = find_in_grid(self.container_baixo.interior, r, c)
            widget2 = find_in_grid(self.container_baixo.interior, r, c+1)
            widget3 = find_in_grid(self.container_baixo.interior, r, c+2)
            
            if widget1 != None:
                widget1.grid_forget()
                
            if widget2 != None:
                widget2.grid_forget()
                
            if widget3 != None:
                widget3.grid_forget()
            r += 1

        r = 1
        for b in barras:
            label1 = Label(self.container_baixo.interior, text=b.tipo, anchor=W)
            label1.grid(row=r, column=c)
            
            label2 = Label(self.container_baixo.interior, text=b.ni.id, anchor=W)
            label2.grid(row=r, column=c+1)
            
            label3 = Label(self.container_baixo.interior, text=b.nf.id, anchor=W)
            label3.grid(row=r, column=c+2)

            r += 1

##        self.hbar.config(command=self.canvas_barras.xview)
##        self.vbar.config(command=self.canvas_barras.yview)
##        self.canvas_barras.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        
            
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
 

