from flask import abort
from database import Database

#------------------------------------------------------------------------------------------------#
# Lista todos os formatos de dados adicionais
#------------------------------------------------------------------------------------------------#
def listar():

    resp = {
        'formatodado' : [],
        'quantidadeRegistros': 0
    }
    
    sql =   'SELECT                            ' \
            '   ID_FORMT_DADO,                 ' \
            '   DES_FORMT_DADO,                ' \
            '   EXEMP_FORMT                    ' \
            'FROM DBORCA.FORMT_DADO ORDER BY 1  '
    
    c = Database()
    s = c.executaSQLFetchall(sql)

    for row in s:
        resp['quantidadeRegistros'] += 1    
        resp['formatodado'].append({
            'idFormtDado': row['ID_FORMT_DADO'],
            'desFormtDado': row['DES_FORMT_DADO'],
            'exempFormt': row['EXEMP_FORMT']
        })

    return resp

#------------------------------------------------------------------------------------------------#
# Consulta formato de dados adicionais pelo id
#------------------------------------------------------------------------------------------------#
def consulta_id(idFormtDado):

    sql =   'SELECT                            ' \
            '   ID_FORMT_DADO,                 ' \
            '   DES_FORMT_DADO,                ' \
            '   EXEMP_FORMT                    ' \
            'FROM DBORCA.FORMT_DADO             ' \
            'WHERE ID_FORMT_DADO = ' + str(idFormtDado)
    
    c = Database()
    row = c.executaSQLFetchone(sql)
    
    if not row: abort(400,description="Registro Formato de Dado Adicional Não Encontrado")

    resp = {
        'formatodado': {
            'idFormtDado': row['ID_FORMT_DADO'],
            'desFormtDado': row['DES_FORMT_DADO'],
            'exempFormt': row['EXEMP_FORMT']
        }
    }

    return resp