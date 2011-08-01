#-*-coding:utf-8-*-
'''
Created on 31/07/2011

@author: Valença, João Luiz de Deus Holanda
'''
import pygtk
pygtk.require("2.0")
import gtk.glade
import gobject
from bd import BancoDados
import funcoesGenericas
import ModeloDatagrid

class GuardarOS(object):
    def __init__(self):
        self.fechar = False
        '''Arquivo'''
        self.arquivo = gtk.glade.XML('winGuardarOS.glade')
        
        '''Janela'''
        self.winGuardarOS = self.arquivo.get_widget('winGuardarOS')
        color = gtk.gdk.color_parse('white')
        self.winGuardarOS.modify_bg(gtk.STATE_NORMAL, color)
        
        self.btfSelecionarArquivo = self.arquivo.get_widget('btfSelecionarArquivo')
        
        '''Text Box'''
        self.txtNumeroOS = self.arquivo.get_widget('txtNumeroOS')
        self.txtPasta = self.arquivo.get_widget('txtPasta')
        self.txtCPFCNPJ = self.arquivo.get_widget('txtCPFCNPJ')

        '''Text View'''
        self.txtvObs = self.arquivo.get_widget('txtvObs')
        
        '''Combobox e suas configurações'''
        self.cbxNomeCliente = self.arquivo.get_widget('cbxNomeCliente')
        self.storeClientes= gtk.ListStore(gobject.TYPE_STRING)
        try:
            self.clientes = BancoDados().select('funcionario', 'nome', ' ')
            i = 0
            while i < len(self.clientes):
                self.storeClientes.append([self.clientes[i][0]])
                i+=1
            self.inserirComboBox(self.storeClientes, self.cbxNomeCliente)
            if(len(self.clientes) < 1):
                funcoesGenericas.mostrarAviso(self.winGuardarOS, 'Provavelmente nenhum funcionário'+
                                              ' foi cadastrado!'+'\nFavor cadastrar um!')
                self.fechar = True
        except:
            funcoesGenericas.mostrarAviso(self.winGuardarOS,'Provavelmente nenhum funcionário foi'+
                                          ' cadastrado!'+'\nFavor cadastrar um!')
            self.fechar = True
            
        self.cbxServicos = self.arquivo.get_widget('cbxServicos')
        self.storeServicos = gtk.ListStore(gobject.TYPE_STRING)
        try:
            self.servicos = BancoDados().select('servico', 'nome', ' ')
            i = 0
            while i < len(self.servicos):
                self.storeServicos.append([self.servicos[i][0]])
                i+=1
            self.inserirComboBox(self.storeServicos, self.cbxServicos)
            if(len(self.clientes) < 1):
                funcoesGenericas.mostrarAviso(self.winGuardarOS, 'Nenhum serviço cadastrado!'+
                                              '\nFavor cadastrar pelo menos um serviço')
                self.fechar = True
        except:
            funcoesGenericas.mostrarAviso(self.winGuardarOS,'Nenhum serviço cadastrado!'+
                                              '\nFavor cadastrar pelo menos um serviço')
            self.fechar = True
        
        '''Botões'''
        self.btVerifica = self.arquivo.get_widget('btVerifica')
        self.btInserirServico = self.arquivo.get_widget('btInserirServico')
        self.btRemoverServico = self.arquivo.get_widget('btRemoverServico')
        self.btGravarOS = self.arquivo.get_widget('btGravarOS')
        self.btLimpar = self.arquivo.get_widget('btLimpar')
        
        '''Label'''
        self.lblNomeCliente = self.arquivo.get_widget('lblNomeCliente')
        self.textelbl = self.lblNomeCliente.get_text()
        
        '''Instanciando um objeto para usar a classe ModeloDatagrid'''
        self.dataGrid = ModeloDatagrid.ModeloDataGrid()
        
        '''Iniciando o treeView'''
        self.inicio = True        
        self.iniciarTreeview()
        self.excluir = False
        self.servicoSelecionado = 0
        
    def iniciarTreeview(self):
        '''Iniciando os valores da tabela contida no TreeView''' 
        if self.inicio:
            self.modeloLista = gtk.ListStore(str, str)
            self.trvServicosEscolhidos = self.arquivo.get_widget('trvServicosEscolhidos')
            self.ID = [0,1]
            self.nomes = ["Nome","Descrição"]
            self.dataGrid.definirTabela(2, self.ID, self.nomes, self.trvServicosEscolhidos, 
                                        self.modeloLista)
            self.ListaParaAdicionar = []
        else:
            self.ListaParaAdicionar.sort()
            self.inserindoNoDataGrid(self.ListaParaAdicionar)
    
    def inserindoNoDataGrid(self,listaParaAdicionar):
        '''Coloca os valores no tree view'''
        i = 0
        for i in range(len(listaParaAdicionar)):
            self.dataGrid.inserirNoTreeView(self.modeloLista, listaParaAdicionar[i])
    
    def excluirServico(self, widget = None):
        '''Exclui um servico que foi escolhido erroneamente'''
        listaAux = self.ListaParaAdicionar
        self.servicosAtuais = self.dataGrid.getValor(self.trvServicosEscolhidos, 1)
        self.servicoSelecionado = self.dataGrid.getValor(self.trvServicosEscolhidos, 0)
        for i in range(len(listaAux)):
            if listaAux[i][0] == self.servicoSelecionado:
                break
        listaAux.pop(i)
        self.atualizar()
    
    def pegarValorComboBox(self, widget):
        '''Retorna o valor selecionado no combobox'''
        model = widget.get_model()
        iter = widget.get_active_iter()
        try:
            ComboChoice =  model.get_value(iter, 0)
            return ComboChoice + ""
        except:
            print '\n'
        
    def adicionarServicoNaLista(self, widget = None):
        jaTem = False
        servicoEscolhido = self.pegarValorComboBox(self.cbxServicos)
        descricao = BancoDados().select(" servico ", " descricao, nome ", " where nome = '"+ 
                                      servicoEscolhido + "'")[0][0]
        j = 0
        while j in range(len(self.ListaParaAdicionar)):
            if servicoEscolhido == self.ListaParaAdicionar[j][0]:
                funcoesGenericas.mostrarAviso(self.winGuardarOS,"Serviço já escolhido."+
                                              " Favor selecionar outro!")
                jaTem = True
                break
            j+=1
        if not(jaTem):
            self.ListaParaAdicionar.append([servicoEscolhido,descricao])
            self.atualizar()
    
    def atualizar(self):
        '''Atualiza o tree View'''
        self.inicio = False
        self.modeloLista.clear()
        self.iniciarTreeview()
        
    def inserirComboBox(self, lista, cbx):
        '''Insere Valores no combobox'''
        cbx.set_model(lista)
        self.cell = gtk.CellRendererText()
        cbx.pack_start(self.cell, True)
        cbx.add_attribute(self.cell, 'text',0)
        
    def sair(self, fechamento = None):
        '''Fecha a janela'''
        self.winGuardarOS.destroy()
        gtk.main_quit()    
    
    def verificaDocumento(self, widget = None):
        eIgual = False
        numeracaoDocumentos = BancoDados().select(' cliente ', ' documento, nome ', ' ')
        i = 0
        posicao = None
        while i < len(numeracaoDocumentos):
            if numeracaoDocumentos[i][0] == self.txtCPFCNPJ.get_text():
                eIgual = True
                posicao = i
                i = len(numeracaoDocumentos)
            i+=1
        if eIgual:
            self.lblNomeCliente.set_text(numeracaoDocumentos[posicao][1])
        else:
            funcoesGenericas.mostrarAviso(self.winGuardarOS, 'Numero de Documento inválido!!')
            self.lblNomeCliente.set_text(self.textelbl)
            
    def limpar(self, widget = None):
        self.txtCPFCNPJ.set_text('')
        self.txtNumeroOS.set_text('')
        self.txtPasta.set_text('')
        self.txtvObs.get_buffer().set_text('')
        self.ListaParaAdicionar = []
        self.atualizar()
        
    def copiarImagem(self):
        origem = ('/'+str(self.btfSelecionarArquivo.get_file()).split(':')[2].split('>')[0][3:])
        nomeArquivo = (str(self.btfSelecionarArquivo.get_file()).split(':')[2].split('>')[0][3:].split('/'))
        nomeArquivo = nomeArquivo[len(nomeArquivo)-1]
        
        print "origem = "+(origem)
        input = file((origem), 'r')
        output = file('OS/'+nomeArquivo, "w")
        for line in input:
            output.write(line)
        input.close()
        output.close()
        return 'OS/'+nomeArquivo
        
    def guardarOS(self, widget = None):
        '''Armazena no banco a relação OS e serviço'''
        try:
            valor = BancoDados().select("os", "id, alterada", "where id ='"+self.txtNumeroOS.get_text()+"'")
            existe = False
            print (valor)
            m = 0
            while m < len(valor):
                print valor[m][0]
                if(valor[m][0] == int(self.txtNumeroOS.get_text()) and valor[m][1] != 1):
                    existe = True
                m+=1
            if existe and self.lblNomeCliente.get_text() != 'Sem Cliente Selecionado' and \
            self.txtCPFCNPJ != '' and self.txtPasta != '' and self.pegarValorComboBox(self.cbxNomeCliente)!=\
            None and self.btfSelecionarArquivo.get_file() != None:
                local = self.copiarImagem()
                k = 0
                idFuncinario = BancoDados().select("funcionario", "id", "where nome = '"+
                                                   self.pegarValorComboBox(self.cbxNomeCliente)+"'")[0][0]
                idCliente = BancoDados().select("cliente", "id", "where nome = '"+self.lblNomeCliente.get_text()+"'")[0][0]
                dict = {"obs":self.txtvObs.get_buffer().get_text(self.txtvObs.get_buffer().\
                            get_start_iter(),self.txtvObs.get_buffer().get_end_iter()),
                        "cliente_id":idCliente,
                        "funcionario_id": idFuncinario,
                        "scaner":local,
                        "pasta":self.txtPasta.get_text(),
                        "alterada": 1
                        }
                dict2 = {"id":self.txtNumeroOS.get_text()}
                alteracao = BancoDados().update("os", dict, dict2)
                if(alteracao != None):
                    while k in range(len(self.ListaParaAdicionar)):
                        id = BancoDados().select("servico", "id", "where nome = '"+self.ListaParaAdicionar[k][0]
                                                 +"'")[0][0]
                        if BancoDados().inserir('os_servico', {
                                                               "servico_id" : str(id),
                                                               "os_id":self.txtNumeroOS.get_text()
                                                               }) == None:
                            print 'Erro servico None'
                        k += 1
                        print self.txtNumeroOS.get_text()
                        print 'id = '+str(id)
                else:
                    funcoesGenericas.mostrarAviso(self.winGuardarOS, "O número da OS não existe")
                self.limpar()
            else:
                funcoesGenericas.mostrarAviso(self.winGuardarOS,"Possiveis problemas:\n"+
                                              "1- O número da OS não existe;\n"+
                                              "2- Não preencheu todos os Campos;\n"+
                                              "3- Não escolheu nenhum serviço;\n"+
                                              "4- A ordem de serviço já foi guardada. Caso deseje alterar "+ 
                                              "vá no menu e selecione alterar OS\n"+
                                              "5- Não escolheu nenhum funcionário;\n"+
                                              "6- A cópida da OS não foi selecionada.")
        except:
            funcoesGenericas.mostrarAviso(self.winGuardarOS, "Erro ao copiar imagem!!!!\n"+
                                          "Verifique se o endereço da imagem possui caracter especial,"+
                                          "caso contenha coloque em um local onde o endereço resultante"+
                                          "não possua caracter especial.") 
            
    def mostrarJanela(self):
        self.winGuardarOS.connect('destroy', self.sair)
        self.btVerifica.connect('clicked', self.verificaDocumento)
        self.btRemoverServico.connect('clicked', self.excluirServico)
        self.btInserirServico.connect('clicked', self.adicionarServicoNaLista)
        self.btLimpar.connect('clicked', self.limpar)
        self.btGravarOS.connect('clicked', self.guardarOS)
        self.winGuardarOS.show_all()
        if self.fechar:
            self.sair()
        gtk.main()
        
#a = GuardarOS()
#a.mostrarJanela()