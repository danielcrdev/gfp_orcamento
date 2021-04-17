from flask   import Blueprint, request, jsonify
from service import orcamento, linha_orcamento, liberacao_linha_orcamento, situacao_orcamento, tipo_dado_adicional
from service import nivel_linha_orcamento, linha_orcamento_dado_adicional, destino_receita, formato_dado_adicional
from service import padrao_percentual_destino_receita, natureza_linha_orcamento, modelo_orcamento

basePath = '/gfp'
api = Blueprint('api', __name__, url_prefix=basePath)

def get_blueprint():
    return api

#------------------------------------------------------------------------------------------------#
# Orçamento
#------------------------------------------------------------------------------------------------#

@api.route('/v1/orcamento', methods=['GET'])
def get_all_orcamento():
    return orcamento.listar(), 200

@api.route('/v1/orcamento/<int:_idOrcam>', methods=['GET'])
def get_by_id_orcamento(_idOrcam):
    return orcamento.consulta_id(_idOrcam), 200

@api.route('/v1/orcamento', methods=['POST'])
def post_orcamento():
    return orcamento.incluir(request), 201

@api.route('/v1/orcamento/<int:_idOrcam>', methods=['DELETE'])
def delete_orcamento(_idOrcam):
    return orcamento.excluir(_idOrcam), 200

#------------------------------------------------------------------------------------------------#
# Linha de Orçamento
#------------------------------------------------------------------------------------------------#

@api.route('/v1/orcamento/<int:_idOrcam>/linha', methods=['GET'])
def get_all_linha_orcamento(_idOrcam):
    return linha_orcamento.listar(_idOrcam), 200

@api.route('/v1/orcamento/<int:_idOrcam>/linha/<int:_idLinOrcam>', methods=['GET'])
def get_by_id_linha_orcamento(_idOrcam, _idLinOrcam):
    return linha_orcamento.consulta_id(_idOrcam, _idLinOrcam), 200

@api.route('/v1/orcamento/<int:_idOrcam>/linha', methods=['POST'])
def post_linha_orcamento(_idOrcam):
    return linha_orcamento.incluir(_idOrcam, request), 201

#------------------------------------------------------------------------------------------------#
# Liberação Linha de Orçamento
#------------------------------------------------------------------------------------------------#

@api.route('/v1/orcamento/<int:_idOrcam>/linha/<int:_idLinOrcam>/liberacao', methods=['GET'])
def get_all_liberacao_inha_orcamento(_idOrcam, _idLinOrcam):
    return liberacao_linha_orcamento.listar(_idOrcam, _idLinOrcam), 200

@api.route('/v1/orcamento/<int:_idOrcam>/linha/<int:_idLinOrcam>/liberacao/<string:_datLinOrcam>', methods=['GET'])
def get_by_id_liberacao_inha_orcamento(_idOrcam, _idLinOrcam, _datLinOrcam):
    return liberacao_linha_orcamento.consulta_id(_idOrcam, _idLinOrcam, _datLinOrcam), 200

@api.route('/v1/orcamento/<int:_idOrcam>/linha/<int:_idLinOrcam>/liberacao', methods=['POST'])
def post_liberacao_inha_orcamento(_idOrcam, _idLinOrcam):
    return liberacao_linha_orcamento.incluir(_idOrcam, _idLinOrcam, request), 201


#------------------------------------------------------------------------------------------------#
# Dados adicionais de uma linha de orçamento
#------------------------------------------------------------------------------------------------#

@api.route('/v1/orcamento/<int:_idOrcam>/linha/<int:_idLinOrcam>/dadoadicional', methods=['GET'])
def get_all_linha_orcamento_dado_adicional(_idOrcam, _idLinOrcam):
    return linha_orcamento_dado_adicional.listar(_idOrcam, _idLinOrcam), 200

