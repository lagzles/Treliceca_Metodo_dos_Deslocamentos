from tkinter import *  
from tkinter import messagebox, filedialog
import geometria_002 as geo
import os
import matplotlib.pyplot as plt
import rigidez_001 as rig
import rigidez_002 as rig2
import calculo_gui_003 as calc_gui

n_vaos = 0
steeldeck_str = ''


def find_in_grid(frame, row, column):
    for children in frame.children.values():
        info = children.grid_info()
        try:
            if info['row'] == (row) and info['column'] == (column):
                return children
        except:
            a = 1
    return None

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

    pmedio = (220, 70)

    # cota da cumeeira
    p1 = (70, 16)
    p5 = (220, 16)
    
    p1a = (70, 33)
    p1b = (70, 9.0)
    p5a = (220, 33)
    p5b = (220, 9.0)
    
    can.create_line(p1,  p5,  fill="blue",width=1)
    can.create_line(p1a,  p1b,  fill="blue",width=1)
    can.create_line(p5a,  p5b,  fill="blue",width=1)
    can.create_text(130, 6, font="Times 9",
                    text="apoio", fill="blue")

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
        ss = 0
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
        
        self.label_n_vaos = Label(self.container_topo, text='Número de Vãos =', height=1).grid(row=0, column=1)

        self.variable = IntVar(master)
        lixta = [1,2,3,4,5,6,7,8,9,10]    
        self.w = OptionMenu(self.container_topo, self.variable, *lixta, 
                            command=lambda x: self.create_vaos_label(self.variable.get()))
        self.w.config(width=5)
        self.w.grid(row=0, column=2)

        self.label_porticos = Label(self.container_topo,
                                    text='Nº Porticos =', height=1).grid(row=2, column=1)
        self.text_porticos = Entry(self.container_topo, width=5)
        self.text_porticos.insert(0, "1")
        self.text_porticos.grid(row=2, column=2)

        ###################################################################################
        ###################################################################################        

        self.labellabel = Label(self.container_direito, text='\t')
        self.labellabel.grid(row=3, column=5)

##        self.button_mostrar = Button(self.container_direito, text='Desenhar', command=self.desenhar_portico)
##        self.button_mostrar.config(width=10)
##        self.button_mostrar.grid(row=4, column = 6)

        self.button_calc = Button(self.container_direito, text='Calcular', command=self.calcular_viga)
        self.button_calc.config(width=10)
        self.button_calc.grid(row=5, column = 6)
        
        #valores geometricos de influencia
        self.label_pe_direito = Label(self.container_direito, text='Pe Direito =', height=1)#.grid(row=1, column=1)
        self.label_pe_direito.config(justify=RIGHT)
        self.label_pe_direito.grid(row=1, column=1)
        
        self.label_pe_direito2 = Label(self.container_direito, text='[m]', height=1).grid(row=1, column=3)
        self.text_pe_direito = Entry(self.container_direito, width=5)
        self.text_pe_direito.insert(0, "12.0")
        self.text_pe_direito.grid(row=1, column=2)

        self.label_largura_inf = Label(self.container_direito, text='Distancia entre Vigas =', height=1).grid(row=2, column=1)
        self.label_largura_inf2 = Label(self.container_direito, text='[m]', height=1).grid(row=2, column=3)
        self.text_largura_inf = Entry(self.container_direito, width=5)
        self.text_largura_inf.insert(0, "10.0")
        self.text_largura_inf.grid(row=2, column=2)

        self.label_vazio4 = Label(self.container_direito, text='\t', height=1).grid(row=3, column=1)
##        self.label_vazio4 = Label(self.container_direito, text='\t', height=1).grid(row=2, column=4)

        self.label_cp = Label(self.container_direito, text='Carga Permanente =', height=1).grid(row=4, column=1)
        self.label_cp = Label(self.container_direito, text='[kg/m2]', height=1).grid(row=4, column=3)
        self.text_cp = Entry(self.container_direito, width=5)
        self.text_cp.insert(0, "20.0")
        self.text_cp.grid(row=4, column=2)

        self.label_su = Label(self.container_direito, text='Sobrecarga Utilidade =', height=1).grid(row=5, column=1)
        self.label_su = Label(self.container_direito, text='[kg/m2]', height=1).grid(row=5, column=3)
        self.text_su = Entry(self.container_direito, width=5)
        self.text_su.insert(0, "15.0")
        self.text_su.grid(row=5, column=2)

        self.label_pd = Label(self.container_direito, text='Sobrecarga Vento =', height=1).grid(row=6, column=1)
        self.label_pd = Label(self.container_direito, text='[kg/m2]', height=1).grid(row=6, column=3)
        self.text_pd = Entry(self.container_direito, width=5)
        self.text_pd.insert(0, "50.0")
        self.text_pd.grid(row=6, column=2)

        self.desenho_2d = IntVar()
        self.desenho_2d.set(1)
