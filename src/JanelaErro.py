#-*-coding:utf-8-*-
'''
Created on 19/01/2011

@author: João Luiz
'''
import gtk


def mostrarAviso(janela, mensagem, titulo = 'Aviso!'):
    """Mostra na tela uma mensagem e um botao de OK.
     Recebe a janela que esta padrao na tela no momento e uma string de mensagem """
    dialog = gtk.Dialog(titulo,
                 janela,  # the window that spawned this dialog
                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,("OK", 1))
    dialog.vbox.pack_start(gtk.Label(mensagem))
    dialog.show_all()
    result = dialog.run()
    if result == 1:
        dialog.destroy()