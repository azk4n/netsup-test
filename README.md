criar 2 bancos de dados POSTGRESQL:

- netsupdb
- netsupdb-test (para os testes, populado no inicio da execução dos testes e truncado ao final)

# backend (flask):

``` bash

# Passo 1 - clonar este repo
git clone https://github.com/azk4n/netsup-test
cd netsup-test

# Passo 2 - criar e ativar virtualenv
virtualenv --python=python3 venv
source venv/bin/activate
cd flask/

# Passo 3 - configure o seu usuario do banco de dados onde esta <azk4n>
nano config.py

# Passo 4 - deps
pip install -r requirements.txt

# Passo 5 - cria as tabelas do teste no banco netsupdb
flask db upgrade

# Passo 6 - carga de dados (para usar no frontend ou caso for testar a API via postman, curl, etc)
python fixtures.py

# Passo 7 - executar, localhost:5000
flask run

# Passo 8 - testes (possuem fixture automaticas que sao removidas apos conclusao dos testes, necessita do banco netsupdb_test criado)
pytest

```


# frontend (vue):

``` bash
# deps
npm install

# localhost:8080
npm run dev

# tests
npm test
```

# frontend (angularjs):

``` bash
# deps
npm install

# localhost:8000
npm run dev

# tests
npm test
```

# Problema:

Na minha visão o problema era saber <b>quanto</b> pagar e <b>o que</b> pagar para determinado doutor entre um periodo de tempo.

O resultado final da gerar_relatorio, com os dados da fixture (Passo 6), seria mais ou menos isso:

``` json
{
    "id_doutor": "1",
    "nome_doutor": "Foo Bar",
    "dt_ciclo": "\"2019-02-19\" - \"2019-02-27\"",
    "dt_previsao_pagamento": "2018-12-03",
    // totais de atendimento sao calculados com base nos totais das jobs
    "total_atendimento_ciclo": 255,
    "total_horas_extras_ciclo": 205,
    "total_reembolso_ciclo": 50,
    "total_geral_ciclo": 510,
    "jobs": [
	// job aqui é cada job que o doutor fez no range de dt_ciclo
		// primeira job
        {
            "id_doutor": "1",
            "id_job": 1,
            "dt_pagamento_job": "job.dt_pagamento_job",
            "dt_ciclo": "\"2019-02-19\" - \"2019-02-27\"",
            "dt_previsao_pagamento": "job.dt_previsao_pagamento",
            "total_atendimento_job": 200,
            "total_horas_extras_job": 160,
            "total_reembolso_job": 40,
            "total_geral_job": 400,
            "tipo_servico": "Foo Bar",
            "dh_ult_encerramento": "job.dh_ult_encerramento",
            "atendimentos": [ 
				// atendimentos por job
                {
                    "id_atendimento": 1,
                    "id_job": 1,
                    "valor_atendimento": 100,
                    "valor_horas_extras": 80,
                    "valor_reembolso": 20,
                    "total_atendimento": 200
                },
                {
                    "id_atendimento": 2,
                    "id_job": 1,
                    "valor_atendimento": 100,
                    "valor_horas_extras": 80,
                    "valor_reembolso": 20,
                    "total_atendimento": 200
                }
            ]
        },
        // segunda job
        {
            "id_doutor": "1",
            "id_job": 2,
            "dt_pagamento_job": "job.dt_pagamento_job",
            "dt_ciclo": "\"2019-02-19\" - \"2019-02-27\"",
            "dt_previsao_pagamento": "job.dt_previsao_pagamento",
            "total_atendimento_job": 55,
            "total_horas_extras_job": 45,
            "total_reembolso_job": 10,
            "total_geral_job": 110,
            "tipo_servico": "Foo Bar",
            "dh_ult_encerramento": "job.dh_ult_encerramento",
            "atendimentos": [
				// outro atendimento por job
                {
                    "id_atendimento": 3,
                    "id_job": 2,
                    "valor_atendimento": 55,
                    "valor_horas_extras": 45,
                    "valor_reembolso": 10,
                    "total_atendimento": 110
                }
            ]
        }
    ]
}
```