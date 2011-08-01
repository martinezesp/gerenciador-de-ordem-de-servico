#-*-coding:utf-8-*-
'''
Created on 12/01/2011

@author: diogo
IMPORTANTE: Necessario arquivos .glade na mesma pasta
'''
import pygtk
import gobject
pygtk.require("2.0")
import gtk, gtk.glade
import funcoesGenericas
import winAlterarSenha
from bd import BancoDados
import winMenu

class Logar(object):
    def __init__(self):
        self.arquivo = gtk.glade.XML('winLogin.glade')
        self.winLogin = self.arquivo.get_widget('winLogin')
        color = gtk.gdk.color_parse('white')
        self.winLogin.modify_bg(gtk.STATE_NORMAL, color)
        self.txtSenha = self.arquivo.get_widget('txtSenha')
        self.txtLogin = self.arquivo.get_widget('txtLogin')
        self.btLogar = self.arquivo.get_widget('btLogar')
        self.btAlterarSenha = self.arquivo.get_widget('btAlterarSenha')
    
    def sair(self, button = None):
        '''Funcao para sair da tela'''
        self.winLogin.destroy()
        gtk.main_quit()
    
    def verificaTecla(self,widget, tecla):
        if tecla.keyval == 65293 or tecla.keyval == 65421:#tecla enter pressionada
            self.logar()
        elif tecla.keyval == 65307:#tecla esc pressionada função sair é executada
            self.sair()
    
    def logar(self, widget = None):
        con = BancoDados()
        try:
            admin = False
            login = self.txtLogin.get_text()
            if (self.txtSenha.get_text() == con.select("funcionario", "login, senha, administrador", 
                                                                    "where login = '" +
                                                                    login+"'")[0][1]):
                funcoesGenericas.mostrarAviso(self.winLogin, 'Entrando no sistema...')
                self.sair()
                admin = con.select("funcionario", "login, administrador", 
                                                                    "where login = '" +
                                                                    login+"'")[0][1]
                print int(admin)
                if int(admin) == 1:
                    admin = True
                janela = winMenu.menu(admin)
                janela.iniciarJanela()
            else:
                funcoesGenericas.mostrarAviso(self.winLogin, 'Login ou senha estão errados!')
        except:
            funcoesGenericas.mostrarAviso(self.winLogin, 'Login ou senha estão errados!')
    def alterar(self, widget = None):
        if(self.txtLogin.get_text() == ''):
            funcoesGenericas.mostrarAviso(self.winLogin, "Favor preencha apenas o login!")
        else:
            try:
                login = BancoDados().select("funcionario", "login", "where login = '"+
                                            self.txtLogin.get_text()+"'")[0][0]
                a = winAlterarSenha.AlterarSenha(str(login))
                a.mostrarJanela()
            except:
                funcoesGenericas.mostrarAviso(self.winLogin,"Login inexistente")
    
    def exibirTela(self):
        self.btLogar.connect('clicked', self.logar)
        self.winLogin.connect('destroy', self.sair)
        self.btAlterarSenha.connect('clicked', self.alterar)
        self.winLogin.connect('key-press-event',self.verificaTecla)
        self.winLogin.show_all()
        gtk.main()