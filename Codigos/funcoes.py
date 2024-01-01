# ------------ IMPORTAÇÕES ------------ #
import os   # Biblioteca para manipular os arquivos, caminhos e diretórios
# Código-fonte: https://github.com/python/cpython/blob/3.10/Lib/os.py

# ------------ FUNÇÕES ------------ #

# --- Função para atualizar os dados do índice


def atualizarIndice(dicionario, dicio_indice):

    if dicionario:
        for chave in dicionario:
            # Caso a palavra já esteja no dicionário
            if dicio_indice.get(chave):
                for e in dicionario[chave]:
                    dicio_indice[chave][e] = dicionario[chave][e]
            # Caso não
            else:
                dicio_indice[chave] = dicionario[chave]

    return dicio_indice


# --- Função para buscar uma palavra específica no índice
def buscarPalavra(caminho_raiz, palavra, dicionario):
    dicionario = montarDicionario(caminho_raiz, dicionario)

    # Caso a palavra esteja no índice
    if dicionario.get(palavra):     # Verifica se aquela palavra está no índice
        dicio = dicionario[palavra]

        total = 0
        lista = []
        aux = 0

        # Percorre o dicionário em busca dos caminhos em que aquela palavra mais aparece
        while aux >= 0:
            maior = 0
            escolhido = ''

            for chave in dicio:
                if dicio[chave] > maior:
                    maior = dicio[chave]
                    escolhido = [chave, dicio[chave]]
                    aux += 1  # Ele vai percorrer o while mais uma vez, para verificar se existe um caminho com maior incidência daquela palavra

            aux -= 1

            try:    # Tenta remover a chave do dicionário, caso ela exista
                removido = dicio.pop(chave)
                lista.append(escolhido)
                # Adiciona a quantidade na vaiável do total
                total += escolhido[1]

            except KeyError:    # Caso a chave não exista
                aux -= 1

        # Função para imprimir os elementos da palavra
        imprimirPalavra(lista, palavra, total)

    # Caso a palavra não esteja no índice
    else:
        print('\n\t>> Essa palavra não está no documento\n')


# --- Função para os dados do dicionário no documento do índice
def guardarIndice(caminho_raiz, dicionario):

    caminho_atual = os.getcwd()

    # Se o caminho atual for diferente, ele muda para o caminho raíz para guardar o índice
    mudarCaminho(caminho_atual, caminho_raiz)

    # Abre o índice para escrever
    with open('Indice.txt', 'w+', encoding='utf8') as indice:
        for chave in dicionario:
            indice.write(f'{chave}: {dicionario[chave]}\n')

    # Retorna ao caminho principal
    mudarCaminho(caminho_raiz, caminho_atual)


# --- Função para guardar as palavras no dicionário
def guardarPalavras(caminho_arquivo, dicionario, parte):
    # Verifica se a chave já existe
    if dicionario.get(parte):

        # Se o caminho não existir
        if dicionario[parte].get(caminho_arquivo) == None:
            dicio_aux = {}
            dicio_aux[caminho_arquivo] = 1
            dicionario[parte].update(dicio_aux)

        # Se o caminho já existir
        else:
            numero = dicionario[parte].get(caminho_arquivo)
            numero = int(numero)
            numero += 1
            dicionario[parte][caminho_arquivo] = numero

    # Se a chave não existir
    else:
        dicio_aux = {}
        dicio_aux[rf'{caminho_arquivo}'] = 1
        dicionario[parte] = dicio_aux

    return dicionario


# --- Função para imprimir os dados de uma palavra específica
def imprimirPalavra(lista, palavra, total):
    print(f'| CHAVE: {str(palavra).title()} ')
    # Percorre os caminhos e as quantidades na lista
    for e in lista:
        print(f'| CAMINHO(S): {e[0]}')
        print(f'| QUANTIDADE: {e[1]}')
    print(f'| QUANTIDADE TOTAL: {total}')


# --- Função para mudar o caminho
def mudarCaminho(primeiro, segundo):
    if primeiro != segundo:
        os.chid(segundo)


# --- Função para ler os arquivos
def lerArquivo(caminho_arquivo, dicionario):
    try:
        with open(f'{caminho_arquivo}', 'r+', encoding='utf8') as arquivo:
            leitura = arquivo.read()
            arquivo.seek(0)

        leitura_pontua = retirarPontuacoes(leitura)

        dicionario = separarPalavras(
            caminho_arquivo, dicionario, leitura_pontua)

    except FileNotFoundError:
        print('\n\t>> Arquivo não encontrado!\n')

    return dicionario


