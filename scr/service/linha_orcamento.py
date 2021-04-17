from database import Database
from service import orcamento, nivel_linha_orcamento, natureza_linha_orcamento
from flask import abort

#------------------------------------------------------------------------------------------------#
# Lista todos as linhas de orçamento de um orçamento
#------------------------------------------------------------------------------------------------#
def listar(idOrcam):
    
    resp = {
        'quantidadeRegistros': 0,
        'linhaorcamento' : []
    }

    resp.update((orcamento.consulta_id(idOrcam)))

    sql =   'SELECT                     ' \
            '   ID_ORCAM,               ' \
            '   ID_LIN_ORCAM,           ' \
            '   ID_LIN_ORCAM_PAI,       ' \
            '   ID_NVEL_LIN_ORCAM,      ' \
            '   COD_NATUZ_LIN_ORCAM,    ' \
            '   COD_LIN_ORCAM,          ' \
            '   DES_LIN_ORCAM           ' \
            'FROM DBORCA.LIN_ORCAM       ' \
            'WHERE ID_ORCAM = ' + str(idOrcam)

    c = Database()
    s = c.executaSQLFetchall(sql) 

    for row in s:
        resp['quantidadeRegistros'] += 1
        resp['linhaorcamento'].append({
            'idOrcam': row['ID_ORCAM'],
            'idLinOrcam': row['ID_LIN_ORCAM'],
            'idLinOrcamPai': row['ID_LIN_ORCAM_PAI'],
            'idNvelLinOrcam': row['ID_NVEL_LIN_ORCAM'],
            'codNatuzLinOrcam': row['COD_NATUZ_LIN_ORCAM'],
            'codLinOrcam': row['COD_LIN_ORCAM'],
            'desLinOrcam': row['DES_LIN_ORCAM']
        })
    
    return resp


#------------------------------------------------------------------------------------------------#
# Consulta linha orçamento pelo id e orçamento
#------------------------------------------------------------------------------------------------#
def consulta_id(idOrcam, idLinOrcam):

    sql =   'SELECT                     ' \
            '   ID_ORCAM,               ' \
            '   ID_LIN_ORCAM,           ' \
            '   ID_LIN_ORCAM_PAI,       ' \
            '   ID_NVEL_LIN_ORCAM,      ' \
            '   COD_NATUZ_LIN_ORCAM,    ' \
            '   COD_LIN_ORCAM,          ' \
            '   DES_LIN_ORCAM           ' \
            '   FROM DBORCA.LIN_ORCAM    ' \
            'WHERE  ID_ORCAM        = ' + str(idOrcam) + ' ' \
            'AND    ID_LIN_ORCAM    = ' + str(idLinOrcam)
    
    c = Database()
    row = c.executaSQLFetchone(sql)

    if not row: abort(400,description="Registro Linha Orçamento Não Encontrado")

    resp = {
        'linhaorcamento': {
            'idOrcam': row['ID_ORCAM'],
            'idLinOrcam': row['ID_LIN_ORCAM'],
            'idLinOrcamPai': row['ID_LIN_ORCAM_PAI'],
            'idNvelLinOrcam': row['ID_NVEL_LIN_ORCAM'],
            'codNatuzLinOrcam': row['COD_NATUZ_LIN_ORCAM'],                
            'codLinOrcam': row['COD_LIN_ORCAM'],
            'desLinOrcam': row['DES_LIN_ORCAM']
        }
    }

    resp.update((orcamento.consulta_id(idOrcam)))

    return resp


#------------------------------------------------------------------------------------------------#
# Incluir linha orçamento da base
#------------------------------------------------------------------------------------------------#
def incluir(idOrcam, req):

    r = req.get_json()
    r['idOrcam']    = idOrcam

    resp = {
        'mensagem': 'Linha do orçamento incluído com sucesso',
        'linhaorcamento': r
    }

    resp.update(orcamento.consulta_id(r['idOrcam']))
    resp.update(nivel_linha_orcamento.consulta_id(r['idNvelLinOrcam']))
    resp.update(natureza_linha_orcamento.consulta_id(r['codNatuzLinOrcam']))
    if r['idLinOrcamPai'] > 0 : resp.update( { 'linhaorcamentopai': consulta_id(r['idOrcam'],r['idLinOrcamPai']) } )

    if resp['linhaorcamentopai']['linhaorcamento']['idNvelLinOrcam'] == 'LD': 
        abort(400,description="Linha Orçamento Pai não pode ser uma Linha Detalhe!")

    c = Database()
    c.conecta()
    c.abreCursor()

    sql = 'SELECT COALESCE(MAX(A.ID_LIN_ORCAM),0)+1 AS ID_LIN_ORCAM ' \
        'FROM DBORCA.LIN_ORCAM A ' \
        'WHERE A.ID_ORCAM = ' + str(idOrcam)

    r['idLinOrcam'] = c.executaSQLFetchoneCursorAberto(sql)['ID_LIN_ORCAM']

    sql = 'INSERT INTO DBORCA.LIN_ORCAM (ID_ORCAM, ID_LIN_ORCAM, ID_LIN_ORCAM_PAI, ID_NVEL_LIN_ORCAM, COD_NATUZ_LIN_ORCAM, COD_LIN_ORCAM, DES_LIN_ORCAM) VALUES (' \
        ' ' + str(r['idOrcam'])             + ' ,' \
        ' ' + str(r['idLinOrcam'])          + ' ,' \
        ' ' + str(r['idLinOrcamPai'])       + ' ,' \
        '"' + str(r['idNvelLinOrcam'])      + '",' \
        '"' + str(r['codNatuzLinOrcam'])    + '",' \
        '"' + str(r['codLinOrcam'])         + '",' \
        '"' + str(r['desLinOrcam'])         + '")' 
    
    c.executaSQLInsertCursorAberto(sql)
    c.commit()
    c.desconecta()

    return resp
