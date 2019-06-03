from dxfwrite import DXFEngine as dxf

def desenhar_linhas(dwg, ponto_i, ponto_f):
    line = dxf.line(start=ponto_i, end=ponto_f)
    line['layer'] = 'DIMENSIONS'
    line['color'] = '5'
    dwg.add(line)
##    print('.')
    dwg.save()


def desenhar_banzos(dwg, ponto_i, ponto_f):
    line = dxf.line(start=ponto_i, end=ponto_f)
    line['layer'] = 'DIMENSIONS'
    line['color'] = '4'
    dwg.add(line)
##    print('.')
    dwg.save()


def desenhar_montantes(dwg, ponto_i, ponto_f):
    line = dxf.line(start=ponto_i, end=ponto_f)
    line['layer'] = 'DIMENSIONS'
    line['color'] = '3'
    dwg.add(line)
##    print('.')
    dwg.save()


def desenhar_diagonais(dwg, ponto_i, ponto_f):
    line = dxf.line(start=ponto_i, end=ponto_f)
    line['layer'] = 'DIMENSIONS'
    line['color'] = '2'
    dwg.add(line)
##    print('.')
    dwg.save()

