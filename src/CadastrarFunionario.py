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
import JanelaErro
import gobject


class CadastroFuncionario(object):
    '''Classe de comunicação com a janela cadastro de Funcionario '''
    
    '''Metodos'''
    
    def __init__(self, primeiroAcesso = False):
        '''Construtor'''
        '''Arquivo'''
        self.janelaPrincipal = gtk.glade.XML('winCadastrarFuncionario.glade')
        self.primeiroAcesso = primeiroAcesso
        
        '''Janela'''
        self.winCadastrarFuncionario = self.janelaPrincipal.get_widget('winCadastrarFuncionario')
        color = gtk.gdk.color_parse('white')
        self.winCadastrarFuncionario.modify_bg(gtk.STATE_NORMAL, color)        
        
        '''TextBoxs'''
        self.txtNome = self.janelaPrincipal.get_widget('txtNome')
        self.txtLogin = self.janelaPrincipal.get_widget('txtLogin')
        self.txtSenha = self.janelaPrincipal.get_widget('txtSenha')
        self.txtCodigo = self.janelaPrincipal.get_widget('txtCodigo')
        self.tvObservacao = self.janelaPrincipal.get_widget('tvObservacao')
        self.txtNascimento = self.janelaPrincipal.get_widget('txtDataNascimento')
        self.txtEndereco = self.janelaPrincipal.get_widget('txtEndereco')
        self.txtNumero = self.janelaPrincipal.get_widget('txtNumero')
        self.txtComplemento =  self.janelaPrincipal.get_widget('txtComplemento')
        self.txtBairro = self.janelaPrincipal.get_widget('txtBairro')
        self.txtCidade = self.janelaPrincipal.get_widget('txtCidade')
        self.txtEstado = self.janelaPrincipal.get_widget('txtEstado')
        self.txtTelefone = self.janelaPrincipal.get_widget('txtTelefone')
        self.txtDDD = self.janelaPrincipal.get_widget('txtDDD')
        self.txtEmail = self.janelaPrincipal.get_widget('txtEmail')
        self.txtDocumento = self.janelaPrincipal.get_widget('txtDocumento')
        self.txtCEP = self.janelaPrincipal.get_widget('txtCEP')
        
        '''Imagens'''
        self.fcbFoto = self.janelaPrincipal.get_widget('fcbFoto')
        
        '''ComboBoxs'''
        self.cbxTipoDocumento = self.janelaPrincipal.get_widget('cbxTipoDocumento')
        self.cbxCargo = self.janelaPrincipal.get_widget('cbxCargo')
        
        self.rbSim = self.janelaPrincipal.get_widget('rbSim')
        self.rbNao = self.janelaPrincipal.get_widget('rbNao')
        
        '''Botões'''
        self.btFinalizar = self.janelaPrincipal.get_widget('btEntrada')
        self.btSair = self.janelaPrincipal.get_widget('btSair')
        self.btLimpar = self.janelaPrincipal.get_widget('btLimpar')
        
        
        '''Lista com os valores do Combo Box Tipo de Documento'''
        self.listaDocumentos = gtk.ListStore(gobject.TYPE_STRING)
        self.listaDocumentos.append(['Carteira de Trabalho'])
        self.listaDocumentos.append(['RG'])
        self.listaDocumentos.append(['CPF'])
        self.listaDocumentos.append(['Outro'])
        
        '''Colocando os valores no ComboBox Tipo de Documento'''
        self.cbxTipoDocumento.set_model(self.listaDocumentos)
        cell = gtk.CellRendererText()
        self.cbxTipoDocumento.pack_start(cell, True)
        self.cbxTipoDocumento.add_attribute(cell, 'text',0)
        
        '''Lista com os valores do Combo Box Cargo'''
        self.listaCargo = gtk.ListStore(gobject.TYPE_STRING)
        self.listaCargo.append(['Administrador'])
        self.listaCargo.append(['Vendedor'])
        self.listaCargo.append(['Gerente'])
        self.listaCargo.append(['Outro'])
        
        '''Colocando os valores no ComboBox Cargo'''
        self.cbxCargo.set_model(self.listaCargo)
        cell2 = gtk.CellRendererText()
        self.cbxCargo.pack_start(cell2, True)
        self.cbxCargo.add_attribute(cell2, 'text',0)

    def valorTipoDocumento(self):
        '''Funao que retorna o valor do combo box tipo de documento'''
        self.valorAtual = self.cbxTipoDocumento.get_model()
        self.iter = self.cbxTipoDocFornecedorumento.get_active_iter()
        self.ComboChoice =  self.valorAtual.get_value(self.iter, 0)
        return self.ComboChoice
    
    def valorCargo(self):
        '''Funao que retorna o valor do combo box cargo'''
        self.valorFinal = self.cbxCargo.get_model()
        self.iter2 = self.cbxCargo.get_active_iter()
        self.ComboChoice2 =  self.valorFinal.get_value(self.iter2, 0)
        return self.ComboChoice2
        
    def cadastrarFuncionario(self, button):
        '''Funcao que e executada quando o botao cadastrar for clicado ja tratando os campos obrigatorios'''
        if self.txtNome.get_text()  == '' or self.txtEndereco.get_text() == ''or self.txtTelefone.get_text() == '' or self.txtDDD.get_text() == '' or self.txtDocumento.get_text() == '' or self.txtLogin.get_text() == '' or self.txtSenha.get_text() == '':
            '''Caso algum campo obrigatorio nao for preenchido ele nao cadastrara'''
            JanelaErro.mostrarAviso(self.winCadastrarFuncionario,'Algum campo obrigatório não foi preenchido.\nFavor preenchê-lo')
        else:
            if self.txtNumero.get_text().isdigit() and self.txtDDD.get_text().isdigit():
                '''Aqui vao ficar todas as funcoes de conexao com banco de dados para cadastro de fornecedor'''
                if self.persistirCadastro():
                    JanelaErro.mostrarAviso(self.winCadastrarFuncionario,"Cadastro realizado com sucesso!")
                    self.limparCadastro(self.btLimpar)
                else:
                    JanelaErro.mostrarAviso(self.winCadastrarFuncionario,"Erro ao tentar cadastrar o Funcionário")
            else:
                JanelaErro.mostrarAviso(self.winCadastrarFuncionario,'Algum campo que deveria conter apenas números, contém letras.\nFavor corrigir!')
    
        
    def persistirCadastro(self):
        """Funcao local para persistir o cadastro do funcionario no banco de dados"""
        if(self.primeiroAcesso):
            admin = '1'
        else:
            if self.rbSim.get_active():
                admin = '1'
            else:
                admin = '0'
        dictCampos = {"NOME" : self.txtNome.get_text(),
                       "LOGIN" : self.txtLogin.get_text(),
                       "SENHA" : self.txtSenha.get_text(),
                       "DOCUMENTO" : self.txtDocumento.get_text(),
                       "TIPO_DOCUMENTO" : funcoesGenericas.getValorAtualComboBox(self.cbxTipoDocumento),       
                       "TELEFONE" : self.txtTelefone.get_text(),
                       "DDD" : self.txtDDD.get_text(),
                       "EMAIL" : self.txtEmail.get_text(),
                       "CEP" : self.txtCEP.get_text(),
                       "NASCIMENTO": self.txtNascimento.get_text(),
                       "CARGO": funcoesGenericas.getValorAtualComboBox(self.cbxCargo),
                       "ENDERECO" : funcoesGenericas.formatarEndereco(self.txtEndereco.get_text(), 
                                                                      self.txtNumero.get_text(),
                                                                      self.txtComplemento.get_text(),
                                                                      self.txtBairro.get_text(),
                                                                      self.txtCidade.get_text(), 
                                                                      self.txtEstado.get_text()),
                      "administrador": admin
                      } 
        con = BancoDados()

        if con.inserir("funcionario",dictCampos) != None:
            return True
        else:
            return False
    
  
    def sairCadastro(self, button):
        '''Funcao para sair da tela'''
        self.winCadastrarFuncionario.destroy()
        gtk.main_quit()
    def limparCadastro(self, button):
        '''Funcao para limpar os campos'''
        self.txtNome.set_text('')
        self.txtEndereco.set_text('')
        self.txtNumero.set_text('')
        self.txtComplemento.set_text('')
        self.txtBairro.set_text('')
        self.txtCidade.set_text('')
        self.txtEstado.set_text('')
        self.txtTelefone.set_text('')
        self.txtDDD.set_text('DDD')
        self.txtEmail.set_text('')
        self.txtDocumento.set_text('')
        self.tvObservacao.get_buffer().set_text("")
        self.txtLogin.set_text('')
        self.txtSenha.set_text('')
        self.txtCodigo.set_text('')
        self.txtNascimento.set_text('')
        self.txtCEP.set_text('')
        
    def iniciarJanela(self):
        '''Funcao que abre a janela'''
        self.winCadastrarFuncionario.connect('destroy',self.sairCadastro)
        self.btFinalizar.connect('clicked', self.cadastrarFuncionario)
        self.btLimpar.connect('clicked', self.limparCadastro)
        self.btSair.connect('clicked', self.sairCadastro)
        self.winCadastrarFuncionario.show_all()
        gtk.main()

        
if __name__ == "__main__":
    janela = CadastroFuncionario()
    janela.iniciarJanela()