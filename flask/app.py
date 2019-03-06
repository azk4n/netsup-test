from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, exc
from sqlalchemy.orm import validates
from decorators import require_login
import simplejson as json
from flask_migrate import Migrate
from exceptions import Error
import pytest
import psycopg2

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.errorhandler(Error)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/ping', methods=['GET'])
@require_login
def ping():
    return jsonify({'result': 'OK'})


@app.route('/pessoas/<string:pessoa_id>', methods=['GET'])
@require_login
def pessoa_detail(pessoa_id):
    result = db.engine.execute(text("SELECT * FROM public.pessoa WHERE id={}".format(pessoa_id)).execution_options(autocommit=True))
    if result.rowcount == 0:
        raise Error('Nenhum registro encontrado', status_code=404)
    return jsonify({'result': dict(row) for row in result})


@app.route('/pessoas', methods=['POST'])
@require_login
def pessoa():
    """ API para testar o frontend """
    json = request.get_json()

    nome = json['nome'] or None
    profissao = json['profissao'] or None
    idade = json['idade'] or None

    query = "SELECT * FROM public.pessoa WHERE 1=1"
    if nome:
        query += " AND upper(nome)='{}'".format(nome.upper())
    if idade:
        query += " AND idade='{}'".format(idade)
    if profissao:
        query += " AND upper(profissao)='{}'".format(profissao.upper())

    result = db.engine.execute(text(query).execution_options(autocommit=True))
    if result.rowcount == 0:
        raise Error('Nenhum registro encontrado', status_code=404)

    return jsonify({'result': [dict(row) for row in result]})


@app.route('/gerar_relatorio', methods=['POST'])
@require_login
def gerar_relatorio():
    id_doutor = request.form.get('id_doutor')
    dt_ciclo_inicial = request.form.get('dt_ciclo_inicial')
    dt_ciclo_final = request.form.get('dt_ciclo_final')

    query = text(
        """
        SELECT * FROM public.custo_atendimento
        WHERE id_doutor={}
        """.format(id_doutor)).execution_options(autocommit=True)

    if dt_ciclo_inicial and dt_ciclo_final:
        query = text(
            """
            SELECT * FROM public.custo_atendimento
            WHERE id_doutor={}
            AND dt_ciclo BETWEEN '{}' AND '{}'
            """.format(id_doutor, dt_ciclo_inicial, dt_ciclo_final)).execution_options(autocommit=True)
    try:
        custos = db.engine.execute(query)
    except exc.OperationalError as ex:
        raise Error('Falha ao conectar com o banco de dados', status_code=500)

    if custos.rowcount == 0:
        raise Error('Nenhum registro encontrado', status_code=404)

    nome_doutor = db.engine.execute(text(
        """SELECT nome FROM public.doutor
        WHERE id={}
        """.format(id_doutor)).execution_options(autocommit=True)
    ).fetchone()

    jobs = []
    # variaveis a serem incrementadas
    total_atendimento_ciclo = 0
    total_horas_extras_ciclo = 0
    total_reembolso_ciclo = 0
    total_geral_ciclo = 0

    ciclo_json = {
       "id_doutor": id_doutor,
       "nome_doutor": nome_doutor[0],
       "dt_ciclo": '{} - {}'.format(dt_ciclo_inicial, dt_ciclo_final),
       "dt_previsao_pagamento": "2018-12-03",
       "total_atendimento_ciclo": total_atendimento_ciclo,
       "total_horas_extras_ciclo": total_horas_extras_ciclo,
       "total_reembolso_ciclo": total_reembolso_ciclo,
       "total_geral_ciclo": total_geral_ciclo,
       "jobs": []
    }
    for custo in custos:
        # jobs feitas pelo doutor no range entre dt_ciclo's
        jobs.append(custo.id_job)

    # usando set para impedir jobs duplicadas
    for job in list(set(jobs)):
        # variaveis a serem incrementadas
        total_atendimento_job = 0
        total_horas_extras_job = 0
        total_reembolso_job = 0
        total_geral_job = 0

        # pega id do tipo_servico do job
        id_tipo_servico = db.engine.execute(text(
            """
            SELECT id_tipo_servico FROM public.job
            WHERE id={}
            """.format(job)).execution_options(autocommit=True)
        ).fetchone()

        # usa id para selecionar nome do tipo_servico
        tipo_servico = db.engine.execute(text(
            """
            SELECT nome FROM public.tipo_servico
            WHERE id={}
            """.format(id_tipo_servico[0])).execution_options(autocommit=True)
        ).fetchone()

        job_json = {
            "id_doutor": id_doutor,
            "id_job": job,
            "dt_pagamento_job": 'job.dt_pagamento_job',
            "dt_ciclo": '{} - {}'.format(dt_ciclo_inicial, dt_ciclo_final),
            "dt_previsao_pagamento": 'job.dt_previsao_pagamento',
            "total_atendimento_job": 0,
            "total_horas_extras_job": 0,
            "total_reembolso_job": 0,
            "total_geral_job": 0,
            "tipo_servico": tipo_servico[0],
            "dh_ult_encerramento": 'job.dh_ult_encerramento',
            "atendimentos": []
        }
        # custos de atendimento por job
        custos = db.engine.execute(text(
            """
            SELECT * FROM public.custo_atendimento
            WHERE id_job={}
            """.format(job)).execution_options(autocommit=True)
        )

        for custo in custos:
            # incrementa valores totais da job
            total_atendimento_job += custo.valor_atendimento
            total_horas_extras_job += custo.valor_horas_extras
            total_reembolso_job += custo.valor_reembolso
            total_geral_job += (custo.valor_atendimento + custo.valor_horas_extras + custo.valor_reembolso)
            custo_json = {
               "id_atendimento": custo.id,
               "id_job": custo.id_job,
               "valor_atendimento": custo.valor_atendimento,
               "valor_horas_extras": custo.valor_horas_extras,
               "valor_reembolso": custo.valor_reembolso,
               "total_atendimento": custo.valor_atendimento + custo.valor_horas_extras + custo.valor_reembolso
            }
            job_json['atendimentos'].append(custo_json)

        # add valor total dos custos da job no json de segundo nivel (job)
        job_json['total_atendimento_job'] = total_atendimento_job
        job_json['total_horas_extras_job'] = total_horas_extras_job
        job_json['total_reembolso_job'] = total_reembolso_job
        job_json['total_geral_job'] = total_geral_job

        # add job no json de primeiro nivel (ciclo)
        ciclo_json['jobs'].append(job_json)

        # add valor total dos custos das jobs no json de primeiro nivel (ciclo)
        ciclo_json['total_atendimento_ciclo'] += total_atendimento_job
        ciclo_json['total_horas_extras_ciclo'] += total_horas_extras_job
        ciclo_json['total_reembolso_ciclo'] += total_reembolso_job
        ciclo_json['total_geral_ciclo'] += total_geral_job

    return jsonify(ciclo_json)


if __name__ == '__main__':
    app.run()
