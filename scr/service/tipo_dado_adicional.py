from flask import abort
from database import Database
from service import orcamento, formato_dado_adicional

#------------------------------------------------------------------------------------------------#
# Lista todos os tipos de dado adicional
#------------------------------------------------------------------------------------------------#
def listar(idOrcam):

    resp = {
        'tipodadoadicional' : [],
        'quantidadeRegistros': 0
    }

    resp.update(orcamento.consulta_id(idOrcam))
    
    sql =   'SELECT ' \
            '   ID_ORCAM, ' \
            '   ID_TPO_DADO_ADCIO, ' \
            '   ID_FORMT_DADO, ' \
            '   DES_TPO_DADO_ADCIO ' \
            'FROM DBORCA.TPO_DADO_ADCIO ' \
            'WHERE ID_ORCAM = ' + str(idOrcam)
    
    c = Database()
    s = c.executaSQLFetchall(sql)

    for row in s:
        resp['quantidadeRegistros'] += 1    
        resp['tipodadoadicional'].append({
            'idOrcam': row['ID_ORCAM'],
            'idTpoDadoAdcio': row['ID_TPO_DADO_ADCIO'],
            'idFormtDado': row['ID_FORMT_DADO'],
            'desTpoDadoAdcio': row['DES_TPO_DADO_ADCIO']
        })

    return resp

#------------------------------------------------------------------------------------------------#
# Consulta tipo de dado adicional pelo id
#------------------------------------------------------------------------------------------------#
def consulta_id(idOrcam, idTpoDadoAdcio):

    sql =   'SELECT ' \
            '   ID_ORCAM, ' \
            '   ID_TPO_DADO_ADCIO, ' \
            '   ID_FORMT_DADO, ' \
            '   DES_TPO_DADO_ADCIO ' \
            'FROM DBORCA.TPO_DADO_ADCIO ' \
            'WHERE ID_ORCAM = ' + str(idOrcam) + ' ' \
            'AND   ID_TPO_DADO_ADCIO = ' + str(idTpoDadoAdcio)
    
    c = Database()
    row = c.executaSQLFetchone(sql)
    
    if not row: abort(400,description="Tipo de Dado Adicional Não Encontrado")

    resp = {
        'tipodadoadicional': {
            'idOrcam': row['ID_ORCAM'],
            'idTpoDadoAdcio': row['ID_TPO_DADO_ADCIO'],
            'idFormtDado': row['ID_FORMT_DADO'],
            'desTpoDadoAdcio': row['DES_TPO_DADO_ADCIO']
        }
    }

    resp['tipodadoadicional'].update(formato_dado_adicional.consulta_id(row['ID_FORMT_DADO']))

    return resp

#------------------------------------------------------------------------------------------------#
# Incluir tipo de dado adicional
#------------------------------------------------------------------------------------------------#
def incluir(idOrcam, req):
    
    r = req.get_json()
    r['idOrcam'] = idOrcam

    resp = {
        'mensagem': 'Registro Tipo Dado Adicional Incluído com sucesso',
        'tipodadoadicional': r,
    }

    resp.update(orcamento.consulta_id(r['idOrcam']))
    resp.update(formato_dado_adicional.consulta_id(r['idFormtDado']))

    c = Database()
    c.conecta()
    c.abreCursor()

    sql = 'SELECT COALESCE(MAX(A.ID_TPO_DADO_ADCIO),0)+1 AS ID_TPO_DADO_ADCIO ' \
        'FROM DBORCA.TPO_DADO_ADCIO A ' \
        'WHERE ID_ORCAM = ' + str(idOrcam)

    r['idTpoDadoAdcio'] = c.executaSQLFetchoneCursorAberto(sql)['ID_TPO_DADO_ADCIO']

    sql = 'INSERT INTO DBORCA.TPO_DADO_ADCIO (ID_ORCAM, ID_TPO_DADO_ADCIO, ID_FORMT_DADO, DES_TPO_DADO_ADCIO) VALUES (' \
        ' ' + str(r['idOrcam'])            + ' ,' \
        ' ' + str(r['idTpoDadoAdcio'])     + ' ,' \
        ' ' + str(r['idFormtDado'])        + ' ,' \
        '"' + str(r['desTpoDadoAdcio'])    + '")' 
    
    c.executaSQLInsertCursorAberto(sql)
    c.commit()
    c.desconecta()

    return resp