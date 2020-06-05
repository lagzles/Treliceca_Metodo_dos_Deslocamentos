from tkinter import Tk, Entry, Canvas, Label, Button, Frame, Scrollbar, Y, X, OptionMenu, IntVar, BOTH, StringVar
from tkinter import HORIZONTAL, VERTICAL, BOTTOM, TOP, LEFT, RIGHT
from tkinter import font as tkfont
import tkinter as tk
# import matplotlib.pyplot as plt
import rigidez_002 as rig
from auxiliar import center, find_in_grid, salvar, stringSecaoBarra


n_vaos = 0
steeldeck_str = ''

cumeeira = None
lista_vaos = []
calculo_master = None
lista_cargas = []
trelica_objeto = None

barras_removidas = []


class Verificar:
    def __init__(self, master, trelica_obj):
        self.master = master        
        master.title('Verificar Barras da Treliça')
        global cumeeira
        global lista_vaos
        global calculo_master
        global lista_cargas
        global trelica_objeto        

        trelica_objeto = trelica_obj
        cumeeira = trelica_objeto.cumeeira
        calculo_master = self
        lista_cargas = trelica_objeto.carregamentos
        
        self.master.geometry("810x770")
       
        self.container_topo = Frame(self.master)
        self.container_topo.grid(row=1, column=1)

        self.container_meio = Frame(self.master)
        self.container_meio.grid(row=2, column=1)

        self.container_resumo = Frame(self.master)
        self.container_resumo.grid(row=3, column=1)

        # lista de Label's das barras
        self.bars = []
        # canvas em que serão apresentados os Label's das barras
        self.bars_canvas = Canvas(self.master, width=680, height=450)
        # Frame dentro do canvas dos Label's das barras
        self.bars_frame = Frame(self.bars_canvas)
        # Scroll acrescentar barra de 'scroll' no canvas dos Label's das barras
        self.scrollbar = Scrollbar(self.bars_canvas, orient="vertical",
                                   command=self.bars_canvas.yview)
        
        # bars_canvas { bars_frame
        #               scrollbar
        
        self.bars_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.bars_canvas.grid(row=4,column=1)

        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.button_salvar = Button(self.master, text='salvar', command=lambda: self.salvar_trelica())
        self.button_salvar.grid(row=5, column=1)

        # seta uma janela dentro do frame
        self.canvas_frame = self.bars_canvas.create_window((0,0),
                                                           window=self.bars_frame,
                                                           anchor="n")

        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]
        # bars_frame  { canvas_frame
        
        self.master.bind_all("<MouseWheel>", self.mouse_scroll)
        self.master.bind_all("<Button-4>", self.mouse_scroll)
        self.master.bind_all("<Button-5>", self.mouse_scroll)
        self.master.bind("<Configure>", self.on_frame_configure)
        
        self.bars_canvas.bind("<Configure>", self.barr_width)
        
        ####################################################################
        # Canvas de desenho da Viga Treliçada
        ####################################################################
        hei = 200
        wid = 780
        self.frame_projecao = Frame(self.container_topo, width=wid, height=hei)
        self.frame_projecao.pack(expand=True, fill=BOTH)
        # self.canvas_projecao = Canvas(self.container_topo, width=wid,
        self.canvas_projecao = Canvas(self.frame_projecao, width=wid,
                                      height=hei, bd=0, highlightthickness=3,
                                      relief='ridge', scrollregion=(0,0,3200,1000))

        self.hbar = Scrollbar(self.frame_projecao, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.hbar.config(command=self.canvas_projecao.xview)

        self.vbar = Scrollbar(self.frame_projecao, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.canvas_projecao.yview)

        self.canvas_projecao.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas_projecao.pack(side=LEFT, expand=True, fill=BOTH)
        self.desenhar_canvas('')

        #################################################################### 
        # Botões para filtrar barras na representação
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

        #################################################################### 
        # Labels resumo da Viga Treliçada
        ####################################################################
        # self.peso = peso * 1.25
        # self.peso_dobrado = peso_dobrado
        # self.peso_soldado = peso_soldado
        # self.peso_miscelanias = peso * 0.25
        # self.pecas = pecas
        # self.peso_linear = self.peso / self.comprimento

        self.label_resumo_comprimento = Label(self.container_resumo, text='Comprimento: {} [m]'.format(trelica_objeto.comprimento))
        self.label_resumo_comprimento.grid(row=1, column=1)

        self.label_resumo_peso_linear = Label(self.container_resumo, text='{:.2f} kg/m'.format(trelica_objeto.peso_linear))
        self.label_resumo_peso_linear.grid(row=1, column=2)

        self.label_resumo_pecas = Label(self.container_resumo, text='Peças:{}'.format(trelica_objeto.pecas))
        self.label_resumo_pecas.grid(row=1, column=3)

        self.label_resumo_H = Label(self.container_resumo, text='h: {:.2f} m'.format(trelica_objeto.h_viga))
        self.label_resumo_H.grid(row=1, column=4)

        self.label_resumo_peso_dobrado = Label(self.container_resumo, text='Dobrado: {:.2f} kg'.format(trelica_objeto.peso_dobrado))
        self.label_resumo_peso_dobrado.grid(row=2, column=1)

        self.label_resumo_peso_soldado = Label(self.container_resumo, text='Soldado: {:.2f} kg'.format(trelica_objeto.peso_soldado))
        self.label_resumo_peso_soldado.grid(row=2, column=2)

        self.label_resumo_peso_miscelanias = Label(self.container_resumo, text='Miscelanias: {:.2f} kg'.format(trelica_objeto.peso_miscelanias))
        self.label_resumo_peso_miscelanias.grid(row=2, column=3)

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
        global lista_cargas
        global trelica_objeto
        trelica_objeto.analise_matricial()
        for barra in trelica_objeto.barras_objetos:
            barra.verificar()
        
        # atualizar os dados da treliça na GUI
        self.atualizar_propriedades_trelica()

        self.desenhar_canvas('')
        self.remove_bar()

    ############################################################
    ############################################################
    ############################################################
    def salvar_trelica (self):
        print('salvando o bagulho')
        global trelica_objeto

        salvar(trelica_objeto)


    ############################################################
    ############################################################
    # metodo que desenha as barras no canvas de desenho  
    def desenhar_canvas(self, tipo):
        global cumeeira
        global trelica_objeto

        barras_objetos = []

        # separa as barras em seus grupos
        if tipo != '':
            if tipo == 'montante' or tipo == 'diagonal':
                for barr in trelica_objeto.barras_objetos:
                    if barr.tipo == tipo:
                        barras_objetos.append(barr)
            else:
                for barr in trelica_objeto.barras_objetos:
                    if barr.tipo != 'montante' and barr.tipo != 'diagonal':
                        barras_objetos.append(barr)
        else:
            barras_objetos = trelica_objeto.barras_objetos

        # barras_objetos = trelica_objeto.barras_objetos
        nos_objetos = trelica_objeto.nos_objetos
     
        # desenho da viga treliçada
        can = self.canvas_projecao
        metade = int(len(trelica_objeto.barras_objetos) * 0.7)
        mult = 0.9 * (800 / trelica_objeto.barras_objetos[metade].nf.x)
        pe_direito = trelica_objeto.barras_objetos[0].ni.y

        if trelica_objeto.vt == 1:
            dh = 0
        else:
            dh = cumeeira * 3.0 / 100.0 + 3
        hi = 125 + dh*0.5*mult
        
        can.delete('all')

        can.create_text(20, 10, font="Times 9",
                        text="> 70%", fill="blue")
        can.create_text(20, 30, font="Times 9",
                        text=">100%", fill="red")
        can.create_text(150, 10, font="Times 9",
                        text="<70%", fill="green")
        can.create_text(150, 30, font="Times 9",
                        text="digue", fill="black")
        
        fonte_barras = tkfont.Font(family="Times", size=1, weight="bold")
        c = 0

        for b in barras_objetos:
            c = b.id #+=1
            xi = 30 + b.ni.x*mult
            yi = hi - (b.ni.y - pe_direito)*mult
            
            xf = 30 + b.nf.x*mult
            yf = hi - (b.nf.y - pe_direito)*mult

            # cor da barra, conforme o ratio da verificação
            cor = 'black'
            if b.ratio > 1.0:
                cor = 'red'
            elif b.ratio > 0.7:
                cor = 'cyan'
            elif b.ratio <= 0.6:
                cor = 'green'
            # cria a linha da barra
            can.create_line([xi, yi],
                            [xf, yf],
                            fill=cor, width=1)
            # ida da barra
            # posição e cor conforme tipo da barra
            if tipo != '':
                if b.tipo == 'montante':
                    can.create_text((xi+xf)/2, (yf)*1.0 - 11, font=fonte_barras,
                                text=c, fill="green")
                    pass
                elif b.tipo == 'diagonal':
                    can.create_text((xi+xf)/2, (yi+yf)/2 + 3, font=fonte_barras,
                                text=c, fill="black")
                    pass
                else:
                    if b.tipo == 'banzo-superior':
                        can.create_text((xi+xf)/2, (yf)*1.0 - 11, font=fonte_barras,
                                        text=c, fill="red")
                    if b.tipo == 'banzo-inferior':
                        can.create_text((xi+xf)/2, (yi) + 11, font=fonte_barras,
                                        text=c, fill="red")

        for n in nos_objetos:
            xi = 30 + n.x*mult
            yi = hi - (n.y - pe_direito)*mult
            can.create_circle(xi, yi, 2, fill="blue")

            if not n.apoio == False:            
                can.create_line([xi - mult*.5, yi + mult*1], [xi, yi],
                                fill="black", width=1)
                can.create_line([xi + mult*.5, yi + mult*1], [xi, yi],
                                fill="black", width=1)
                can.create_line([xi + mult*.5, yi + mult*1], [xi - mult*.5, yi + mult*1],
                                fill="black", width=1)

                if n.apoio == 'simples':
                    can.create_line([xi + mult*.5, yi + mult*1.5], [xi - mult*.5, yi + mult*1.5],
                                    fill="black", width=1)
    
    ############################################################
    ############################################################

    # remove as barras acrescentadas anteriormente, 
    # self.bars é a lista onde estão as barras que aparece
    def remove_bar(self):
        for bar in self.bars:
            bar.destroy()
        
        self.bars.clear()
    
                
    # Metodo que 'seta' as barras de mesmo tipo, para alimentar o canvas
    def mostrar_barras(self, tipo):
        # master = self.master

        self.remove_bar()
        self.bars = []

        global trelica_objeto
        global cumeeira
        self.desenhar_canvas(tipo)

        barras_objetos = trelica_objeto.barras_objetos
        
        if tipo == 'banzo':
            for conjunto in trelica_objeto.conjunto_banzos:
                self.add_conjunto(conjunto)

        else:    
            cont = 0
            for b in barras_objetos:
                cont += 1
                tipo_barra = b.tipo.split("-")[0]
                if tipo_barra == tipo and tipo != 'banzo':
                    self.add_barr(b) # metodo para adicionar ao canvas
    ############################################################
    ############################################################
    ############################################################

    def add_conjunto(self, conjunto):
        ratio = 0
        compress = 0
        comprimento = 0
        id_ = ''
        # itera entre as barras e pega o maior ratio.
        # este ratio irá "mandar" nas verificações do conjunto
        for barra in conjunto:
            ratio = max(ratio, barra.ratio)
            compress = max(compress, barra.compressao)            
            comprimento += barra.comprimento()
            id_ += ' '+str(barra.id)
        b = None
        for barra in conjunto:
            if barra.compressao == compress:
                b = barra

        secao = stringSecaoBarra(b)

        new_conjunto = Label(self.bars_frame,
                            text = """Barras: ({})   {}  [{}]
                            Seção: {}  l={:.2f} || kx={}  ky={}
                            Compressão: {:.2f} ratio: {:.2f} %""".format(
                                                                         id_,
                                                                         b.tipo,
                                                                         b.id,
                                                                         secao,
                                                                         comprimento,
                                                                         b.kx,
                                                                         b.ky,
                                                                         compress,
                                                                         ratio),
                            )

        self.set_bar_colour(len(self.bars), new_conjunto)

        if ratio > 1:
            new_conjunto.config(fg="red")
        elif ratio > 0.7:
            new_conjunto.config(fg="blue")
        elif ratio > 0.6:
            new_conjunto.config(fg="green")

        new_conjunto.bind("<Button-1>", self.editar_conjunto)
        new_conjunto.pack(side=TOP, fill=X)
        
        self.bars.append(new_conjunto)

    ############################################################
    ############################################################
    # Metodo que cria o Label com as informações da barra
    def add_barr(self, barra):
        if barra != None:
            secao = stringSecaoBarra(barra)

            # Adiciona os Label's no Frame das barras (Frame dentro do canvas)
            new_bar = Label(self.bars_frame,
                            text="""Barra {}    Secão: {}  l={:.2f} ||  kx={}  ky={}\n
                Tração: {:.2f} || ratio: {:.2f} % \n
                Compressão: {:.2f} || ratio: {:.2f} %""".format(barra.id,
                                       secao,
                                       barra.comprimento(),
                                       barra.kx,
                                       barra.ky,
                                       barra.tracao,
                                       abs(barra.ratio_tracao * 100),
                                       barra.compressao,
                                       abs(barra.ratio_compressao * 100)
                                       ), pady=1)

            self.set_bar_colour(len(self.bars), new_bar)

            if barra.ratio > 1:
                new_bar.config(fg="red")
            elif barra.ratio > 0.7:
                new_bar.config(fg="blue")
            elif barra.ratio > 0.6:
                new_bar.config(fg="green")

            new_bar.bind("<Button-1>", self.editar_barra)
            new_bar.pack(side=TOP, fill=X)
            
            self.bars.append(new_bar)

    ############################################################
    ############################################################
    
    # metodo para mostrar dados da barra, abre nova janela para edição
    def editar_conjunto(self, event): 
        # estudar possibilidade de usar expressão regular
        # text vira uma lista com as id's das barras
        text = event.widget['text']        
        text1 = text.split("(")[1].split(')')[0].split()
        text2 = int(text.split("[")[1].split(']')[0].split()[0])
        b_id = []
        for t in text1:
            b_id.append(int(t))
        
        root2 = Tk()
        ModificarSection(root2, [text2, b_id])
        center(root2)

    # metodo para mostrar dados da barra, abre nova janela para edição
    def editar_barra(self, event): 
        # estudar possibilidade de usar expressão regular
        text = event.widget['text'].split(" ")
        b_id = int(float(text[1]))
        
        root2 = Tk()
        ModificarSection(root2, b_id)
        center(root2)

    ############################################################
    ############################################################
    def atualizar_propriedades_trelica(self):
        global trelica_objeto

        trelica_objeto.propriedades()

        self.label_resumo_comprimento.config( text='Comprimento: {} [m]'.format(trelica_objeto.comprimento))
        self.label_resumo_peso_linear.config( text='{:.2f} kg/m'.format(trelica_objeto.peso_linear))
        self.label_resumo_peso_dobrado.config( text='Dobrado: {:.2f} kg'.format(trelica_objeto.peso_dobrado))
        self.label_resumo_peso_soldado.config( text='Soldado: {:.2f} kg'.format(trelica_objeto.peso_soldado))
        self.label_resumo_peso_miscelanias.config( text='Miscelanias: {:.2f} kg'.format(trelica_objeto.peso_miscelanias))
        self.label_resumo_pecas.config( text='Peças:{}'.format(trelica_objeto.pecas))

                
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

tk.Canvas.create_circle = _create_circle



####################################################################################
#  GUI Para alterar as seções das barras.
####################################################################################
class ModificarSection:

    def __init__(self, master, barra_id):
        self.master = master
        master.title('Janela das Barras')
        tipos_section = ['soldado', 'dobrado']
        global trelica_objeto

        barras = trelica_objeto.barras_objetos
        conjunto_barras = []
        # caso seja apenas uma barra
        if int == type(barra_id):
            barra_id = barra_id
            for barr in barras:
                if barr.id == barra_id:
                    barra = barr
            conjunto_barras = [barra]

        else: # caso seja um conjunto
            for i in barra_id[1]:
                for barr in barras:
                    if barr.id == i:
                        conjunto_barras.append(barr)
                    if barr.id == int(barra_id[0]):
                        barra = barr

        secao = stringSecaoBarra(barra) # perfil da barra
        tipo = barra.section.tipo # tipo de perfil | soldado / dobrado

        # default -> 'soldado'
        entry_state = 'normal'
        option_state = 'disabled'
        secao_index = '-' #0

        lista_secao = ['',
                        '292x2.00',
                        '292x2.25',
                        '292x2.65',
                        '292x3.00']
        if tipo == 'dobrado':
            entry_state = 'disabled'
            option_state = 'normal'
            secao_index = secao #lista_secao.index(secao)

        # apresenta a ID da barra
        self.label_barra_id = Label(self.master, text='Barra {}'.format(barra_id))
        self.label_barra_id.grid(row=2, column=1)
        
        # apresenta o tipo de seção
        self.label_tipo_section = Label(self.master, text='Tipo de Seção')
        self.label_tipo_section.grid(row=3, column=1)
        # dropdown com tipos de seção para selecionar
        self.variable_tipo = StringVar(self.master)
        self.variable_tipo.set(tipo)
        self.w_i = OptionMenu(self.master, self.variable_tipo, *tipos_section, 
                              command=lambda x: self.modificar_tipo(self.variable_tipo.get()))
        self.w_i.config(width=12)
        self.w_i.grid(row=4, column=1)

        # apresenta a seção atual
        self.label_section_atual = Label(self.master, text='Seção Atual')
        self.label_section_atual.grid(row=5, column=1)
        self.label_section_atual_ = Label(self.master, text=secao)
        self.label_section_atual_.grid(row=6, column=1)

        # ENTRY's para alterar seção da barra
        r = 2
        self.labe1 = Label(self.master, text='d  [mm]= ', height=1)
        self.labe1.grid(row=r, column=3)
        self.entry_d = Entry(self.master, width=5, state=entry_state)
        self.entry_d.insert(0, str(barra.section.d*10))
        self.entry_d.grid(row=r, column=4)
        r += 1
        self.labe1 = Label(self.master, text='tw [mm]= ', height=1)
        self.labe1.grid(row=r, column=3)
        self.entry_tw = Entry(self.master, width=5, state=entry_state)
        self.entry_tw.insert(0, str(barra.section.tw*10))
        self.entry_tw.grid(row=r, column=4)
        r += 1
        self.labe1 = Label(self.master, text='bf [mm]= ', height=1)
        self.labe1.grid(row=r, column=3)
        self.entry_bf = Entry(self.master, width=5, state=entry_state)
        self.entry_bf.insert(0, str(barra.section.bfs*10))
        self.entry_bf.grid(row=r, column=4)
        r += 1
        self.labe1 = Label(self.master, text='tf [mm]= ', height=1)
        self.labe1.grid(row=r, column=3)
        self.entry_tf = Entry(self.master, width=5, state=entry_state)
        self.entry_tf.insert(0, str(barra.section.tfs*10))
        self.entry_tf.grid(row=r, column=4)
        r += 1
        
        # apresenta as seções
        self.label_section = Label(self.master, text='Seção')
        self.label_section.grid(row=r, column=3)
        # dropdown com tipos de seção para selecionar
        # TODO acrescentar metodo: ao mudar tipo, alterar ENTRY's
        self.variable_section = StringVar(self.master)
        self.variable_section.set(secao_index)
        self.w_section = OptionMenu(self.master, self.variable_section, *lista_secao )
        self.w_section.config(width=12, state=option_state)
        self.w_section.grid(row=r, column=4)

        r = 2
        self.labe1 = Label(self.master, text='kx = ', height=1)
        self.labe1.grid(row=r, column=5)
        self.entry_kx = Entry(self.master, width=5)
        self.entry_kx.insert(0, str(barra.kx))
        self.entry_kx.grid(row=r, column=6)
        r += 1
        self.labe1 = Label(self.master, text='ky = ', height=1)
        self.labe1.grid(row=r, column=5)
        self.entry_ky = Entry(self.master, width=5)
        self.entry_ky.insert(0, str(barra.ky))
        self.entry_ky.grid(row=r, column=6)

        self.button_ok = Button(self.master, text='Ok', command=lambda :self.modificar_barra(conjunto_barras))
        self.button_ok.grid(row=7, column = 1)

        # self.button_deletar = Button(self.master, text='Deletar Barra', command=lambda :self.deletar_barra(barra_id))
        # self.button_deletar.grid(row=7, column = 3)

    def modificar_tipo(self, tipo):
        if tipo == 'soldado':
            entry_state = 'normal'
            option_state = 'disabled'
            secao_index = 0
            self.variable_section.set(int(secao_index))

            self.entry_d.config(state=entry_state)
            self.entry_tw.config(state=entry_state)
            self.entry_bf.config(state=entry_state)
            self.entry_tf.config(state=entry_state)
            self.entry_tf.config(state=entry_state)
            self.w_section.config(state=option_state)

            self.entry_d.insert(0, '300')
            self.entry_tw.insert(0, '3.75')
            self.entry_bf.insert(0, '125')
            self.entry_tf.insert(0, '4.75')
                

        elif tipo == 'dobrado':
            entry_state = 'disabled'
            option_state = 'normal'
            # secao_index = 1

            # self.variable_section.set(int(secao_index))

            self.entry_d.insert(0, '292')
            self.entry_tw.insert(0, '')
            self.entry_bf.insert(0, '89')
            self.entry_tf.insert(0, '')
        
            self.entry_d.config(state=entry_state)
            self.entry_tw.config(state=entry_state)
            self.entry_bf.config(state=entry_state)
            self.entry_tf.config(state=entry_state)
            self.entry_tf.config(state=entry_state)
            self.w_section.config(state=option_state)

    def modificar_barra(self, barras):
        print('modificar barras')
        global calculo_master

        for barra in barras:
            tipo = self.variable_tipo.get()

            if tipo == 'soldado':
                d = float(self.entry_d.get()) /10
                tw = float(self.entry_tw.get()) /10
                bf = float(self.entry_bf.get()) /10
                tf = float(self.entry_tf.get()) /10 
            
            elif tipo == 'dobrado':
                secao = self.variable_section.get()
                d, tw = secao.split('x')
                d = float(d)/10
                tw = float(tw)/10
                bf = 8.9
                tf = tw

            kx = float(self.entry_kx.get())
            ky = float(self.entry_ky.get())

            dicionario = {'tipo': tipo,
                        'd': d,
                        'tw': tw,
                        'bf': bf,
                        'tf': tf,
                        'kx': kx,
                        'ky': ky,
                        }
            barra.set_section(dicionario)
            barra.verificar()

            mostrar_tipo = barra.tipo.split('-')[0]
        calculo_master.atualizar_propriedades_trelica()
        calculo_master.mostrar_barras(mostrar_tipo)
        print('...')
        self.master.destroy()

