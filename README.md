# Finance API

![Tests](https://github.com/probstella/finance-api-fastapi/actions/workflows/tests.yml/badge.svg)

API REST para controle de despesas pessoais, com resumo mensal por categoria.
Feita com FastAPI, SQLAlchemy e SQLite, com testes automatizados em pytest.

## Funcionalidades

- Cadastro, listagem, consulta e remoção de despesas
- Validação automática dos dados (ex.: valor deve ser maior que zero)
- Resumo mensal agrupado por categoria

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/expenses` | Cria uma despesa |
| GET | `/expenses` | Lista as despesas |
| GET | `/expenses/{id}` | Busca uma despesa |
| DELETE | `/expenses/{id}` | Remove uma despesa |
| GET | `/summary/{ano}/{mes}` | Total do mês por categoria |

## Como rodar

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

A documentação interativa fica em `http://localhost:8000/docs`.

## Testes

```bash
python -m pytest tests -v
```

Os testes usam um banco SQLite em memória, sem afetar os dados reais.

## Tecnologias

Python, FastAPI, SQLAlchemy, SQLite, Pydantic, pytest

## Próximos passos

- Migrar para PostgreSQL
- Autenticação com JWT
- Containerização com Docker
