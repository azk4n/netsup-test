#!/usr/bin/python3
import pytest
from app import app as _app
from app import db as _db
from sqlalchemy import text
from models import TipoServico, Doutor, Job, CustoAtendimento
from datetime import date


@pytest.yield_fixture(scope="session")
def app():
    db_uri = _app.config["SQLALCHEMY_DATABASE_URI"]
    # append _test no URI configurado
    test_db_uri = f"{db_uri}_test"
    _app.config['SQLALCHEMY_DATABASE_URI'] = test_db_uri

    with _app.app_context():
        yield _app


@pytest.yield_fixture
def tipo_servico(db):
    # setup
    model = TipoServico(nome="Foo Bar", tipo="atendimento")
    db.session.add(model)
    db.session.commit()
    yield model
    # teardonw
    db.session.delete(model)
    db.session.commit()


@pytest.yield_fixture
def doutor(db):
    # setup
    model = Doutor(nome="Foo Bar")
    db.session.add(model)
    db.session.commit()
    yield model
    # teardonw
    db.session.delete(model)
    db.session.commit()


@pytest.yield_fixture
def job_1(db, doutor, tipo_servico):
    model = Job(
        problema="test",
        dh_agendamento_cliente=date.today(),
        cep="38557700",
        estado="MG",
        cidade="test",
        bairro="test",
        logradouro="test",
        numero="test",
        complemento="test",
        longitude=20.321312,
        latitude=20.321312,
        tipo="atendimento",
        id_tipo_servico=tipo_servico.id,
        id_doutor=doutor.id,
    )
    db.session.add(model)
    db.session.commit()
    yield model
    # teardown
    db.session.delete(model)
    db.session.commit()


@pytest.yield_fixture
def job_2(db, doutor, tipo_servico):
    model = Job(
        problema="test",
        dh_agendamento_cliente=date.today(),
        cep="38557700",
        estado="MG",
        cidade="test",
        bairro="test",
        logradouro="test",
        numero="test",
        complemento="test",
        longitude=20.321312,
        latitude=20.321312,
        tipo="atendimento",
        id_tipo_servico=tipo_servico.id,
        id_doutor=doutor.id,
    )
    db.session.add(model)
    db.session.commit()
    yield model
    # teardown
    db.session.delete(model)
    db.session.commit()


@pytest.yield_fixture
def custo_1(db, doutor, job_1):
    model = CustoAtendimento(
        id_job=job_1.id,
        id_atendimento=1,
        id_doutor=doutor.id,
        dh_ult_encerramento=date.today(),
        dt_ciclo=date(2019, 2, 20),
        dt_previsao_pagamento=date.today(),
        dt_pagamento=date.today(),
        dt_ult_agendamento=date.today(),
        ano=2019,
        trimestre=2,
        mes=2,
        valor_atendimento=100.00,
        valor_horas_extras=80.00,
        valor_reembolso=20.00,
        total_atendimento=200.00,
    )
    db.session.add(model)
    db.session.commit()
    yield model
    # teardonw
    db.session.delete(model)
    db.session.commit()


@pytest.yield_fixture
def custo_2(db, doutor, job_1):
    model = CustoAtendimento(
        id_job=job_1.id,
        id_atendimento=1,
        id_doutor=doutor.id,
        dh_ult_encerramento=date.today(),
        dt_ciclo=date(2019, 2, 25),
        dt_previsao_pagamento=date.today(),
        dt_pagamento=date.today(),
        dt_ult_agendamento=date.today(),
        ano=2019,
        trimestre=2,
        mes=2,
        valor_atendimento=100.00,
        valor_horas_extras=80.00,
        valor_reembolso=20.00,
        total_atendimento=200.00,
    )
    db.session.add(model)
    db.session.commit()
    yield model
    # teardown
    db.session.delete(model)
    db.session.commit()


@pytest.yield_fixture
def custo_3(db, doutor, job_2):
    model = CustoAtendimento(
        id_job=job_2.id,
        id_atendimento=4,
        id_doutor=doutor.id,
        dh_ult_encerramento=date.today(),
        dt_ciclo=date(2019, 2, 26),
        dt_previsao_pagamento=date.today(),
        dt_pagamento=date.today(),
        dt_ult_agendamento=date.today(),
        ano=2019,
        trimestre=2,
        mes=2,
        valor_atendimento=55.00,
        valor_horas_extras=45.00,
        valor_reembolso=10.00,
        total_atendimento=110.00,
    )
    db.session.add(model)
    db.session.commit()
    yield model
    # teardown
    db.session.delete(model)
    db.session.commit()


@pytest.yield_fixture
def client(app):
    # test client para requisicoes na api
    client = app.test_client()
    yield client


@pytest.yield_fixture(scope="session")
def db(app):
    # cria database no setup
    _db.create_all()
    yield _db
    # dropa no teardown
    _db.drop_all()
