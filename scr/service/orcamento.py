from flask import abort
from database import Database

#------------------------------------------------------------------------------------------------#
# Lista todos os orçamentos da base
#------------------------------------------------------------------------------------------------#
def listar():

    resp = {
        'orcamento' : [],
        'quantidadeRegistros': 0
    }
    
    sql = 'SELECT ' \
            'ID_ORCAM, ' \
            'ID_SIT_ORCAM, ' \
            'DES_ORCAM, ' \
            'DATE_FORMAT(DAT_INI_EXERC, "%Y-%m-%d") AS DAT_INI_EXERC, ' \
            'DATE_FORMAT(DAT_FIM_EXERC, "%Y-%m-%d") AS DAT_FIM_EXERC  ' \
            'FROM DBORCA.ORCAM ORDER BY 1'
    
    c = Database()
    s = c.executaSQLFetchall(sql)

    for row in s:
        resp['quantidadeRegistros'] += 1    
        resp['orcamento'].append({
            'idOrcam': row['ID_ORCAM'],
            'idSitOrcam': row['ID_SIT_ORCAM'],
            'desOrcam': row['DES_ORCAM'],
            'datIniExerc': row['DAT_INI_EXERC'],
            'datFimExerc': row['DAT_FIM_EXERC']
        })

    return resp

#------------------------------------------------------------------------------------------------#
# Consulta orçamento pelo id
#------------------------------------------------------------------------------------------------#
def consulta_id(idOrcam):

    sql = 'SELECT ' \
            'ID_ORCAM, ' \
            'ID_SIT_ORCAM, ' \
            'DES_ORCAM, ' \
            'DATE_FORMAT(DAT_INI_EXERC, "%Y-%m-%d") AS DAT_INI_EXERC, ' \
            'DATE_FORMAT(DAT_FIM_EXERC, "%Y-%m-%d") AS DAT_FIM_EXERC  ' \
            'FROM DBORCA.ORCAM ' \
            'WHERE ID_ORCAM = ' + str(idOrcam)
    
    c = Database()
    row = c.executaSQLFetchone(sql)
    
    if not row: abort(400,description="Registro Orçamento Não Encontrado")

    resp = {
        'orcamento': {
            'idOrcam': row['ID_ORCAM'],
            'idSitOrcam': row['ID_SIT_ORCAM'],
            'desOrcam': row['DES_ORCAM'],
            'datIniExerc': row['DAT_INI_EXERC'],
            'datFimExerc': row['DAT_FIM_EXERC']
        }
    }

    return resp


#------------------------------------------------------------------------------------------------#
# Incluir orçamento da base
#------------------------------------------------------------------------------------------------#
def incluir(req):
    r = req.get_json()

    c = Database()
    c.conecta()
    c.abreCursor()

    rMaxId = c.executaSQLFetchoneCursorAberto("SELECT COALESCE(MAX(A.ID_ORCAM),0)+1 AS ID_ORCAM FROM DBORCA.ORCAM A")
    r['idOrcam'] = rMaxId['ID_ORCAM']

    sql = 'INSERT INTO DBORCA.ORCAM (ID_ORCAM, ID_SIT_ORCAM, DES_ORCAM, DAT_INI_EXERC, DAT_FIm_EXERC) VALUES (' \
        ' ' + str(r['idOrcam'])        + ' ,' \
        '"' + str(r['idSitOrcam'])     + '",' \
        '"' + str(r['desOrcam'])       + '",' \
        '"' + str(r['datIniExerc'])    + '",' \
        '"' + str(r['datFimExerc'])    + '")'
    
    c.executaSQLInsertCursorAberto(sql)
    c.commit()
    c.desconecta()

    resp = {
        'mensagem': 'Orçamento incluído com sucesso',
        'orcamento': r
    }

    return resp

#------------------------------------------------------------------------------------------------#
# Excluir definitivamente orçamento da base
#------------------------------------------------------------------------------------------------#
def excluir(idOrcam):

    o = consulta_id(idOrcam)

    resp = {
        'mensagem': 'Orçamento Excluído Com Sucesso',
        'orcamento': o
    }

    c = Database()
    script = []
    
    sql = "DELETE FROM DBORCA.ORCAM WHERE ID_ORCAM = " + str(idOrcam)
    script.append(sql)

    if c.executaSQLFetchone("SELECT COUNT(*) FROM DBORCA.LIN_ORCAM WHERE ID_ORCAM = " + str(idOrcam))['COUNT(*)'] > 0:
        sql = "DELETE FROM DBORCA.LIN_ORCAM WHERE ID_ORCAM = " + str(idOrcam)
        script.append(sql)

    if c.executaSQLFetchone("SELECT COUNT(*) FROM DBORCA.LIN_ORCAM_DADO_ADCIO WHERE ID_ORCAM = " + str(idOrcam))['COUNT(*)'] > 0:
        sql = "DELETE FROM DBORCA.LIN_ORCAM_DADO_ADCIO WHERE ID_ORCAM = " + str(idOrcam)
        script.append(sql)

    if c.executaSQLFetchone("SELECT COUNT(*) FROM DBORCA.LIBRC_LIN_ORCAM WHERE ID_ORCAM = " + str(idOrcam))['COUNT(*)'] > 0:
        sql = "DELETE FROM DBORCA.LIBRC_LIN_ORCAM WHERE ID_ORCAM = " + str(idOrcam)
        script.append(sql)

    if c.executaSQLFetchone("SELECT COUNT(*) FROM DBORCA.LIBRC_LIN_ORCAM_RECTA WHERE ID_ORCAM = " + str(idOrcam))['COUNT(*)'] > 0:
        sql = "DELETE FROM DBORCA.LIBRC_LIN_ORCAM_RECTA WHERE ID_ORCAM = " + str(idOrcam)
        script.append(sql)

    if c.executaSQLFetchone("SELECT COUNT(*) FROM DBORCA.TPO_DADO_ADCIO WHERE ID_ORCAM = " + str(idOrcam))['COUNT(*)'] > 0:
        sql = "DELETE FROM DBORCA.TPO_DADO_ADCIO WHERE ID_ORCAM = " + str(idOrcam)
        script.append(sql)

    if c.executaSQLFetchone("SELECT COUNT(*) FROM DBORCA.DSTNO_RECTA WHERE ID_ORCAM = " + str(idOrcam))['COUNT(*)'] > 0:
        sql = "DELETE FROM DBORCA.DSTNO_RECTA WHERE ID_ORCAM = " + str(idOrcam)
        script.append(sql)

    if c.executaSQLFetchone("SELECT COUNT(*) FROM DBORCA.PDRAO_PER_DSTNO_RECTA WHERE ID_ORCAM = " + str(idOrcam))['COUNT(*)'] > 0:
        sql = "DELETE FROM DBORCA.PDRAO_PER_DSTNO_RECTA WHERE ID_ORCAM = " + str(idOrcam)
        script.append(sql)

    c.executaListaSQLScript(script)

    return resp