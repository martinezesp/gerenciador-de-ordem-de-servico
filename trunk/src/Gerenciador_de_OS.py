#-*-coding:utf-8-*-
'''
Created on 31/07/2011

@author: Valença, João Luiz de Deus Holanda
'''
import pygtk
import gobject
pygtk.require("2.0")
import gtk, gtk.glade
import funcoesGenericas
import CadastrarFunionario
import winLogin
from bd import BancoDados

a = BancoDados().select("funcionario", "count(*)", '')
if int(a[0][0]) == 0:
    funcoesGenericas.mostrarAviso(None, "Primeiro acesso, favor cadastrar um funcionário como administrador!!")
    janela = CadastrarFunionario.CadastroFuncionario(True)
    janela.iniciarJanela()
    janela = winLogin.Logar()
    janela.exibirTela()
else:
    janela = winLogin.Logar()
    janela.exibirTela()