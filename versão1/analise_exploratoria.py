def abrir_arquivos(nome_arquivo):
    '''
    abre o arquivo com o padrao e retorna uma lista com todas as linhas da tabela
    '''

    if (nome_arquivo == "Manaus.csv"):
        with open(nome_arquivo, encoding = 'iso-8859-1') as arquivo_csv:
            arquivo_aberto = arquivo_csv.read()
            todas_linhas = arquivo_aberto.split("\n")
            
            return todas_linhas[1:]
    else:
        with open(nome_arquivo) as arquivo_txt:
            arquivo_aberto = arquivo_txt.read()
            todas_linhas = arquivo_aberto.split("\n")
            
            return todas_linhas[0:-1]


def quantidade_elementos_comparatorio():
    '''
    faz duas chamadas a função 'quantidade_elementos', uma carregando o arquivo
    antes da limpeza e a outra o arquivo após a limpeza, desse modo compara a
    mudança
    '''
    print("\nQUANTIDADE DE ELEMENTOS EM CADA ARQUIVO:")
    dados = abrir_arquivos("Manaus.csv")
    quantidade_elementos(dados, "Manaus.csv")

    dados = abrir_arquivos("dadosLimpos.txt")
    quantidade_elementos(dados, "dadosLimpos.txt")

def quantidade_elementos(dados, nome):
    '''
    Quantos exemplos e atributos há na base de dados após a limpeza e organização?
    '''

    quantLinhas = 0
    quantColunas = 0

    linha = dados[0].split(';')
    quantColunas = len(linha)

    quantLinhas = len(dados)

    print(f"{nome}::   {quantLinhas}   {quantColunas}")


def quantidade_individuos_recuperados(dados):
    '''
    Qual a porcentagem de indivíduos recuperados em relação ao todo?
    '''
    quant_elementos = 0
    quant_recuperados = 0
    quant_obtos = 0
    porcentagem = 0

    for linha in dados:
        itens_da_linha = linha.split(";")
        resultado = itens_da_linha[3]

        quant_elementos += 1

        if resultado == 'Recuperado':
            quant_recuperados += 1
        else:
            quant_obtos += 1

    porcentagem = round(quant_recuperados/quant_elementos, 5)
    print(f"\n\nQUANTIDADE CLASSIFICAÇÃO: \nele:{quant_elementos}   " +
        f"recu:{quant_recuperados}   obt:{quant_obtos}   %{porcentagem}")


def quantidade_masculinos_femininos(dados):
    '''
    Os casos acometeram mais indivíduos do sexo masculino ou feminino?
    informa a quantidade total e a porcentagem de individuos de cada
    sexo contaminados
    '''
    quant_elementos = 0
    quant_homens = 0
    quant_mulheres = 0
    porcent_homens = 0
    porcent_mulheres = 0

    for linha in dados:
        itens_da_linha = linha.split(";")

        quant_elementos += 1

        if itens_da_linha[1] == 'M':
            quant_homens += 1
        else:
            quant_mulheres += 1

    porcent_homens = round(quant_homens/quant_elementos, 5)
    porcent_mulheres = round(quant_mulheres/quant_elementos, 5)

    print(f"\n\nQUANTIDADE SEXO INFECTADO: \nele:{quant_elementos}   " +
        f"homens:{quant_homens}quant  {porcent_homens}%   " +
        f"mulheres:{quant_mulheres}quant  {porcent_mulheres}%")


def idade_individuos_contaminados(dados):
    '''
    Qual a média e desvio padrão de idade dos indivíduos que contraíram COVID-19?
    Qual o indivíduo mais jovem e o mais idoso a contraírem tal enfermidade?
    '''
    casos_por_idade = {}
    mais_jovem = 200
    mais_velho = -1

    for linha in dados:
        itens_da_linha = linha.split(";")
        idade = int(itens_da_linha[0])

        if idade not in casos_por_idade:
            casos_por_idade[idade] = 1
        else:
            casos_por_idade[idade] += 1
        
        if idade < mais_jovem:
            mais_jovem = idade
        elif idade > mais_velho:
            mais_velho = idade
    
    #calculo da media
    somatorio_idades = 0
    quantidade_elementos = 0
    for idade, quantidade in casos_por_idade.items():
        somatorio_idades += idade*quantidade
        quantidade_elementos += quantidade

    media = somatorio_idades/quantidade_elementos

    #calculo desvio padrao
    numerador_desvio_padrao = 0
    for idade, quantidade in casos_por_idade.items():
        numerador_desvio_padrao += (idade - media)**2

    #TODO: PARECE ESTAR ERRADO
    desvio_padrao = (numerador_desvio_padrao/quantidade_elementos)**(1/2)

    print(f"\n\nCASOS POR IDADE:")
    print("media: {0}   desvio padrao: {1}".format(media, desvio_padrao))
    print("mais novo: {0}   mais velho: {1}".format(mais_jovem, mais_velho))


def bairro_com_mais_casos(dados):
    '''
    Qual o bairro com maior incidência de casos?
    '''
    bairros = {}
    nome_bairro_maior_incidencia = -1
    quant_bairro_maior_incidencia = -1

    for linha in dados:
        itens_da_linha = linha.split(";")
        bairro_da_linha = itens_da_linha[6]

        if bairro_da_linha not in bairros:
            bairros[bairro_da_linha] = 1 
        else:
            bairros[bairro_da_linha] += 1 

    for bairro in bairros:
        if quant_bairro_maior_incidencia < bairros[bairro]:
            nome_bairro_maior_incidencia = bairro
            quant_bairro_maior_incidencia = bairros[bairro]
    
    print(f"\n\nBAIRRO COM MAIOR INCIDENCIA DE CASOS:\n" +
        f"nome:{nome_bairro_maior_incidencia}   " +
        f"quant:{quant_bairro_maior_incidencia}")