##        self.check_pil_metalico = Checkbutton(self.container_direito,
##                                           text="Desenho 2D   ",
##                                           variable=self.desenho_2d).grid(row=1, column=6)

        self.viga_transicao = IntVar()
        self.viga_transicao.set(0)
        self.check_vt = Checkbutton(self.container_direito,
                                    text="V.T.",
                                    variable=self.viga_transicao,
                                    command=self.vt_cobertura).grid(row=2, column=6)

##        self.trelica = IntVar()
##        self.trelica.set(1)
##        self.check_metalico = Checkbutton(self.container_direito,
##                                           text="Viga treliçada",
##                                           variable=self.trelica).grid(row=2, column=6)

        


        
        
        self.label_vazio115 = Label(self.container_direito, text='\t', height=1).grid(row=13, column=1)

        self.label_vazio117 = Label(self.container_direito, text='\t', height=1).grid(row=15, column=1)
        ##################################################################################        
        ##################################################################################

        self.canvas_imagem = Canvas(self.container_meio, width=400,
                                    height=115, bd=0, highlightthickness=2, relief='ridge')
        self.lbl = Label(self.container_meio, text='\t', height=1).grid(row=1, column=1)
        self.canvas_imagem.grid(row=2, column=1)
        # 500 x 500
        can = self.canvas_imagem
        canvas_cobertura(can)

        ########################################################################################################
        ####################################################################
 
    def update_steel_deck(self, n):
        global steeldeck_str
        steeldeck_str = n
                
    def print_on_canvas(self):
        print('diaushduiauisd')

    def vt_cobertura(self):
        vt = self.viga_transicao.get()
        if vt == 0:
            widget1 =  find_in_grid(self.container_direito, 7, 1)
            widget2 =  find_in_grid(self.container_direito, 7, 3)
            widget3 =  find_in_grid(self.container_direito, 7, 2)
            
            widget11 =  find_in_grid(self.container_direito, 13, 1)
            widget22 =  find_in_grid(self.container_direito, 13, 3)
            widget33 =  find_in_grid(self.container_direito, 13, 2)


            if widget1 != None:
                widget1.grid_forget()
##                print('k1')
            if widget2 != None:
                widget2.grid_forget()
##                print('k2')
            if widget3 != None:
                widget3.grid_forget()
##                print('k3')

            if widget11 != None:
                widget11.grid_forget()
##                print('k11')
            if widget22 != None:
                widget22.grid_forget()
##                print('k22')
            if widget33 != None:
                widget33.grid_forget()
##                print('k33')

            widget11 =  find_in_grid(self.container_direito, 13, 1)
            if widget11 != None:
                widget11.grid_forget()