# --- Função que separa os arquivos que serão lidos em um determinado diretório
def lerDiretorio(caminho_diretorio, dicionario):
    for caminho, diretorios, arquivos in os.walk(caminho_diretorio):

        for arquivo in arquivos:    # Percorre os arquivos daquela pasta
            # Verifica se o arquivo é txt e não é o documento para guardar o índice
            if 'txt' in arquivo and 'Indice' not in arquivo:
                primeiro = caminho_diretorio
                segundo = arquivo
                # Junta o caminho do diretório com o nome do arquivo, para conseguir o caminho do arquivo
                caminho = os.path.join(primeiro, segundo)
                dicionario = lerArquivo(caminho, dicionario)

        return dicionario


# --- Função que monta um dicionário com as informações contidas no índice
def montarDicionario(caminho_raiz, dicionario):
    # Tenta ler o documento do índice, caso ele exista
    try:
        with open('Indice.txt', 'r', encoding='utf8') as indice:
            arquivo = indice.readlines()

    # Caos o documento não seja encontrado, ele cria um novo
    except FileNotFoundError:
        arquivo = open('Indice.txt', 'w+', encoding='utf8')
        arquivo.close()
        arquivo = []

    dicio_indice = {}   # Dicionário para guardar o conteúdo do índice

    for linha in arquivo:
        contadora = 0
        aux = True

        while aux == True:
            # Pegar a chave
            if linha[contadora] == ':':
                chave = linha[:contadora]
                aux = False
            contadora += 1

        # Váriavel que armazena o dicionário
        dicio_aux = eval(linha[contadora:])

        dicio_indice[chave] = dicio_aux

    dicio_indice = atualizarIndice(dicionario, dicio_indice)

    guardarIndice(caminho_raiz, dicio_indice)

    return dicio_indice


# --- Função para remover um diretório específico do índice
def removerDiretorio(caminho_diretorio, dicionario):
    # Percorre pelos dados daquele determinado diretório
    for caminho, diretorios, arquivos in os.walk(caminho_diretorio):

        for arquivo in arquivos:
            if 'txt' in arquivo and 'Indice' not in arquivo:
                primeiro = caminho_diretorio
                segundo = arquivo
                caminho = os.path.join(primeiro, segundo)
                dicionario = removerArquivo(caminho, dicionario)

    return dicionario


# --- Função para remover um arquivo do índice
def removerArquivo(caminho_arquivo, dicionario):
    lista = []

    for chave in dicionario:

        if dicionario[chave].get(caminho_arquivo):
            dicionario[chave].pop(caminho_arquivo)

            if not dicionario[chave]:
                lista.append(chave)

    for palavra in lista:
        dicionario.pop(palavra)

    return dicionario


# --- Função para retirar as pontuações do arquivo
def retirarPontuacoes(leitura):
    pontuacao = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''

    for p in leitura:

        if p in pontuacao:
            leitura = leitura.replace(p, ' ')
    leitura = leitura.lower()

    return leitura


# --- Função que pega cada palavra do arquivo
def separarPalavras(caminho_arquivo, dicionario, leitura):
    parte = ''  # Variável usada para armazenar as partes da linha até que formem uma palavra

    for palavra in leitura:     # Percorre todas as partes da lista
        if palavra == ' ' or palavra == '\n':

            if parte != '':     # Quando uma palavra é formada
                dicionario = guardarPalavras(
                    caminho_arquivo, dicionario, parte)
                parte = ''

        else:
            parte += palavra

    return dicionario


# --- Função para visualizar o índice
def visualizarIndice():
    try:
        with open('Indice.txt', 'r', encoding='utf8') as indice:
            print()
            print(
                '-=-=-=-=-=-=-=-=-=-=-=-=-=-= DOCUMENTO: ÍNDICE -=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            print()
            arquivo = indice.readlines()

            # Se o arquivo não estiver vazio
            if arquivo:
                for a in arquivo:
                    if a != '\n':
                        print(a)

            else:
                print('\n\t>> Não há informações para serem exibidas!')

    except FileNotFoundError:
        print()
        print('\n\t>> Indice.txt não existe!')
