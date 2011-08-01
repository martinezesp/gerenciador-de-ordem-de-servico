#-*-coding:utf-8-*-
'''
Created on 31/07/2011

@author: Valença, João Luiz de Deus Holanda
'''

import pygtk
pygtk.require("2.0")
import gtk, gtk.glade

class ModeloDataGrid(object):
    '''Classe usada para construir datagrid usando treeview'''
    
    def __init__(self):
        self.teste = 1
        
    def getValor(self,widget, coluna):
        '''Funcao que retorna a string correspondente a linha escolhida e a primeira coluna'''
        self.iterr = widget.get_selection().get_selected()[1]
        return widget.get_selection().get_selected()[0].get_value(self.iterr, coluna)

    def definirTabela(self,quantidadeColuna,vetorID,vetorNome,treeView, lista):
        '''
        Constructor. treeView e o ponteiro para o objeto treeview da janela.
        lista tem que ser do tipo gtk.ListStore
        '''
        for i in range(quantidadeColuna):
            self.desenharTabela(vetorID[i], vetorNome[i], treeView)
        treeView.set_model(lista)
    
    def inserirNoTreeView(self, lista, listaParaAdicionar):
        '''Funcao que insere no dataGrid o valor desejado(listaParaAdicionar)
        lista e listaParaAdicionar tem que ser do tipo gtk.ListStore
        '''
        lista.append(listaParaAdicionar)
        
    def desenharTabela(self,id, titulo, treeView):
        coluna = gtk.TreeViewColumn(titulo,gtk.CellRendererText()
                , text = id)
        coluna.set_resizable(True)        
        coluna.set_sort_column_id(id)
        treeView.append_column(coluna)
        