@api.route('/v1/orcamento/<int:_idOrcam>/linha/<int:_idLinOrcam>/dadoadicional/<string:_idTpoDadoAdcio>', methods=['GET'])
def get_by_id_linha_orcamento_dado_adicional(_idOrcam, _idLinOrcam, _idTpoDadoAdcio):
    return linha_orcamento_dado_adicional.consulta_id(_idOrcam, _idLinOrcam, _idTpoDadoAdcio), 200

@api.route('/v1/orcamento/<int:_idOrcam>/linha/<int:_idLinOrcam>/dadoadicional', methods=['POST'])
def post_linha_orcamento_dado_adicional(_idOrcam, _idLinOrcam):
    return linha_orcamento_dado_adicional.incluir(_idOrcam, _idLinOrcam, request), 201

#------------------------------------------------------------------------------------------------#
# Destino Receita
#------------------------------------------------------------------------------------------------#

@api.route('/v1/orcamento/<int:_idOrcam>/destinoreceita', methods=['GET'])
def get_all_destino_receita(_idOrcam):
    return destino_receita.listar(_idOrcam), 200

@api.route('/v1/orcamento/<int:_idOrcam>/destinoreceita/<int:_idDstnoRecta>', methods=['GET'])
def get_by_id_destino_receita(_idOrcam, _idDstnoRecta):
    return destino_receita.consulta_id(_idOrcam, _idDstnoRecta), 200

@api.route('/v1/orcamento/<int:_idOrcam>/destinoreceita', methods=['POST'])
def post_destino_receita(_idOrcam):
    return destino_receita.incluir(_idOrcam, request), 201

#------------------------------------------------------------------------------------------------#
# Padrão Percentual Destino Receita
#------------------------------------------------------------------------------------------------#

@api.route('/v1/orcamento/<int:_idOrcam>/destinoreceita/<int:_idDstnoRecta>/percentualdestino', methods=['GET'])
def get_all_padrao_percentual_destino_receita(_idOrcam, _idDstnoRecta):
    return padrao_percentual_destino_receita.listar(_idOrcam, _idDstnoRecta), 200

@api.route('/v1/orcamento/<int:_idOrcam>/destinoreceita/<int:_idDstnoRecta>/percentualdestino/<int:_idLinOrcam>', methods=['GET'])
def get_by_id_padrao_percentual_destino_receita(_idOrcam, _idDstnoRecta,_idLinOrcam):
    return padrao_percentual_destino_receita.consulta_id(_idOrcam, _idDstnoRecta, _idLinOrcam), 200

@api.route('/v1/orcamento/<int:_idOrcam>/destinoreceita/<int:_idDstnoRecta>/percentualdestino', methods=['POST'])
def post_padrao_percentual_destino_receita(_idOrcam, _idDstnoRecta):
    return padrao_percentual_destino_receita.incluir(_idOrcam, _idDstnoRecta, request), 201

#------------------------------------------------------------------------------------------------#
# Tipo Dado Adicional
#------------------------------------------------------------------------------------------------#

@api.route('/v1/orcamento/<int:_idOrcam>/dadoadicional', methods=['GET'])
def get_all_tipo_dado_adicional(_idOrcam):
    return tipo_dado_adicional.listar(_idOrcam), 200

@api.route('/v1/orcamento/<int:_idOrcam>/dadoadicional/<int:_idTpoDadoAdcio>', methods=['GET'])
def get_by_id_tipo_dado_adicional(_idOrcam, _idTpoDadoAdcio):
    return tipo_dado_adicional.consulta_id(_idOrcam, _idTpoDadoAdcio), 200

@api.route('/v1/orcamento/<int:_idOrcam>/dadoadicional', methods=['POST'])
def post_tipo_dado_adicional(_idOrcam):
    return tipo_dado_adicional.incluir(_idOrcam, request), 201


#------------------------------------------------------------------------------------------------#
# Criar Modelos Orçamento
#------------------------------------------------------------------------------------------------#

@api.route('/v1/orcamento/modelo/<string:_codModelo>', methods=['POST'])
def post_modelo_orcamento(_codModelo):
    return modelo_orcamento.criar(_codModelo, request), 201

