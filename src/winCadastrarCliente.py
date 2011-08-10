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
from bd import BancoDados

class CadastrarEmpresa:
    
    def __init__(self): 
        #Carrega a interface a partir do arquivo glade
        self.arvoreDeWidgets = gtk.glade.XML('winCadastrarCliente.glade')
    
    
        #Associa os widgets a variaveis;
    
        #Widget Pai (Janela Principal)
        self.janelaPrincipal = self.arvoreDeWidgets.get_widget('winCadastrarCliente')
        color = gtk.gdk.color_parse('white')
        self.janelaPrincipal.modify_bg(gtk.STATE_NORMAL, color)
    
        #Widget Filhos
    
        #Widgets Recebidos como parametros do formulario:   
        self.txtNome = self.arvoreDeWidgets.get_widget('txtNome')
        self.txtDocumento = self.arvoreDeWidgets.get_widget('txtDocumento')
        self.cbxTipoDocumento = self.arvoreDeWidgets.get_widget('cbxTipoDocumento')
        self.txtEndereco = self.arvoreDeWidgets.get_widget('txtEndereco')
        self.txtNumero = self.arvoreDeWidgets.get_widget('txtNumero')
        self.txtComplemento = self.arvoreDeWidgets.get_widget('txtComplemento')
        self.txtBairro = self.arvoreDeWidgets.get_widget('txtBairro')
        self.txtCidade = self.arvoreDeWidgets.get_widget('txtCidade')
        self.txtEstado = self.arvoreDeWidgets.get_widget('txtEstado')
        self.txtTelefone = self.arvoreDeWidgets.get_widget('txtTelefone')
        self.txtEmail = self.arvoreDeWidgets.get_widget('txtEmail')
        self.txtObservacao = self.arvoreDeWidgets.get_widget('txtObservacao')
        self.fcbLogo = self.arvoreDeWidgets.get_widget('fcbLogo')
        self.txtDDD = self.arvoreDeWidgets.get_widget('txtDDD')
    
    
        #Fim dos widgets de recebimento
    
        #Botoes
        self.btEntrada = self.arvoreDeWidgets.get_widget('btEntrada')
        self.btLimpar = self.arvoreDeWidgets.get_widget('btLimpar')
        self.btSair = self.arvoreDeWidgets.get_widget('btSair')
    
        #INICIO DO CARREGAMENTO DO COMBO BOX
        self.store = gtk.ListStore(gobject.TYPE_STRING)
        '''A partir daqui, basta inserir na lista store, os valores que irao aparecer no combo box ex:'''
        self.store.append (["CPF"])
        self.store.append (["RG"])
        self.store.append (["CNPJ"])
        self.store.append (["OUTRO"])
    
        #Colocando os valores no ComboBox
        self.cbxTipoDocumento.set_model(self.store)
        self.cell = gtk.CellRendererText()
        self.cbxTipoDocumento.pack_start(self.cell, True)
        self.cbxTipoDocumento.add_attribute(self.cell, 'text',0)

    
    
    def limpar(self,widget = None):
        self.txtNome.set_text("")
        self.txtDocumento.set_text("")
        self.txtEndereco.set_text("")
        self.txtNumero.set_text("")
        self.txtComplemento.set_text("")
        self.txtBairro.set_text("")
        self.txtCidade.set_text("")
        self.txtEstado.set_text("")
        self.txtTelefone.set_text("")
        self.txtEmail.set_text("")
        self.txtObservacao.get_buffer().set_text("")
        
        
    def persistirCadastro(self,widget):
        """Funcao local para persistir o cadastro da empresa no banco de dados"""
        #TO DO: Falta ver a parte do logo
        dictCampos = {"nome" : self.txtNome.get_text(),
                       "documento" :self.txtDocumento.get_text(),
                       "tipo_documento" : funcoesGenericas.getValorAtualComboBox(self.cbxTipoDocumento),
                       "email" : self.txtEmail.get_text(),
                       "telefone1" : self.txtTelefone.get_text(),
                       "ddd": self.txtDDD.get_text(),
                       "endereco" : funcoesGenericas.formatarEndereco(self.txtEndereco.get_text(),
                                                                      self.txtNumero.get_text(),
                                                                      self.txtComplemento.get_text(),
                                                                      self.txtBairro.get_text(),
                                                                      self.txtCidade.get_text(),
                                                                      self.txtEstado.get_text())
                        }
        con = BancoDados()
        
        if con.inserir("cliente",dictCampos) != None:
            return True
        else:
            return False
    def cadastrar(self,widget = None):
        """Funcao atrelada ao botao de cadastro"""
        if self.txtNome.get_text() == "" or self.txtDocumento.get_text() == "" or self.txtTelefone.get_text() == "" :
            funcoesGenericas.mostrarAviso(self.janelaPrincipal, "Erro, um ou mais campos obrigatorios nao foram preenchidos")
        else:
            if self.txtDocumento.get_text().isdigit() and self.txtTelefone.get_text().isdigit() and (self.txtNumero.get_text() == "" or self.txtNumero.get_text().isdigit()):
                if self.persistirCadastro(widget):
                    funcoesGenericas.mostrarAviso(self.janelaPrincipal,"Cadastro realizado com sucesso!")
                    self.limpar(0)
                else:
                    funcoesGenericas.mostrarAviso(self.janelaPrincipal,"Erro!!")
            else:
                funcoesGenericas.mostrarAviso(self.janelaPrincipal,"Algum campo que deveria conter apenas numero contem letras. Favor corrigir")
                
                
    
    def mudarcb(self,widget):
        """Funcao usada para quando mudar o valor do comboBox, mas nao faz nenhuma acao"""
        pass
        
    def sair(self,widget = None):
        self.janelaPrincipal.destroy()        
        gtk.main_quit()
        
    def iniciarJanela(self):    
        self.janelaPrincipal.connect('destroy', self.sair)
        self.btEntrada.connect('clicked', self.cadastrar)
        self.btLimpar.connect('clicked', self.limpar)
        self.btSair.connect('clicked', self.sair)
        #Exibe toda interface
        self.janelaPrincipal.show_all()
        #Inicia o loop principal de eventos (GTK MainLoop)
        gtk.main()
        

#if __name__ == "__main__":
#    janela = CadastrarEmpresa()
#    janela.iniciarJanela()
