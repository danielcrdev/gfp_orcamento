from flask import abort
from database import Database

#------------------------------------------------------------------------------------------------#
# Lista todos as situações orçamento
#------------------------------------------------------------------------------------------------#
def listar():

    resp = {
        'situacaoorcamento' : [],
        'quantidadeRegistros': 0
    }
    
    sql =   'SELECT                             ' \
            '   ID_SIT_ORCAM,                   ' \
            '   DES_SIT_ORCAM                   ' \
            'FROM DBORCA.SIT_ORCAM ORDER BY 1    '
    
    c = Database()
    s = c.executaSQLFetchall(sql)

    for row in s:
        resp['quantidadeRegistros'] += 1    
        resp['situacaoorcamento'].append({
            'idSitOrcam': row['ID_SIT_ORCAM'],
            'desSitOrcam': row['DES_SIT_ORCAM']
        })

    return resp

#------------------------------------------------------------------------------------------------#
# Consulta situação orçamento pelo id
#------------------------------------------------------------------------------------------------#
def consulta_id(idSitOrcam):

    sql =   'SELECT                             ' \
            '   ID_SIT_ORCAM,                   ' \
            '   DES_SIT_ORCAM                   ' \
            'FROM DBORCA.SIT_ORCAM               ' \
            'WHERE ID_SIT_ORCAM = "' + str(idSitOrcam) + '"'
    
    c = Database()
    row = c.executaSQLFetchone(sql)
    
    if not row: abort(400,description="Registro Situação Orçamento Não Encontrado")

    resp = {
        'situacaoorcamento': {
            'idSitOrcam': row['ID_SIT_ORCAM'],
            'desSitOrcam': row['DES_SIT_ORCAM']
        }
    }

    return resp