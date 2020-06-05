from tkinter import Tk, Entry, Canvas, Label, Button, Frame, Scrollbar, Y, X, OptionMenu, IntVar, BOTH
from tkinter import HORIZONTAL, VERTICAL, BOTTOM, TOP, LEFT, RIGHT, messagebox, filedialog
from tkinter import font as tkfont
import tkinter as tk
import verificar_gui_002 as verificar_gui
import desenhar
import os
from auxiliar import center
# import matplotlib.pyplot as plt
# import rigidez_002 as rig

#  TODO inserir função de remover barras - util para montantes

n_vaos = 0
steeldeck_str = ''

cumeeira = None
lista_vaos = []
calculo_master = None
lista_cargas = []
trelica_objeto = None

barras_removidas = []

class Calculo:
    
    def __init__(self, master,
                 trelica_obj,
                 vaos):
        self.master = master        
        master.title('Análise da Treliça')
        global cumeeira
        global lista_vaos
        global calculo_master
        global lista_cargas
        global trelica_objeto        

        trelica_objeto = trelica_obj
        cumeeira = trelica_objeto.cumeeira
        lista_vaos = vaos
        calculo_master = self
        lista_cargas = trelica_objeto.carregamentos
        
        self.master.geometry("810x750")
       
        self.container_topo = Frame(self.master)
        self.container_topo.grid(row=1, column=1)

        self.container_meio = Frame(self.master)
        self.container_meio.grid(row=2, column=1)

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

        self.bars_canvas.grid(row=3,column=1)
        self.scrollbar.pack(side=RIGHT, fill=Y)

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
                                   text='Re Analisar',
                                   command=self.re_analisar)
        self.botao_analisar.config(width=15)
        self.botao_analisar.grid(row=2, column = 1)
        
        self.botao_verificar = Button(self.container_meio,
                                   text='Verificar',
                                   command=self.verificar)
        self.botao_verificar.config(width=15)
        self.botao_verificar.grid(row=2, column = 2)

        self.botao_desenhar = Button(self.container_meio,
                                   text='DXF',
                                   command=self.desenhar)
        self.botao_desenhar.config(width=15)
        self.botao_desenhar.grid(row=1, column = 4)

    
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
        
        self.desenhar_canvas('')
        self.remove_bar()

    # metodo que desenha as barras no canvas de desenho  
    def desenhar_canvas(self, tipo):
        global cumeeira
        global trelica_objeto

        barras_objetos = trelica_objeto.barras_objetos
        nos_objetos = trelica_objeto.nos_objetos
     
        # desenho da viga treliçada
        can = self.canvas_projecao
        metade = int(len(barras_objetos) * 0.7)
        mult = 0.9 * (800 / barras_objetos[metade].nf.x)
        pe_direito = barras_objetos[0].ni.y

        if trelica_objeto.vt == 1:
            dh = 0
        else:
            dh = cumeeira * 3.0 / 100.0 + 3
        hi = 125 + dh * 0.5 * mult
        
        can.delete('all')
        c = 0

        can.create_text(20, 10, font="Times 9",
                        text="Nós", fill="blue")
        can.create_text(20, 30, font="Times 9",
                        text="Barras", fill="red")
        
        fonte_barras = tkfont.Font(family="Times", size=5, weight="bold")
        fonte_nos = tkfont.Font(family="Times", size=3)
        
        for b in barras_objetos:
            c = b.id #+=1
            tipo_barra = b.tipo.split("-")[0]
            if tipo_barra == tipo or tipo == '':
                xi = 30 + b.ni.x*mult
                yi = hi - (b.ni.y - pe_direito)*mult
                
                xf = 30 + b.nf.x*mult
                yf = hi - (b.nf.y - pe_direito)*mult
                
                can.create_line([xi, yi],
                                [xf, yf],
                                fill="black", width=1)
                if tipo != '':
                    can.create_text((xi+xf)/2, (yi+yf)/2*1.05, font=fonte_barras,
                                    text=c, fill="red")

        for n in nos_objetos:
            xi = 30 + n.x*mult
            yi = hi - (n.y - pe_direito)*mult
            yyi = hi - (n.y*1.1 - pe_direito)*mult

            can.create_circle(xi, yi, 3, fill="blue")
            can.create_text(xi+0, yyi, font=fonte_nos, text=int(n.id), fill="blue")

            if not n.apoio == False:            
                can.create_line([xi - mult*.5, yi + mult*1], [xi, yi],
                                fill="red", width=1)
                can.create_line([xi + mult*.5, yi + mult*1], [xi, yi],
                                fill="red", width=1)
                can.create_line([xi + mult*.5, yi + mult*1], [xi - mult*.5, yi + mult*1],
                                fill="red", width=1)

                if n.apoio == 'simples':
                    can.create_line([xi + mult*.5, yi + mult*1.5], [xi - mult*.5, yi + mult*1.5],
                                    fill="blue", width=1)


    # Metodo que cria o Label com as informações da barra
    def add_barr(self, barra):
        if barra != None:
            # Adiciona os Label's no Frame das barras (Frame dentro do canvas)
            new_bar = Label(self.bars_frame,
                            text="{} {} - Nó(i) {} - Nó(f) {} - Tração: {:.2f}  - Compressão: {:.2f}".format(barra.id,
                                                                                                             barra.tipo,
                                                                                                             barra.ni.id,
                                                                                                             barra.nf.id,
                                                                                                             barra.tracao,
                                                                                                             barra.compressao), pady=10)
            
            self.set_bar_colour(len(self.bars), new_bar)

            new_bar.bind("<Button-1>", self.printar_dados)
            new_bar.pack(side=TOP, fill=X)
            
            self.bars.append(new_bar)

    # remove as barras acrescentadas anteriormente, 
    # self.bars é a lista onde estão as barras que aparece
    def remove_bar(self):
        for bar in self.bars:
            bar.destroy()
        
        self.bars.clear()


    def printar_dados(self, event): # metodo para mostrar dados da barra, abrir nova janela e trocar nós
        # estudar possibilidade de usar expressão regular
        b_id = int(float(event.widget['text'].split(" ")[0]))
        no_i = int(float(event.widget['text'].split(" ")[4]))
        no_f = int(float(event.widget['text'].split(" ")[7]))
        
        root2 = Tk()
        TrocarNos(root2, b_id, no_i, no_f)
                
    # Metodo que 'seta' as barras de mesmo tipo, para alimentar o canvas
    def mostrar_barras(self, tipo):
        # master = self.master

        self.remove_bar()
        self.bars = []

        global trelica_objeto
        global cumeeira
        self.desenhar_canvas(tipo)
        barras = []

        barras_objetos = trelica_objeto.barras_objetos
        
        # x_i = 0
        # x_f = x_i + dx
        # verificar pecas por no inicial e final
            
        cont = 0
        for b in barras_objetos:
            cont += 1
            tipo_barra = b.tipo.split("-")[0]
            if tipo_barra == tipo:
                if tipo != "banzo":
                    barras.append(b) # pra que isso?! mistérios
                    self.add_barr(b) # metodo para adicionar ao canvas
                else:
                    self.add_barr(b) # metodo para adicionar ao canvas

    def otimizar_soldado(self, barra):
        almas = [35.0,37.5,40.0]
        mesas = [12.5,15.0,17.5,20.0,22.5,25.0,27.5,30.0,33.0]
        tws = [0.375, 0.475, 0.635, 0.8 ]
        tfs = [0.475, 0.635, 0.8, 0.952, 1.27, 1.588, 1.94, 2.24, 2.54]
        coisa = 0
        try:
            for alma in almas:
                for tw in tws:
                    for mesa in mesas:
                        for tf in tfs:
                            if tf > 0.635 and mesa == 12.5:
                                break
                            if mesa > 25 and tf < 0.8:
                                break
                            if (tf / tw) > 4:
                                break
                            if tw > tf:
                                break

                            dic = {
                                    'd': alma,
                                    'tw': tw,
                                    'bf':mesa,
                                    'tf':tf,
                                    'tipo': 'soldado'
                                    }
                            coisa += 1

                            barra.section.set_section(dic)
                            barra.verificar()
                            barra.set_propriedades()
                            # print((coisa))
                            if barra.ratio < 1:
                                return True
        except Exception as e:
            print(e)
            return False


    def criar_conjuntos(self, trelica_objeto):
        # global trelica_objeto
        # barras_objetos = trelica_objeto.barras_objetos
        conjuntos = []
        n_vaos = len(trelica_objeto.pontos_vao)

        for tipo_banzo in ['banzo-superior','banzo-inferior']:
            banzos = []

            # colocar primeiro banzos superiores
            for barra in trelica_objeto.barras_objetos:
                if barra.tipo == tipo_banzo:
                    banzos.append(barra)

            # banzos.append(banzos_superiores)
            # banzos.append(banzos_inferiores)                
            for i in range(n_vaos - 1):
                xi = trelica_objeto.pontos_vao[i][0]
                xff = trelica_objeto.pontos_vao[i+1][0]

                parcial_e = []
                parcial_m = []
                parcial_d = []
                parcial_e, parcial_d, parcial_m = preencher_parcial(banzos, xi, xff, trelica_objeto.vt, trelica_objeto.h_viga)
                
                if parcial_e[0] != None:
                    conjuntos.append(parcial_e)
                a = []
                lista = type(a)
                if parcial_m[0] != None:
                    if type(parcial_m[0]) == lista:                               
                        for parcial in parcial_m:
                            conjuntos.append(parcial)
                    else:
                        conjuntos.append(parcial_m)
                if parcial_d[0] != None:
                    conjuntos.append(parcial_d)
            
        for conjunto in conjuntos:
            trelica_objeto.conjunto_banzos.append(conjunto)
        

    def homogeneizar_conjuntos(self, trelica_objeto):
        # global trelica_objeto
        for conjunto in trelica_objeto.conjunto_banzos:
            compress = 0
            b = None
            for barra in conjunto:
                compress = max(compress, barra.compressao)
                if barra.compressao == compress:
                    b = barra
            try:
                self.otimizar_soldado(b)
            except Exception as e:
                print('deu merda 1')
                print(e)

            dic = {
                    'd': b.section.d,
                    'tw': b.section.tw,
                    'bf': b.section.bfs,
                    'tf': b.section.tfs,
                    'tipo': b.section.tipo
                    }
            try:
                for barra in conjunto:
                    barra.section.set_section(dic)
                    barra.verificar()
                    barra.set_peso()
            except:
                print('deu merda 2')


    def verificar(self):
        global trelica_objeto
        root2 = Tk()
        self.criar_conjuntos(trelica_objeto)
        self.homogeneizar_conjuntos(trelica_objeto)

        for barra in trelica_objeto.barras_objetos:
            if barra.section.tipo == 'dobrado':
                # em casos de treliças muito altas, a diagonal sera dividida.
                # nestes casos, deve-se alterar o kx, pois ele influencia a resistencia do perfil calculado                
                if trelica_objeto.h_viga > 3 and barra.tipo == 'diagonal':
                    barra.set_kx(2)
                else:
                    barra.set_kx(1)

                esp_2 = {'d': 29.2,
                         'tw': 0.2,
                         'bf': 8.9,
                         'tf': 0.2,
                         'tipo': 'dobrado'
                         }
                esp_225 = {'d': 29.2,
                         'tw': 0.225,
                         'bf': 8.9,
                         'tf': 0.225,
                         'tipo': 'dobrado'
                         }

                esp_265 = {'d': 29.2,
                         'tw': 0.265,
                         'bf': 8.9,
                         'tf': 0.265,
                         'tipo': 'dobrado'
                         }

                esp_3 = {'d': 29.2,
                         'tw': 0.3,
                         'bf': 8.9,
                         'tf': 0.3,
                         'tipo': 'dobrado'
                         }
                
                for dic in [esp_2, esp_225, esp_265, esp_3]:
                    barra.section.set_section(dic)
                    barra.verificar()
                    barra.set_peso()
                    if barra.ratio < 1:
                        break
                
                if barra.ratio > 1:
                    dicionario = {'tipo': 'soldado',
                                'd': 30,
                                'tw': 0.375,
                                'bf': 12.5,
                                'tf': 0.475,
                                }
                    barra.section.set_section(dicionario)
                    barra.verificar()

        trelica_objeto.analise_matricial()
        # self.homogeneizar_conjuntos(trelica_objeto)
        trelica_objeto.propriedades()
        verificar_gui.Verificar(root2, trelica_objeto)
        
        center(root2)
        self.master.destroy()

    def desenhar(self):
        currdir = os.getcwd()
        tempdir = filedialog.asksaveasfilename(parent=self.master,
                                               initialdir=currdir,
                                               title='Selecione o Diretorio onde quer salvar o arquivo DXF',
                                               filetypes = (("Arquivos dxf","*.dxf"),("Toudos","*.*")))
        if (tempdir[-4:-1]+tempdir[-1]) != '.dxf':
            tempdir += '.dxf'
        
        desenhar.desenhar_trelica(trelica_objeto, tempdir)
        pass