def bairros_com_mais_recuperados(dados):
    '''
    Quais os três bairros com maior incidência de casos recuperados?
    '''
    bairros = {}
    nome_bairro_maior_recuperacao = ['', '', '']
    quant_bairro_maior_recuperacao = [-1, -1, -1]

    for linha in dados:
        itens_da_linha = linha.split(";")
        resultado = itens_da_linha[3]
        bairro_da_linha = itens_da_linha[6]

        if resultado == 'Recuperado':
            if bairro_da_linha not in bairros:
                bairros[bairro_da_linha] = 1 
            else:
                bairros[bairro_da_linha] += 1 

    for i in range(3):
        for bairro in bairros:
            if quant_bairro_maior_recuperacao[i] < bairros[bairro]:
                nome_bairro_maior_recuperacao[i] = bairro
                quant_bairro_maior_recuperacao[i] = bairros[bairro]
        del bairros[nome_bairro_maior_recuperacao[i]]

    print(f"\n\n3 BAIRROS COM MAIS RECUPERADOS:\n" +
        f"nomes:{nome_bairro_maior_recuperacao}   " +
        f"recuperados:{quant_bairro_maior_recuperacao}")


def tipos_testes_efetuados(dados):
    #mostra todos os tipos de testes feitos e o percentual de cada um
    quant_elementos = 0
    quant_por_testes = {}

    for linha in dados:
        itens_da_linha = linha.split(";")
        teste = itens_da_linha[5]

        quant_elementos += 1

        if teste not in quant_por_testes:
            quant_por_testes[teste] = [1]
        else:
            quant_por_testes[teste][0] += 1
    
    #add a porcentagem de cada teste
    for teste, valor in quant_por_testes.items():
        porcentagem = round((valor[0]/quant_elementos)*100, 3)
        quant_por_testes[teste].append(porcentagem)
    
    print(f"\n\nBAIRRO COM MAIOR INCIDENCIA DE CASOS:")
    print(f"total   {quant_elementos}   100%")
    for teste, valor in quant_por_testes.items():
        print(f"{teste}   {valor[0]}   {valor[1]}%")


def taxa_fatalidade(dados):
    '''
    Qual taxa de letalidade pode ser calculada a partir do conjunto de dados?
    Para calcular esta taxa, considere a fração do total de óbitos pelo total
    de casos.
    '''
    quant_elementos = 0
    quant_obtos = 0
    porcentagem = 0

    for linha in dados:
        itens_da_linha = linha.split(";")
        resultado = itens_da_linha[3]

        quant_elementos += 1

        if resultado == 'Óbito':
            quant_obtos += 1

    porcentagem = round(quant_obtos/quant_elementos, 5)
    print(f"\n\nTAXA FATALIDADE: \n{porcentagem}")



def coeficiente_correlacao_person(dados):
    '''
    Qual o tipo de correlação, mediante coeficiente de correlação de Pearson,
    entre a idade e o número de casos? Para responder a esta pergunte, agrupe o 
    número de casos por idade e efetue o cálculo de tal coeficiente. Indique, a 
    partir do resultado, a natureza desta correlação, se é positiva ou negativa,
    e qual sua intensidade.
    '''
    casos_por_idade = {}

    for linha in dados:
        itens_da_linha = linha.split(";")
        idade = int(itens_da_linha[0])

        if idade not in casos_por_idade:
            casos_por_idade[idade] = 1
        else:
            casos_por_idade[idade] += 1
    
    #todas as operacoes de somatoria necessarias
    somatorio_idades = 0
    somatorio_quant = 0
    somatorio_quadrado_idades = 0
    somatorio_quadrado_quant = 0
    somatorio_idades_x_quant = 0
    quantidade_elementos = 0
    for idade, quantidade in casos_por_idade.items():
        somatorio_idades += idade
        somatorio_quant += quantidade
        somatorio_quadrado_idades += idade**2
        somatorio_quadrado_quant += quantidade**2
        somatorio_idades_x_quant += idade*quantidade
        quantidade_elementos += quantidade

    primeiro_termo = quantidade_elementos*somatorio_idades_x_quant
    segundo_termo = somatorio_idades*somatorio_quant
    numerador = primeiro_termo - segundo_termo
    
    primeiro_termo = ((quantidade_elementos*somatorio_quadrado_idades) - somatorio_quadrado_idades)**(1/2)
    segundo_termo = ((quantidade_elementos*somatorio_quadrado_quant) - somatorio_quadrado_quant)**(1/2)
    denominador = primeiro_termo*segundo_termo

    coeficiente_de_person = numerador/denominador

    print("\n\ncasos ordenados por idade")
    contador = 0
    for key in sorted(casos_por_idade):
        if contador < 5:
            print ("{0}: {1}   ".format(key, casos_por_idade[key]), end='')
        else:
            print ("{0}: {1}".format(key, casos_por_idade[key]))
            contador = 0

        contador += 1
    
    print(f"\n\nCOEFICIENTE DE CORRELACAO DE PEARSON:")
    print("valor: {0}".format(round(coeficiente_de_person, 5)))


if (__name__ == '__main__'):
    
    dados = abrir_arquivos("dadosLimpos.txt")

    quantidade_elementos_comparatorio()

    quantidade_individuos_recuperados(dados)

    quantidade_masculinos_femininos(dados)

    bairro_com_mais_casos(dados)

    bairros_com_mais_recuperados(dados)

    tipos_testes_efetuados(dados)

    taxa_fatalidade(dados)

    idade_individuos_contaminados(dados)

    coeficiente_correlacao_person(dados)