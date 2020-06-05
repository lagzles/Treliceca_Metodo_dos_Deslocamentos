from xlwt import Borders, Font, XFStyle
from xlwt import Workbook
from tkinter import messagebox, filedialog



def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
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

def find_in_grid(frame, row, column):
    for children in frame.children.values():
        info = children.grid_info()
        try:
            if info['row'] == (row) and info['column'] == (column):
                return children
        except:
            pass
    return None


def stringSecaoBarra(barra):
    if barra != None:
        secao = 'AxBxC'
        if barra.section.tipo == 'soldado':
            secao = '{:.0f}x{:.0f}x{:.2f}x{:.2f}'.format(
                                            barra.section.d * 10,
                                            barra.section.bfs * 10,
                                            barra.section.tw * 10,
                                            barra.section.tfs * 10,   
                                            )
        else:
            secao = '{:.0f}x{:.2f}'.format(
                                    barra.section.d * 10,
                                    barra.section.tw * 10,
                                    )
    return secao


def salvar(trelica_objeto):
    borders = Borders()
    bord = 2
    borders.left = bord
    borders.right = bord
    borders.top = bord
    borders.bottom = bord

    bord_lateral = Borders()
    bord = 2
    bord_lateral.left = bord
    bord_lateral.right = bord
    ## FONTES
    fonte_titulo = Font()
    fonte_titulo.name = 'Times New Roman'
    fonte_titulo.bold = True
    fonte_titulo.height = 240
    fonte_titulo.borders = bord_lateral

    fonte_normal = Font()
    fonte_normal.name = 'Times New Roman'
    fonte_normal.borders = bord_lateral
    
    fonte_normal_problema = Font()
    fonte_normal_problema.name = 'Times New Roman'
    fonte_normal_problema.borders = bord_lateral
    fonte_normal_problema.colour_index = 2 #5=amarelo | 4=azul | 3=verde | 2=vermelho

    fonte_destaque = Font()
    fonte_destaque.name = 'Arial'
    fonte_destaque.colour_index = 4  # azul
    ## ESTILOS
    estilo_titulo = XFStyle()
    estilo_titulo.borders = borders
    estilo_titulo.font = fonte_titulo
    estilo_titulo.alignment.horz = 2

    estilo_sub_titulo = XFStyle()
    estilo_sub_titulo.borders = borders
    estilo_sub_titulo.alignment.horz = 2
    estilo_sub_titulo.font = fonte_destaque

    estilo_normal = XFStyle()
    estilo_normal.font = fonte_normal
    estilo_normal.num_format_str = "#,##0.00"
    estilo_normal.alignment.horz = 2

    estilo_normal_esquerda = XFStyle()
    estilo_normal_esquerda.font = fonte_normal

    estilo_normal_tabela = XFStyle()
    estilo_normal_tabela.font = fonte_normal
    estilo_normal_tabela.borders = borders
    estilo_normal_tabela.alignment.horz = 2
    estilo_normal_tabela.num_format_str = "#,##0.00"

    estilo_normal_tabela_red = XFStyle()
    estilo_normal_tabela_red.font = fonte_normal_problema
    estilo_normal_tabela_red.borders = borders
    estilo_normal_tabela_red.alignment.horz = 2
    estilo_normal_tabela_red.num_format_str = "#,##0.00"

    estilo_destaque = XFStyle()
    estilo_destaque.font = fonte_destaque
    # estilo_destaque.alignment.horz = 2
    estilo_destaque.alignment.vertical = 2

    estilo_destaque_tabela = XFStyle()
    estilo_destaque_tabela.font = fonte_destaque
    estilo_destaque_tabela.borders = borders
    estilo_destaque_tabela.alignment.horz = 2

    estilo_id_tabela = estilo_normal_tabela
    estilo_id_tabela.alignment.num_format_str = "#0"

    text_file =  filedialog.asksaveasfile(mode='w', defaultextension=".xls",filetypes=[('excel files','.xls')])
    wb = Workbook()
    sheet = wb.add_sheet('Treliceca')
    sheet.col(2).width = 0x0d00 + 22
    sheet.col(4).width = 0x0d00 + 40
    sheet.col(7).width = 0x0d00 + 15
    sheet.col(8).width = 0x0d00 + 15
    
    vt = trelica_objeto.vt
    banzo_reto = trelica_objeto.banzo_reto
    # padrão de viga treliçada
    viga = 'Viga de Cobertura Treliçada com banzos paralelos'
    
    if vt ==1:
        viga = 'Viga de Transição Treliçada'
    if banzo_reto == 1:
        viga = 'Viga de Cobertura Treliçada com banzo inferior reto'

    # combinações de carregamentos atuando na treliça
    carregamento_grav = trelica_objeto.carregamentos[0]
    carregamento_cv = trelica_objeto.carregamentos[1]
    vaos = ''
    for ponto in trelica_objeto.pontos_vao:
        vaos += ' ' + str(ponto[0]) + ','

    # pesos calculados da treliça
    peso = trelica_objeto.peso
    peso_dobrado = trelica_objeto.peso_dobrado
    peso_soldado = trelica_objeto.peso_soldado
    peso_linear = trelica_objeto.peso_linear
    peso_miscelanias = trelica_objeto.peso_miscelanias
    # pecas = trelica_objeto.pecas
    h_viga = trelica_objeto.h_viga

    # lista com as barras da treliça, separadas por tipo
    banzos_inferiores = []
    banzos_superiores = []
    diagonais = []
    montantes = []

    for barra in trelica_objeto.barras_objetos:
        if barra.tipo == 'diagonal':
            diagonais.append(barra)
        elif barra.tipo == 'montante':
            montantes.append(barra)
        elif barra.tipo == 'banzo-superior':
            banzos_superiores.append(barra)
        elif barra.tipo == 'banzo-inferior':
            banzos_inferiores.append(barra)

    lista_barras =[banzos_inferiores, banzos_superiores, montantes, diagonais]

    linha = 0

    # inserindo o titulo = viga
    sheet.write_merge(linha,linha,1,11, viga, estilo_titulo)
    linha += 1

    sheet.write_merge(linha,linha,1,11, 'Dados da Viga Treliçada', estilo_sub_titulo)
    linha += 1

    sheet.write_merge(linha,linha,8,11, 'Combinações [kg/m]', estilo_destaque_tabela)
    sheet.write(linha, 1, 'Vãos[m]=', estilo_destaque)
    sheet.write_merge(linha, linha, 2, 4, vaos, estilo_normal)
    linha += 1

    sheet.write(linha, 1, 'Altura [m]', estilo_destaque)
    sheet.write(linha, 2, h_viga, estilo_normal)
    
    sheet.write(linha, 4, 'Soldado [kg]', estilo_destaque)
    sheet.write(linha, 5, peso_soldado, estilo_normal)
    
    sheet.write_merge(linha, linha, 8, 9, 'Grav. ', estilo_destaque_tabela)
    sheet.write_merge(linha, linha,10, 11, 'Vento', estilo_destaque_tabela)
    linha += 1

    sheet.write(linha, 1, 'Peso [kg]', estilo_destaque)
    sheet.write(linha, 2, peso, estilo_normal)    
    
    sheet.write(linha, 4, 'Dobrado [kg]', estilo_destaque)
    sheet.write(linha, 5, peso_dobrado, estilo_normal)

    sheet.write_merge(linha, linha, 8, 9, '1.25xCP + 1.5xSC + 1.4xSU', estilo_normal_tabela)
    sheet.write_merge(linha, linha,10, 11, '1.0xCP + 1.4xCV', estilo_normal_tabela)
    linha += 1

    sheet.write(linha, 1, 'Y [kg/m]', estilo_destaque)
    sheet.write(linha, 2, peso_linear, estilo_normal)

    sheet.write(linha, 4, 'Miscelanias [kg]', estilo_destaque)
    sheet.write(linha, 5, peso_miscelanias, estilo_normal)
    
    sheet.write_merge(linha, linha, 8, 9, carregamento_grav, estilo_normal_tabela)
    sheet.write_merge(linha, linha,10, 11, carregamento_cv, estilo_normal_tabela)
    linha += 2
    

    # Barras da treliça
    sheet.write_merge(linha, linha, 1, 11, 'Barras da Treliça', estilo_destaque_tabela)
    linha += 1
    sheet.write(linha, 1, 'id', estilo_destaque_tabela)
    sheet.write(linha, 2, ' ', estilo_destaque_tabela)
    sheet.write(linha, 3, 'tipo ', estilo_destaque_tabela)
    sheet.write(linha, 4, 'seção ', estilo_destaque_tabela)
    sheet.write(linha, 5, 'Peso [kg]', estilo_destaque_tabela)
    sheet.write(linha, 6, 'l [m]', estilo_destaque_tabela)
    sheet.write(linha, 7, 'Comp [kgf]', estilo_destaque_tabela)
    sheet.write(linha, 8, 'Tração [kgf]', estilo_destaque_tabela)
    sheet.write(linha, 9, 'Ratio ', estilo_destaque_tabela)
    sheet.write(linha, 10, 'compr.', estilo_destaque_tabela)
    sheet.write(linha, 11, 'tração', estilo_destaque_tabela)
    linha += 1

    for lista in lista_barras:
        for barra in lista:
            estilo = estilo_normal_tabela
            if barra.ratio > 1:
                estilo = estilo_normal_tabela_red
            else:
                estilo = estilo_normal_tabela
            sheet.write(linha, 1, barra.id, estilo)
            sheet.write(linha, 2, barra.tipo, estilo)
            sheet.write(linha, 3, barra.section.tipo, estilo)
            sheet.write(linha, 4, stringSecaoBarra(barra), estilo)
            sheet.write(linha, 5, barra.peso, estilo)
            sheet.write(linha, 6, barra.comprimento(), estilo)
            sheet.write(linha, 7, barra.compressao, estilo)
            sheet.write(linha, 8, barra.tracao, estilo)
            sheet.write(linha, 9, barra.ratio, estilo)
            sheet.write(linha, 10, barra.ratio_compressao, estilo)
            sheet.write(linha, 11, barra.ratio_tracao, estilo)
            linha += 1

    linha = 1
    sheet.write(linha, 15, 'Reações nos Apoios = [h1, v1, v2, v3, ..., vn] ', estilo_normal_esquerda)
    linha += 1

    sheet.write(linha, 15, 'Apoios numerados conforme desenho do canvas', estilo_normal_esquerda)
    linha += 1
    sheet.write(linha, 15, 'Numeração da esquerda, para direita', estilo_normal_esquerda)
    linha += 1

    sheet.write(linha, 15, 'F', estilo_destaque_tabela)
    sheet.write_merge(linha, linha, 16, 17, 'kgf', estilo_destaque_tabela)
    linha += 1

    sheet.write(linha, 15, ' ', estilo_destaque_tabela)
    sheet.write(linha, 16, 'grav', estilo_destaque_tabela)
    sheet.write(linha, 17, 'vento', estilo_destaque_tabela)
    linha += 1

    reacoes_grav = trelica_objeto.reacoes_grav
    reacoes_cv = trelica_objeto.reacoes_cv
    qtd_reacoes = len(reacoes_grav)

    sheet.write(linha, 15, 'Fx 1', estilo_destaque_tabela)
    sheet.write(linha, 16, reacoes_grav[0], estilo_normal_tabela)
    sheet.write(linha, 17, reacoes_cv[0], estilo_normal_tabela)
    linha += 1
    
    for i in range(1, qtd_reacoes):
        sheet.write(linha, 15, 'Fy {:.0f}'.format(i), estilo_destaque_tabela)
        sheet.write(linha, 16, reacoes_grav[i], estilo_normal_tabela)
        sheet.write(linha, 17, reacoes_cv[i], estilo_normal_tabela)
        linha += 1

    wb.save(text_file.name)