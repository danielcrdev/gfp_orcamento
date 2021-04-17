from flask import abort
from database import Database
from service import orcamento


#------------------------------------------------------------------------------------------------#
# Cria um modelo de Orçamento
#------------------------------------------------------------------------------------------------#
def criar(codModel, req):

    # Cria Orçamento
    resp = orcamento.incluir(req)
    idOrcam = resp['orcamento']['idOrcam']

    # Configura o modelo do Orçamento
    if   codModel == '50-30-20': criar_modelo_50_30_20(idOrcam)
    elif codModel == 'X': criar_modelo_x(idOrcam)
    else: abort(400,description="Modelo de Orcamento Não Existente")

    return resp


#------------------------------------------------------------------------------------------------#
# Cria Modelo Padrão Orçamento 50-30-20
#------------------------------------------------------------------------------------------------#
def criar_modelo_50_30_20(idOrcam):
    
    script = []

    # Linha Orçamento         
    sql = "INSERT INTO DBORCA.LIN_ORCAM (ID_ORCAM, ID_LIN_ORCAM, ID_LIN_ORCAM_PAI, ID_NVEL_LIN_ORCAM, COD_NATUZ_LIN_ORCAM, COD_LIN_ORCAM, DES_LIN_ORCAM) VALUES " \
	"(" + str(idOrcam) + ", 1, 0, 'LD', 'R', 'R1000', 'Receita')," \
    "(" + str(idOrcam) + ", 2, 0, 'LD', 'D', 'D1000', 'Essencial')," \
    "(" + str(idOrcam) + ", 3, 0, 'LD', 'D', 'D2000', 'Lazer')," \
    "(" + str(idOrcam) + ", 4, 0, 'LD', 'D', 'D3000', 'Investimento')"
    script.append(sql)

    # Destino Receira
    sql = "INSERT INTO DBORCA.DSTNO_RECTA (ID_ORCAM, ID_DSTNO_RECTA, DES_DSTNO_RECTA) VALUES " \
	"(" + str(idOrcam) + ", 0, 'Nenhum Destino')," \
	"(" + str(idOrcam) + ", 1, 'Padrão 50-30-20 Orçamento')," \
    "(" + str(idOrcam) + ", 2, 'Essencial')," \
    "(" + str(idOrcam) + ", 3, 'Lazer')," \
    "(" + str(idOrcam) + ", 4, 'Investimento')"
    script.append(sql)

    # Parão de Percentual de Destino Receita        
    sql = "INSERT INTO DBORCA.PDRAO_PER_DSTNO_RECTA (ID_ORCAM, ID_LIN_ORCAM, ID_DSTNO_RECTA, VAL_PERC) VALUES " \
	"(" + str(idOrcam) + ", 2, 1,  50.00)," \
	"(" + str(idOrcam) + ", 3, 1,  30.00)," \
	"(" + str(idOrcam) + ", 4, 1,  20.00)," \
    "(" + str(idOrcam) + ", 2, 2, 100.00)," \
    "(" + str(idOrcam) + ", 3, 3, 100.00)," \
    "(" + str(idOrcam) + ", 4, 4, 100.00)"
    script.append(sql)

    # Tipo de Dados Adicional
    #sql = "INSERT INTO DBORCA.TPO_DADO_ADCIO (ID_ORCAM, ID_TPO_DADO_ADCIO, DES_TPO_DADO_ADCIO, ID_FORMT_DADO) VALUES " \
	#"(" + str(idOrcam) + ", 1, 'Nota Fiscal', 1)," \
	#"(" + str(idOrcam) + ", 2, 'Comprovante', 1)"
    #script.append(sql)

    c = Database()
    c.executaListaSQLScript(script)

    return None


#------------------------------------------------------------------------------------------------#
# Cria um modelo x
#------------------------------------------------------------------------------------------------#
def criar_modelo_x(idOrcam):

    # Criar configuração do Orçamento
    script = []

    return None