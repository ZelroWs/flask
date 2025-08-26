# 🚀 Flask Social Platform

Meu primeiro projeto completo em Flask! Uma plataforma social com sistema de autenticação, posts, comentários e mensagens privadas.

Para acessar é necessário criar um registro!! Caso se sinta desconfortavel em criar um cadastro novo, pode utilizar:<br>
usuário: teste@gmail.com<br>
senha: teste<br>

Acesse o site:  <a href="https://flask-estudo-bernardo.onrender.com/"> Flask Social Platform
                            <img src="app/static/img/Flask.png" alt="responder" width="50px">
                        </a>

## ✨ Funcionalidades

- **🔐 Sistema de Autenticação**
  - Registro e login de usuários
  - Hash de senhas com Bcrypt
  - Sessões de usuário com Flask-Login

- **💬 Sistema de Posts**
  - Criar posts públicos
  - Comentar em posts
  - Todos os posts vinculados ao usuário

- **📧 Mensagens Privadas**
  - Enviar mensagens para outros usuários
  - Sistema de identificação por e-mail
  - Histórico de mensagens pessoal

- **👤 Perfil de Usuário**
  - Todos as ações vinculadas ao usuário
  - Identificação em posts e comentários
  - Dados pessoais protegidos

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask** - Framework web principal
- **Flask-SQLAlchemy** - ORM para banco de dados
- **Flask-Login** - Gerenciamento de sessões
- **Flask-WTF** - Formulários e validações
- **Flask-Migrate** - Migrações do banco de dados
- **Bcrypt** - Criptografia de senhas

### Banco de Dados
- **SQLAlchemy** - ORM principal
- **PostgreSQL** - Banco de dados em produção
- **SQLite** - Banco de dados em desenvolvimento

### Frontend
- **Jinja2** - Templates HTML
- **Bootstrap** - Estilização (se aplicável)
- **WTForms** - Formulários renderizados
