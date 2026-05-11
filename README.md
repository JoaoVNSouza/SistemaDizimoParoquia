# Sistema de Dízimo — Paróquia

> Plataforma web para **gestão de fiéis, lançamento de pagamentos de dízimo, emissão de comprovantes e relatórios** de uma paróquia católica. Pensado para uso interno da secretaria paroquial: cadastrar fiéis, registrar contribuições, acompanhar inadimplência e visualizar a arrecadação mês a mês em um painel único.

---

## Visão geral

O sistema centraliza o ciclo completo do dízimo paroquial:

- 👥 **Cadastro de fiéis** — dados pessoais, contato e endereço, com status ativo/inativo.
- 💰 **Registro de dízimos** — valor, data de pagamento, mês/ano de referência e forma de pagamento (Dinheiro, PIX ou Cartão).
- 🧾 **Comprovantes** — geração de comprovante individual por contribuição para entregar ao fiel.
- 📊 **Dashboard** — KPIs de arrecadação do mês e do ano, total de fiéis ativos, inadimplentes do mês corrente e últimos pagamentos.
- 📈 **Gráfico mensal** — arrecadação por mês do ano em barras interativas (Plotly), com *fallback* automático para tabela HTML caso o Plotly não esteja disponível.
- 📑 **Relatórios** — filtros por ano e mês com totalização da arrecadação.
- 🔐 **Autenticação** — área restrita por login; usuários da secretaria gerenciados pelo Django Admin.

---

## 🧱 Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| Linguagem | **Python 3.13** (`.python-version`) — container roda em Python 3.12-slim |
| Framework Web | **Django 5.2** |
| Banco de dados | **PostgreSQL 16** (`psycopg` 3.x) |
| Gráficos | **Plotly** |
| Manipulação de dados | **Pandas** |
| Containerização | **Docker** + **Docker Compose** |
| Deploy | Pronto para **EasyPanel** (compose dedicado) |
| Front-end | Bootstrap (via templates Django) |

### Estrutura dos apps Django

```
core/         → settings, urls e wsgi do projeto
usuarios/     → login, logout e cadastro de usuários
fieis/        → CRUD de fiéis (model Fiel)
dizimo/       → CRUD de pagamentos e comprovante
dashboard/    → painel principal, histórico por fiel e relatório
templates/    → templates HTML compartilhados (base, 404, dashboard etc.)
static/       → assets estáticos
```

---

## 🚀 Como rodar (Python local)

> Use esta opção se você já tem Python e Postgres instalados na máquina.

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd SistemaDizimoParoquia
```

### 2. Crie e ative um ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```


### 3. Instale as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto (já existe um exemplo no repositório). Exemplo mínimo:

```dotenv
SECRET_KEY=chave-em-producao
DEBUG=True
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=

POSTGRES_DB=db_name
POSTGRES_USER=user_admin
POSTGRES_PASSWORD=pasword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Aplique as migrações

```bash
python manage.py migrate
```

### 6. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 8. Suba o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse **http://localhost:8000** 🎉

---

## 🐳 Como rodar (Docker)

O projeto vem com **três arquivos compose** prontos:

| Arquivo | Para que serve |
|---|---|
| `docker-compose.local.yml` | Desenvolvimento local — publica a porta 8000 e expõe o Postgres no host |
| `docker-compose.yml` | Produção padrão |
| `docker-compose easypanel.yml` | Deploy no EasyPanel |


### Subir em produção

```bash
docker compose up -d --build
```

A aplicação roda com **Gunicorn** (3 workers) atrás de um proxy reverso (já configurado com `SECURE_PROXY_SSL_HEADER` e `USE_X_FORWARDED_HOST`).

---

## ⚙️ Variáveis de ambiente

| Variável | Descrição | Padrão |
|---|---|---|
| `SECRET_KEY` | Chave secreta do Django | *(obrigatória em produção)* |
| `DEBUG` | Modo debug | `False` |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por vírgula | `*` |
| `CSRF_TRUSTED_ORIGINS` | Origens confiáveis para CSRF (com `https://`) | *(vazio)* |
| `DATABASE_URL` | URL completa do banco (opcional, prioritária) | — |
| `POSTGRES_DB` | Nome do banco | `dizimo` |
| `POSTGRES_USER` | Usuário do banco | `dizimo` |
| `POSTGRES_PASSWORD` | Senha do banco | `dizimo` |
| `POSTGRES_HOST` | Host do banco | `localhost` |
| `POSTGRES_PORT` | Porta do banco | `5432` |
| `POSTGRES_HOST_PORT` | Porta publicada no host (compose local) | `5433` |
| `DJANGO_SUPERUSER_USERNAME` | Cria superusuário automaticamente no boot | — |
| `DJANGO_SUPERUSER_PASSWORD` | Senha do superusuário | — |
| `DJANGO_SUPERUSER_EMAIL` | E-mail do superusuário | `admin@example.com` |

---

## 🔐 Autenticação

- Login obrigatório em todas as telas do dashboard e nos CRUDs (`@login_required`).
- Login: `/usuarios/login/` — Logout: `/usuarios/logout/`.
- Gestão de usuários e permissões via Django Admin em `/admin/`.

---

## 📜 Créditos/Licença

Desenvolvido para apoiar a gestão financeira e pastoral da comunidade paroquial. Projeto de uso interno paroquial. Adapte a licença conforme a necessidade da paróquia/organização.
