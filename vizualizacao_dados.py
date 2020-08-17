import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from limpeza_dos_dados import Dados

class graficos:

    def __init__(self):
        self.dados = Dados('Manaus.csv').get_dados()
        self.dados_limpos = Dados('Manaus.csv').get_dados_limpos()


    def bairro_com_mais_casos(self):
        '''
        Retorna os 10 bairros com mais casos e um somatorio dos casos dos outros bairros
        '''
        colunas_remover = ['_idade', '_sexo', '_classificacao',
            '_dt_notificacao', '_tipo_teste','_bairro_mapa',]

        recuperados = self.dados_limpos[self.dados_limpos['_conclusao'] == 'Recuperado']

        recuperados_por_bairro = recuperados.set_index(colunas_remover).count(level="_bairro_mapa")
        bairros = []

        #10 maiores
        for i in range(10):
            temp = recuperados_por_bairro[
                recuperados_por_bairro['_conclusao'] == int(recuperados_por_bairro.max())
                ]
            
            bairros.append(([temp.index.values[0], temp["_conclusao"].values[0]]))

            recuperados_por_bairro.drop(index=temp.index.values[0], inplace = True)

        somatoria = recuperados_por_bairro.sum(axis = 0, skipna = True)

        bairros.append(["bairros restantes", somatoria.values[0]])
        
        return bairros


    def histograma_bairros(self):
        '''
        Exibe em um histograma os dados retornados de bairro_com_mais_casos()
        '''

        bairros = self.bairro_com_mais_casos()

        nomes = [i[0] for i in bairros]
        valores = [j[1] for j in bairros]
        popPos = np.arange(len(nomes))

        plt.bar(popPos, valores, width = 0.9, color = (0.3,0.1,0.4,0.6))
        plt.xticks([r for r in range(len(nomes))], nomes, rotation=90)

        # Text on the top of each barplot
        for i in range(len(nomes)):
            plt.text(x = i-0.4 , y = valores[i]+100, s = valores[i], size = 9)

        plt.xlabel('População')
        plt.title('População de cidades brasileiras')
        plt.show()


    def casos_por_grupo_etario(self):
        '''
        soma os casos que ocorreram com individuos em um espaço de 10 anos e retorna
        '''
        idades = self.dados_limpos['_idade']
        maior_idades = int(self.dados_limpos['_idade'].max())

        casos_por_grupo_etario = []
        for i in range(0, maior_idades, 10):
            casos_por_grupo_etario.append(["{0} a {1}".format(i, i+10), idades[(idades >= i) & (idades < 10+i)].count()])
        
        return casos_por_grupo_etario


    def histograma_grupo_etario(self):

        casos_por_grupo_etario = self.casos_por_grupo_etario()

        nomes = [i[0] for i in casos_por_grupo_etario]
        valores = [j[1] for j in casos_por_grupo_etario]
        popPos = np.arange(len(nomes))

        plt.bar(popPos, valores, width = 0.9, color = (0.3,0.1,0.4,0.6))
        plt.xticks([r for r in range(len(nomes))], nomes, rotation=90)

        # Text on the top of each barplot
        for i in range(len(nomes)):
            plt.text(x = i-0.4 , y = valores[i]+100, s = valores[i], size = 9)

        plt.xlabel('População')
        plt.title('População de cidades brasileiras')
        plt.show()

a = graficos()
#a.histograma_bairros()
a.histograma_grupo_etario()