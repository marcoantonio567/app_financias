# Financeiro App

Aplicacao web de controle financeiro pessoal feita com Django.

O projeto permite cadastrar entradas e saidas, acompanhar historico paginado e visualizar dashboards com metricas dos ultimos 30 dias (ou por mes selecionado).

## Funcionalidades

- Cadastro de lancamentos financeiros (entrada e saida).
- Calculo automatico de totais de entradas, saidas e saldo.
- Listagem dos 20 ultimos lancamentos na tela principal.
- Historico completo com paginacao.
- Dashboard com graficos (Chart.js) e filtro por mes.
- Protecao de acesso por senha PIN de 6 digitos (sessao).

## Tecnologias

- Python 3.12+
- Django 6.0.4
- SQLite (banco padrao do Django)
- HTML + CSS + JavaScript
- Chart.js (via CDN)

## Estrutura do Projeto

```text
financeiro_app/
|-- core/                   # Configuracoes do projeto Django
|-- financas/               # App principal
|   |-- migrations/
|   |-- templates/financas/
|   |-- forms.py
|   |-- models.py
|   |-- urls.py
|   `-- views.py
|-- manage.py
`-- README.md
```

## Como Executar

1. Clone ou baixe este repositorio.
2. Entre na pasta do projeto:

```bash
cd financeiro_app
```

1. Crie e ative um ambiente virtual.

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

1. Instale as dependencias:

```bash
pip install "Django==6.0.4"
```

1. Rode as migracoes:

```bash
python manage.py migrate
```

1. Inicie o servidor:

```bash
python manage.py runserver
```

1. Acesse no navegador:

```text
http://127.0.0.1:8000/
```

## PIN de Acesso

O app exige uma senha numerica de 6 digitos para liberar as telas.

- Chave usada: `FINANCEIRO_APP_PIN` em `core/settings.py`
- Valor atual no projeto: `162636`

Para alterar, edite o arquivo `core/settings.py` e mude o valor da constante.

## Rotas Principais

- `/` ou `/lancamentos/` -> cadastro e resumo de lancamentos
- `/historico/` -> historico paginado
- `/dashboard/` -> graficos e indicadores
- `/senha/` -> validacao do PIN
- `/admin/` -> painel administrativo do Django

## Modelo de Dados

O app possui o modelo `Lancamento` com os campos:

- `tipo` (`E` para Entrada, `S` para Saida)
- `descricao`
- `valor`
- `data`
- `criado_em`

## Melhorias Futuras (Sugestoes)

- Incluir autenticacao de usuario (login Django).
- Criar testes automatizados para views e formularios.

