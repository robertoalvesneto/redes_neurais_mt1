def retornarListaDoArquivo(nomeArquivo):
    #abre o arquivo com o padrao encode certo e retorna uma lista
    #com todas as linhas da tabela

    with open(nomeArquivo, encoding = 'iso-8859-1') as arquivoCSV:
        arquivoAberto = arquivoCSV.read()
        todasLinhas = arquivoAberto.split("\n")
        
        return todasLinhas[1:]


def apagarColunas(linhasDoCSV):
    #apaga as colunas que nao sao importantes para o trabalho
    
    '''foi considerado os 'bairro_mapa' pois esses sao os bairros considerados
    oficialmente, enquanto a coluna 'bairros' contem não oficiais, os não
    oficiais ficam dentro dos oficiais'''

    '''colunas mantidas: idade, sexo, classificacao, conclusao, dt_notificacao, 
    tipo_teste, bairro_mapa'''
    documentoModificado = ''

    for linha in linhasDoCSV:
        itensDaLinha = linha.split(";")

        if len(itensDaLinha) > 2:
            linhaModificada = itensDaLinha[0] + ";" + itensDaLinha[2] + ";" 
            linhaModificada += itensDaLinha[4] + ";" + itensDaLinha[9] + ";"
            linhaModificada += itensDaLinha[10] + ";" + itensDaLinha[16] + ";"
            linhaModificada += itensDaLinha[27] + "\n"
        
        documentoModificado += linhaModificada
    
    return documentoModificado


def apagarDadosNaoConfirmados(documentoSemColunas):
    #apaga as linhas onde o teste para covid nao deu confirmado

    '''no banco de dados ouve dois casos de erro onde haviam aspas  nos dados,
    como essas foram as duas unicas incidencias podem ser removidas diretamente
    aqui, já que uma função buscando aspas para somente essas duas linhas seria
    muito custosa'''
    documentoSemColunas = documentoSemColunas.split("\n")

    documentoModificado = ''

    for linha in documentoSemColunas:
        itensDaLinha = linha.split(";")

        if len(itensDaLinha) > 1 and itensDaLinha[2] == 'Confirmado':
            documentoModificado += linha + "\n"

    return documentoModificado


def apagarLinhasVazias(documentoDadosConfirmados):
    #apaga as linhas onde o teste para covid naofoi confirmado

    dadosSemLinhasVazias = apagarLinhasVaziasDeUmIndice(documentoDadosConfirmados, 0)
    dadosSemLinhasVazias = apagarLinhasVaziasDeUmIndice(dadosSemLinhasVazias, 1)
    dadosSemLinhasVazias = apagarLinhasVaziasDeUmIndice(dadosSemLinhasVazias, 2)
    dadosSemLinhasVazias = apagarLinhasVaziasDeUmIndice(dadosSemLinhasVazias, 3)
    dadosSemLinhasVazias = apagarLinhasVaziasDeUmIndice(dadosSemLinhasVazias, 4)
    dadosSemLinhasVazias = apagarLinhasVaziasDeUmIndice(dadosSemLinhasVazias, 5)
    dadosSemLinhasVazias = apagarLinhasVaziasDeUmIndice(dadosSemLinhasVazias, 6)

    return dadosSemLinhasVazias

def apagarLinhasVaziasDeUmIndice(documentoDadosConfirmados, indice):
    #apaga as linhas de um indice especifico onde o teste para covid nao foi
    #confirmado

    '''no banco de dados ouve dois casos de erro onde haviam aspas  nos dados,
    como essas foram as duas unicas incidencias podem ser removidas diretamente
    aqui, já que uma função buscando aspas para somente essas duas linhas seria
    muito custosa'''
    documentoDadosConfirmados = documentoDadosConfirmados.split("\n")

    documentoModificado = ''

    for linha in documentoDadosConfirmados:
        itensDaLinha = linha.split(";")

        if len(itensDaLinha) > 1 and itensDaLinha[indice] != '':
            documentoModificado += linha + "\n"

    return documentoModificado


