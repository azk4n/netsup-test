#!/usr/bin/python3
from .fixtures import *


def test_registros_encontrados(client, db, tipo_servico, custo_1, custo_2, custo_3, job_1, job_2, doutor):
    response = client.post('/gerar_relatorio', data=dict(
            id_doutor='1',
            dt_ciclo_inicial='2019-02-19',
            dt_ciclo_final='2019-02-27'
        ),
        headers={"Authorization": "test"},
        follow_redirects=True)
    assert 200 == response.status_code
    assert 'id_doutor' in response.get_json().keys()


def test_nenhum_registro_encontrado(client, db, tipo_servico, custo_1, custo_2, custo_3, job_1, job_2, doutor):
    response = client.post('/gerar_relatorio', data=dict(
            id_doutor='1',
            dt_ciclo_inicial='2019-02-10',
            dt_ciclo_final='2019-02-15'
        ),
        headers={"Authorization": "test"},
        follow_redirects=True)
    assert 404 == response.status_code
    expected_error = 'Nenhum registro encontrado'
    assert expected_error in response.get_json()['message']


def test_falha_conectar_banco(app, client, db, tipo_servico, custo_1, custo_2, custo_3, job_1, job_2, doutor):
    # fechando a sessao do banco para teste
    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    test_db_uri = f"{db_uri}xxx"
    app.config['SQLALCHEMY_DATABASE_URI'] = test_db_uri

    response = client.post('/gerar_relatorio', data=dict(
            id_doutor='1',
            # range existente na fixture, deveria retornar os registros como o primeiro test
            dt_ciclo_inicial='2019-02-19',
            dt_ciclo_final='2019-02-27'
        ),
        headers={"Authorization": "test"},
        follow_redirects=True)
    assert 500 == response.status_code
    expected_error = 'Falha ao conectar com o banco de dados'
    assert expected_error in response.get_json()['message']

    app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_uri}"
