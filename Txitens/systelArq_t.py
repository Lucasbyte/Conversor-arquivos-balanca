import os
import time
import os.path

pasta = '.systel/'

#proximas linhas utlitarios para movimentações de arquivo, cria pasta systel e arquivo config para fins futuros
#classe Arquivo

def lerArquivo(arquivo, r='r'):
    return open(arquivo, r, encoding='latin-1')
try: 
    config = lerArquivo('.systel/config.txt')
    config.close()
except:
    try:
        os.mkdir(pasta)
        config = lerArquivo('.systel/config.txt')
        config.close()
    except:
        #os.mkdir(pasta)
        config = lerArquivo('.systel/config.txt', 'w')
        config.close()
def dadosArquivo(f):
    arquivo =  open(f, 'r', encoding='utf-8')
    nome, extensão = f.split('.')
    copia = f
    arquivo.close()
    return f   
def copiarArquivo(f):
    arquivo =  lerArquivo(f, 'r')
    nome, extensão = f.split('.')
    copia = nome + '(2).txt'
    arquivo_copia = lerArquivo(copia, 'w')
    for linha in arquivo:
        arquivo_copia.write(linha)
    arquivo_copia.close()
    arquivo.close()
    os.remove(f)
    return copia  
class Arquivo(object):
    def __init__(self, arquivo):
        self.arquivo_aberto = dadosArquivo(arquivo)
    def getArquivo_aberto(self):
        return self.arquivo_aberto
def arquivo_existe(f):
    if(os.path.isfile(f)): 
        arquivo = lerArquivo(f, 'r')
        arquivo.close()
    else:
        arquivo = lerArquivo(f, 'w')
        arquivo.close()

def separar_dados_plu(l):
    linha = l
    secao = (linha[0:2])
    plu = (linha[5:11])
    nome = linha[20:35]
    preco = linha[11:17]
    venda = linha[4]
    validade = linha[17:20]
    return secao, plu, nome, preco, venda, validade


def criar_itens(f):
    txitens = f
    itens_71 = lerArquivo('itens.txt', 'w')
    itens6 = lerArquivo('itens6.txt', 'w')
    receita = lerArquivo('receita.txt', 'w')
    for linha in txitens:
        secao, plu, nome, preco, venda, validade = separar_dados_plu(linha)
        nome = linha[20:51]
        new_line = linha[:(len(linha)-1)]
        if len(new_line) < 72:
            new_line = new_line + ' '*(72 - len(new_line))+ '\n'
            itens_71.write(new_line)
        print(secao, plu, nome, preco, venda, validade)
        linhaMgv = secao+venda+plu+preco+validade+nome+(" "*20)+plu+"0000"+plu+'110000000000000000000000000000000000030000000000000000000000000000'
        print(len(linhaMgv)) 
        itens6.write(linhaMgv+'\n')
        #010000003001659000PIMENTAO AMARELO KG                               0000030000000001110000000000000000000000000000000000030000000000000000000000000000
    
    
    txitens.close()
    itens_71.close()
    #time.sleep(20)

def criar_csv(f):
    txitens = f
    itensCSV_P = open('CSV-SYSTEL-ponto.csv', 'w')
    itensCSV_V = open('CSV-SYSTEL-virgula.csv', 'w')
    for linha in txitens:
        secao, plu, nome, preco, venda, validade = separar_dados_plu(linha)
        secao = int(secao)
        plu = int(plu)
        preco = f'{(float(preco)/100):.2f}'
        vendaNum = int(venda)
        venda = ''
        if vendaNum == 0: venda = 'PESO     '
        elif vendaNum == 1: venda = 'UNIDAD   '
        itensCSV_P.write(f'SEÇAO {secao};{plu};{nome};{plu};{str(preco.replace(",","."))};{preco};{venda};{validade};"";0;0;"";"";"";N;0;0;0;"";0;0;0;0;0;0;0;0;0;0;G;"";"";""\n')
        itensCSV_V.write(f'SEÇAO {secao};{plu};{nome};{plu};{str(preco.replace(".",","))};{preco};{venda};{validade};"";0;0;"";"";"";N;0;0;0;"";0;0;0;0;0;0;0;0;0;0;G;"";"";""\n')
        
        #Seção 99;430;Farinha Cenoura;430;35,99;29;PESO     ;179;"";0;0;"";"";"";N;"";1;100;"";0;0;0;0;0;0;0;0;0;0;G;"";29/06/2023 17:24:04;""
    txitens.close()
    itensCSV_P.close()
    itensCSV_V.close()

class Txitens(Arquivo):
    def __init__(self):
        Arquivo.__init__(self, arquivo='txitens.txt')
    
    def modificar(self):
        itens_file_name = self.getArquivo_aberto() 
        nome_arquivo_mgv = itens_file_name
        txitens = lerArquivo(nome_arquivo_mgv, 'r') 
        criar_itens(txitens)
        txitens.close()
        copiarArquivo(nome_arquivo_mgv)
    pass

txitens = Txitens()
txitens.modificar()