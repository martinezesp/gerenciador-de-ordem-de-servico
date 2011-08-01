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

class ListaServico(object):
    def __init__(self):
        '''Arquivo'''
        self.arquivo = gtk.glade.XML('winListaServico.glade')
        
        '''Janela'''
        self.winListaServico = self.arquivo.get_widget('winListaServico')
        
        '''Radio button'''
        self.rbNome = self.arquivo.get_widget('rbNome')
        self.rbDescricao = self.arquivo.get_widget('rbDescricao')
        
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
            self.modeloLista = gtk.ListStore(str, str)
            self.tvListaServico = self.arquivo.get_widget('tvListaServico')
            self.ID = [0,1]
            self.nomes = ["Nome","Descrição"]
            self.pesquisa()
            self.dataGrid.definirTabela(2, self.ID, self.nomes, self.tvListaServico, 
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
            servicos = BancoDados().select("servico", " nome, descricao", " ")
            self.ListaParaAdicionar = []
            if servicos != ():
                i = 0
                while i < len(servicos):
                    texto = str(self.txtPesquisa.get_text())
                    texto = texto.upper()
                    nomes = str(servicos[i][0])
                    nomes  = nomes.upper()
                    descricoes = str(servicos[i][1])
                    descricoes = descricoes.upper()
                    if(self.rbNome.get_active() and (texto in nomes)) or (self.rbDescricao.get_active() and (texto in descricoes)):
                        self.ListaParaAdicionar.append([servicos[i][0], servicos[i][1]])
                    i += 1
                self.atualizar()
            else:
                self.atualizar()
                funcoesGenericas.mostrarAviso(self.winListaServico, "Não foi encontrado nenhum resultado para pesquisa escolhida!!!")
        else:
            funcoesGenericas.mostrarAviso(self.winListaServico, "Digite algo no campo pesquisa!")
    
    def atualizar(self):
        '''Atualiza o tree View'''
        self.inicio = False
        self.modeloLista.clear()
        self.iniciarTreeview()
    
    def sair(self, fechamento = None):
        '''Fecha a janela'''
        self.winListaServico.destroy()
        gtk.main_quit()
            
    def verificaTecla(self,window = None, tecla = None):
        if tecla.keyval == 65421 or tecla.keyval == 65293:
            self.pesquisa()
    
    def iniciarJanela(self):
        self.btPesquisar.connect('clicked', self.pesquisa)
        self.btSair.connect('clicked', self.sair)
        self.txtPesquisa.connect('key-press-event', self.verificaTecla)
        self.winListaServico.connect('destroy', self.sair)
        self.winListaServico.show_all()
        gtk.main()