##                print('k11')
            
            canvas_cobertura(self.canvas_imagem)
            self.create_vaos_label(1)
            
        else:
            canvas_vt(self.canvas_imagem)
            self.create_vaos_label(1)
            self.label_avt = Label(self.container_direito, text='Area Influencia =', height=1).grid(row=7, column=1)
            self.label_avt2 = Label(self.container_direito, text='[m2]', height=1).grid(row=7, column=3)
            self.text_avt = Entry(self.container_direito, width=5)
            self.text_avt.insert(0, "0.0")
            self.text_avt.grid(row=7, column=2)

            self.label_qtd_vt = Label(self.container_direito, text='Vigas Apoiando =', height=1).grid(row=13, column=1)
            self.label_qtd_vt2 = Label(self.container_direito, text='[un.]', height=1).grid(row=13, column=3)
            self.text_qtd_vt = Entry(self.container_direito, width=5)
            self.text_qtd_vt.insert(0, "1.0")
            self.text_qtd_vt.grid(row=13, column=2)
            

    def create_vaos_label(self, n):    
        master = self.master
        global n_vaos
        n_vaos = n

        widget =  find_in_grid(self.container_esquerdo, 1, 1)
        if widget != None:
                widget.grid_forget()
                
        if self.viga_transicao.get() == 0:
            self.label_cumeeira = Label(self.container_esquerdo, text='Cumeeira [m]', height=1).grid(row=1, column=1)
        else:
            self.label_cumeeira = Label(self.container_esquerdo, text='Apoio [m]', height=1).grid(row=1, column=1)
            
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
                self.labe1 = Label(self.container_esquerdo, text='{} vão [m]'.format(i+1), height=1).grid(row=(r+i), column=1)
                self.entry = Entry(self.container_esquerdo, width=5)
                self.entry.insert(0, '0')
                self.entry.grid(row=(r+i), column=2)
        else:
            for i in range(1):
                self.labe1 = Label(self.container_esquerdo, text='{} vão [m]'.format(i+1), height=1).grid(row=(r+i), column=1)
                self.entry = Entry(self.container_esquerdo, width=5)
                self.entry.insert(0, '0')
                self.entry.grid(row=(r+i), column=2)

    def calcular_viga(self):
        master = self.master
        n = n_vaos

        cp = float(self.text_cp.get())
        sc = 25.0
        su = float(self.text_su.get())
        pd = float(self.text_pd.get())

        # combinações gravitacionais
        comb_sc = - (cp*1.25 + sc * 1.5 + su * 1.2)
        comb_su = - (cp*1.25 + sc * 1.2 + su * 1.5)
        # combinação de vento
        comb_cv = - cp + pd * 1.4

        # valor 'menor' das combinações gravitacionais
        comb_grav =  min(comb_su, comb_sc)

        #verifica se o carregamento dominante é o vento, ou gravitacional
        if abs(comb_cv) > max(abs(comb_su), abs(comb_sc)):
            vento = 1
        else:
            vento = 0        
        
        pilar_metalico = 1
        n_porticos = int(self.text_porticos.get())
        vao_secundaria = float(self.text_largura_inf.get())*1
        desenho_2d = 1
        trelica = 1
        viga_transicao = int(self.viga_transicao.get())
        
        # Valor do pe direito
        pe_direito = float(self.text_pe_direito.get())*1
        # Pegar valores de cada vão
        lista_vaos = []
        r = 2
        for i in range(n):
            widget = find_in_grid(self.container_esquerdo, r + i, 2)
            lista_vaos.append(float(widget.get())*1)

        if viga_transicao == 1:
            cumeeira = 0
        else:
            cumeeira = float(self.entry_cumeeira.get())*1
        
        currdir = os.getcwd()
        tempdir = ""

        # retorno = [barras, nós]
        retorno = geo.geometrizar(tempdir, n, lista_vaos, cumeeira, pe_direito, desenho_2d, trelica, n_porticos, vao_secundaria, vento)

        vaos = sum(lista_vaos)

        carga_grav = comb_grav * vao_secundaria
        carga_cv = comb_cv * vao_secundaria

        # calculo matricial da viga treliçada
        # barras_objetos = retorno[0]
        # nos_objetos = retorno[1]
##        rig.analise_matriz_carregamentos(retorno[1], retorno[0],
##                                         [carga_grav, carga_cv])

        carregamentoss = [carga_grav, carga_cv]
        rig2.analise_matriz_carregamentos(retorno[2], carregamentoss)
        print('analise')

        root2 = Tk()
        calc_gui.Calculo(root2, retorno[2].nos_objetos, retorno[2].barras_objetos, cumeeira, lista_vaos,
                         [carga_grav, carga_cv])
##        calc_gui.Calculo(root2, retorno[1], retorno[0], cumeeira, lista_vaos,
##                         [carga_grav, carga_cv])


 

def mostrar_about_box():
    messagebox.showinfo("About Box", """Programa desenvolvido para automatizar o desenho
em 2D ou 3D dos pórticos metalicos de alma cheia,
ou viga de cobertura treliçados em 'dxf'.

Para importar no programa Strap, com finalidade
de Auxiliar na velocidade de modelagem da estrutura.
    """)


root = Tk()

my_gui = Interface(root)
root.mainloop()