def preencher_parcial(barras, xi, xf, vt, h):
    parcial = []
    for barra in barras:
        barra_xi = barra.ni.x
        barra_xf = barra.nf.x

        # bool_1 = barra_xi >= xi
        bool_2 = barra_xi < xf
        bool_3 = barra_xf > xi
        bool_4 = barra_xf <= xf

        if bool_2 and bool_3 and bool_4:
            parcial.append(barra)
    
    quantidade = len(parcial)

    # tamanho é o valor de barras que irão compor os conjuntos
    # tamanho faz referencia aos conjutos das barra iniciais e finais
    tamanho = 3 
    if h > 3 and barra.tipo == 'banzo-inferior':
        tamanho = 2

    parcial_e = parcial[0:tamanho]
    if quantidade >= tamanho*2:
        parcial_d = parcial[len(parcial)-tamanho:]
    elif tamanho < quantidade < tamanho*2:                
        parcial_d = parcial[tamanho:]
    else:
        parcial_d = [None]

    parcial_mm = parcial[tamanho:len(parcial)-tamanho]
    quantidade_meio = quantidade - tamanho*2 
    parcial_m = []
    
    # tamanho_int é a quantidade de barras que farão parte dos conjuntos intermediarios
    tamanho_int = 4
    if h > 3  and barra.tipo == 'banzo-inferior':
        tamanho_int = 2

    if tamanho_int >= quantidade_meio > 0:
        parcial_m = parcial_mm
    elif quantidade_meio > tamanho_int:
        resto = quantidade_meio
        contador = 0
        while resto > tamanho_int:
            resto -= tamanho_int
            index_i = tamanho + contador * tamanho_int
            index_f = tamanho + (contador + 1)*tamanho_int
            parcial_m.append(parcial[index_i:index_f])
            contador += 1
        
        parcial_m.append(parcial[index_f:len(parcial)-tamanho])
    else:
        parcial_m = [None]

    return parcial_e, parcial_d, parcial_m


