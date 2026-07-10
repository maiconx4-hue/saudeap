# SaúdeAP — Backend (Flask + SQLAlchemy + MySQL)

Sistema de controle de medicamentos em UBS do Amapá — backend completo com API REST, templates HTML e painel administrativo.

## Estrutura

```
backend/
├── app.py                 # Factory do Flask, rotas de páginas e auth
├── auth.py                # Login/logout (sessão)
├── admin.py               # Rotas do painel administrativo (renderiza templates)
├── config.py              # Configurações (string de conexão MySQL)
├── models.py              # Modelos: UBS, Medicamento, Estoque, Movimentacao
├── requirements.txt       # Dependências Python
├── .env.example           # Template de variáveis de ambiente
├── routes/
│   ├── __init__.py
│   ├── publico.py         # API pública: consulta de medicamentos + lista de UBS
│   ├── ubs.py             # CRUD de UBS (API)
│   ├── medicamento.py     # CRUD de Medicamentos (API)
│   ├── estoque.py         # CRUD de Estoque (API)
│   └── movimentacao.py    # Entradas/Saídas (API — atualiza estoque)
├── templates/             # Templates Jinja2 (frontend HTML)
│   ├── index.html         # Página pública de consulta
│   ├── login.html         # Tela de login
│   ├── base_admin.html    # Layout do painel (sidebar + header)
│   ├── dashboard.html     # Dashboard com stats e gráficos
│   ├── medicamentos.html  # CRUD de medicamentos
│   ├── ubs.html           # CRUD de UBS
│   ├── estoque.html       # CRUD de estoque
│   ├── movimentacoes.html # Registro de entradas/saídas
│   └── relatorios.html    # Relatórios (estoque baixo, vencidos, etc.)
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css      # Estilos globais (paleta SUS, responsivo)
│   └── js/
│       └── app.js         # Helpers JS (API, modal, toast, badges)
└── README.md
```

## Como rodar

1. **Instale as dependências:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure o banco MySQL:**
   ```bash
   cp .env.example .env
   # Edite .env com suas credenciais do MySQL
   ```

3. **Crie o banco no MySQL:**
   ```sql
   CREATE DATABASE saudeap CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

4. **Execute o servidor:**
   ```bash
   python app.py
   ```
   As tabelas são criadas automaticamente. Acesse: http://localhost:5000

## Credenciais de acesso (demo)

```
E-mail: admin@saudeap.gov.br
Senha:  admin123
```

## Endpoints da API

### Públicos
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/ubs` | Lista todas as UBS |
| GET | `/api/consulta?q=paracetamol` | Busca medicamento por nome/princípio ativo |

### UBS
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/ubs/` | Lista todas |
| GET | `/api/ubs/<id>` | Obtém uma UBS |
| POST | `/api/ubs/` | Cria UBS |
| PUT | `/api/ubs/<id>` | Atualiza UBS |
| DELETE | `/api/ubs/<id>` | Remove UBS |

### Medicamentos
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/medicamentos/` | Lista (filtro `?q=`) |
| GET | `/api/medicamentos/<id>` | Obtém um |
| POST | `/api/medicamentos/` | Cria |
| PUT | `/api/medicamentos/<id>` | Atualiza |
| DELETE | `/api/medicamentos/<id>` | Remove |

### Estoque
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/estoques/` | Lista (filtros `?ubs_id=` e `?medicamento_id=`) |
| GET | `/api/estoques/<id>` | Obtém um |
| POST | `/api/estoques/` | Cria |
| PUT | `/api/estoques/<id>` | Atualiza |
| DELETE | `/api/estoques/<id>` | Remove |

### Movimentações
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/movimentacoes/` | Lista (filtro `?tipo=Entrada\|Saída`) |
| POST | `/api/movimentacoes/` | Registra entrada/saída (atualiza estoque) |
| DELETE | `/api/movimentacoes/<id>` | Remove |

## Páginas

| Rota | Descrição |
|------|-----------|
| `/` | Consulta pública de medicamentos |
| `/auth/login` | Tela de login |
| `/dashboard` | Painel administrativo (requer login) |
| `/medicamentos` | CRUD de medicamentos (requer login) |
| `/ubs` | CRUD de UBS (requer login) |
| `/estoque` | CRUD de estoque (requer login) |
| `/movimentacoes` | Movimentações (requer login) |
| `/relatorios` | Relatórios (requer login) |