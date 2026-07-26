# Football School Management System

Система управления футбольной школой: учёт игроков 9–10 лет, расписание тренировок, отметка посещаемости, генерация отчётов.

Построена по принципам **Clean Architecture** — бизнес-логика полностью изолирована от фреймворков, базы данных и внешних сервисов, что позволяет менять технические детали (БД, API-фреймворк, очереди задач), не трогая ядро приложения.

---

## Содержание

- [Архитектура](#архитектура)
- [Стек технологий](#стек-технологий)
- [Структура проекта](#структура-проекта)
- [Запуск проекта](#запуск-проекта)
- [Примеры сценариев использования](#примеры-сценариев-использования)
- [Тестирование](#тестирование)
- [Roadmap](#roadmap)

---

## Архитектура

Проект разделён на 4 независимых слоя. Зависимости всегда направлены **внутрь**, к Domain — внешние слои знают о внутренних, но не наоборот.

```mermaid
graph TD
    subgraph Presentation["Presentation — FastAPI + React"]
        API[FastAPI эндпоинты]
        Schemas[Pydantic-схемы]
    end

    subgraph Application["Application — сценарии использования"]
        UC1[CreateTrainingUseCase]
        UC2[MarkAttendanceUseCase]
        UC3[CreatePlayerUseCase]
        Interfaces[Repository-интерфейсы / Protocol]
    end

    subgraph Domain["Domain — бизнес-правила"]
        Entities[Сущности: Player, Training, Attendance, Report]
        Rules[Правила: overlaps_with, is_eligible_age]
    end

    subgraph Infrastructure["Infrastructure — БД, очереди"]
        Repos[SQLAlchemy-репозитории]
        DB[(PostgreSQL)]
        Queue[Celery / RQ]
    end

    API --> UC1
    API --> UC2
    API --> UC3
    UC1 --> Rules
    UC2 --> Rules
    UC3 --> Rules
    UC1 --> Interfaces
    UC2 --> Interfaces
    UC3 --> Interfaces
    Interfaces -.реализует.-> Repos
    Repos --> DB
    Entities --> Rules

    style Domain fill:#e8f5e9,stroke:#2e7d32
    style Application fill:#e3f2fd,stroke:#1565c0
    style Infrastructure fill:#fff3e0,stroke:#e65100
    style Presentation fill:#f3e5f5,stroke:#6a1b9a
```

### Слои и их ответственность

| Слой | Ответственность | Зависит от |
|---|---|---|
| **Domain** | Сущности и бизнес-правила (пересечение тренировок, возрастной ценз 9–10 лет) | Ничего внешнего (только стандартная библиотека Python) |
| **Application** | Сценарии использования (use cases), дирижирующие Domain и репозиториями через Dependency Injection | Domain |
| **Infrastructure** | Конкретные реализации: PostgreSQL через SQLAlchemy, Alembic-миграции, очереди задач | Application (реализует его интерфейсы) |
| **Presentation** | FastAPI-эндпоинты, Pydantic-схемы валидации запросов, React-фронтенд | Application |

### Ключевой принцип: Dependency Inversion

Application определяет **интерфейсы** репозиториев через `Protocol` (например, `TrainingRepository`), не зная, что репозиторий работает с PostgreSQL. Infrastructure **реализует** эти интерфейсы (`SqlAlchemyTrainingRepository`). Это позволяет:
- тестировать Application-логику с фейковыми репозиториями в памяти, без реальной БД;
- заменить PostgreSQL на другую СУБД, не меняя ни строчки в Domain/Application.

### Поток данных для одного запроса

```mermaid
sequenceDiagram
    participant Client as Клиент (React / Swagger)
    participant API as FastAPI эндпоинт
    participant UC as Use Case
    participant Domain as Domain-правило
    participant Repo as Repository
    participant DB as PostgreSQL

    Client->>API: POST /trainings (JSON)
    API->>API: Валидация через Pydantic
    API->>UC: execute(training_date, start_time, ...)
    UC->>Repo: get_by_date_range(...)
    Repo->>DB: SELECT * FROM trainings WHERE date = ...
    DB-->>Repo: существующие тренировки
    Repo-->>UC: list[Training]
    UC->>Domain: has_overlap(candidate, existing)
    Domain-->>UC: True / False
    alt Пересечение найдено
        UC-->>API: raise TrainingOverlapError
        API-->>Client: 409 Conflict
    else Всё ок
        UC->>Repo: save(candidate)
        Repo->>DB: INSERT INTO trainings ...
        DB-->>Repo: сохранённая строка с id
        Repo-->>UC: Training
        UC-->>API: Training
        API-->>Client: 201 Created
    end
```

---

## Стек технологий

| Категория | Технология |
|---|---|
| Backend | Python 3.12, FastAPI |
| Валидация | Pydantic v2 |
| База данных | PostgreSQL 16 |
| ORM / миграции | SQLAlchemy 2.0, Alembic |
| Асинхронные задачи | Celery / RQ *(в разработке)* |
| Frontend | React + TypeScript *(в разработке)* |
| Тестирование | pytest |
| Контейнеризация | Docker, docker-compose |

---

## Структура проекта

```
TrainingControl/
├── domain/                # Бизнес-правила — не зависит ни от чего внешнего
│   ├── entities/           # Player, Training, Attendance, Report
│   ├── rules/              # overlaps_with, is_eligible_age
│   └── exceptions.py
│
├── application/            # Сценарии использования
│   ├── interfaces/         # Repository-контракты (Protocol)
│   ├── use_cases/          # CreateTraining, MarkAttendance, CreatePlayer
│   └── dto/                # Данные между Presentation и Application
│
├── infrastructure/          # Технические реализации
│   ├── db/
│   │   ├── models.py        # SQLAlchemy ORM-модели
│   │   ├── session.py        # Подключение к БД
│   │   └── repositories/      # Реализации репозиториев
│   ├── migrations/            # Alembic
│   └── queue/                 # Celery/RQ задачи (отчёты)
│
├── presentation/
│   ├── api/
│   │   ├── main.py             # Точка входа FastAPI
│   │   ├── schemas/             # Pydantic request/response модели
│   │   ├── routers/              # players, trainings, attendance
│   │   └── dependencies.py        # DI-провайдеры
│   └── frontend/                   # React + TS (в разработке)
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── .env                             # Не коммитится, см. .env.example
```

---

## Запуск проекта

### Требования

- Docker и Docker Compose
- Python 3.12 (для локальной разработки/миграций вне контейнера)

### 1. Клонировать репозиторий и настроить окружение

```bash
git clone <repo-url>
cd TrainingControl
```

Создать файл `.env` в корне проекта:

```
POSTGRES_PASSWORD=secretpassword123
DATABASE_URL=postgresql://postgres:secretpassword123@localhost:5432/training_control
```

> `DATABASE_URL` использует `localhost` — эта переменная нужна для локального запуска Alembic-миграций.
> Внутри `docker-compose.yml` для сервиса `api` эта переменная переопределяется на `db` (имя сервиса в Docker-сети).

### 2. Поднять всё через Docker Compose

```bash
docker-compose up --build
```

Это поднимет два контейнера:
- `db` — PostgreSQL 16 на порту `5432`
- `api` — FastAPI-приложение на порту `8000`

### 3. Применить миграции (если ещё не применены)

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows
# source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
alembic upgrade head
```

### 4. Проверить, что всё работает

Открыть в браузере: **http://localhost:8000/docs** — интерактивная Swagger-документация API.

---

## Примеры сценариев использования

### Создать игрока

```http
POST /players/
Content-Type: application/json

{
  "first_name": "Иван",
  "last_name": "Петров",
  "birth_date": "2016-08-10",
  "position": "forward",
  "season_start_date": "2026-09-01"
}
```

Если возраст игрока на `season_start_date` не входит в диапазон 9–10 лет — вернётся `422` с пояснением.

### Создать тренировку

```http
POST /trainings/
Content-Type: application/json

{
  "date": "2026-08-01",
  "start_time": "18:00:00",
  "end_time": "19:00:00",
  "location": "Стадион Динамо"
}
```

Если тренировка пересекается по времени с уже существующей на ту же дату — вернётся `409 Conflict`.

### Отметить посещаемость группы игроков на тренировке

```http
POST /trainings/{training_id}/attendance
Content-Type: application/json

{
  "items": [
    { "player_id": 1, "status": "present" },
    { "player_id": 2, "status": "absent" },
    { "player_id": 3, "status": "late" }
  ]
}
```

Все записи сохраняются **атомарно** — в одной транзакции: либо сохраняются все, либо (при ошибке хотя бы одной записи) не сохраняется ни одна.

---

## Тестирование

```bash
pytest -v
```

Тесты разделены на два вида:
- **Unit-тесты** (`domain/tests/`, `application/tests/`) — быстрые, используют фейковые репозитории в памяти, не требуют БД.
- **Интеграционные тесты** (`infrastructure/tests/`) — работают с реальной PostgreSQL, требуют запущенный `docker-compose up -d db`.

---

## Roadmap

- [x] Domain: сущности и бизнес-правила
- [x] Application: use cases с Dependency Injection
- [x] Infrastructure: PostgreSQL, Alembic, репозитории
- [x] Presentation: FastAPI-эндпоинты (players, trainings, attendance)
- [x] Контейнеризация (Docker + docker-compose)
- [ ] Report: генерация отчётов через Celery/RQ
- [ ] Нечёткая логика: рекомендации по нагрузке (зелёная/жёлтая/красная зона)
- [ ] ML-прогноз посещаемости
- [ ] React-фронтенд
- [ ] CI/CD (GitHub Actions) и деплой