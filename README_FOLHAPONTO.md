# Sistema de Folha de Ponto

Sistema completo para controle de horas trabalhadas e cálculo de salários.

## Funcionalidades

- ✅ Autenticação JWT (login/cadastro)
- ✅ Perfil de usuário com valor/hora
- ✅ Registro de ponto (até 3 períodos por dia)
- ✅ Códigos de trabalho/projeto
- ✅ Dashboard com insights
- ✅ Sistema de aprovação (supervisor)
- ✅ Cálculo automático de salários
- ✅ Interface admin completa

## Tecnologias

- Django 4.2.7
- Django REST Framework
- JWT Authentication
- SQLite (desenvolvimento)

## Instalação

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Executar migrações:
```bash
python manage.py migrate
```

3. Criar superusuário:
```bash
python manage.py createsuperuser
```

4. Iniciar servidor:
```bash
python manage.py runserver
```

## Endpoints da API

### Autenticação
- `POST /api/accounts/register/` - Cadastro
- `POST /api/accounts/login/` - Login
- `POST /api/accounts/token/refresh/` - Renovar token
- `GET /api/accounts/profile/` - Ver perfil
- `PUT /api/accounts/profile/update/` - Atualizar perfil

### Controle de Ponto
- `GET /api/timetrack/work-codes/` - Listar códigos de trabalho
- `GET /api/timetrack/time-records/` - Listar registros
- `POST /api/timetrack/time-records/` - Criar registro
- `GET /api/timetrack/time-records/{id}/` - Detalhes do registro
- `PUT /api/timetrack/time-records/{id}/` - Atualizar registro
- `DELETE /api/timetrack/time-records/{id}/` - Excluir registro

### Dashboard e Relatórios
- `GET /api/timetrack/dashboard/` - Dashboard principal
- `GET /api/timetrack/salaries/` - Histórico de salários
- `GET /api/timetrack/relatorio/{ano}/{mes}/` - Relatório mensal

## Exemplos de Uso

### Cadastro
```json
POST /api/accounts/register/
{
    "username": "joao.silva",
    "email": "joao@empresa.com",
    "first_name": "João",
    "last_name": "Silva",
    "password": "senha123",
    "password_confirm": "senha123",
    "valor_hora": "25.50"
}
```

### Login
```json
POST /api/accounts/login/
{
    "username": "joao.silva",
    "password": "senha123"
}
```

### Registrar Ponto
```json
POST /api/timetrack/time-records/
{
    "data": "2025-01-15",
    "entrada1": "08:00",
    "saida1": "12:00",
    "entrada2": "13:00",
    "saida2": "17:00",
    "work_code": 1,
    "observacoes": "Trabalho no projeto X"
}
```

## Acesso Admin

- URL: http://localhost:8000/admin/
- Gerencie usuários, perfis, códigos de trabalho e registros de ponto

## Frontend React

O frontend está na pasta `frontend/` e possui as seguintes páginas:

- **Login/Cadastro** - Autenticação de usuários
- **Dashboard** - Visão geral com estatísticas do mês
- **Registrar Ponto** - Interface para marcar entrada/saída (até 3 períodos)
- **Histórico** - Visualizar registros de ponto por mês/ano
- **Perfil** - Editar informações pessoais e valor/hora

### Como executar o frontend:

```bash
cd frontend
npm start
```

Frontend rodará em: http://localhost:3000

### Como executar o backend:

```bash
python manage.py runserver
```

Backend rodará em: http://localhost:8000

## Sistema Completo Implementado

✅ **Backend Django** com APIs REST completas
✅ **Frontend React** com todas as páginas funcionais  
✅ **Autenticação JWT** entre frontend e backend
✅ **Interface responsiva** com Tailwind CSS
✅ **Validações** de horários e dados
✅ **Dashboard** com insights e estatísticas
✅ **Sistema completo** pronto para uso!