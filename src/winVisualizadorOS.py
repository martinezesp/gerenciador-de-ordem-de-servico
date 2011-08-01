#-*-coding:utf-8-*-
'''
Created on 13/01/2011

@author: João Luiz
'''
import pygtk
import bd
pygtk.require("2.0")
import gtk.glade

class VisualizarOS(object):
    def __init__(self, enderecoImagem = 'img/logoTransparente.png'):
        print enderecoImagem
        '''Arquivo'''
        self.arquivo = gtk.glade.XML('winVisualizadorOS.glade')
        '''Janela'''
        self.winVisualizadorOS = self.arquivo.get_widget('winVisualizadorOS')
        '''Imagem'''
        self.imgOS = self.arquivo.get_widget('imgOS')
        self.imgOS.set_from_file(enderecoImagem)
        '''Botões'''
        self.btImprimir = self.arquivo.get_widget('btImprimir')
        self.btSair = self.arquivo.get_widget('btSair')
    def sair(self, fechamento = None):
        '''Fecha a janela'''
        self.winVisualizadorOS.destroy()
        gtk.main_quit()
        
    def mostrarJanela(self):
        self.winVisualizadorOS.connect('destroy', self.sair)
        self.btSair.connect('clicked', self.sair)
        self.winVisualizadorOS.show_all()
        gtk.main()       