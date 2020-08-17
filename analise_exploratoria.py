import pandas as pd
import numpy as np
from scipy import stats

from limpeza_dos_dados import Dados


class analise:

    def __init__(self):
        self.dados = Dados('Manaus.csv').get_dados()
        self.dados_limpos = Dados('Manaus.csv').get_dados_limpos()


    def quantidade_elementos_comparatorio(self):
        '''
        Quantos exemplos e atributos há na base de dados após a limpeza e organização?
        '''

        linha_dados1, coluna_dados1 = self.dados.shape
        linha_dados2, coluna_dados2 = self.dados_limpos.shape

        print("\nQUANTIDADE DE ELEMENTOS EM CADA ARQUIVO:")
        print("linhas: {0}   colunos: {1}".format(linha_dados1, coluna_dados1))
        print("linhas: {0}   colunos: {1}".format(linha_dados2, coluna_dados2))


    def quantidade_individuos_recuperados(self):
        '''
        Qual a porcentagem de indivíduos recuperados em relação ao todo?
        '''
        quant_elementos = self.dados_limpos.shape[0]
        quant_recuperados = self.dados_limpos[
            self.dados_limpos['_conclusao'] == 'Recuperado'
            ].shape[0]
        quant_obitos = quant_elementos - quant_recuperados

        porcentagem = round(round(quant_recuperados/quant_elementos, 4)*100, 5)

        string = "\n\nQUANTIDADE CLASSIFICAÇÃO: \nele:{0}   recu:{1}   obt:{2}   {3}%"
        print(string.format(quant_elementos, quant_recuperados, quant_obitos, porcentagem))


    def quantidade_masculinos_femininos(self):
        '''
        Os casos acometeram mais indivíduos do sexo masculino ou feminino?
        informa a quantidade total e a porcentagem de individuos de cada
        sexo contaminados
        '''

        quant_elementos = self.dados_limpos.shape[0]
        quant_homens = self.dados_limpos[self.dados_limpos['_sexo'] == 'M'].shape[0]
        quant_mulheres = self.dados_limpos[self.dados_limpos['_sexo'] == 'F'].shape[0]

        porcent_homens = round(round(quant_homens/quant_elementos, 5)*100, 5)
        porcent_mulheres = round(round(quant_mulheres/quant_elementos, 5)*100, 5)

        print(f"\n\nQUANTIDADE SEXO INFECTADO: \nele:{quant_elementos}   " +
            f"homens: {quant_homens} / {porcent_homens}%   " +
            f"mulheres: {quant_mulheres} / {porcent_mulheres}%")


    def idade_individuos_contaminados(self):
        '''
        Qual a média e desvio padrão de idade dos indivíduos que contraíram COVID-19?
        Qual o indivíduo mais jovem e o mais idoso a contraírem tal enfermidade?
        '''
        idades = self.dados_limpos['_idade']
        mais_jovem = int(idades.min())
        mais_velho = int(idades.max())

        media = idades.mean()
        desvio_padrao = idades.std()

        print(f"\n\nCASOS POR IDADE:")
        print("media: {0}   desvio padrao: {1}".format(media, desvio_padrao))
        print("mais novo: {0}   mais velho: {1}".format(mais_jovem, mais_velho))


    def bairro_com_mais_casos(self):
        '''
        Qual o bairro com maior incidência de casos?

        a coluna que sera mantida nao importa, porem deve ser mantida duas
        colunas para funcionar o count
        '''
        colunas_remover = ['_sexo', '_classificacao', '_conclusao',
            '_dt_notificacao', '_tipo_teste','_bairro_mapa']

        casos_por_bairro = self.dados_limpos.set_index(colunas_remover).count(level="_bairro_mapa")

        bairro_com_mais_casos = casos_por_bairro[
            casos_por_bairro['_idade'] == int(casos_por_bairro.max())
            ]

        print("\n\nBAIRRO COM MAIOR INCIDENCIA DE CASOS:")
        print(bairro_com_mais_casos.index.values[0])


    def bairros_com_mais_recuperados(self):
        '''
        Quais os três bairros com maior incidência de casos recuperados?
        '''
        colunas_remover = ['_idade', '_sexo', '_classificacao',
            '_dt_notificacao', '_tipo_teste','_bairro_mapa',]

        recuperados = self.dados_limpos[self.dados_limpos['_conclusao'] == 'Recuperado']

        recuperados_por_bairro = recuperados.set_index(colunas_remover).count(level="_bairro_mapa")
        bairros = []

        for i in range(3):
            bairros.append(recuperados_por_bairro[
                recuperados_por_bairro['_conclusao'] == int(recuperados_por_bairro.max())
                ])
            recuperados_por_bairro.drop(index=bairros[i].index.values[0], inplace = True)


        print("\n\nBAIRRO COM MAIOR INCIDENCIA DE CASOS:")
        for i in range(3):
            print("{0}   {1}".format(bairros[i].index.values[0], bairros[i]["_conclusao"].values[0]))


    def tipos_testes_efetuados(self):
        #mostra todos os tipos de testes feitos e o percentual de cada um
        colunas_remover = ['_sexo', '_classificacao', '_conclusao',
            '_dt_notificacao', '_tipo_teste','_bairro_mapa']

        quant_elementos = self.dados_limpos.shape[0]

        tipos_testes = self.dados_limpos.set_index(colunas_remover).count(level="_tipo_teste")
        tipos_testes.rename(columns={"_idade": "quantidade"}, inplace = True)

        porcentagens = []
        for valor in tipos_testes.values:
            porcentagens.append("{0}%".format(round(round(valor[0]/quant_elementos, 5)*100, 5)))

        tipos_testes['porcentagem'] = porcentagens

        print("\n\nTIPOS DE TESTES EFETUADOS:")
        print(tipos_testes)


    def taxa_fatalidade(self):
        '''
        Qual taxa de letalidade pode ser calculada a partir do conjunto de dados?
        Para calcular esta taxa, considere a fração do total de óbitos pelo total
        de casos.
        '''
        quant_elementos = self.dados_limpos.shape[0]
        quant_recuperados = self.dados_limpos[
            self.dados_limpos['_conclusao'] == 'Recuperado'
            ].shape[0]
        quant_obitos = quant_elementos - quant_recuperados

        porcentagem = round(round(quant_obitos/quant_elementos, 5)*100, 5)

        print("\n\nLETALIDADE: \n{0}%".format(porcentagem))


    def coeficiente_correlacao_person(self):
        '''
        Qual o tipo de correlação, mediante coeficiente de correlação de Pearson,
        entre a idade e o número de casos? Para responder a esta pergunte, agrupe o 
        número de casos por idade e efetue o cálculo de tal coeficiente. Indique, a 
        partir do resultado, a natureza desta correlação, se é positiva ou negativa,
        e qual sua intensidade.
        '''
        colunas_remover = ['_idade', '_sexo', '_classificacao',
            '_dt_notificacao', '_tipo_teste','_bairro_mapa',]

        casos_por_idade = self.dados_limpos.set_index(colunas_remover).count(level="_idade")
        casos_por_idade.rename(columns={"_conclusao": "quantidade"}, inplace = True)
        idades = casos_por_idade.index.values

        idades = idades.astype(int)
        
        quantidades = casos_por_idade['quantidade'].values
        print("\n\n CORRELACAO DE PEARSON")
        print(stats.pearsonr(idades, quantidades))


a = analise()
a.quantidade_elementos_comparatorio()
a.quantidade_individuos_recuperados()
a.quantidade_masculinos_femininos()
a.idade_individuos_contaminados()
a.bairro_com_mais_casos()
a.bairros_com_mais_recuperados()
a.taxa_fatalidade()
a.tipos_testes_efetuados()
a.coeficiente_correlacao_person()