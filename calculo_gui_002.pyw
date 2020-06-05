from tkinter import *  
##from tkinter import messagebox, filedialog
##import geometria_001 as geo
import matplotlib.pyplot as plt
import rigidez_001 as rig


n_vaos = 0
steeldeck_str = ''

cumeeira = None
nos_objetos = []
barras_objetos = []
lista_vaos = []
calculo_master = None
lista_cargas = []


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
                 cumeeiraa, vaos, cargas):
        self.master = master        
        master.title('Calculo Treliças')
        ss = 0
        global nos_objetos
        global barras_objetos
        global cumeeira
        global lista_vaos
        global calculo_master
        global lista_cargas

        nos_objetos = nos_objetoss
        barras_objetos = barras_objetoss
        cumeeira = cumeeiraa
        lista_vaos = vaos
        calculo_master = self
        lista_cargas = cargas
        
        self.master.geometry("810x750")
       
        self.container_topo = Frame(self.master)
        self.container_topo.grid(row=1, column=1)

        self.container_meio = Frame(self.master)
        self.container_meio.grid(row=2, column=1)


        self.bars = []
        self.bars_canvas = Canvas(self.master,width=680,
                                      height=450)
        self.bars_frame = Frame(self.bars_canvas)

        self.scrollbar = Scrollbar(self.bars_canvas, orient="vertical",
                                   command=self.bars_canvas.yview)        
        self.bars_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.bars_canvas.grid(row=3,column=1)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas_frame = self.bars_canvas.create_window((0,0),
                                                           window=self.bars_frame,
                                                           anchor="n")

        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]


        self.master.bind("<Configure>", self.on_frame_configure)
        self.master.bind_all("<MouseWheel>", self.mouse_scroll)
        self.master.bind_all("<Button-4>", self.mouse_scroll)
        self.master.bind_all("<Button-5>", self.mouse_scroll)
        self.bars_canvas.bind("<Configure>", self.barr_width)
        
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
        self.botao_completo.config(width=15)
        self.botao_completo.grid(row=1, column = 0)

        self.botao_banzos = Button(self.container_meio,
                                   text='Banzos',
                                   command=lambda : self.mostrar_barras('banzo'))
        self.botao_banzos.config(width=15)
        self.botao_banzos.grid(row=1, column = 1)
        
        self.botao_montantes = Button(self.container_meio,
                                   text='Montantes',
                                   command=lambda : self.mostrar_barras('montante'))
        self.botao_montantes.config(width=15)
        self.botao_montantes.grid(row=1, column = 2)
        
        self.botao_diagonais = Button(self.container_meio,
                                   text='Diagonais',
                                   command=lambda : self.mostrar_barras('diagonal'))
        self.botao_diagonais.config(width=15)
        self.botao_diagonais.grid(row=1, column = 3)

        self.botao_analisar = Button(self.container_meio,
                                   text='Analisar',
                                   command=self.re_analisar)
        self.botao_analisar.config(width=15)
        self.botao_analisar.grid(row=1, column = 4)

    
    ############################################################
    ################### ADAPTADO DO SCROLLER ###################
    ############################################################
        
    def recolour_bars(self):
        for index, barr in enumerate(self.bars):
            self.set_bar_colour(index, barr)


    def set_bar_colour(self, position, barr):
        _, bar_style_choice = divmod(position, 2)

        my_scheme_choice = self.colour_schemes[bar_style_choice]

        barr.configure(bg=my_scheme_choice["bg"])
        barr.configure(fg=my_scheme_choice["fg"])


    def on_frame_configure(self, event=None):
        self.bars_canvas.configure(scrollregion=self.bars_canvas.bbox("all"))


    def barr_width(self, event):
        canvas_width = event.width
        self.bars_canvas.itemconfigure(self.canvas_frame, width=canvas_width)


    def mouse_scroll(self, event):
        if event.delta:
            self.bars_canvas.yview_scroll(-1*int(event.delta/120), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            self.bars_canvas.yview_scroll(move, "units")

    ############################################################
    ############################################################
    ############################################################
    def re_analisar (self):
        print('analisando novamente')
        global nos_objetos
        global barras_objetos
        global lista_cargas
        rig.analise_matriz_carregamentos(nos_objetos,
                                         barras_objetos,
                                         lista_cargas)
        self.desenhar_canvas('')
        self.remove_bar()
            
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

        can.create_text(20, 20, font="Times 9",
                        text="Nós", fill="blue")
        can.create_text(20, 40, font="Times 9",
                        text="Barras", fill="red")
        
        for b in barras_objetos:
            c +=1
            if b.tipo == tipo or tipo == '':
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
                        if int(b.ni.id) % 2 == 0:
                            yyi = hi - (b.ni.y*1.03 - pe_direito)*mult
                        elif int(b.ni.id) % 2 != 0:
                            yyi = hi - (b.ni.y*.97 - pe_direito)*mult
                            
                        if int(b.nf.id) % 2 == 0:
                            yyf = hi - (b.nf.y*1.03 - pe_direito)*mult
                        elif int(b.nf.id) % 2 != 0:
                            yyf = hi - (b.nf.y*.97 - pe_direito)*mult
                            
                        can.create_text(xi+0, yyi, font="Times 7",
                                        text=int(b.ni.id), fill="blue")
                        
                        can.create_text(xf+0, yyf, font="Times 7",
                                        text=int(b.nf.id), fill="blue")
##                        can.create_text(xi+mult, yi, font="Times 7",
##                                        text=int(b.ni.id), fill="blue")
##                        can.create_text(xf+mult, yf, font="Times 6",
##                                        text=int(b.nf.id), fill="blue")                            
            
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


    def add_barr(self, barra_id, barra):
        if barra != None:
            new_bar = Label(self.bars_frame, text="{} {} - Nó(i) {} - Nó(f) {} - Tração: {:.2f}  - Compressão: {:.2f}".format(barra.id,
                                                                                                                              barra.tipo,
                                                                                                                              barra.ni.id,
                                                                                                                              barra.nf.id,
                                                                                                                              barra.tracao,
                                                                                                                              barra.compressao), pady=10)
            ##
            
            new_canv = Canvas(self.bars_frame)
            self.set_bar_colour(len(self.bars), new_bar)

            new_bar.bind("<Button-1>", self.printar_dados)
            new_bar.pack(side=TOP, fill=X)
            
            self.bars.append(new_bar)


    def remove_bar(self):
        for i in range(len(self.bars)):
            self.bars[0].destroy()
            self.bars.remove(self.bars[0])


    def printar_dados(self, event):
        # estudar possibilidade de usar expressão regular
        b_id = int(float(event.widget['text'].split(" ")[0]))
        noi = int(float(event.widget['text'].split(" ")[4]))
        nof = int(float(event.widget['text'].split(" ")[7]))
        
        for barra in barras_objetos:
            if barra.id == b_id:
                barra_obj = barra

        for no in nos_objetos:
            if no.id == noi:
                noi_obj = no
                
            if no.id == nof:
                nof_obj = no

        root2 = Tk()
        TrocarNos(root2, b_id, noi, nof)
                





    def mostrar_barras(self, tipo):
        master = self.master

        self.remove_bar()
        self.bars = []

        global nos_objetos
        global barras_objetos
        global cumeeira
        self.desenhar_canvas(tipo)
        barras = []

        cont = 0
        for b in barras_objetos:
            cont += 1
            if b.tipo == tipo:
                barras.append(b)
                self.add_barr(cont, b)

                
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

tk.Canvas.create_circle = _create_circle


class TrocarNos:

    def __init__(self, master, barra_id, noi_id, nof_id):
        self.master = master
        master.title('Janela das Barras')
        global nos_objetos
        global barras_objetos

        # pega o objeto barra conforme id passada
        for barra in barras_objetos:
            if barra.id == barra_id:
                barra_obj = barra
                
        lixta_i = [noi_id - 2, noi_id - 1, noi_id, noi_id + 1, noi_id + 2]
        lixta_f = [nof_id - 2, nof_id - 1, nof_id, nof_id + 1, nof_id + 2]
        for no in nos_objetos:            
            # pega objetos nós conforme id's passadas
            if no.id == noi_id:
                noi_obj = no
                
            if no.id == nof_id:
                nof_obj = no

        self.label_barra_id = Label(self.master, text='Barra {}'.format(barra_id))
        self.label_barra_id.grid(row=2, column=1)

        self.label_no_i = Label(self.master, text='Nó Inicial: {}'.format(noi_id))
        self.label_no_i.grid(row=3, column=1)
        self.label_no_i_posicao = Label(self.master, text='(x:{}, y:{})'.format(noi_obj.x, noi_obj.y))
        self.label_no_i_posicao.grid(row=3, column=2)

        self.label_no_i = Label(self.master, text='Nó Final: {}'.format(nof_id))
        self.label_no_i.grid(row=4, column=1)
        self.label_no_f_posicao = Label(self.master, text='(x:{}, y:{})'.format(nof_obj.x, nof_obj.y))
        self.label_no_f_posicao.grid(row=4, column=2)

        self.label_new_no_i = Label(self.master, text='Novo nó Inicial')
        self.label_new_no_i.grid(row=5, column=1)
        
        self.variable_i = IntVar(self.master)
        self.variable_i.set(int(noi_obj.id))
        self.w_i = OptionMenu(self.master, self.variable_i, *lixta_i)
        self.w_i.config(width=5)
        self.w_i.grid(row=5, column=3)
        
        self.label_new_no_f = Label(self.master, text='Novo nó Final')
        self.label_new_no_f.grid(row=6, column=1)

        self.variable_f = IntVar(self.master)
        self.variable_f.set(int(nof_obj.id))
        self.w_f = OptionMenu(self.master, self.variable_f, *lixta_f)
        self.w_f.config(width=5)
        self.w_f.grid(row=6, column=3)

        self.button_ok = Button(self.master, text='Ok', command=lambda :self.modificar_barra(barra_id))
        #self.button_calc.config(width=10)
        self.button_ok.grid(row=7, column = 2)

    def modificar_barra(self, barra_id):
        print('modificar barras')
        new_no_i = self.variable_i.get()
        new_no_f = self.variable_f.get()
        contador = 0

        if new_no_f == 0 or new_no_i == 0:
            self.master.destroy()
            
        for barra in barras_objetos:
            if barra.id == barra_id:
                contador += 1
                barra_obj = barra

        for no in nos_objetos:            
            # pega objetos nós conforme id's passadas
            if no.id == new_no_i:
                noi_obj = no
                
            if no.id == new_no_f:
                nof_obj = no

        barra_obj.ni = noi_obj
        barra_obj.nf = nof_obj
        barra_obj.tracao = 0
        barra_obj.compressao = 0
        
        global calculo_master
        calculo_master.desenhar_canvas(barra.tipo)
        self.master.destroy()
        





