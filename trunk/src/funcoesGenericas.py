#-*-coding:utf-8-*-
'''
Created on Jan 11, 2011

@author: jpaborges
'''
from datetime import date, datetime
import gtk
from gobject import TYPE_STRING
from bd import BancoDados
import sys
def logErro(mensagem):
    """Funcao usada para gravar os erros em um arquivo de log centralizado"""
    strLog = "log-" + date.today().isoformat() + ".log"
    arq_log = open(strLog,"a")
    msg = "[ERRO - " + mensagem + " - " + datetime.now().isoformat() + "]\n"
    print (msg)
    c = arq_log.write(msg)
    arq_log.close()

    
def formatarEndereco(endereco, numero, complemento, bairro, cidade, estado):
    """Funcao usada para formatar os diversos campos do endereco em um unico campo para poder ser armazenado no banco de dados """
    numero += ""
    str = endereco + ", N " + numero
    if complemento != "":
        str += " " + complemento
    str += " Bairro:" + bairro + " Cidade: " + cidade + " - " + estado
    
    return str

def mostrarAviso(janela, mensagem):
    """Mostra na tela um mensageBox, uma telinha, com uma mensagem e um botao de OK.\n
     Recebe a janela que esta padrao na tela no momento e uma string de mensagem """
    dialog = gtk.Dialog('AVISO!',
                 janela,  # the window that spawned this dialog
                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,("OK", 1))
    dialog.vbox.pack_start(gtk.Label(mensagem))
    dialog.show_all()
    result = dialog.run()
    if result == 1:
        dialog.destroy()
        
def formatarComboBox(tabela, indice, texto):
    """Funcao para preenchimento de combobox, usando banco de dados.\n
        Recebe como parametro o nome da tabela, o nome da coluna de indice, o nome da coluna de texto\n
        Retorna  1 gtkList e 1 dicionario. O dicionario tem o ID e o NOME"""
    store = None
    dicValores = {}
    b = BancoDados()
    tuplaDados = b.select(tabela, [indice,texto], "")
    if tuplaDados != None:
        store = gtk.ListStore(TYPE_STRING)
        for dado in tuplaDados:
            dicValores[dado[1]] = dado[0] #O dicionario tem a chave sendo o nome e o ID sendo o valor
            #print(dicValores)
            store.append([dado[1]])
    
    retorno = (store,dicValores)
    
    return retorno

def getValorAtualComboBox(widget):
    """Retorna o valor que esta sendo exibido no ComboBox como escolha apenas. Recebe como parametro um ComboBox e retorna uma string"""
    try:
        model = widget.get_model()
        iter = widget.get_active_iter()
        ComboChoice =  model.get_value(iter, 0)
        return ComboChoice + ""
    except:
        return ""
    
def getValorAtualComboBoxEntry(widget):
    """Retorna apenas o valor atual que esta escrito no combo box pelo usuario"""
    return widget.child.get_text()
    
def getIDEmpresa():
    """Retorna o id da empresa ao qual o sistema foi logado"""
    #TO DO: Implementar essa funcao
    return 0

def getIDUsuario():
    """Retorna o id do usuario ao qual o sistema foi logado"""
    #TO DO: Implementar essa funcao
    return 0

def geraDicionario(lista1,lista2):
    """Funcao usada para gerar um dicionario a partir de 2 listas de mesmo tamanho da seguinta forma:
    {lista1[0]: lista2[0], lista1[1]: lista2[1]}"""
    if len(lista1) != len(lista2):
        return None
    dic = {}
    dic = dict(zip(lista1,lista2))
    return dic

def geraListadeListas():
    """Funcao que gera uma lista de listas por um arquivo no formato:
    nome1 int1 int2 int3
    nome2 int4 int5 int6"""
    arq = open('arq.txt','r')
    a = arq.readlines()
    b = []
    for i in a:
        b = b + [list(i.split())]
    for i in b:
        for j in range(3):
            i[j+1] = int(i[j+1])
    return b
def validaTipos(var, tipo):
    """Funcao usada para validar tipos de dados.
    var->string que se deseja validar
    tipo-> string referente ao tipo que você deseja que seja validado (int, float ou datetime)"""
    if tipo == 'int':
        try:
            int(var)
            return True
        except ValueError:
            return False
    elif tipo == 'float':
        try:
            float(var)
            return True
        except ValueError:
            return False
    elif tipo == 'datetime':
        if var[2] != '/' or var[5] != '/':
            return False
        if len(var) != 10 or len(var) != 8:
            return False
        nums = var.split('/')
        for i in range(len(nums)):
            try:
                nums[i] = int(nums[i])
            except ValueError:
                return False
        if len(nums) != 3 or nums[0] > 31 or nums[1] > 12:
            return False
        if nums[0] > 29 and nums[1] == 2:
            return False
        elif nums[0] == 29 and nums[1] == 2 and not((nums[2] % 4 == 0 and nums[2] % 100 != 0) or nums[2] % 400 == 0):
            return False
        elif nums[0] == 31 and (nums[1] in [4,6,9,11]):
            return False
        return True
def converterStringParaDatetime(string):
    """funcao que, como o nome diz, converte uma string no forrmato 'dd/mm/aaaa' para uma variável datetime"""
    nums = string.split('/')
    for i in range(len(nums)):
        try:
            nums[i] = int(nums[i])
        except ValueError:
            return False
    ret = datetime(nums[2],nums[1],nums[0])
    return ret
def validarCC(value, force_cnpj=False):
    '''Funcao que verifica a validade de CPF ou CNPJ,
       recebe como parametros o CPF/CNPJ no formato de string, para definicao de CNPJ colocar o segundo parametro como True para CPF apenas colocar o primeiro parametro e/ou o segundo como False
       retorna uma tupla contendo na primeira posicao se eh valido ou nao e na segunda o tipo se eh CPF ou CNPJ'''
    def calcdv(numb):
        result = int()
        seq = reversed(((range(9, id_type[1], -1)*2)[:len(numb)]))
        for digit, base in zip(numb, seq):
            result += int(digit)*int(base)
        dv = result % 11
        return (dv < 10) and dv or 0

    id_type = (len(value)>11 or force_cnpj) \
        and ['CNPJ', 1] or ['CPF', -1]
    numb, xdv = value[:-2], value[-2:]
    dv1 = calcdv(numb)
    dv2 = calcdv(numb + str(dv1))
    return (('%d%d' % (dv1, dv2) == xdv and True or False), id_type[0])
