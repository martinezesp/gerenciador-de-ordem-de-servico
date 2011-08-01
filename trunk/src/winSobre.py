#-*-coding:utf-8-*-
'''
Created on 31/07/2011

@author: Valença, João Luiz de Deus Holanda
'''
import pygtk
pygtk.require("2.0")
import gtk.glade

class Sobre(object):
    def __init__(self):
        '''Arquivo'''
        self.janelaPrincipal = gtk.glade.XML('winSobre.glade')
        self.winSobre = self.janelaPrincipal.get_widget('winSobre')
        self.imgDord = self.janelaPrincipal.get_widget('imgDord')
        self.imgDord.set_from_file('img/logoDord.png')
        self.lblDord = self.janelaPrincipal.get_widget('lblDord')
        self.lblDord.set_use_markup(True)
        self.lblDord.set_markup('<span size="20900" foreground="#28166f"><b>Dord Consultoria em Informática</b></span>')
        self.lblEmpresa = self.janelaPrincipal.get_widget('lblEmpresa')
        self.lblVersao = self.janelaPrincipal.get_widget('lblVersao')
        self.lblUltimaLateracao = self.janelaPrincipal.get_widget('lblUltimaLateracao')
        versao, empresa, alteracao = self.lerLicenca()
        self.lblVersao.set_text(versao)
        self.lblEmpresa.set_text(empresa)
        self.lblUltimaLateracao.set_text(alteracao)
        
    def lerLicenca(self):
        arquivo = open("licenca.txt","r")
        versao = arquivo.readline()
        empresa = arquivo.readline()
        ultimaAlteracao = arquivo.readline()
        arquivo.close()
        return versao, empresa, ultimaAlteracao
    
    def sair(self, widget = None):
        self.winSobre.destroy()
        gtk.main_quit()
    
    def iniciarJanela(self):
        '''Funcao que abre a janela'''        
        self.winSobre.connect('destroy', self.sair)
        self.winSobre.show_all()
        gtk.main()      
        