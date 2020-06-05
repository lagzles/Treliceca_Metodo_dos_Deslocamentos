# -*- coding: utf-8 -*-
import zznos_002 as ns
import zzbarras_003_teste as br

class Portico(object):
			
		def __init__(self): #, lista_vaos, pe_direito, cumeeira, inclinacao):
			lista_vaos = [22]
			pe_direito = 12.5
			cumeeira = 22
			inclinacao = 3.0 / 100.
			quantidade_porticos = 1
			self.lista_vaos = lista_vaos
			self.pe_direito = pe_direito
			self.inclinacao = inclinacao
			self.cumeeira = cumeeira
			self.lista_nos = []
			self.lista_barras = []
			self.gdl = 0

			self.GerarBarrasEPontos()
			self.DefinirGDL()



		def DefinirGDL(self):
			numeroNos = len(self.lista_nos)
			print(numeroNos*3, self.gdl)
			self.gdl = numeroNos*3

		def GerarBarrasEPontos(self):
			# numero de vaos
			n = len(lista_vaos)
			# numero de pilares
			np = n + 1

			lista_nos = []
			lista_nos_repetidos = []
			lista_barras = []

			# altura livre não eh altura abaixo da viga, isso esta errado
			altura_total = pe_direito
			pontos_base = []
			pontos_topo = []
			pontos_viga = []

			cumeeira_alinhada = False
			# criar lista com os pontos de base e topo dos pilares
			ptA_base = [0, 0]
			ptA_topo = [0, 0 + altura_total]

			# Pontos de cumeeira, abaixo e acima da viga, respectivamente
			h_cumeeira = altura_total + cumeeira * inclinacao

			# cota 'x' do ponto inicial até a cumeeira
			x_cumeeira = 0 + cumeeira
			largura = sum(lista_vaos) * 1

			########################################################################
			########################################################################

			# definição dos angulos de rotação dos pilares
			ang = 0
			ang2 = 90

			cota = 0
			dx = 0

			oitao = 0
			for k in range(int(1)):
				pontos_base = []
				pontos_topo = []
				# incremento de distancia para cada portico

				pontos_topo.append([0, altura_total]) ########3

				oitao = 0
				# loop que vai gradativamente definindo a largura do oitao
				# definindo os pontos de base e topo dos vãos
				for vao in lista_vaos:	
					oitao += vao
					# # caso a largura parcial do oitao seja menor que a dist. cumeeira
					if oitao < cumeeira:
						cota = altura_total + oitao*inclinacao
					
					elif oitao == cumeeira: # caso coincida com a posicao da cumeeira
						cota = h_cumeeira
						cumeeira_alinhada = True
						
					elif oitao > cumeeira: # caso o parcial do oitao seja maior que a cumeeira
						cota = h_cumeeira - (oitao - cumeeira)*inclinacao
						
					# caso a cumeeira esteja entre dois parciais do oitao
					if oitao > cumeeira > (oitao - vao):
						pontos_topo.append([cumeeira, h_cumeeira])
						# acrescenta o ponto de viga da cumeeira
					
					pontos_base.append([oitao, 0])
					pontos_topo.append([oitao, cota ])
					# após definido os pontos de cada parcial do oitao, se define os pontos das vigas
				# salvar cota do lado direito do galpao
			
			# lançar nós e barras das vigas, no objeto Portico
			nof = None
			for p in range(len(pontos_topo)):
				pontoi = pontos_topo[p]
				pontof = pontos_topo[p+1]
				vao = pontof[0] - pontoi[0]
				cota = pontof[1]
				if p == 0:
					gdl = self.gdl
					noi = ns.Nos(pontoi[0], pontoi[1], gdl +1, gdl + 2, gdl + 3, 0, 0, 0, False)
					self.gdl += 3
					self.lista_nos.append(noi)
				else:
					noi = nof

				nof = self.PontosIntermediariosDaViga(noi, vao, cota)

			# lançar nós das bases e barras das colunas, no objeto Portico
			for ponto in pontos_base:
				x = ponto[0]
				y = ponto[1]
				gdl = self.gdl

				apoio = 'engaste'
				gx = gdl + 1
				gy = gdl + 2
				gz = gdl + 3
				self.gdl += 3

				nob = ns.Nos(x, y, gx, gy, gz, 0, 0, 0, apoio)
				self.lista_nos.append(nob)

				for no in self.lista_nos:
					if no.x == nob.x and no.y != 0:
						barraId = len(self.lista_barras)+1
						coluna = br.Barras(nob,no,barraId,1,1)
						self.lista_barras.append(coluna)


		def PontosIntermediariosDaViga(self, noi, vao, cota):
			# no2
			xb = noi.x
			yb = noi.y
			
			# no4
			xt = vao
			yt = cota

			# divisão padrão do vão em 3 partes
			n = 3
			if (xt-xb) < 8000: # caso tenha um 'vao' menor que 8m, não dividir
				n = 1
				# situacao mais comum quando cumeeira esta no meio do vao
			if n != 1:
				dx = (xt-xb) / n
				dy = (yt-yb) / n


				gdl = self.gdl
				ptFim = ns.Nos(xb+dx, yb+dy, gdl+1, gdl+2, gdl+3, 0, 0, 0,False)
				self.gdl += 3
				# para divisao padrao do vao, em 3 partes
				for j in range(0, n):
					if j == 0:
						ptInicio = noi
					else:
						ptInicio = ptFim

					gdl = self.gdl
					ptFim = ns.Nos(xb+dx*(j+1), yb+dy*(j+1), gdl+1, gdl+2, gdl+3, 0, 0, 0,False)
					self.gdl += 3
					
					barra_id = len(self.lista_barras) + 1
					barraIntermediaria = br.Barras(ptInicio, ptFim, barra_id, n , n)

					self.lista_barras.append(barraIntermediaria)
					self.lista_nos.append(ptFim)
					self.pontos_viga.append(ptFim)
			elif n == 1:
				ptInicio = noi
				gdl = self.gdl
				ptFim = ns.Nos(xt, yt, gdl+1, gdl+2, gdl+3, 0, 0, 0,False)
				self.gdl += 3

				barra_id = len(self.lista_barras) + 1
				barraIntermediaria = br.Barras(ptInicio, ptFim, barra_id, n , n)

				self.lista_barras.append(barraIntermediaria)
				self.lista_nos.append(ptFim)
				self.pontos_viga.append(ptFim)

			return ptFim


	# # iteracao para lancar as vigas
	# for i in range(len(pontos_viga)-1):
	# 	# no2
	# 	xb = pontos_viga[i][0]
	# 	yb = pontos_viga[i][1]
	# 	zb = pontos_viga[i][2]
		
	# 	# no4
	# 	xt = pontos_viga[i+1][0]
	# 	yt = pontos_viga[i+1][1]
	# 	zt = pontos_viga[i+1][2]
	# 	# divisão padrão do vão em 3 partes
	# 	n = 3
	# 	if (xt-xb) < 8000: # caso tenha um 'vao' menor que 8m, não dividir
	# 		n = 1
	# 		# situacao mais comum quando cumeeira esta no meio do vao
	# 	if n != 1:
	# 		# para divisao padrao do vao, em 3 partes
	# 		for j in range(0, n):
	# 			dx = (xt-xb) / n
	# 			dz = (zt-zb) / n
				
	# 			ptInicio = (xb + dx * (j), yb, zb + dz*j)
	# 			ptFim = (xb + dx * (j + 1), yt, zb + dz*(j+1))
	# 			framing = criarFraming(ptInicio, ptFim, framingTypeSoldado)

	# 			# condicionantes para definicao da altura da viga em cada ponto
	# 			# por padrao o valor da altura eh de d_meio 
	# 			# condicionantes para o ponto inicial
				
	# 	elif n == 1:
	# 		ptInicio = (xb, yb, zb)
	# 		ptFim = (xt, yt, zt)
	# 		framing = criarFraming(ptInicio, ptFim, framingTypeSoldado)


