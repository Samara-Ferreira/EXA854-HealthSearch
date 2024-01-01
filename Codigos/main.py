'''/*******************************************************************************
Autor: Samara dos Santos Ferreira
Componente Curricular: MI - Algoritmos e Programação I
Concluido em: 03/07/2022
Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
trecho de código de outro colega ou de outro autor, tais como provindos de livros e
apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
******************************************************************************************/'''

# ------------ IMPORTAÇÕES ------------ #
import os   # Biblioteca para manipular os arquivos, caminhos e diretórios
# Código-fonte: https://github.com/python/cpython/blob/3.10/Lib/os.py

import sys  # Biblioteca para pegar os argumentos de linha

import funcoes  # Biblioteca das funções do programa

# ------------ PROGRAMA PRINCIPAL ------------ #

# Limpa o terminal após cada uso
os.system('cls')

# --- ENTRADA DO PROGRAMA
entrada = sys.argv[1::]

caminho_raiz = os.getcwd()  # Pega o caminho raíz do programa, onde o arquivo.py está armazenado

dicionario = {}

comando = entrada.pop(0)

# Caso o caminho tenha espaços em branco
if len(entrada) > 1:
    entrada = ' '.join(entrada)

elif len(entrada) >= 1 and type(entrada) == list:
    entrada = entrada[0]

# Adicionar um arquivo de texto ou diretório
if comando == '-a':
    
    if entrada:
        if 'txt' in entrada:
            dicionario = funcoes.lerArquivo(entrada, dicionario)
            dicionario = funcoes.montarDicionario(caminho_raiz, dicionario)

        else:
            dicionario = funcoes.lerDiretorio(entrada, dicionario)
            dicionario = funcoes.montarDicionario(caminho_raiz, dicionario)

    else:
        print('\n\t>> ERRO! É necessário digitar o caminho do arquivo ou do diretório após o comando.')

# Remover um arquivo ou diretório do índice
elif comando == '-r':

    if entrada:
        if 'txt' in entrada:
            dicionario = funcoes.montarDicionario(caminho_raiz, dicionario)
            dicionario = funcoes.removerArquivo(entrada, dicionario)
            funcoes.guardarIndice(caminho_raiz, dicionario)

        else:
            dicionario = funcoes.montarDicionario(caminho_raiz, dicionario)
            dicionario = funcoes.removerDiretorio(entrada, dicionario)
            funcoes.guardarIndice(caminho_raiz, dicionario)
    
    else:
        print('\n\t>> ERRO! É necessário digitar o caminho do arquivo ou do diretório após o comando.')

# Buscar uma palavra específica
elif comando == '-b':

    if entrada:
        dicionario = funcoes.montarDicionario(caminho_raiz, dicionario)
        funcoes.buscarPalavra(caminho_raiz, entrada, dicionario)

    else:
        print('\n\t>> ERRO! É necessário digitar a palavra após o comando.')

# Visualizar as informações do índice
elif comando == '-v':
    funcoes.visualizarIndice()

else:
    print('\n\t>> Opção inválida! Tente novamente.')
    print('\n\t----------- OPÇÕES VÁLIDAS -----------')
    print('\n\t[-a] Adicionar um arquivo ou diretório\n\t[-r] Remover um arquivo ou diretório\n\t[-b] Buscar uma palavra específica no Indice.txt\n\t[-v] Visualizar o índice')
    print('\n\t>> IMPORTANTE: Colocar o comando e ao lado o caminho do arquivo ou diretório, caso escolha adicionar ou remover.')
