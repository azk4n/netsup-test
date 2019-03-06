#!/usr/bin/python3
import pytest
from app import db
from sqlalchemy import text
from models import TipoServico, Doutor, Job, CustoAtendimento, Pessoa
from datetime import date


tipo_servico = TipoServico(nome="Foo Bar", tipo="atendimento")
db.session.add(tipo_servico)
db.session.commit()

doutor = Doutor(nome="Foo Bar")
db.session.add(doutor)
db.session.commit()

job_1 = Job(
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
db.session.add(job_1)
db.session.commit()

job_2 = Job(
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
db.session.add(job_2)
db.session.commit()

custo_1 = CustoAtendimento(
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
db.session.add(custo_1)
db.session.commit()

custo_2 = CustoAtendimento(
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
db.session.add(custo_2)
db.session.commit()

custo_3 = CustoAtendimento(
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
db.session.add(custo_3)
db.session.commit()

# model Pessoa para frontend

pessoa_1 = Pessoa(nome="Ciclano", profissao="Desenvolvedor", idade=22)
db.session.add(pessoa_1)

pessoa_2 = Pessoa(nome="Fulano", profissao="Tester", idade=30)
db.session.add(pessoa_2)

pessoa_3 = Pessoa(nome="Beltrano", profissao="Diretor", idade=44)
db.session.add(pessoa_3)

db.session.commit()
