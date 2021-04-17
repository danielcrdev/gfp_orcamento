from flask import abort
from database import Database

#------------------------------------------------------------------------------------------------#
# Lista todos as níveis de linha de orçamento
#------------------------------------------------------------------------------------------------#
def listar():

    resp = {
        'nivellinhaorcamento' : [],
        'quantidadeRegistros': 0
    }
    
    sql =   'SELECT                               ' \
            '   ID_NVEL_LIN_ORCAM,                ' \
            '   DES_NVEL_LIN_ORCAM                ' \
            'FROM DBORCA.NVEL_LIN_ORCAM ORDER BY 1 '
    
    c = Database()
    s = c.executaSQLFetchall(sql)

    for row in s:
        r = {}
        resp['quantidadeRegistros'] += 1    
        resp['nivellinhaorcamento'].append({
            'idNvelLinOrcam': row['ID_NVEL_LIN_ORCAM'],
            'desNvelLinOrcam': row['DES_NVEL_LIN_ORCAM']
        })

    return resp

#------------------------------------------------------------------------------------------------#
# Consulta nível de linha de orçamento pelo id
#------------------------------------------------------------------------------------------------#
def consulta_id(idNvelLinOrcam):

    sql =   'SELECT                               ' \
            '   ID_NVEL_LIN_ORCAM,                ' \
            '   DES_NVEL_LIN_ORCAM                ' \
            'FROM DBORCA.NVEL_LIN_ORCAM            ' \
            'WHERE ID_NVEL_LIN_ORCAM = "' + str(idNvelLinOrcam) + '"'
    
    c = Database()
    row = c.executaSQLFetchone(sql)
    
    if not row: abort(400,description="Registro Nível Linha Orçamento Não Encontrado")

    resp = {
        'nivellinhaorcamento': {
            'idNvelLinOrcam': row['ID_NVEL_LIN_ORCAM'],
            'desNvelLinOrcam': row['DES_NVEL_LIN_ORCAM']
        }
    }

    return resp