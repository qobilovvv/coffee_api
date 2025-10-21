# Coffee Shop API — User Management Service

This service implements a complete user management system for the Coffee Shop API.
It includes:

1. User registration with email verification

2. JWT-based authentication (access & refresh tokens)

3. Role-based authorization (User / Admin)

5. Automatic cleanup of unverified users after 2 days (via Celery)

6. Admin panel's endpoints for managing users

Built using FastAPI, SQLAlchemy, PostgreSQL, and Celery, following an asynchronous, modular, production-ready architecture.



## Run the project
1. ```git clone https://github.com/qobilovvv/coffee_api.git```
2. Create .env file
```commandline
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/coffee_db
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_URL=redis://redis:6379/0
```
3. Run with Docker Compose
4. ```docker-compose up --build```