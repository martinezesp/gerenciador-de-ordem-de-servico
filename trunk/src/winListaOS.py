#-*-coding:utf-8-*-
'''
Created on 31/07/2011

@author: Valença, João Luiz de Deus Holanda
'''
import pygtk
pygtk.require("2.0")
import gtk.glade
from bd import BancoDados
import funcoesGenericas
import ModeloDatagrid
import winVisualizadorOS

class ListaOS(object):
    def __init__(self):
        '''Arquivo'''
        self.arquivo = gtk.glade.XML('winListaOS.glade')
        
        '''Janela'''
        self.winListaOS = self.arquivo.get_widget('winListaOS')
        
        '''Radio button'''
        self.rbOS = self.arquivo.get_widget('rbOS')
        self.rbDocumento = self.arquivo.get_widget('rbDocumento')
        self.rbNomeCliente = self.arquivo.get_widget('rbNomeCliente')
        
        '''Botões'''
        self.btPesquisar = self.arquivo.get_widget('btPesquisar')
        self.btVisualizarOS = self.arquivo.get_widget('btVisualizarOS')
        self.btSair = self.arquivo.get_widget('btSair')
        
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
            self.modeloLista = gtk.ListStore(str, str, str, str)
            self.tvListaOS = self.arquivo.get_widget('tvListaOS')
            self.ID = [0,1,2,3]
            self.nomes = ["Nº da OS","Pasta","Documento do Cliente","Nome do Cliente"]
            self.dataGrid.definirTabela(4, self.ID, self.nomes, self.tvListaOS, 
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
        if(self.txtPesquisa.get_text() != ''):
            if self.rbOS.get_active():
                filtro = 'os.id'
            elif self.rbDocumento.get_active():
                filtro = 'cliente.documento'
            elif self.rbNomeCliente.get_active():
                filtro = 'cliente.nome'
            self.ListaParaAdicionar = []
            OS = BancoDados().select("os, cliente", " os.id, os.pasta, cliente.documento, cliente.tipo_documento" +
            ", cliente.nome ", "where cliente_id = cliente.id and "+ filtro + " = '" + self.txtPesquisa.get_text()+"' ")
            if OS != ():
                i = 0
                while i < len(OS):
                    self.ListaParaAdicionar.append([str(OS[i][0]),OS[i][1],OS[i][2]+' - '+OS[i][3], OS[i][4]])
                    i += 1
                self.atualizar()
            else:
                self.atualizar()
                funcoesGenericas.mostrarAviso(self.winListaOS, "Não foi encontrado nenhum resultado para pesquisa escolhida!!!")
        else:
            funcoesGenericas.mostrarAviso(self.winListaOS, "Digite algo no campo pesquisa!")
    
    def atualizar(self):
        '''Atualiza o tree View'''
        self.inicio = False
        self.modeloLista.clear()
        self.iniciarTreeview()
    
    def exibirOS(self, widget = None):
        id = ModeloDatagrid.ModeloDataGrid().getValor(self.tvListaOS, 0)
        imgOS = BancoDados().select("os", "scaner", " where id = '"+str(id)+"' ")
        #print imgOS[0][0]
        winVisualizadorOS.VisualizarOS('/'+imgOS[0][0]).mostrarJanela()
    
    def sair(self, fechamento = None):
        '''Fecha a janela'''
        self.winListaOS.destroy()
        gtk.main_quit()
        
    def verificaTecla(self,window = None, tecla = None):
        if tecla.keyval == 65421 or tecla.keyval == 65293:
            self.exibirOS()
            
    def verificaTeclaTXT(self,window = None, tecla = None):
        if tecla.keyval == 65421 or tecla.keyval == 65293:
            self.pesquisa()
    
    def iniciarJanela(self):
        self.btPesquisar.connect('clicked', self.pesquisa)
        self.btVisualizarOS.connect('clicked', self.exibirOS)
        self.btSair.connect('clicked', self.sair)
        self.tvListaOS.connect('key-press-event', self.verificaTecla)
        self.txtPesquisa.connect('key-press-event', self.verificaTeclaTXT)
        self.winListaOS.connect('destroy', self.sair)
        self.winListaOS.show_all()
        gtk.main()
            