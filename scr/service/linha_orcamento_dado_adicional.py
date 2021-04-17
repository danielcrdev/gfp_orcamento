from database import Database
from service import orcamento, linha_orcamento, tipo_dado_adicional
from flask import abort

#------------------------------------------------------------------------------------------------#
# Lista todos os dados adicionais de uma linha de orçamento
#------------------------------------------------------------------------------------------------#
def listar(idOrcam, idLinOrcam):
    
    resp = {
        'quantidadeRegistros': 0,
        'linhaorcamentodadoadicional' : []
    }

    resp.update(linha_orcamento.consulta_id(idOrcam, idLinOrcam))

    sql =   'SELECT ' \
            '   ID_ORCAM, ' \
            '   ID_LIN_ORCAM, ' \
            '   ID_TPO_DADO_ADCIO, ' \
            '   IND_DADO_OBRIG ' \
            'FROM DBORCA.LIN_ORCAM_DADO_ADCIO ' \
            'WHERE ID_ORCAM =  ' + str(idOrcam) + ' ' \
            'AND   ID_LIN_ORCAM = "' + str(idLinOrcam) + '"'

    c = Database()
    s = c.executaSQLFetchall(sql) 

    for row in s:
        resp['quantidadeRegistros'] += 1
        resp['linhaorcamentodadoadicional'].append({
            'idOrcam': row['ID_ORCAM'],
            'idLinOrcam': row['ID_LIN_ORCAM'],
            'idTpoDadoAdcio': row['ID_TPO_DADO_ADCIO'],
            'indDadoObrig': row['IND_DADO_OBRIG']
        })
    
    return resp


#------------------------------------------------------------------------------------------------#
# Consulta dado adicionais da linha do orçamento pela chave (linha e tipo de dados)
#------------------------------------------------------------------------------------------------#
def consulta_id(idOrcam, idLinOrcam, idTpoDadoAdcio):

    sql =   'SELECT ' \
            '   ID_ORCAM, ' \
            '   ID_LIN_ORCAM, ' \
            '   ID_TPO_DADO_ADCIO, ' \
            '   IND_DADO_OBRIG ' \
            'FROM DBORCA.LIN_ORCAM_DADO_ADCIO ' \
            'WHERE ID_ORCAM =  ' + str(idOrcam) + ' ' \
            'AND   ID_LIN_ORCAM = "' + str(idLinOrcam) + '"' \
            'AND   ID_TPO_DADO_ADCIO = "' + str(idTpoDadoAdcio) + '"'
    
    c = Database()
    row = c.executaSQLFetchone(sql)

    if not row: abort(400,description="Registro Dado Adicional de Linha do Orçamento Não Encontrado")

    resp = {
        'linhaorcamentodadoadicional': {
            'idOrcam': row['ID_ORCAM'],
            'idLinOrcam': row['ID_LIN_ORCAM'],
            'idTpoDadoAdcio': row['ID_TPO_DADO_ADCIO'],
            'indDadoObrig': row['IND_DADO_OBRIG']
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
        'mensagem': 'Dado adicional de Linha do orçamento incluído com sucesso',
        'linhaorcamentodadoadicional': r,
    }

    resp.update(linha_orcamento.consulta_id(idOrcam, idLinOrcam))
    resp.update(tipo_dado_adicional.consulta_id(idOrcam, r['idTpoDadoAdcio']))

    sql = 'INSERT INTO DBORCA.LIN_ORCAM_DADO_ADCIO (ID_ORCAM, ID_LIN_ORCAM, ID_TPO_DADO_ADCIO, IND_DADO_OBRIG) VALUES (' \
        ' ' + str(r['idOrcam'])            + ' ,' \
        ' ' + str(r['idLinOrcam'])         + ' ,' \
        ' ' + str(r['idTpoDadoAdcio'])     + ' ,' \
        '"' + str(r['indDadoObrig'])       + '")' 
    
    c = Database()
    c.executaSQLInsert(sql)

    return resp