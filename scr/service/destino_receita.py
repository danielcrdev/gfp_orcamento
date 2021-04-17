from flask import abort
from database import Database
from service import orcamento

#------------------------------------------------------------------------------------------------#
# Lista todos os destinos de receita
#------------------------------------------------------------------------------------------------#
def listar(idOrcam):

    resp = {
        'quantidadeRegistros': 0,
        'destinoreceita' : []
    }

    resp.update(orcamento.consulta_id(idOrcam))
    
    sql =   'SELECT ' \
            '   ID_ORCAM, ' \
            '   ID_DSTNO_RECTA, ' \
            '   DES_DSTNO_RECTA ' \
            'FROM DBORCA.DSTNO_RECTA ' \
            'WHERE ID_ORCAM = ' + str(idOrcam)
    
    c = Database()
    s = c.executaSQLFetchall(sql)

    for row in s:
        resp['quantidadeRegistros'] += 1    
        resp['destinoreceita'].append({
            'idOrcam': row['ID_ORCAM'],
            'idDstnoRecta': row['ID_DSTNO_RECTA'],
            'desDstnoRecta': row['DES_DSTNO_RECTA']
        })

    return resp

#------------------------------------------------------------------------------------------------#
# Consulta destino receita pelo id
#------------------------------------------------------------------------------------------------#
def consulta_id(idOrcam, idDstnoRecta):

    sql =   'SELECT ' \
            '   ID_ORCAM, ' \
            '   ID_DSTNO_RECTA, ' \
            '   DES_DSTNO_RECTA ' \
            'FROM DBORCA.DSTNO_RECTA ' \
            'WHERE ID_ORCAM = ' + str(idOrcam) + ' ' \
            'AND   ID_DSTNO_RECTA = ' + str(idDstnoRecta)
    
    c = Database()
    row = c.executaSQLFetchone(sql)
    
    if not row: abort(400,description="Registro Destino Receita Não Encontrado")

    resp = {
        'destinoreceita': {
            'idOrcam': row['ID_ORCAM'],
            'idDstnoRecta': row['ID_DSTNO_RECTA'],
            'desDstnoRecta': row['DES_DSTNO_RECTA']
        }
    }

    return resp

#------------------------------------------------------------------------------------------------#
# Incluir destino receita
#------------------------------------------------------------------------------------------------#
def incluir(idOrcam, req):
    
    r = req.get_json()
    r['idOrcam'] = idOrcam

    c = Database()
    c.conecta()
    c.abreCursor()

    sql = 'SELECT COALESCE(MAX(A.ID_DSTNO_RECTA),0)+1 AS ID_DSTNO_RECTA ' \
        'FROM DBORCA.DSTNO_RECTA A ' \
        'WHERE A.ID_ORCAM = ' + str(idOrcam)

    r['idDstnoRecta'] = c.executaSQLFetchoneCursorAberto(sql)['ID_DSTNO_RECTA']

    if r['idDstnoRecta'] == 1:
        # Se for primeiro registro, inclui registro 0 = Nenhum Destino
        sql = 'INSERT INTO DBORCA.DSTNO_RECTA (ID_ORCAM, ID_DSTNO_RECTA, DES_DSTNO_RECTA) VALUES (' \
        ' ' + str(r['idOrcam']) + ', 0, "Nenhum Destino")'
        c.executaSQLInsertCursorAberto(sql)

    sql = 'INSERT INTO DBORCA.DSTNO_RECTA (ID_ORCAM, ID_DSTNO_RECTA, DES_DSTNO_RECTA) VALUES (' \
        ' ' + str(r['idOrcam'])          + ' ,' \
        ' ' + str(r['idDstnoRecta'])     + ' ,' \
        '"' + str(r['desDstnoRecta'])    + '")' 
    
    c.executaSQLInsertCursorAberto(sql)
    c.commit()
    c.desconecta()

    resp = {
        'mensagem': 'Registro Destino Receita incluído com sucesso',
        'destinoreceita': r,
    }

    return resp