def proporcaoDeTodasAsColunas(dados):
    '''da uma nocao da situacao dos dados, quanto que nao foi preenchido, tirando a 
    conclusão e o tipó de teste que tiverem respectivamente 2/3 e 1/4 de omissao, no
    resto faltou poucos dados'''
    print("\n")
    proporcaoDadosNaoInformados(dados, 0, "IDADE")
    proporcaoDadosNaoInformados(dados, 1, "SEXO")
    proporcaoDadosNaoInformados(dados, 2, "CLASSIFICACAO")
    proporcaoDadosNaoInformados(dados, 3, "CONCLUSAO")
    proporcaoDadosNaoInformados(dados, 4, "DATA NOTIFICACAO")
    proporcaoDadosNaoInformados(dados, 5, "TIPO TESTE")
    proporcaoDadosNaoInformados(dados, 6, "BAIRRO")

def proporcaoDadosNaoInformados(documentoSemColunas, indice, nomeColuna):
    #informa a quantidade de campos vazios de uma coluna
    documentoSemColunas = documentoSemColunas.split("\n")

    #ambos comecao em -1 para desconsiderar a priumeira linha
    quantTotal = 0
    quantNaoInformadas = 0

    for linha in documentoSemColunas:
        itensDaLinha = linha.split(";")

        if len(itensDaLinha) > 1:
            quantTotal += 1
            if itensDaLinha[indice] == '':
                quantNaoInformadas += 1

    if quantNaoInformadas != 0:
        porcentagem = round(quantNaoInformadas/quantTotal, 5)
    else:
        porcentagem = 0

    print(f"{nomeColuna}: {quantNaoInformadas} de {quantTotal} campos" +
        f" vazios: {porcentagem}%")


def comparacaoBairroEBairroMapa(linhasDoCSV):
    '''funcao meramente exemplificativa, a coluna 'bairros' é preenchido pelos
    proprios moradores, entao la contem bairros nao oficiais e tambem mesmos
    bairros mas escritos de formas diferentes por erro de escrita.
    a coluna 'bairros mapa' contem os bairros oficiais e mais algumas zonas prox
    de manaus como br-174 e rio taruma-mirim'''

    bairros = []
    bairrosMapa = []

    for linha in linhasDoCSV:
        itensDaLinha = linha.split(";")
        colunasManter = [3, 27]
        colunaAtual = 0
        

        #TODO: REMOVER ESSE FOR
        for item in itensDaLinha:
            if colunaAtual == 3:
                linhaVazia = (item == '')
                primeiraLinha = (item == '_bairro')
                if (item not in bairros) and not linhaVazia and not primeiraLinha:
                    bairros.append(item)
            
            elif colunaAtual == 27:
                linhaVazia = (item == '')
                primeiraLinha = (item == '_bairro_mapa')

                if (item not in bairrosMapa) and not linhaVazia and not primeiraLinha:
                    bairrosMapa.append(item)
            
            colunaAtual += 1
    
    print(len(bairros))
    print(bairros)
    print()
    print(len(bairrosMapa))
    print(bairrosMapa)


def criarArquivoFinal(dadosSemLinhasVazias):
    with open("dadosLimpos.txt","w+") as dadosLimpos:
        for linha in dadosSemLinhasVazias:
            dadosLimpos.write(linha)


#TODO: ESSA FUNÇÃO N PERTENCE A ESSE ARQUIVO
def busca(dadosSemLinhasVazias):
    documento = dadosSemLinhasVazias.split("\n")

    vetor = []

    for linha in documento:
        itensDaLinha = linha.split(";")

        if len(itensDaLinha) > 2 and itensDaLinha[3] not in vetor:
            vetor.append(itensDaLinha[3])

    return vetor


linhasDoCSV = retornarListaDoArquivo('Manaus.csv')

#comparacaoBairroEBairroMapa(linhasDoCSV)

#ANTES DE APAGAR QUALQUER LINHA
documentoSemColunas = apagarColunas(linhasDoCSV)
proporcaoDeTodasAsColunas(documentoSemColunas)

#APAGANDO LINHAS ONDE COVID N FOI CONFIRMADO
dadosConfirmados = apagarDadosNaoConfirmados(documentoSemColunas)
proporcaoDeTodasAsColunas(dadosConfirmados)

#APAGANDO LINHAS QUE TENHAM DADOS FALTANDO EM QUALQUER COLUNA
dadosSemLinhasVazias = apagarLinhasVazias(dadosConfirmados)
proporcaoDeTodasAsColunas(dadosSemLinhasVazias)

criarArquivoFinal(dadosSemLinhasVazias)