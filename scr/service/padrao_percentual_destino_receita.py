from flask import abort
from database import Database
from service import destino_receita, linha_orcamento

#------------------------------------------------------------------------------------------------#
# Lista todos os percentuais de um destino de receita
#------------------------------------------------------------------------------------------------#
def listar(idOrcam, idDstnoRecta):

    resp = {
        'percentualdestinoreceita' : [],
        'quantidadeRegistros': 0
    }

    resp.update(destino_receita.consulta_id(idOrcam, idDstnoRecta))
    
    sql =   'SELECT ' \
            '   ID_ORCAM, ' \
            '   ID_LIN_ORCAM, ' \
            '   ID_DSTNO_RECTA, ' \
            '   VAL_PERC ' \
            'FROM DBORCA.PDRAO_PER_DSTNO_RECTA ' \
            'WHERE ID_ORCAM = ' + str(idOrcam) + ' ' \
            'AND   ID_DSTNO_RECTA = ' + str(idDstnoRecta)
    
    c = Database()
    s = c.executaSQLFetchall(sql)

    for row in s:
        resp['quantidadeRegistros'] += 1    
        resp['percentualdestinoreceita'].append({
            'idOrcam': row['ID_ORCAM'],
            'idLinOrcam': row['ID_LIN_ORCAM'],
            'idDstnoRecta': row['ID_DSTNO_RECTA'],
            'valPerc': str(row['VAL_PERC'])
        })

    return resp

#------------------------------------------------------------------------------------------------#
# Consulta percentual destino de receita pela chave
#------------------------------------------------------------------------------------------------#
def consulta_id(idOrcam, idDstnoRecta, idLinOrcam):

    sql =   'SELECT ' \
            '   ID_ORCAM, ' \
            '   ID_LIN_ORCAM, ' \
            '   ID_DSTNO_RECTA, ' \
            '   VAL_PERC ' \
            'FROM DBORCA.PDRAO_PER_DSTNO_RECTA ' \
            'WHERE ID_ORCAM = ' + str(idOrcam) + ' ' \
            'AND   ID_LIN_ORCAM = ' + str(idLinOrcam) + ' ' \
            'AND   ID_DSTNO_RECTA = ' + str(idDstnoRecta)            
    
    c = Database()
    row = c.executaSQLFetchone(sql)
    
    if not row: abort(400,description="Registro Padrão Percentual de Destino Receita Não Encontrado")

    resp = {
        'percentualdestinoreceita': {
            'idOrcam': row['ID_ORCAM'],
            'idLinOrcam': row['ID_LIN_ORCAM'],
            'idDstnoRecta': row['ID_DSTNO_RECTA'],
            'valPerc': str(row['VAL_PERC'])
        }
    }

    return resp

#------------------------------------------------------------------------------------------------#
# Incluir percentual destino de receita
#------------------------------------------------------------------------------------------------#
def incluir(idOrcam, idDstnoRecta, req):

    if not idDstnoRecta > 0: abort(400,description="Destino Receita deve ser maior que ZERO")

    r = req.get_json()
    r['idOrcam'] = idOrcam
    r['idDstnoRecta'] = idDstnoRecta

    resp = {
        'mensagem': 'Registro Padrão Percentual de Destino Receita Incluído com sucesso',
        'percentualdestinoreceita': r
    }

    resp.update(destino_receita.consulta_id(idOrcam, idDstnoRecta))
    resp.update(linha_orcamento.consulta_id(idOrcam, r['idLinOrcam']))

    if not resp['linhaorcamento']['codNatuzLinOrcam'] == 'D': abort(400,description="Linha de Orçamento de Destino Receita deve ser Dívidas")

    sql = 'INSERT INTO DBORCA.PDRAO_PER_DSTNO_RECTA (ID_ORCAM, ID_LIN_ORCAM, ID_DSTNO_RECTA, VAL_PERC) VALUES (' \
        ' ' + str(r['idOrcam'])        + ' ,' \
        ' ' + str(r['idLinOrcam'])     + ' ,' \
        ' ' + str(r['idDstnoRecta'])   + ' ,' \
        ' ' + str(r['valPerc'])        + ' )' 
    
    c = Database()
    c.executaSQLInsert(sql)

    return resp