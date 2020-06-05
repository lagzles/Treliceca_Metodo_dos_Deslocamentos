from tkinter import Tk
from tkinter import messagebox, Label, Button, Text, Frame, IntVar, OptionMenu, Entry, Canvas, Checkbutton
# import geometria_003 as geo
import os
import trelica_010 as trel
import rigidez_002 as rig2
import analise_gui_003 as calc_gui
from auxiliar import center, find_in_grid


n_vaos = 0

def canvas_vt(can):    
    can.delete('all')

    for x in range(70,370,30):
        for y in range(40,70,30):
            p1i = (x, y)
            p2i = (x+30, y)

            p1s = (x, y+30)
            p2s = (x+30, y+30)

            can.create_line(p1i, p1s, fill="black", width=3)
            can.create_line(p2i, p2s, fill="black", width=3)
            can.create_line(p1i, p2i, fill="black", width=3)
            can.create_line(p1s, p2s, fill="black", width=3)
            if x >= 220:
                can.create_line(p1s, p2i, fill="black", width=3)
            else:
                can.create_line(p1i, p2s, fill="black", width=3)

    # cota do apoio 1
    p1 = (70, 16)
    p5 = (170, 16)
    
    p1a = (70, 33)
    p1b = (70, 9.0)
    p5a = (160, 21)
    p5b = (160, 9.0)
    
    can.create_line(p1,  p5,  fill="blue",width=1) # horizontal
    can.create_line(p1a,  p1b,  fill="blue",width=1) # vertical
    can.create_line(p5a,  p5b,  fill="blue",width=1) # vertical
    can.create_text(115, 6, font="Times 9",
                    text="apoio 1", fill="blue")

    # viga apoiando
    p1 = (160, 39)
    p2 = (160, 22)
    can.create_line(p1,  p2,  fill="red",width=2) # vertical
    p1 = (155, 39)
    p2 = (165, 39)
    can.create_line(p1,  p2,  fill="red",width=2) # mesa inf
    p1 = (155, 22)
    p2 = (165, 22)
    can.create_line(p1,  p2,  fill="red",width=2) # mesa sup

    # cota do apoio 2
    p1 = (160, 16)
    p5 = (280, 16)
    
    p1a = (160, 21)
    p1b = (160, 9.0)
    p5a = (280, 21)
    p5b = (280, 9.0)
    
    can.create_line(p1,  p5,  fill="blue",width=1) # horizontal
    can.create_line(p1a,  p1b,  fill="blue",width=1) # vertical
    can.create_line(p5a,  p5b,  fill="blue",width=1) # vertical
    can.create_text(225, 6, font="Times 9",
                    text="apoio 2", fill="blue")

    # viga apoiando
    p1 = (280, 39)
    p2 = (280, 22)
    can.create_line(p1,  p2,  fill="red",width=2) # vertical
    p1 = (275, 39)
    p2 = (285, 39)
    can.create_line(p1,  p2,  fill="red",width=2) # mesa inf
    p1 = (275, 22)
    p2 = (285, 22)
    can.create_line(p1,  p2,  fill="red",width=2) # mesa sup

    # cota do vão
    p1 = (70, 90)
    p5 = (370, 90)
    
    p1a = (70, 75)
    p1b = (70, 95)
    p5a = (370, 75)
    p5b = (370, 95)
    
    can.create_line(p1,  p5,  fill="blue",width=1)
    can.create_line(p1a,  p1b,  fill="blue",width=1)
    can.create_line(p5a,  p5b,  fill="blue",width=1)
    can.create_text(220, 97, font="Times 9",
                    text="vão", fill="blue")

 
