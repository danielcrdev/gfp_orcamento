from flask import abort
from database import Database

#------------------------------------------------------------------------------------------------#
# Lista todos as natureza linha orçamento
#------------------------------------------------------------------------------------------------#
def listar():

    resp = {
        'naturezalinhaorcamento' : [],
        'quantidadeRegistros': 0
    }
    
    sql =   'SELECT                             ' \
            '   COD_NATUZ_LIN_ORCAM,            ' \
            '   DES_NATUZ_LIN_ORCAM             ' \
            'FROM DBORCA.NATUZ_LIN_ORCAM         '
    
    c = Database()
    s = c.executaSQLFetchall(sql)

    for row in s:
        resp['quantidadeRegistros'] += 1    
        resp['naturezalinhaorcamento'].append({
            'codNatuzLinOrcam': row['COD_NATUZ_LIN_ORCAM'],
            'desNatuzLinOrcam': row['DES_NATUZ_LIN_ORCAM']
        })

    return resp

#------------------------------------------------------------------------------------------------#
# Consulta Natureza Linha Orçamento pelo id
#------------------------------------------------------------------------------------------------#
def consulta_id(codNatuzLinOrcam):

    sql =   'SELECT                             ' \
            '   COD_NATUZ_LIN_ORCAM,            ' \
            '   DES_NATUZ_LIN_ORCAM             ' \
            'FROM DBORCA.NATUZ_LIN_ORCAM               ' \
            'WHERE COD_NATUZ_LIN_ORCAM = "' + str(codNatuzLinOrcam) + '"'
    
    c = Database()
    row = c.executaSQLFetchone(sql)
    
    if not row: abort(400,description="Registro Natureza Linha Orçamento Não Encontrado")

    resp = {
        'naturezalinhaorcamento': {
            'codNatuzLinOrcam': row['COD_NATUZ_LIN_ORCAM'],
            'desNatuzLinOrcam': row['DES_NATUZ_LIN_ORCAM']
        }
    }

    return resp