# metodo para criar os circulos no canvas
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

tk.Canvas.create_circle = _create_circle


####################################################################################
#  GUI Para alterar pontos iniciais e finais das barras.
#  Ideal para alterar orientação de diagonais
####################################################################################
class TrocarNos:

    def __init__(self, master, barra_id, noi_id, nof_id):
        self.master = master
        master.title('Janela das Barras')
        global trelica_objeto

        nos_objetos = trelica_objeto.nos_objetos
                
        lixta_i = [noi_id - 3, noi_id - 2, noi_id - 1, noi_id, noi_id + 1, noi_id + 2, noi_id + 3, noi_id + 4]
        lixta_f = [nof_id - 3, nof_id - 2, nof_id - 1, nof_id, nof_id + 1, nof_id + 2, nof_id + 3, nof_id + 4]
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

        self.label_new_no_i = Label(self.master, text='Alterar nó Inicial')
        self.label_new_no_i.grid(row=5, column=1)
        
        self.variable_i = IntVar(self.master)
        self.variable_i.set(int(noi_obj.id))
        self.w_i = OptionMenu(self.master, self.variable_i, *lixta_i)
        self.w_i.config(width=5)
        self.w_i.grid(row=5, column=2)
        
        self.label_new_no_f = Label(self.master, text='Alterar nó Final')
        self.label_new_no_f.grid(row=6, column=1)

        self.variable_f = IntVar(self.master)
        self.variable_f.set(int(nof_obj.id))
        self.w_f = OptionMenu(self.master, self.variable_f, *lixta_f)
        self.w_f.config(width=5)
        self.w_f.grid(row=6, column=2)

        self.button_ok = Button(self.master, text='Ok', command=lambda :self.modificar_barra(barra_id))
        self.button_ok.grid(row=7, column = 1)

        self.button_deletar = Button(self.master, text='Deletar Barra', command=lambda :self.deletar_barra(barra_id))
        self.button_deletar.grid(row=7, column = 3)

    def modificar_barra(self, barra_id):
        print('modificar barras')
        new_no_i = self.variable_i.get()
        new_no_f = self.variable_f.get()
        contador = 0
        barras_objetos = trelica_objeto.barras_objetos
        nos_objetos = trelica_objeto.nos_objetos

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
    
    def deletar_barra(self, barra_id):
        global trelica_objeto
        global barras_removidas
        pass

        # for barra in trelica_objeto.barras_objetos:
        #     if barra.id == barra_id:
        #         index = trelica_objeto.barras_objetos.index(barra)
        #         break
        
        # barra_removida = trelica_objeto.barras_objetos.pop(index)
        # barras_removidas.append(barra_removida)

        # print('barra removida', barra_id)
        # global calculo_master
        # calculo_master.desenhar_canvas(barra.tipo)
        self.master.destroy()