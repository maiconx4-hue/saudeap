# SaúdeAP

Sistema web para gerenciamento e consulta de medicamentos das UBS do Estado do Amapá.

## Tecnologias

- Python
- Flask
- SQLAlchemy
- MySQL / PostgreSQL
- HTML, CSS e JavaScript

## Funcionalidades

- Cadastro de UBS
- Cadastro de medicamentos
- Controle de estoque e movimentações
- Dashboard administrativo
- Consulta pública

## Autenticação e implantação

As rotas administrativas e as APIs administrativas exigem um JWT de um usuário
ativo com papel `admin`. As senhas são armazenadas somente como hash; não há
usuário ou senha padrão no código.

1. Copie `.env.example` para `.env` e preencha `SECRET_KEY` e
   `JWT_SECRET_KEY` com valores aleatórios longos. Em produção, mantenha
   `JWT_COOKIE_SECURE=true` e configure essas variáveis no provedor, não em
   arquivos versionados.
2. Configure o banco por `DATABASE_URL` ou pelas variáveis `DB_*`.
3. Ao iniciar a aplicação, a tabela `usuarios` é criada junto às demais. Crie
   o primeiro administrador pelo seed:

   ```powershell
   $env:ADMIN_EMAIL = "admin@exemplo.gov.br"
   $env:ADMIN_PASSWORD = Read-Host "Senha inicial do administrador"
   python seed_admin.py
   ```

O endpoint `POST /auth/token` recebe `email` e `password` em JSON e retorna um
JWT Bearer. O login web em `/auth/login` grava o JWT em cookie HttpOnly. Para
integrações, envie `Authorization: Bearer <access_token>`.





para usar o banco local, remova/comente DATABASE_URL no .env; enquanto ela existir, a aplicação sempre prioriza o PostgreSQL do Render.