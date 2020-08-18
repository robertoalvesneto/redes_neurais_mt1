import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from limpeza_dos_dados import Dados

class Graficos:

    def __init__(self):
        self.dados = Dados('Manaus.csv').get_dados()
        self.dados_limpos = Dados('Manaus.csv').get_dados_limpos()


    def __bairro_com_mais_casos(self):
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


    def __casos_por_grupo_etario(self):
        '''
        soma os casos que ocorreram com individuos em um espaço de 10 anos e retorna
        '''
        idades = self.dados_limpos['_idade']
        maior_idades = int(self.dados_limpos['_idade'].max())

        casos_por_grupo_etario = []
        for i in range(0, maior_idades, 10):
            casos_por_grupo_etario.append(["{0} a {1}".format(i, i+10), idades[(idades >= i) & (idades < 10+i)].count()])
        
        return casos_por_grupo_etario


    def __casos_por_dia(self):
        '''
        Calcula e retorna o total de casos em cada um dos 10 ultimos dias
        '''
        dados = self.dados_limpos
        dias = dados['_dt_notificacao'].values
        dias = [dia.split('/') for dia in dias]
        
        datas_por_quant_casos = []
        for i in range(10):
            maior_dia = ''
            maior_mes = ''
            maior_ano = ''

            for dia in dias:
                if dia[2] > maior_ano:
                    maior_dia, maior_mes, maior_ano = dia[0], dia[1], dia[2]

                if dia[2] == maior_ano and dia[1] > maior_mes:
                    maior_dia, maior_mes, maior_ano = dia[0], dia[1], dia[2]

                if dia[2] == maior_ano and dia[1] == maior_mes and dia[0] > maior_dia:
                    maior_dia, maior_mes, maior_ano = dia[0], dia[1], dia[2]
            
            maior_data = "{0}/{1}/{2}".format(maior_dia, maior_mes, maior_ano)
            
            temp = [maior_data, dados[dados['_dt_notificacao'] == maior_data].count()[0]]
            datas_por_quant_casos.append(temp)

            #remove todas as datas iguais
            dados = dados[dados['_dt_notificacao'] != maior_data]
            dias = dados['_dt_notificacao'].values
            dias = [dia.split('/') for dia in dias]

        return datas_por_quant_casos


    def __casos_recuperados(self):
        '''
        Calcula e retorna o total de casos recuperados em cada um dos 10 ultimos dias
        '''
        dados = self.dados_limpos
        datas_por_quant_casos = self.__casos_por_dia()

        datas_por_quant_recuperados = []
        for data_por_quant in datas_por_quant_casos:
            recuperado = (dados['_conclusao'] == 'Recuperado')
            data = (dados['_dt_notificacao'] == data_por_quant[0])
            recuperada_data = dados[(data) & (recuperado)]

            temp = [data_por_quant[0], recuperada_data.count()[0]]

            datas_por_quant_recuperados.append(temp)

            #remove todas as datas iguais
            dados = dados[dados['_dt_notificacao'] != data_por_quant[0]]
        
        return datas_por_quant_recuperados


    def histograma_bairros(self):
        '''
        Exibe em um histograma os dados retornados de bairro_com_mais_casos()
        '''
        bairros = self.__bairro_com_mais_casos()

        nomes = [i[0] for i in bairros]
        valores = [j[1] for j in bairros]
        popPos = np.arange(len(nomes))

        plt.bar(popPos, valores, width = 0.9, color = (0.3,0.1,0.4,0.6))
        plt.xticks([r for r in range(len(nomes))], nomes, rotation=90)

        for i in range(len(nomes)):
            plt.text(x = i-0.4 , y = valores[i]+100, s = valores[i], size = 9)

        plt.title('Total de casos por bairro')
        plt.show()


    def histograma_grupo_etario(self):
        '''
        Exibe em um histograma os dados retornados de __casos_por_grupo_etario()
        '''
        casos_por_grupo_etario = self.__casos_por_grupo_etario()

        nomes = [i[0] for i in casos_por_grupo_etario]
        valores = [j[1] for j in casos_por_grupo_etario]
        popPos = np.arange(len(nomes))

        plt.bar(popPos, valores, width = 0.9, color = (0.3,0.1,0.4,0.6))
        plt.xticks([r for r in range(len(nomes))], nomes, rotation=90)

        for i in range(len(nomes)):
            plt.text(x = i-0.4 , y = valores[i]+100, s = valores[i], size = 9)

        plt.title('Casos por gupo etário')
        plt.show()


    def histograma_casos_ultimos_10_dias(self):
        '''
        Exibe em um histograma os dados retornados de __casos_por_dia()
        '''
        casos_por_dia = self.__casos_por_dia()

        nomes = [i[0] for i in casos_por_dia]
        valores = [j[1] for j in casos_por_dia]
        popPos = np.arange(len(nomes))

        plt.bar(popPos, valores, width = 0.9, color = (0.3,0.1,0.4,0.6))
        plt.xticks([r for r in range(len(nomes))], nomes, rotation=90)

        for i in range(len(nomes)):
            plt.text(x = i-0.4 , y = valores[i]+100, s = valores[i], size = 9)

        plt.title('Casos de COVID-19 nos ultimos 10 dias')
        plt.show()


    def histograma_casos_recuperados(self):
        '''
        Exibe em um histograma os dados retornados de __casos_recuperados()
        '''
        casos_recuperados = self.__casos_recuperados()

        nomes = [i[0] for i in casos_recuperados]
        valores = [j[1] for j in casos_recuperados]
        popPos = np.arange(len(nomes))

        plt.bar(popPos, valores, width = 0.9, color = (0.3,0.1,0.4,0.6))
        plt.xticks([r for r in range(len(nomes))], nomes, rotation=90)

        for i in range(len(nomes)):
            plt.text(x = i-0.4 , y = valores[i]+100, s = valores[i], size = 9)

        plt.title('Pessoas recuperadas nos ultimos 10 dias')
        plt.show()



graficos = Graficos()

graficos.histograma_bairros()
graficos.histograma_grupo_etario()
graficos.histograma_casos_ultimos_10_dias()
graficos.histograma_casos_recuperados()
