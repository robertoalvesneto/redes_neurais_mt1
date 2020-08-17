import pandas as pd
import numpy as np

class Dados():

    def __init__(self, arquivo):
        self.nome_arquivo = arquivo
        self.dados = None
        self.dados_limpos = None

        self.__abrir_arquivo()
        self.__limpar_dados(self.dados)


    def __abrir_arquivo(self):
        #abre o arquivo e cria um dataframe com eles

        dados = pd.read_csv(self.nome_arquivo, sep=";", encoding = 'iso-8859-1')
        
        self.dados = dados


    def __remover_colunas(self, dados):
        #apaga as colunas que nao sao importantes para o trabalho
        
        '''foi considerado os 'bairro_mapa' pois esses sao os bairros considerados
        oficialmente, enquanto a coluna 'bairros' contem não oficiais, os não
        oficiais ficam dentro dos oficiais'''

        '''colunas mantidas: idade, sexo, classificacao, conclusao, dt_notificacao, 
        tipo_teste, bairro_mapa'''
        
        colunas_removidas = dados.drop([
            '_faixa etária','_bairro','_comorb_renal','_comorb_diabetes',
            '_comorb_imuno','_comorb_cardio','_taxa','_dt_evolucao','_raca',
            '_dt_sintomas','_criterio','_sintoma_garganta','_sintoma_dispneia',
            '_sintoma_febre','_sintoma_tosse','_sintoma_outros','_etnia',
            '_profiss_saude','_srag','_se_notificacao','_distrito',
            '_comorb_respiratoria','_comorb_cromossomica','_comorb_hepatica',
            '_comorb_neurologica','_comorb_hemato','_comorb_obessidade',
            '_origem','_evolução'
            ], axis=1)

        return colunas_removidas


    def __apagar_dados_nao_confirmados(self, dados_sem_colunas):
        #apaga as linhas onde o teste para covid nao deu confirmado

        '''no banco de dados ouve dois casos de erro onde haviam aspas  nos dados,
        como essas foram as duas unicas incidencias podem ser removidas diretamente
        aqui
        ['Confirmado', 'Em análise', 'Descartado', 'SRA.DAS GRACAS"', '10"']'''

        dados_confirmados = dados_sem_colunas[dados_sem_colunas._classificacao == 'Confirmado']
        
        return dados_confirmados


    def __apagar_linhas_vazias(self, dados_confirmados):
        #apaga as linhas onde o teste para covid nao foi confirmado

        sem_linhas_vazias = dados_confirmados.dropna()

        return sem_linhas_vazias


    def __limpar_dados(self, dados):
        dados_sem_colunas = self.__remover_colunas(dados)
        dados_confirmados = self.__apagar_dados_nao_confirmados(dados_sem_colunas)
        dados_limpos = self.__apagar_linhas_vazias(dados_confirmados)

        self.dados_limpos = dados_limpos


    def get_dados(self):
        return self.dados


    def get_dados_limpos(self):
        return self.dados_limpos



