#-*-coding:utf-8-*-
import MySQLdb #@UnresolvedImport
from datetime import date, datetime
import funcoesGenericas
class BancoDados(object):
    """classe que separa a camada de banco de dados do da camada logica da aplicacao"""
    def __init__(self):
        self.__con = None
        self.__cursor = None
        self.__servidor = "localhost"#Caso o banco fique em outro computador colocar o endereço aqui
        self.__usuario = "root"
        self.__senha = "senhaCadastrada" #Alterar
        self.__db = "GerenciadorOS"
        self.__conectado = False
    
    def recebeDadosConexao(self, serv, user, senha, datab):
        """metodo que recebe os dados de conexao ao BD"""
        self.__servidor = serv
        self.__usuario = user
        self.__senha = senha
        self.__db = datab
    def __conectar(self):
        """metodo que conecta ao BD"""
        if self.__conectado:
            return True
        try:
            self.__con = MySQLdb.connect(self.__servidor, self.__usuario, self.__senha)
            self.__con.select_db(self.__db)
            self.__cursor = self.__con.cursor()
            self.__conectado = True
        except:
            funcoesGenericas.mostrarAviso(None,"Erro ao conectar com o Banco de Dados")
            return False
    def desconectar(self):
        """metodo que desconecta do BD"""
        if self.__conectado:
            pass
        self.__conectado = False
        pass
    def __formata(self,arg):
        if type(arg) == str:
            return "'" + arg + "'"
        elif type(arg) == date or type(arg) == datetime:
            return "'" + arg.isoformat() + "'"
        return str(arg)
    def select(self, tabela, campos, condicao):
        """metodo que usa o select do SQL tabela->string campos->lista de string ou None para todos, condicao->dict com nome da tabela do sql e valor do campo correspondente OU string de condicao do SQL (nessa forma, a verificacao de dados deve ser feita antes de entrar nessa funcao)"""
        if self.__conectado == False:
            self.__conectar()
        if self.__conectado == True:
            if type(condicao) == type("string"):
                str = "SELECT "
                if campos == None:
                    str = str + "*"
                else:
                    str = str + campos + ' from '+ tabela + ' ' + condicao + ';'
                try:
                    self.__cursor.execute(str)
                    rs = self.__cursor.fetchall()
                    return rs
                except:
                    return None
    def update(self, tabela, dict, dict2):
        """metodo que usa o update do SQL tabela->string dict->dicionario(string,string)
        que contem os atributos a serem modificados dict2->dicionario(string,string) que contem
        o filtro para quem se quer que modifique"""
        if self.__conectado == False:
            self.__conectar()
        if self.__conectado == True:
            str = "UPDATE " + tabela + " SET "
            bool = False
            for i in dict.keys():
                if bool:
                    str = str + ", "
                else:
                    bool = True
                str = str + i + "=%s"
            str = str + " WHERE (1=1"
            for i in dict2.keys():
                str = str + " " + "AND " + i + "=%s"
            str += ");"
            try:
                self.__cursor.execute(str,tuple(dict.values()) + tuple(dict2.values()))
                b = self.__cursor.fetchall()
                return b
            except:
                return None
                
                
    def inserir(self, tabela, dict):
        """metodo que usa o insert do SQL tabela->string dict->dicionario(string,string) que contera os dados a ser inseridos nos respectivos campos"""
        if self.__conectado == False:
            self.__conectar()
        if self.__conectado == True:
            str = "INSERT INTO " + tabela + " ("
            bool = False
            for i in dict.keys():
                if bool:
                    str = str + ", "
                else:
                    bool = True
                str = str + i.upper()
            str += ") VALUES (%s" + (",%s"*(len(dict)-1)) + ")"
            try:
                self.__cursor.execute(str,tuple(dict.values()))
                b = self.__cursor.fetchall()
                return b
            except:
                return None
    def remover(self, tabela, dict):
        """metodo que usa o delete do SQL tabela->string dict->dicionario(string,string) que contem os dados para filtrar quem deve ser removido"""
        if self.__conectado == False:
            self.__conectar()
        if self.__conectado == True:
            str = "DELETE FROM " + tabela + " WHERE (1=1"
            for i in dict.keys():
                str += " " + "AND " + i + "=%s"
            str += ")"
            try:
                self.__cursor.execute(str,tuple(dict.values()))
                b = self.__cursor.fetchall()
                return b
            except:
                return None