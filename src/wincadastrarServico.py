#-*-coding:utf-8-*-
'''
Created on 13/01/2011

@author: João Luiz
'''
import pygtk
pygtk.require("2.0")
import gtk.glade
from bd import BancoDados
import funcoesGenericas

class CadastroServico(object):
    def __init__(self):
        self.arquivo = gtk.glade.XML('wincadastrarServico.glade')
        self.wincadastrarServico = self.arquivo.get_widget('wincadastrarServico')
        color = gtk.gdk.color_parse('white')
        self.wincadastrarServico.modify_bg(gtk.STATE_NORMAL, color)
        self.txtNomeServico = self.arquivo.get_widget('txtNomeServico')
        self.txtDescricao = self.arquivo.get_widget('txtDescricao')
        self.btCadastrar = self.arquivo.get_widget('btCadastrar')
        self.btLimpar = self.arquivo.get_widget('btLimpar')
    
    def cadastrar(self, widget = None):
        
        if not(self.txtNomeServico.get_text() == '' or  self.txtDescricao.get_buffer().get_text(self.txtDescricao.get_buffer().\
                                                                      get_start_iter(),
                                                                      self.txtDescricao.get_buffer().\
                                                                      get_end_iter()) == ''):
            dict = {"nome" : self.txtNomeServico.get_text(),
                    "descricao" : self.txtDescricao.get_buffer().get_text(self.txtDescricao.get_buffer().\
                                                                          get_start_iter(),
                                                                          self.txtDescricao.get_buffer().\
                                                                          get_end_iter())
                    }
            con = BancoDados()
            if con.inserir("servico",dict) != None:
                funcoesGenericas.mostrarAviso(self.wincadastrarServico, "Serviço cadastrado com sucesso!")
                self.limpar()
            else:
                funcoesGenericas.mostrarAviso(self.wincadastrarServico, "Não foi possivel cadastrar o serviço.")
        else:
            funcoesGenericas.mostrarAviso(self.wincadastrarServico, 'Favor preencher todos os campos!')
    
    def limpar(self, windget = None):
        self.txtDescricao.get_buffer().set_text('')
        self.txtNomeServico.set_text('')
    
    def sair(self, button):
        '''Funcao para sair da tela'''
        self.wincadastrarServico.destroy()
        gtk.main_quit()
    
    def mostrarJanela(self):
        self.wincadastrarServico.connect('destroy',self.sair)
        self.btCadastrar.connect('clicked', self.cadastrar)
        self.btLimpar.connect('clicked', self.limpar)
        self.wincadastrarServico.show_all()
        gtk.main()
    
    
#a = CadastroServico()
#a.mostrarJanela()
    
    
    
    
        