def canvas_cobertura(can):    
    can.delete('all')
    p1 = (70,70)
    p2 = (70,40)
    
    p3 = (130,70)
    p4 = (130,35)
    
    p5 = (190,70)
    p6 = (190,30)

    p7 = (250,70)
    p8 = (250,35)
    
    p9 = (310,70)
    p10 = (310,40)
    
    p11 = (370,70)
    p12 = (370,45)

    # linhas verticais
    can.create_line(p1,  p2,  fill="black",width=3)
    can.create_line(p3,  p4,  fill="black",width=3)
    can.create_line(p5,  p6,  fill="black",width=3)
    can.create_line(p7,  p8,  fill="black",width=3)
    can.create_line(p9,  p10, fill="black",width=3)
    can.create_line(p11, p12, fill="black",width=3)
    # linhas horizontais
    can.create_line(p2,  p4,  fill="black",width=3)
    can.create_line(p4,  p6,  fill="black",width=3)
    can.create_line(p6,  p8,  fill="black",width=3)
    can.create_line(p8,  p10, fill="black",width=3)
    can.create_line(p10, p12, fill="black",width=3)

    # cota do pé direito
    p1 = (45, 70)
    p2 = (45, 40)        
    p1a = (55, 70)
    p1b = (40,  70)        
    p2a = (55, 40)
    p2b = (40,  40)
    can.create_line(p1,  p2,  fill="blue",width=1)
    can.create_line(p1a,  p1b,  fill="blue",width=1)
    can.create_line(p2a,  p2b,  fill="blue",width=1)
    can.create_text(35, 55, font="Times 9", text="pd", fill="blue")

    # cota da cumeeira
    p1 = (70, 16)
    p5 = (190, 16)
    
    p1a = (70, 33)
    p1b = (70, 9.0)
    p5a = (190, 20)
    p5b = (190, 9.0)
    
    can.create_line(p1,  p5,  fill="blue",width=1)
    can.create_line(p1a,  p1b,  fill="blue",width=1)
    can.create_line(p5a,  p5b,  fill="blue",width=1)
    can.create_text(130, 6, font="Times 9",
                    text="cumeeira", fill="blue")

    # cota dos vaos
    p1 = (70, 90)
    p2 = (130, 90)
    p3 = (190, 90)

    p1a = (70,80)
    p1b = (70,95)
    p2a = (130,80)
    p2b = (130,95)
    p3a = (190,80)
    p3b = (190,95)

    can.create_line(p1,  p2,  fill="blue",width=1)
    can.create_line(p2,  p3,  fill="blue",width=1)
    can.create_line(p1a,  p1b,  fill="blue",width=1)        
    can.create_line(p2a,  p2b,  fill="blue",width=1)
    can.create_line(p3a,  p3b,  fill="blue",width=1)

    can.create_text(100, 95, font="Times 9",
                    text="vao1", fill="blue")
    can.create_text(160, 95, font="Times 9",
                    text="vao2", fill="blue")


