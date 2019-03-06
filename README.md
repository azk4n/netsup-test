criar 2 bancos de dados POSTGRESQL:

- netsupdb
- netsupdb-test (para os testes, populado no inicio da execução dos testes e truncado ao final)

# backend (flask):

``` bash

# clonar este repo
git clone https://github.com/azk4n/netsup-test
cd netsup-test

# criar e ativar virtualenv
virtualenv --python=python3 venv
source venv/bin/activate

cd flask/

# configure o seu usuario do banco de dados onde esta <azk4n>
nano config.py

# deps
pip install -r requirements.txt

# cria as tabelas do teste no banco netsupdb
flask db upgrade

# carga de dados (para usar no frontend ou caso for testar a API via postman, curl, etc)
python fixtures.py

# localhost:5000
flask run

# testes (possuem fixture automaticas que sao removidas apos conclusao dos testes, necessita do banco netsupdb_test criado)
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
