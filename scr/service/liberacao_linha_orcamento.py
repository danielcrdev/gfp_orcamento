from database import Database
from service import orcamento, linha_orcamento, destino_receita
from flask import abort

#------------------------------------------------------------------------------------------------#
# Lista todos as liberações de valores de uma linha de orçamento
#------------------------------------------------------------------------------------------------#
def listar(idOrcam, idLinOrcam):
    
    resp = {
        'quantidadeRegistros': 0,
        'liberacaolinhaorcamento' : []
    }

    resp.update(linha_orcamento.consulta_id(idOrcam, idLinOrcam))

    sql =   'SELECT                                                          ' \
            '   ID_ORCAM,                                                    ' \
            '   ID_LIN_ORCAM,                                                ' \
            '   DATE_FORMAT(DAT_LIN_ORCAM, "%Y-%m-%d") AS DAT_LIN_ORCAM,     ' \
            '   VAL_LIN_ORCAM,                                               ' \
            '   DES_COMEN                                                    ' \
            'FROM DBORCA.LIBRC_LIN_ORCAM                                      ' \
            'WHERE  ID_ORCAM        = ' + str(idOrcam)     + ' ' \
            'AND    ID_LIN_ORCAM    = ' + str(idLinOrcam)

    c = Database()
    s = c.executaSQLFetchall(sql) 

    for row in s:
        resp['quantidadeRegistros'] += 1
        resp['liberacaolinhaorcamento'].append({
            'idOrcam': row['ID_ORCAM'],
            'idLinOrcam': row['ID_LIN_ORCAM'],
            'datLinOrcam': row['DAT_LIN_ORCAM'],
            'valLinOrcam': str(row['VAL_LIN_ORCAM']),
            'desComen': row['DES_COMEN']
        })
    
    return resp


#------------------------------------------------------------------------------------------------#
# Consulta liberação de valores de linha orçamento pela chava (data e id)
#------------------------------------------------------------------------------------------------#
def consulta_id(idOrcam, idLinOrcam, datLinOrcam):

    sql =   'SELECT                                                          ' \
            '   ID_ORCAM,                                                    ' \
            '   ID_LIN_ORCAM,                                                ' \
            '   DATE_FORMAT(DAT_LIN_ORCAM, "%Y-%m-%d") AS DAT_LIN_ORCAM,     ' \
            '   VAL_LIN_ORCAM,                                               ' \
            '   DES_COMEN                                                    ' \
            '   FROM DBORCA.LIBRC_LIN_ORCAM  ' \
            'WHERE ID_ORCAM         =  ' + str(idOrcam)     + ' ' \
            'AND   ID_LIN_ORCAM     =  ' + str(idLinOrcam)  + ' ' \
            'AND   DAT_LIN_ORCAM    = "' + str(datLinOrcam) + '"'
    
    c = Database()
    row = c.executaSQLFetchone(sql)

    if not row: abort(400,description="Registro Liberação Linha Orçamento Não Encontrado")
    
    resp = {
        'liberacaolinhaorcamento': {
            'idOrcam': row['ID_ORCAM'],
            'idLinOrcam': row['ID_LIN_ORCAM'],
            'datLinOrcam': row['DAT_LIN_ORCAM'],
            'valLinOrcam': str(row['VAL_LIN_ORCAM']),
            'desComen': row['DES_COMEN']
        }
    }

    resp.update(linha_orcamento.consulta_id(idOrcam, idLinOrcam))

    return resp


#------------------------------------------------------------------------------------------------#
# Incluir linha orçamento da base
# Campon datLinOrcam no formato "AAAA-MM-DD", exemplo: 2021-01-01
#------------------------------------------------------------------------------------------------#
def incluir(idOrcam, idLinOrcam, req):
    
    r = req.get_json()
    r['idOrcam'] = idOrcam
    r['idLinOrcam'] = idLinOrcam

    resp = {
        'mensagem': 'Liberação de valor de Linha do orçamento incluído com sucesso',
        'liberacaolinhaorcamento': r,
    }

    resp.update(linha_orcamento.consulta_id(idOrcam, idLinOrcam))

    c = Database()
    c.conecta()
    c.abreCursor()

    # Insere na base
    sql = 'INSERT INTO DBORCA.LIBRC_LIN_ORCAM (ID_ORCAM, ID_LIN_ORCAM, DAT_LIN_ORCAM, VAL_LIN_ORCAM, DES_COMEN) VALUES (' \
        ' ' + str(r['idOrcam'])       + ' ,' \
        ' ' + str(r['idLinOrcam'])    + ' ,' \
        '"' + str(r['datLinOrcam'])   + '",' \
        ' ' + str(r['valLinOrcam'])   + ' ,' \
        '"' + str(r['desComen'])      + '")' 
    
    c.executaSQLInsertCursorAberto(sql)

    # Quando a linha de orçamento é de receita o sistema deve informar qual destido de orçamento desta receita
    if resp['linhaorcamento']['codNatuzLinOrcam'] == 'R':

        resp.update(destino_receita.consulta_id(r['idOrcam'], r['idDstnoRecta']))
        
        sql = 'INSERT INTO DBORCA.LIBRC_LIN_ORCAM_RECTA (ID_ORCAM, ID_LIN_ORCAM, DAT_LIN_ORCAM, ID_DSTNO_RECTA) VALUES (' \
            ' ' + str(r['idOrcam'])       + ' ,' \
            ' ' + str(r['idLinOrcam'])    + ' ,' \
            '"' + str(r['datLinOrcam'])   + '",' \
            ' ' + str(r['idDstnoRecta'])  + ' )'
        
        c.executaSQLInsertCursorAberto(sql)

    c.commit()
    c.desconecta()

    return resp