#-*-coding:utf-8-*-
'''
Created on 31/07/2011

@author: Valença, João Luiz de Deus Holanda
'''
import pygtk
import bd
pygtk.require("2.0")
import gtk.glade
from bd import BancoDados
import funcoesGenericas
import ModeloDatagrid
import winVisualizadorOS
import winAlterarSenha

class ListaFuncionario(object):
    def __init__(self, admin = False):
        '''Arquivo'''
        self.arquivo = gtk.glade.XML('winListaFuncinario.glade')
        self.admin = admin
        
        '''Janela'''
        self.winListaFuncinario = self.arquivo.get_widget('winListaFuncinario')
        
        '''Radio button'''
        self.rbLogin = self.arquivo.get_widget('rbLogin')
        self.rbDocumento = self.arquivo.get_widget('rbDocumento')
        self.rbNomeFuncionario = self.arquivo.get_widget('rbNomeFuncionario')
        
        '''Botões'''
        self.btSair = self.arquivo.get_widget('btSair')
        self.btPesquisar = self.arquivo.get_widget('btPesquisar')
        self.btAlterarSenha = self.arquivo.get_widget('btAlterarSenha')
        
        '''Textbox'''
        self.txtPesquisa = self.arquivo.get_widget('txtPesquisa')
        
        '''Instanciando um objeto para usar a classe ModeloDatagrid'''
        self.dataGrid = ModeloDatagrid.ModeloDataGrid()
        
        '''Iniciando o treeView'''
        self.inicio = True        
        self.iniciarTreeview()
        self.excluir = False
        self.servicoSelecionado = 0    
    def iniciarTreeview(self):
        '''Iniciando os valores da tabela contida no TreeView''' 
        if self.inicio:
            self.ListaParaAdicionar = []
            self.modeloLista = gtk.ListStore(str, str, str, str, str)
            self.tvListaFuncionario = self.arquivo.get_widget('tvListaFuncionario')
            self.ID = [0,1,2,3,4]
            self.nomes = ["Login", "Nome", "Tipo - rbLoginDocumento", "Cargo", "Email"]
            self.pesquisa()
            self.dataGrid.definirTabela(5, self.ID, self.nomes, self.tvListaFuncionario, 
                                        self.modeloLista)
        else:
            self.ListaParaAdicionar.sort()
            self.inserindoNoDataGrid(self.ListaParaAdicionar)
            
    def inserindoNoDataGrid(self,listaParaAdicionar):
        '''Coloca os valores no tree view'''
        i = 0
        for i in range(len(listaParaAdicionar)):
            self.dataGrid.inserirNoTreeView(self.modeloLista, listaParaAdicionar[i])
            
    def pesquisa(self, button = None):
        if(self.txtPesquisa.get_text() != '' or (self.inicio)):
            pesquisa = self.txtPesquisa.get_text()
            if self.rbLogin.get_active():
                filtro = 'login'
            elif self.rbDocumento.get_active():
                filtro = 'documento'
            elif self.rbNomeFuncionario.get_active():
                filtro = 'nome'
            if self.inicio:
                funcionarios = BancoDados().select("funcionario", " login, nome, tipo_documento, documento, cargo,  email", " ")
            else:
                funcionarios = BancoDados().select("funcionario", " login, nome, tipo_documento, documento, cargo,  email",
                                         "where "+ filtro + " = '" + pesquisa +"' ")
            self.ListaParaAdicionar = []
            if funcionarios != ():
                i = 0
                while i < len(funcionarios):
                    self.ListaParaAdicionar.append([funcionarios[i][0], funcionarios[i][1],funcionarios[i][2]+' - '+
                                                    funcionarios[i][3],funcionarios[i][4], funcionarios[i][5]])
                    i += 1
                self.atualizar()
            else:
                self.atualizar()
                funcoesGenericas.mostrarAviso(self.winListaFuncinario, "Não foi encontrado nenhum resultado para pesquisa escolhida!!!")
        else:
            funcoesGenericas.mostrarAviso(self.winListaFuncinario, "Digite algo no campo pesquisa!")
    
    def atualizar(self):
        '''Atualiza o tree View'''
        self.inicio = False
        self.modeloLista.clear()
        self.iniciarTreeview()
    
    def sair(self, fechamento = None):
        '''Fecha a janela'''
        self.winListaFuncinario.destroy()
        gtk.main_quit()
            
    def verificaTecla(self,window = None, tecla = None):
        if tecla.keyval == 65421 or tecla.keyval == 65293:
            self.pesquisa()
    def alterar(self, widget = None):
        if not(self.admin):
            funcoesGenericas.mostrarAviso(self.winListaFuncinario, "Só administradores tem essa permissão!!")
        else:
            login = ModeloDatagrid.ModeloDataGrid().getValor(self.tvListaFuncionario, 0)
            janela = winAlterarSenha.AlterarSenha(login, self.admin)
            janela.mostrarJanela()
    
    def iniciarJanela(self):
        self.btPesquisar.connect('clicked', self.pesquisa)
        self.btSair.connect('clicked', self.sair)
        self.btAlterarSenha.connect('clicked', self.alterar)
        self.txtPesquisa.connect('key-press-event', self.verificaTecla)
        self.winListaFuncinario.connect('destroy', self.sair)
        self.winListaFuncinario.show_all()
        gtk.main()
