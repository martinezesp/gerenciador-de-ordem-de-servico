#-*-coding:utf-8-*-
'''
Created on 13/01/2011

@author: João Luiz
'''
import pygtk
import bd
pygtk.require("2.0")
import gtk.glade
from bd import BancoDados
import funcoesGenericas
import ModeloDatagrid
import winVisualizadorOS

class ListaCliente(object):
    def __init__(self):
        '''Arquivo'''
        self.arquivo = gtk.glade.XML('winListaCliente.glade')
        
        '''Janela'''
        self.winListaCliente = self.arquivo.get_widget('winListaCliente')
        
        '''Radio button'''
        self.rbEmail = self.arquivo.get_widget('rbEmail')
        self.rbDocumento = self.arquivo.get_widget('rbDocumento')
        self.rbNomeCliente = self.arquivo.get_widget('rbNomeCliente')
        
        '''Botões'''
        self.btSair = self.arquivo.get_widget('btSair')
        self.btPesquisar = self.arquivo.get_widget('btPesquisar')
        
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
            self.tvListaCliente = self.arquivo.get_widget('tvListaCliente')
            self.ID = [0,1,2,3,4]
            self.nomes = ["Nome", "Tipo - Documento", "Telefone", "Endereço", "Email"]
            self.pesquisa()
            self.dataGrid.definirTabela(5, self.ID, self.nomes, self.tvListaCliente, 
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
            if self.rbEmail.get_active():
                filtro = 'email'
            elif self.rbDocumento.get_active():
                filtro = 'documento'
            elif self.rbNomeCliente.get_active():
                filtro = 'cliente.nome'
            if self.inicio:
                clientes = BancoDados().select("cliente", " nome, tipo_documento, documento, ddd, telefone1, endereco, email", " ")
            else:
                clientes = BancoDados().select("cliente", " nome, tipo_documento, documento, ddd, telefone1, endereco, email",
                                         "where "+ filtro + " = '" + pesquisa +"' ")
            self.ListaParaAdicionar = []
            if clientes != ():
                i = 0
                while i < len(clientes):
                    self.ListaParaAdicionar.append([clientes[i][0], clientes[i][1]+ ' - ' +clientes[i][2],
                                                   '('+clientes[i][3]+')'+' '+clientes[i][4][:3]+'-'+clientes[i][4][4:],
                                                   clientes[i][5], clientes[i][6]])
                    i += 1
                self.atualizar()
            else:
                self.atualizar()
                funcoesGenericas.mostrarAviso(self.winListaCliente, "Não foi encontrado nenhum resultado para pesquisa escolhida!!!")
        else:
            funcoesGenericas.mostrarAviso(self.winListaCliente, "Digite algo no campo pesquisa!")
    
    def atualizar(self):
        '''Atualiza o tree View'''
        self.inicio = False
        self.modeloLista.clear()
        self.iniciarTreeview()
    
    def sair(self, fechamento = None):
        '''Fecha a janela'''
        self.winListaCliente.destroy()
        gtk.main_quit()
            
    def verificaTecla(self,window = None, tecla = None):
        if tecla.keyval == 65421 or tecla.keyval == 65293:
            self.pesquisa()
    
    def iniciarJanela(self):
        self.btPesquisar.connect('clicked', self.pesquisa)
        self.btSair.connect('clicked', self.sair)
        self.txtPesquisa.connect('key-press-event', self.verificaTecla)
        self.winListaCliente.connect('destroy', self.sair)
        self.winListaCliente.show_all()
        gtk.main()
