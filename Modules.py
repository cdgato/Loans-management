"""
Módulo contendo toda lógica do sistema de emprestimos
"""
import pickle
import PySimpleGUI as sg
from datetime import datetime
from operator import itemgetter

try:
    with open('dadosEmprestimos.bin', 'rb') as arquivo:
        EMPRESTIMOS = pickle.load(arquivo)
except FileNotFoundError:
    EMPRESTIMOS = []


def cadastrar(informacoes):
    """
    Esta função irá passar os dados de uma lista para um dicionário,
    e passará ele para a lista contendo todos emprestimos.
    :param informacoes: a função receberá uma lista de strings
    :return: 0 para testes.
    """
    try:
        nome = informacoes[0]
        telefone = informacoes[1]
        celular = informacoes[2]
        email = informacoes[3]
        vivencia = informacoes[4]
        data = informacoes[5]
        item = informacoes[6]
        data = datetime.strptime(data, '%d/%m/%Y').date()
        emprestimo = {'nome': nome, 'telefone': telefone, 'celular': celular, 'email': email,
                      'vivencia': vivencia, 'item': item, 'data': data}

        EMPRESTIMOS.append(emprestimo)
        EMPRESTIMOS.sort(key=itemgetter('data'))
        gravar_dados()
        sg.Popup("Cadastro realizado com sucesso", button_color=('white', 'springgreen4'))
        return 0
    except ValueError:
        sg.Popup("Erro no cadastro", button_color=('white', 'springgreen4'))
        return -1


def editar_emprestimo(identificador, novas_informarcoes):
    """
    Função que atualizará dados de um emprestimo já realizado
    :param identificador: recebe o nome em forma de string
    :param novas_informarcoes: recebe uma lista, das novas informações do emprestimo
    :return: 0, para testes
    """
    for emprestimo in EMPRESTIMOS:
        if identificador == emprestimo['nome']:
            emprestimo['nome'] = novas_informarcoes[0]
            emprestimo['telefone'] = novas_informarcoes[1]
            emprestimo['celular'] = novas_informarcoes[2]
            emprestimo['email'] = novas_informarcoes[3]
            emprestimo['vivencia'] = novas_informarcoes[4]
            data = novas_informarcoes[5]
            emprestimo['data'] = datetime.strptime(data, '%d/%m/%Y').date()
            emprestimo['item'] = novas_informarcoes[6]
            gravar_dados()
            return 0
    return -2


def listar_emprestimos():
    """
    Esta é para quando se quiser listar todos os emprestimos, ainda, cadastrados no sistema
    :return: a própria lista de emprestimos
    """
    return EMPRESTIMOS


def buscar_nome(nome):
    """
    Função que irá atrás de um nome recebido, e verificará se está na lista de emprestimos
    :param nome: recebe uma string, que será o nome para quem emprestou
    :return: o dicionário, contendo o nome pesquisado
    """
    for emprestimo in EMPRESTIMOS:
        if nome in emprestimo['nome']:
            return emprestimo
    return -3


def get_informacoes(mes = '', ano = '', item = '', nome = ''):
    """
    função que dará uma lista de nomes, de acordo com o que está sendo buscado.
    :param mes: um objeto datetime.date.month que será passado através da tela de busca.
    :param ano: um objeto datetime.date.year que será passado através da tela de busca.
    :param item: uma string que será passado através da tela de busca.
    :param nome: uma string que será passado através da tela de busca.
    :return: retorna uma lista de nomes.
    """
    lista_nomes = []
    if mes != '' and ano == '':
        for emprestimo in EMPRESTIMOS:
            if mes == emprestimo['data'].month:
                lista_nomes.append(emprestimo['nome'])
        return lista_nomes
    if ano != '' and mes == '':
        for emprestimo in EMPRESTIMOS:
            if ano == emprestimo['data'].year:
                lista_nomes.append(emprestimo['nome'])
        return lista_nomes
    if ano != '' and mes != '':
        for emprestimo in EMPRESTIMOS:
            if ano == emprestimo['data'].year and mes == emprestimo['data'].month:
                lista_nomes.append(emprestimo['nome'])
        return lista_nomes
    if item != '':
        for emprestimo in EMPRESTIMOS:
            if item.lower() in emprestimo['item'].lower():
                lista_nomes.append(emprestimo['nome'])
        return lista_nomes
    if nome != '':
        for emprestimo in EMPRESTIMOS:
            if nome.lower() in emprestimo['nome'].lower():
                lista_nomes.append(emprestimo['nome'])
        return lista_nomes
    if nome == '':
        for emprestimo in EMPRESTIMOS:
            lista_nomes.append(emprestimo['nome'])
        return lista_nomes



def gravar_dados():
    """
    Função irar escrever os dados, em binário, no disco da máquina.
    :return: 0, para testes
    """
    with open('dadosEmprestimos.bin', 'wb') as arquivo:
        pickle.dump(EMPRESTIMOS, arquivo)
        return 0
    return -4


def ler_dados():
    """
    Função irar ler os dados, em binário, no disco da máquina.
    :return: 0, para testes
    """
    try:
        with open('dadosEmprestimos.bin', 'rb') as arquivo:
            global EMPRESTIMOS
            EMPRESTIMOS = pickle.load(arquivo)
            return 0
    except FileNotFoundError:
        return -1


def exlcuir_emprestimo(nome):
    """
    Funcionará em auxílio com o função busca, caso a pessoa deseje excluir o empréstimo que buscou.
    :param emprestimo: receberá um dicionário, contento o emprestimo que deseja excluir
    :return: 0, para testes
    """
    for emprestimo in EMPRESTIMOS:
        if nome == emprestimo['nome']:
            EMPRESTIMOS.remove(emprestimo)
            gravar_dados()
            sg.Popup("Apagado com sucesso!", button_color=('white', 'springgreen4'))
    return 0

