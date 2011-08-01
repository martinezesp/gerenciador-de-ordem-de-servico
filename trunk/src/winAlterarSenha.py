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

class AlterarSenha(object):
    def __init__(self, login = None, admin = False):
        '''Arquivo'''
        self.arquivo = gtk.glade.XML('winAlterarSenha.glade')
        self.admin = admin
        
        self.login = login
        
        '''Janela'''
        self.winAlterarSenha = self.arquivo.get_widget('winAlterarSenha')
        
        '''Botões'''
        self.btAlterar = self.arquivo.get_widget('btAlterar')
        
        '''Textbox'''
        self.txtSenhaAntiga = self.arquivo.get_widget('txtSenhaAntiga')
        self.txtNovaSenha = self.arquivo.get_widget('txtNovaSenha')
        self.txtRNovaSenha = self.arquivo.get_widget('txtRNovaSenha')
    
    def alterar(self, widget = None):
        try:
            senha = BancoDados().select("funcionario","senha" , "where login = '"+self.login+"'")[0][0]
            if(senha == self.txtSenhaAntiga.get_text() or self.admin):
                if(self.txtNovaSenha.get_text() == self.txtRNovaSenha.get_text()):
                    a = BancoDados().update("funcionario", {"senha":self.txtNovaSenha.get_text()}, {"login":self.login})
                    if(a != None):
                        self.txtNovaSenha.set_text('')
                        self.txtRNovaSenha.set_text('')
                        self.txtSenhaAntiga.set_text('')
                        funcoesGenericas.mostrarAviso(self.winAlterarSenha,"Senha alterada com sucesso!")
                    else:
                        funcoesGenericas.mostrarAviso(self.winAlterarSenha,"Erro ao alterar senha!!")
                else:
                    funcoesGenericas.mostrarAviso(self.winAlterarSenha, "Campo Nova senha Diferente do campo Repetir Nova Senha")
            else:
                funcoesGenericas.mostrarAviso(self.winAlterarSenha,"Senha incorreta")
        except:
            funcoesGenericas.mostrarAviso(self.winAlterarSenha,"Login não existe")
    
    def sair(self, fechamento = None):
        '''Fecha a janela'''
        self.winAlterarSenha.destroy()
        gtk.main_quit()
    
    def mostrarJanela(self):
        self.winAlterarSenha.connect('destroy', self.sair)
        self.btAlterar.connect('clicked', self.alterar)
        self.winAlterarSenha.show_all()
        gtk.main()
        
        
         