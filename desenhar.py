from dxfwrite import DXFEngine as dxf

def desenhar_trelica(trelica, filename):
    dwg = dxf.drawing(filename)

    for barra in trelica.barras_objetos:
        pi = [barra.ni.x*100, barra.ni.y*100]
        pf = [barra.nf.x*100, barra.nf.y*100]

        if barra.tipo == 'montante':
            desenhar_montantes(dwg, pi, pf)
        elif barra.tipo == 'diagonal':
            desenhar_diagonais(dwg, pi, pf)
        else:
            desenhar_banzos(dwg, pi, pf)

    if dwg != None:
        dwg.save()

def desenhar_linhas(dwg, ponto_i, ponto_f):
    line = dxf.line(start=ponto_i, end=ponto_f)
    line['layer'] = 'DIMENSIONS'
    line['color'] = '5'
    dwg.add(line)
    # dwg.save()


def desenhar_banzos(dwg, ponto_i, ponto_f):
    line = dxf.line(start=ponto_i, end=ponto_f)
    line['layer'] = 'DIMENSIONS'
    line['color'] = '4'
    dwg.add(line)
    # dwg.save()


def desenhar_montantes(dwg, ponto_i, ponto_f):
    line = dxf.line(start=ponto_i, end=ponto_f)
    line['layer'] = 'DIMENSIONS'
    line['color'] = '3'
    dwg.add(line)
    # dwg.save()


def desenhar_diagonais(dwg, ponto_i, ponto_f):
    line = dxf.line(start=ponto_i, end=ponto_f)
    line['layer'] = 'DIMENSIONS'
    line['color'] = '2'
    dwg.add(line)
    # dwg.save()

