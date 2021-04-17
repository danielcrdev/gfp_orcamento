from flask import abort
from database import Database

#------------------------------------------------------------------------------------------------#
# Lista todos as liberações de valores de uma linha de orçamento de receita
#------------------------------------------------------------------------------------------------#
def listar(idOrcam):

    resp = {
        'liberacaolinhaorcamentoreceita' : [],
        'quantidadeRegistros': 0
    }
    
    sql =   'SELECT                     ' \
            '   ID_ORCAM,               ' \
            '   ID_LIN_ORCAM,           ' \
            '   DAT_LIN_ORCAM,          ' \
            '   ID_DSTNO_RECTA          ' \
            'FROM LIBRC_LIN_ORCAM_RECTA ' \
            'WHERE ID_ORCAM = ' + str(idOrcam)

    c = Database()
    s = c.executaSQLFetchall(sql)

    for row in s:
        resp['quantidadeRegistros'] += 1    
        resp['liberacaolinhaorcamentoreceita'].append({
            'idOrcam': row['ID_ORCAM'],
            'idLinOrcam': row['ID_LIN_ORCAM'],
            'datLinOrcam': row['DAT_LIN_ORCAM'],
            'idDstnoRecta': row['ID_DSTNO_RECTA']
        })

    return resp

#------------------------------------------------------------------------------------------------#
# Consulta liberações de valores de uma linha de orçamento receita pelo id
#------------------------------------------------------------------------------------------------#
def consulta_id(idOrcam, idLinOrcam, datLinOrcam):

    sql =   'SELECT                     ' \
            '   ID_ORCAM,               ' \
            '   ID_LIN_ORCAM,           ' \
            '   DAT_LIN_ORCAM,          ' \
            '   ID_DSTNO_RECTA          ' \
            'FROM LIBRC_LIN_ORCAM_RECTA ' \
            'WHERE ID_ORCAM = ' + str(idOrcam) + ' ' \
            'AND ID_LIN_ORCAM = ' + str(idLinOrcam) + ' ' \
            'AND DAT_LIN_ORCAM = ' + str(datLinOrcam) + ' ' \

    c = Database()
    row = c.executaSQLFetchone(sql)
    
    if not row: abort(400,description="Registro Liberação Linha Orçamento Receita Não Encontrado")

    resp = {
        'liberacaolinhaorcamentoreceita': {
            'idOrcam': row['ID_ORCAM'],
            'idLinOrcam': row['ID_LIN_ORCAM'],
            'datLinOrcam': row['DAT_LIN_ORCAM'],
            'idDstnoRecta': row['ID_DSTNO_RECTA']
        }
    }

    return resp