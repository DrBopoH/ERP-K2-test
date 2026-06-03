# ERP K2 — Модуль обліку замовлень

Тестове завдання для K2 ERP. Fullstack-сервіс автоматизації замовлень:
управління клієнтами, товарами та замовленнями з автоматичним розрахунком суми.

![CI](https://github.com/DrBopoH/ERP-K2-test/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.14-blue)
![Vue](https://img.shields.io/badge/vue-3.5-brightgreen)

---

## Стек

| Шар | Технологія |
|-----|-----------|
| Backend | Python 3.14 · Flask 3 · SQLAlchemy 2 · SQLite |
| Frontend | Vue.js 3 · TypeScript · Vite · Bun |
| Prod | Docker · Gunicorn · Nginx (reverse proxy) |
| Якість | Ruff · Pytest · pytest-cov · GitHub Actions CI |

---

## Швидкий старт — Docker (рекомендовано)

```bash
git clone https://github.com/DrBopoH/ERP-K2-test.git
cd ERP-K2-test/source

docker compose up --build
```

Відкрити: [http://localhost](http://localhost)

> Фронтенд і бекенд спілкуються через внутрішню Docker-мережу.
> Назовні відкритий тільки порт **80** (nginx як reverse proxy на `/api`).

---

## Dev-запуск (без Docker)

### Backend

```bash
cd source/backend

cp .env.example .env          # DATABASE_URL можна лишити порожнім — буде SQLite

uv sync                       # встановлення залежностей
uv run python -m app.main     # запуск Flask dev-сервера
```

API доступне на `http://localhost:5000/api`

### Frontend

```bash
cd source/frontend

cp .env.example .env          # VITE_API_URL можна лишити порожнім — буде http://localhost:5000/api

bun install
bun run dev
```

UI доступне на `http://localhost:5173`

> У dev-режимі Vite проксує `/api` на `localhost:5000` — CORS не потрібен.

---

## Команди розробника

### Backend

```bash
cd source/backend

# Тести з покриттям
uv run python -m pytest --cov=app tests/

# Γокриття коду у форматі web-сторінки
uv run python -m pytest --cov=app --cov-report=html tests/

# Тільки юніт або інтеграційні
uv run pytest tests/unit/
uv run pytest tests/integration/

# Лінтер (перевірка)
uv run ruff check .

# Лінтер (автовиправлення)
uv run ruff check . --fix
```

### Frontend

```bash
cd source/frontend

bun run lint        # ESLint + Oxlint
bun run format      # Prettier
bun run type-check  # vue-tsc
bun run build       # production build
```

---

## Структура проекту

```
ERP-K2-test/
├── .github/workflows/ci.yml   # CI: lint → test (backend), build (frontend)
├── README.md                  # ← ви тут
│
└── source/
    ├── docker-compose.yml     # оркестрація сервісів
    │
    ├── backend/
    │   ├── Dockerfile         # python:3.14-slim + uv + gunicorn
    │   ├── pyproject.toml     # залежності, ruff config
    │   ├── app/
    │   │   ├── core/
    │   │   │   └── config.py  # конфігурація БД, app factory config
    │   │   ├── models.py      # ORM: Client, Product, Order, OrderItem
    │   │   ├── routes.py      # REST API endpoints
    │   │   └── main.py        # Flask app factory (create_app)
    │   └── tests/
    │       ├── conftest.py    # pytest fixtures, SQLite :memory:
    │       ├── unit/          # тести моделей (без БД)
    │       └── integration/   # тести HTTP endpoints
    │
    └── frontend/
        ├── Dockerfile         # bun build → nginx:alpine (multi-stage)
        ├── nginx.conf         # SPA routing + /api proxy_pass
        └── app/
            ├── api/index.ts   # всі fetch-запити до бекенду
            ├── components/    # ClientForm, ProductForm, OrderForm, OrderList
            │   └── ui/        # AppInput, AppButton, AppAlert
            ├── pages/         # ClientsPage, ProductsPage, OrdersPage
            ├── router/        # vue-router
            └── types/         # TypeScript інтерфейси
```

---

## API

| Метод | Endpoint | Опис |
|-------|----------|------|
| `POST` | `/api/clients` | Створити клієнта |
| `GET` | `/api/clients` | Список клієнтів |
| `PUT` | `/api/clients/:id` | Оновити клієнта |
| `DELETE` | `/api/clients/:id` | Видалити клієнта |
| `POST` | `/api/products` | Створити товар |
| `GET` | `/api/products` | Список товарів |
| `PUT` | `/api/products/:id` | Оновити товар |
| `DELETE` | `/api/products/:id` | Видалити товар |
| `POST` | `/api/orders` | Створити замовлення |
| `GET` | `/api/clients/:id/orders` | Замовлення клієнта |

### Бізнес-правила

- Замовлення без клієнта → `404`
- Замовлення без товарів → `400`
- `quantity` не ціле або ≤ 0 → `400`
- Сума розраховується автоматично через `Order.total_amount`

---

## Архітектурні рішення

**`price_at_moment` в `OrderItem`**
Ціна фіксується на момент оформлення замовлення незалежно від майбутніх змін каталогу — стандартна практика облікових систем.

**App factory (`create_app`)**
Ізолює контекст Flask, що дозволяє підмінити `DATABASE_URL` на `sqlite:///:memory:` у тестах без жодних side effects на основну БД.

**Nginx як reverse proxy**
Фронт і бек живуть в окремих контейнерах і спілкуються через внутрішню Docker-мережу. Назовні — один порт 80. CORS відсутній by design.

**Multi-stage Docker build (frontend)**
`build-stage` (Bun) компілює Vue → статика. `production-stage` (nginx:alpine) роздає тільки dist. Фінальний образ не містить Node/Bun — мінімальний розмір.

**SQLite → PostgreSQL**
Для переходу на PostgreSQL достатньо змінити `DATABASE_URL` в `.env`. Код не потребує жодних змін — SQLAlchemy абстрагує діалект.

---

## CI/CD

GitHub Actions запускає два pipeline при кожному push у `main`:

```
backend-lint (Ruff) → backend-test (Pytest) 
frontend-ci (Build placeholder)
```

Тести ізольовані: кожен тест отримує чисту БД у пам'яті через pytest fixture.
