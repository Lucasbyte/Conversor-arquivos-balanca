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







# itensMGV
def criar_itens7(arquivo):
    mgv7 = lerArquivo(pasta+'itens7.txt', 'w')
    codigos_nutri = []
    for linha in arquivo:
        codPlu = linha[78:84]
        codigos_nutri.append(codPlu)
        caractereMeiaOito = linha[68]
        textoModificado = linha[0:43] + (' ')*25 + caractereMeiaOito + linha[69:150] +  "000000|01|                                                                      0000000000000000000000000||0||0000000000000000000000"                                                   
        try: 
            caractereMeiaOito = str(int(linha[68]))
            mgv7.write(textoModificado+"\n")
        except: 
            caractereMeiaOito = linha[69]
            textoModificado = linha[0:43] + (' ')*25+ caractereMeiaOito + linha[70:151] +  "000000|01|                                                                      0000000000000000000000000||0||0000000000000000000000"                                                   
        #+  "000000|01|                                                                      0000000000000000000000000||0||0000000000000000000000"                                                                      0000000000000000000000000||0||0000000000000000000000"

        
        #print(linha)
        #print(linha[0:43], linha[70:150],linha[68], caractereMeiaNove)
            mgv7.write(textoModificado+"\n")
        print(codPlu)
        #modificar_extras_mgv(codPlu_array= codigos_nutri)
    mgv7.close()
    return codigos_nutri

def criar_itens6(arquivo):
    mgv6 = lerArquivo(pasta+'itens6.txt', 'w')
    codigos_nutri = []
    for linha in arquivo:
        codPlu = linha[78:84]
        codigos_nutri.append(codPlu)
        caractereMeiaOito = linha[68]
        textoModificado = linha[0:43] + (' ')*25 + caractereMeiaOito + linha[69:150]
        try: 
            caractereMeiaOito = str(int(linha[68]))
            mgv6.write(textoModificado+"\n")
        except: 
            caractereMeiaOito = linha[69]
            textoModificado = linha[0:43] + (' ')*25 + caractereMeiaOito + linha[70:151] 
        #+  "000000|01|                                                                      0000000000000000000000000||0||0000000000000000000000"                                                                      0000000000000000000000000||0||0000000000000000000000"

            #print(codPlu)
        #print(linha)
        #print(linha[0:43], linha[70:150],linha[68], caractereMeiaNove)
            mgv6.write(textoModificado+"\n")
        #modificar_extras_mgv(codPlu_array= codigos_nutri)
    mgv6.close()
    return codigos_nutri


def modificar_extras_mgv(txinfo='txinfo.txt', infnutri='infnutri.txt', codPlu_array=[]):
    arquivo_existe(txinfo)
    arquivoTxinfo = open(txinfo, 'r', encoding='latin-1')
    receita = open(pasta+'receitasSystel.txt', 'w', encoding='latin-1')    
    for linha in arquivoTxinfo:
            espaco = "                                                                                                    "
            cod = linha[0:6]
            receita_sem_espaco = (linha[106:]).replace("   ","")
            texto = cod + espaco + receita_sem_espaco
            tamanho = len(texto)
            texto = texto + (" "*(2230-tamanho)) +'\n'
            receita.write(texto)
    arquivoTxinfo.close()
    receita.close()


    arquivo_existe(infnutri)
    arquivoInfonutri = lerArquivo(infnutri, 'r')
    nutri = lerArquivo(pasta+'nutriSystel.txt', 'w')
    for linha in arquivoInfonutri:
            codNutri = linha[1:7]
            if len(linha) <= 50:
                print(linha[7:11])
                linha = linha.replace('\n', '') + '|' + ('0'*3) + linha[7:11] + '0' + linha[12:26] + '0'*6 + linha[26:50].replace('\n','') + '0'*9 + '\n'
            if codNutri in  codPlu_array:
                nutri.write(linha)
    arquivoInfonutri.close()
    nutri.close()



class MGV(Arquivo):
    
    def __init__(self):
        Arquivo.__init__(self, arquivo='itensmgv.txt') 

    

    def modificar(self):
        itens_file_name = self.getArquivo_aberto() 
        nome_arquivo_mgv = itens_file_name
        mgv = lerArquivo(nome_arquivo_mgv, 'r') 
        cod_nutri = criar_itens6(arquivo=mgv)
        mgv.close()
        mgv = lerArquivo(nome_arquivo_mgv, 'r') 
        criar_itens7(arquivo=mgv)
        modificar_extras_mgv(codPlu_array=cod_nutri)
        mgv.close()
        copiarArquivo(nome_arquivo_mgv)



while(True):
    if(os.path.isfile('itensMGV.TXT')):
        itensMGV = MGV()
        itensMGV.modificar()
    else: time.sleep(8)