class Interface:

    def __init__(self, master):
        self.master = master
        master.title('Calculo Treliças')
        self.master.geometry("650x375")

        # Containers:
        #           Topo:
        #                   - Numero de vaos
        #                   - Numero de Porticos
        #                   - Informativo do programa
        #           Esquerdo:
        #                   - Entrys para valores de vão
        #                   - Entry para valor da cumeeira
        #           Direito:
        #                   - valor de carregamentos
        #                   - areas de influencia
        #           Direito_extremo:
        #                   - Canvas com apresentação da geometria
        #           Meio:
        #                   - Canvas com representação da viga

        self.container_topo = Frame(self.master)
        self.container_topo.place(x=15, y=15)  
        
        self.container_esquerdo = Frame(self.master)
        self.container_esquerdo.place(x=15, y=100)
        
        # container com valores geometricos, vinculos e carregamentos
        self.container_direito = Frame(self.master)
        self.container_direito.place(x=255, y=15)

        self.container_direito_extremo = Frame(self.master, width=300, height=300)        
        self.container_direito_extremo.place(x=625, y=25)

        self.container_meio = Frame(self.master, width=300, height=300)        
        self.container_meio.place(x=255, y=195)

        ###################################################################################
        ###################################################################################        

        self.button_about = Button(self.container_topo, text="?", command=lambda :mostrar_about_box())
        self.button_about.grid(row=0, column=0)
        
        self.label_n_vaos = Label(self.container_topo, text='Número de Vãos =', height=1)
        self.label_n_vaos.grid(row=0, column=1)

        self.variable = IntVar(master)
        lixta = [1,2,3,4,5,6,7,8,9,10]    
        self.w = OptionMenu(self.container_topo, self.variable, *lixta, 
                            command=lambda x: self.create_vaos_label(self.variable.get()))
        self.w.config(width=5)
        self.w.grid(row=0, column=2)

        ###################################################################################
        ###################################################################################        

        self.labellabel = Label(self.container_direito, text='\t')
        self.labellabel.grid(row=3, column=5)

        self.button_calc = Button(self.container_direito, text='Calcular', command=self.calcular_viga)
        self.button_calc.config(width=10)
        self.button_calc.grid(row=5, column = 6)
        
        #valores geometricos de influencia
        self.label_largura_inf = Label(self.container_direito, text='Distancia entre Vigas =', height=1)
        self.label_largura_inf.grid(row=2, column=1)

        self.label_largura_inf2 = Label(self.container_direito, text='[m]', height=1)
        self.label_largura_inf2.grid(row=2, column=3)

        self.text_largura_inf = Entry(self.container_direito, width=5)
        self.text_largura_inf.insert(0, "10.0")
        self.text_largura_inf.grid(row=2, column=2)

        self.label_altura = Label(self.container_direito, text='Altura da Viga =', height=1)
        self.label_altura.grid(row=3, column=1)

        self.label_altura2 = Label(self.container_direito, text='[m]', height=1)
        self.label_altura2.grid(row=3, column=3)

        self.text_altura = Entry(self.container_direito, width=5)
        self.text_altura.insert(0, "0.0")
        self.text_altura.grid(row=3, column=2)

        self.label_vazio4 = Label(self.container_direito, text='\t', height=1)
        self.label_vazio4.grid(row=4, column=1)

        self.label_cp = Label(self.container_direito, text='Carga Permanente =', height=1)
        self.label_cp.grid(row=5, column=1)

        self.label_cp = Label(self.container_direito, text='[kg/m2]', height=1)
        self.label_cp.grid(row=5, column=3)
        
        self.text_cp = Entry(self.container_direito, width=5)
        self.text_cp.insert(0, "20.0")
        self.text_cp.grid(row=5, column=2)

        self.label_sc = Label(self.container_direito, text='Sobrecarga Norma =', height=1)
        self.label_sc.grid(row=6, column=1)
        
        self.label_sc = Label(self.container_direito, text='[kg/m2]', height=1)
        self.label_sc.grid(row=6, column=3)

        self.text_sc = Entry(self.container_direito, width=5)
        self.text_sc.insert(0, "25.0")
        self.text_sc.grid(row=6, column=2)

        self.label_su = Label(self.container_direito, text='Sobrecarga Utilidade =', height=1)
        self.label_su.grid(row=7, column=1)
        
        self.label_su = Label(self.container_direito, text='[kg/m2]', height=1)
        self.label_su.grid(row=7, column=3)

        self.text_su = Entry(self.container_direito, width=5)
        self.text_su.insert(0, "15.0")
        self.text_su.grid(row=7, column=2)

        self.label_pd = Label(self.container_direito, text='Sobrecarga Vento =', height=1)
        self.label_pd.grid(row=8, column=1)

        self.label_pd = Label(self.container_direito, text='[kg/m2]', height=1)
        self.label_pd.grid(row=8, column=3)

        self.text_pd = Entry(self.container_direito, width=5)
        self.text_pd.insert(0, "50.0")
        self.text_pd.grid(row=8, column=2)

        self.desenho_2d = IntVar()
        self.desenho_2d.set(1)

        # check para situação VT
        self.viga_transicao = IntVar()
        self.viga_transicao.set(0)
        self.check_vt = Checkbutton(self.container_direito,
                                    text="V.T.",
                                    variable=self.viga_transicao,
                                    command=self.vt_cobertura)
        self.check_vt.grid(row=2, column=6)

        # check para banzo inferior RETO
        self.viga_banzo_reto = IntVar()
        self.viga_banzo_reto.set(0)
        self.check_banzo_reto = Checkbutton(self.container_direito,
                                    text="Banzo Reto",
                                    variable=self.viga_banzo_reto)
        self.check_banzo_reto.grid(row=3, column=6)
        
        self.label_vazio115 = Label(self.container_direito, text='\t', height=1)
        self.label_vazio115.grid(row=13, column=1)

        self.label_vazio117 = Label(self.container_direito, text='\t', height=1)
        self.label_vazio117.grid(row=15, column=1)
        ##################################################################################        
        ##################################################################################
        self.canvas_imagem = Canvas(self.container_meio, width=400,
                                    height=115, bd=0, highlightthickness=2, relief='ridge')
        self.lbl = Label(self.container_meio, text='\t', height=1)
        self.lbl.grid(row=1, column=1)
        self.canvas_imagem.grid(row=2, column=1)
        # 500 x 500
        can = self.canvas_imagem
        canvas_cobertura(can)
        ##################################################################################
        ##################################################################################
                
    def print_on_canvas(self):
        print('diaushduiauisd')

    def vt_cobertura(self):
        vt = self.viga_transicao.get()
        # se não for uma vt
        if vt == 0:
            self.check_banzo_reto.grid(row=3, column=6)

            # widget1 =  find_in_grid(self.container_direito, 8, 1)
            # widget2 =  find_in_grid(self.container_direito, 8, 3)
            # widget3 =  find_in_grid(self.container_direito, 8, 2)
            
            widget11 =  find_in_grid(self.container_direito, 13, 1)
            widget22 =  find_in_grid(self.container_direito, 13, 3)
            widget33 =  find_in_grid(self.container_direito, 13, 2)
            
            # if widget1 != None:
            #     widget1.grid_forget()
            # if widget2 != None:
            #     widget2.grid_forget()
            # if widget3 != None:
            #     widget3.grid_forget()

            if widget11 != None:
                widget11.grid_forget()
            if widget22 != None:
                widget22.grid_forget()
            if widget33 != None:
                widget33.grid_forget()

            widget11 =  find_in_grid(self.container_direito, 13, 1)
            if widget11 != None:
                widget11.grid_forget()
            
            canvas_cobertura(self.canvas_imagem)
            
            widget_1 = find_in_grid(self.container_topo, 0, 1)
            if widget_1 != None:
                widget_1.grid_forget()
                Label(self.container_topo, text='Número de Vãos =', height=1).grid(row=0, column=1)
            
            widget_2 = find_in_grid(self.container_direito, 2, 1)
            if widget_2 != None:
                widget_2.grid_forget()
                Label(self.container_direito, text='Distancia entre Vigas =', height=1).grid(row=2, column=1)
            
            widget_3 = find_in_grid(self.container_direito, 2, 3)
            if widget_3 != None:
                widget_3.grid_forget()
                Label(self.container_direito, text='[m]', height=1).grid(row=2, column=3)
            self.create_vaos_label(0)


            widget_1 = find_in_grid(self.container_direito, 5, 3)
            if widget_1 != None:
                widget_1.grid_forget()
                Label(self.container_direito, text='[kg/m²]', height=1).grid(row=5, column=3)
            
            widget_1 = find_in_grid(self.container_direito, 6, 3)
            if widget_1 != None:
                widget_1.grid_forget()
                Label(self.container_direito, text='[kg/m²]', height=1).grid(row=6, column=3)

            widget_1 = find_in_grid(self.container_direito, 7, 3)
            if widget_1 != None:
                widget_1.grid_forget()
                Label(self.container_direito, text='[kg/m²]', height=1).grid(row=7, column=3)
            
            widget_1 = find_in_grid(self.container_direito, 8, 3)
            if widget_1 != None:
                widget_1.grid_forget()
                Label(self.container_direito, text='[kg/m²]', height=1).grid(row=8, column=3)
            



            
        else:
            canvas_vt(self.canvas_imagem)
            # esconde check de banzo reto
            self.check_banzo_reto.grid_forget()

            widget_1 = find_in_grid(self.container_topo, 0, 1)
            if widget_1 != None:
                widget_1.grid_forget()
                Label(self.container_topo, text='Vigas Apoiando =', height=1).grid(row=0, column=1)
            
            # widget_1 = find_in_grid(self.container_direito, 2, 1)
            # if widget_1 != None:
            #     widget_1.grid_forget()
            #     Label(self.container_direito, text='Area Influencia =', height=1).grid(row=2, column=1)

            # widget_1 = find_in_grid(self.container_direito, 6, 3)
            # if widget_1 != None:
            #     widget_1.grid_forget()
            #     Label(self.container_direito, text='[m2]', height=1).grid(row=2, column=3)
            
            widget_1 = find_in_grid(self.container_direito, 5, 3)
            if widget_1 != None:
                widget_1.grid_forget()
                Label(self.container_direito, text='[kgf]', height=1).grid(row=5, column=3)
            
            widget_1 = find_in_grid(self.container_direito, 6, 3)
            if widget_1 != None:
                widget_1.grid_forget()
                Label(self.container_direito, text='[kgf]', height=1).grid(row=6, column=3)
                
            widget_1 = find_in_grid(self.container_direito, 7, 3)
            if widget_1 != None:
                widget_1.grid_forget()
                Label(self.container_direito, text='[kgf]', height=1).grid(row=7, column=3)
            
            widget_1 = find_in_grid(self.container_direito, 8, 3)
            if widget_1 != None:
                widget_1.grid_forget()
                Label(self.container_direito, text='[kgf]', height=1).grid(row=8, column=3)
            

                


    def create_vaos_label(self, n):    
        global n_vaos
        n_vaos = n

        widget =  find_in_grid(self.container_esquerdo, 1, 1)
        if widget != None:
                widget.grid_forget()
                
        if self.viga_transicao.get() == 0:
            self.label_cumeeira = Label(self.container_esquerdo, text='Cumeeira [m]', height=1)
            self.label_cumeeira.grid(row=1, column=1)
        else:
            self.label_cumeeira = Label(self.container_esquerdo, text='Vão [m]', height=1)
            self.label_cumeeira.grid(row=1, column=1)
            
        self.entry_cumeeira = Entry(self.container_esquerdo, width=5)
        self.entry_cumeeira.insert(0, '0')
        self.entry_cumeeira.grid(row=(1), column=2)
        
        r = 2
        for j in range(25):
            widget =  find_in_grid(self.container_esquerdo, r + j, 1)
            widget2 = find_in_grid(self.container_esquerdo, r + j, 2)

            if widget != None:
                widget.grid_forget()
            if widget2 != None:
                widget2.grid_forget()
        if self.viga_transicao.get() == 0:
            for i in range(n):
                self.labe1 = Label(self.container_esquerdo, text='{} vão [m]'.format(i+1), height=1)
                self.labe1.grid(row=(r+i), column=1)
                self.entry = Entry(self.container_esquerdo, width=5)
                self.entry.insert(0, '0')
                self.entry.grid(row=(r+i), column=2)
        else:
            for i in range(n):
                self.labe1 = Label(self.container_esquerdo, text='apoio {} [m]'.format(i+1), height=1)
                self.labe1.grid(row=(r+i), column=1)
                self.entry = Entry(self.container_esquerdo, width=5)
                self.entry.insert(0, '0')
                self.entry.grid(row=(r+i), column=2)


    def calcular_viga(self):
        #master = self.master
        print('='*75)
        print('Entrada de dados:')
        
        n = n_vaos

        cp = float(self.text_cp.get())
        sc = float(self.text_sc.get())
        su = float(self.text_su.get())
        pd = float(self.text_pd.get())

        # carregamentos estão sendo majorados em 8%
        # combinações gravitacionais
        comb_sc = - (cp * 1.25 + sc * 1.5 + su * 1.4)*1.08
        comb_su = - (cp * 1.25 + sc * 1.5 + su * 1.4)*1.08
        # combinação de vento
        comb_cv = (- cp + pd * 1.4)*1.08

        # valor 'menor' das combinações gravitacionais
        comb_grav =  min(comb_su, comb_sc)

        #verifica se o carregamento dominante é o vento, ou gravitacional
        if abs(comb_cv) > max(abs(comb_su), abs(comb_sc)):
            vento = 1
        else:
            vento = 0

        altura_viga = float(self.text_altura.get())
        banzo_reto = int(self.viga_banzo_reto.get())
        cumeeira = float(self.entry_cumeeira.get())*1

        # Pegar valores de cada vão
        lista_vaos = []
        r = 2 # valor default da linha, onde estão os widgets dos vãos
        for i in range(n):
            widget = find_in_grid(self.container_esquerdo, r + i, 2)
            lista_vaos.append(float(widget.get())*1)

        # quando VT, cumeeira vira distancia entre vigas apoiadas
        viga_transicao = int(self.viga_transicao.get())
        if viga_transicao == 1:
            banzo_reto = 0
            vao_secundaria = 1
        else:
            vao_secundaria = float(self.text_largura_inf.get())
        
        carga_grav = comb_grav * vao_secundaria
        carga_cv = comb_cv * vao_secundaria
        # tempdir = ""
        print('Vãos: ', lista_vaos)
        print('Posição da Cumeeira: ', cumeeira)
        print('Combinação Gravitacional [kgf/m]: ', carga_grav)
        print('Combinação de Vento [kgf/m]: ', carga_cv)

        print('='*35)
        trelica_obj = trel.Trelica(n, lista_vaos, cumeeira, vao_secundaria, altura_viga, vento, viga_transicao, banzo_reto)
        # trelica_obj = geo.geometrizar(tempdir, n, lista_vaos, cumeeira, vao_secundaria, altura_viga, vento, viga_transicao, banzo_reto)
        
        # calculo matricial da viga treliçada
        # barras_objetos = retorno[0]
        # nos_objetos = retorno[1]
        carregamentoss = [carga_grav, carga_cv]
        trelica_obj.set_carregamentos(carregamentoss)

        trelica_obj.analise_matricial()
        
        print('Processo Inicial de Cálculo - FIM')
        print('='*75)

        root2 = Tk()
        calc_gui.Calculo(root2, trelica_obj, lista_vaos)
        center(root2)
 

def mostrar_about_box():
    messagebox.showinfo("About Box", """Programa desenvolvido para estudos estimativos
     de vigas treliçadas de cobertura ou vigas de transição treliçadas.
    """)

root = Tk()

my_gui = Interface(root)
center(root)

root.mainloop()

x = input()
