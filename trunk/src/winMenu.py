#-*-coding:utf-8-*-
'''
Created on 13/01/2011

@author: João Luiz
'''
import pygtk
pygtk.require("2.0")
import gtk.glade
'''Import das janelas'''
import winSobre

import winCadastrarCliente
import winListaCliente

import CadastrarFunionario
import winListaFuncinario

import wincadastrarServico
import winListaServico

import winGuardarOS
import winListaOS
'''Import funçõe de outros arquivos'''
import funcoesGenericas
from bd import BancoDados

class menu(object):
    def __init__(self, administration = False):
        '''Arquivo'''
        self.arquivo = gtk.glade.XML('winMenu.glade')
        
        self.administrador = administration
        
        '''Janela'''
        self.winMenu = self.arquivo.get_widget('winMenu')
        color = gtk.gdk.color_parse('white')
        self.winMenu.modify_bg(gtk.STATE_NORMAL, color)
        
        '''Botões'''
        self.btCadastrarCliente = self.arquivo.get_widget('btCadastrarCliente')
        self.btCadastrarFuncionario = self.arquivo.get_widget('btCadastrarFuncionario')
        self.btGerarOS = self.arquivo.get_widget('btGerarOS')
        self.btGuardarOS = self.arquivo.get_widget('btGuardarOS')
        self.btConsultarServicos = self.arquivo.get_widget('btConsultarServicos')
        self.btCadastrarServico = self.arquivo.get_widget('btCadastrarServico')
        self.btConsultarOS = self.arquivo.get_widget('btConsultarOS')
        self.btConsultarCliente = self.arquivo.get_widget('btConsultarCliente')
        self.btConsultarFuncionario = self.arquivo.get_widget('btConsultarFuncionario')
        self.btCreditos = self.arquivo.get_widget('btCreditos')
        
        '''Imagens'''
        self.imgDord = self.arquivo.get_widget('imgDord')
        self.imgDord.set_from_file('img/logoEmpresa.png')
                
        '''Label'''
        self.label1 = self.arquivo.get_widget('label1')
        self.label1.set_use_markup(True)
        self.label1.set_markup('<span size="32000" foreground="black"><b>'+ self.label1.get_text() +'</b></span>')
        
        self.lblDord = self.arquivo.get_widget('lblDord')
        self.lblDord.set_use_markup(True)
        self.lblDord.set_markup('<span size="20900" foreground="#28166f"><b>Dord Consultoria em Informática</b></span>')
    
    def sair(self, widget = None):
        gtk.main_quit()
    
    def cadastrarFuncionario(self, widget = None):
        if self.administrador:
            janela = CadastrarFunionario.CadastroFuncionario()
            janela.iniciarJanela()
        else:
            funcoesGenericas.mostrarAviso(self.winMenu, "Só administradores podem cadastrar funcionários!!!")
    
    def cadastrarCliente(self, widget = None):
        janela = winCadastrarCliente.CadastrarEmpresa()
        janela.iniciarJanela()
        
    def cadastrarServico(self, widget = None):
        janela = wincadastrarServico.CadastroServico()
        janela.mostrarJanela()
    
    def guardarOS(self, widget = None):
        janela = winGuardarOS.GuardarOS()
        janela.mostrarJanela()
        
    def gerarOS(self, widget = None):
        dictOS = {"obs":"Não foi alterada",
                    "cliente_id": 1,
                    "funcionario_id": 1,
                    #"scaner":blob,
                    "pasta":"0 - 0",
                    "alterada": 0
                    }
        criar = BancoDados().inserir("os", dictOS)
        if criar != None:
            numeroOS = BancoDados().select("os", "count(*)", ' ')
            funcoesGenericas.mostrarAviso(self.winMenu, "O número da OS é: "+ str(numeroOS[0][0]))
        else:
            funcoesGenericas.mostrarAviso(self.winMenu, "Erro ao gerar a Ordem de Serviço.")
            
    def consultarOS(self, widget = None):
        janela = winListaOS.ListaOS()
        janela.iniciarJanela()
        
    def consultarClientes(self, widget = None):
        janela = winListaCliente.ListaCliente()
        janela.iniciarJanela()
    
    def consultarServicos(self, widget = None):
        janela = winListaServico.ListaServico()
        janela.iniciarJanela()
    
    def consultarFuncionario(self, widget = None):
        janela = winListaFuncinario.ListaFuncionario(self.administrador)
        janela.iniciarJanela()
    
    def mostrarSobre(self, widget = None):
        janela = winSobre.Sobre()
        janela.iniciarJanela()
    
    def iniciarJanela(self):
        '''Funcao que abre a janela'''
        self.btCreditos.connect('clicked', self.mostrarSobre)
        
        self.btCadastrarCliente.connect('clicked', self.cadastrarCliente)
        self.btConsultarCliente.connect('clicked', self.consultarClientes)
        
        self.btCadastrarFuncionario.connect('clicked', self.cadastrarFuncionario)
        self.btConsultarFuncionario.connect('clicked', self.consultarFuncionario)
        
        self.btCadastrarServico.connect('clicked', self.cadastrarServico)
        self.btConsultarServicos.connect('clicked', self.consultarServicos)
        
        self.btGuardarOS.connect('clicked',self.guardarOS)
        self.btGerarOS.connect('clicked',self.gerarOS)
        self.btConsultarOS.connect('clicked',self.consultarOS)
        
        self.winMenu.connect('destroy', self.sair)
        self.winMenu.show_all()
        gtk.main()