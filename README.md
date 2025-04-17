# agent 1312 (Фб_ЕБЫРЬ)



## 📖 Описание проекта

**agent 1312 (Фб_ЕБЫРЬ)** — это комплексная система автоматизации регистрации, прогрева и запуска рекламных кампаний на Facebook Ads с использованием техники "первобил" и мощного оркестратора LMNR. Проект сочетает:

- Автоматическую **регистрацию** аккаунтов (TempMail, HelperSMS, Tor).
- **Прогрев** активности: имитация реального поведения пользователя.
- Глубокую **классификацию KYC** и фильтрацию.
- Запуск **первобил** (микробюджет + проверка на бесплатные показы).
- Старт **основных Bulk-кампаний**.
- **Мониторинг**, **метрики** и **визуализацию** состояния пула аккаунтов.

Проект построен модульно, легко масштабируется и интегрируется с внешними сервисами (Oxylabs, Prometheus, Grafana).

---

## 🚀 Ключевые функции

1. **End-to-end pipeline** управления через LMNR (LiquidMind Neural Runtime).
2. **Авто-регистрация** аккаунтов:
   - TempMail для email-подтверждения.
   - HelperSMS для приема SMS.
   - Tor для получения разных IP.
3. **Прогрев аккаунтов** мелкими шагами:
   - Переходы, лайки, вступления в группы, заходы в Ads Manager.
4. **Гранулярная KYC-классификация**:
   - Проверка личности, компании, платежей, правил рекламы.
5. **Первобил**:
   - Запуск тестовой кампании с минимальным бюджетом.
   - Автоматическая проверка списания.
6. **Основная Bulk-кампания** по шаблону.
7. **Централизованная конфигурация** через Dynaconf (`settings.toml`, `.env`).
8. **Асинхронная архитектура** с aiohttp, asyncio, Circuit Breaker.
9. **Промышленное логирование** (structlog, JSON) и мониторинг (Prometheus).
10. **Визуализация пула** аккаунтов через NetworkX и Matplotlib.

---

## 📦 Установка и быстрая настройка

> Инструкция для новичков: следуйте шагам один за другим, чтобы запустить проект локально.

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-org/facebook-pervobil-ideal.git
cd facebook-pervobil-ideal
```

### 2. Подготовка окружения

1. Установите Python 3.10+ и [Node.js (для LMNR)](https://nodejs.org/).

2. Создайте виртуальное окружение и активируйте его:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .\.venv\Scripts\activate  # Windows
   ```

3. Установите зависимости Python:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. (Опционально) Установите зависимости Node и LMNR CLI:

   ```bash
   npm install -g lmnr-cli
   ```

### 3. Настройка конфигураций

1. Скопируйте пример конфигов:
   ```bash
   cp settings.toml.example settings.toml
   cp .env.example .env
   ```
2. Откройте `settings.toml` и `.env`, внесите свои ключи:
   - `helper_sms_key`, `oxylabs_api_key`, `password_manager_key`.
   - Строку подключения `db_dsn` к вашей СУБД PostgreSQL.
3. Опционально включите Tor в `settings.toml`: `use_tor = true`.

### 4. Подготовка и запуск сервисов через Docker Compose

```bash
docker-compose up -d
```

Это запустит:

- PostgreSQL (порт 5432)
- Prometheus (порт 9090)
- Grafana (порт 3000)

### 5. Применение миграций (PostgreSQL)

```bash
alembic upgrade head
```

### 6. Запуск LMNR pipeline

```bash
lmnr run facebook_pervobil_ideal --config settings.toml
```

---

## 🔍 Структура проекта

```
facebook-pervobil-ideal/
├── settings.toml           # Dynaconf config
├── .env                    # Секреты
├── lmnr_pipeline.yaml      # Оркестрация
├── modules/                # Исходники модулей
│   ├── config_loader.py    # Dynaconf
│   ├── logger.py           # structlog
│   ├── db.py               # asyncpg
│   ├── circuit_breaker.py  # CircuitBreaker
│   ├── proxy_manager_async.py
│   ├── proxy_api_client.py
│   ├── tempmail_async.py
│   ├── sms_activator_async.py
│   ├── tor_manager.py
│   ├── password_manager.py
│   ├── account_creator.py
│   ├── account_warmer.py
│   ├── account_classifier.py
│   ├── playwright_worker.py
│   ├── ad_manager.py
│   ├── error_handler.py
│   ├── monitoring.py       # Prometheus metrics
│   └── account_visualizer.py
├── tests/                  # Unit/Integration/E2E тесты
├── assets/                 # Логотипы, графика
├── docker-compose.yml
├── requirements.txt
├── package.json            # для LMNR CLI
├── Alembic/                # миграции БД
├── README.md               # Этот файл
└── LICENSE
```

---

## ⚙️ Подробная инструкция по использованию

### Инициализация базы данных

```bash
alembic init Alembic
# настройте alembic.ini на вашу БД
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### Конфигурация LMNR

- `lmnr_pipeline.yaml` описывает узлы и шаги.
- В `settings.toml` задаются параметры, используемые во всех модулях.

### Логирование и мониторинг

- Логи пишутся в STDOUT в формате JSON, уровня INFO и выше.
- Метрики доступны по `http://localhost:8000/metrics` для Prometheus.
- Grafana-дашборд подключается к Prometheus на `http://localhost:3000`.

### Тестирование

#### Unit-тесты

```bash
pytest tests/unit --maxfail=1 --disable-warnings -q
```

#### Integration-тесты

```bash
pytest tests/integration --maxfail=1 --disable-warnings -q
```

#### E2E-тесты

```bash
pytest tests/e2e --maxfail=1 --disable-warnings -q
```

---

## 🛠 Техническая информация и детали реализации

### 1. Конфигурация (Dynaconf)

Используется `Dynaconf` для единого доступа:

```python
from modules.config_loader import settings
print(settings.db_dsn)
print(settings.helper_sms_key)
```

Можно переопределить через переменные окружения или CLI-параметр `--settings-file`.

### 2. Circuit Breaker (aiobreaker)

Применён к всем внешним HTTP-вызовам:

```python
from modules.circuit_breaker import circuit

@circuit()
async def fetch_proxy(...): ...
```

Параметры: `fail_max=5, reset_timeout=60`, можно поменять в `circuit_breaker.py`.

### 3. Асинхронные модули

- `tempmail_async.py` и `sms_activator_async.py` на `aiohttp` + `asyncio` для неблокирующих операций.
- В `playwright_worker.py` используется `playwright.async_api`.

### 4. Прогрев и KYC

Процедуры разбиты:

- **Прогрев**: `visit_home`, `like_posts`, `join_groups`, `visit_ads_manager`.
- **KYC**: `check_identity`, `check_business`, `check_payment`, `check_policies`.

Это позволяет легко добавлять новые шаги в `lmnr_pipeline.yaml`.

### 5. Визуализация

Используется `networkx` для построения графа и `matplotlib`:

```python
from modules.account_visualizer import visualize
await visualize('graph.png')
```

### 6. Безопасность паролей

`password_manager.py` шифрует логины и пароли с `Fernet`:

```python
from modules.password_manager import encrypt_password, decrypt_password
enc = encrypt_password("mypassword")
assert decrypt_password(enc) == "mypassword"
```

### 7. СУБД и таблицы

- `accounts` (login, password\_enc, phone, session, kyc\_status)
- `proxies` (proxy\_url, status, last\_checked)
- `results` (login, kyc\_status, test\_success, firstbill\_amount, campaign\_id)

SQLAlchemy/asyncpg через `modules/db.py`.

### 8. Docker Compose

```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: fbuser
      POSTGRES_PASSWORD: fbpass
      POSTGRES_DB: facebook
    ports:
      - 5432:5432
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - 9090:9090
  grafana:
    image: grafana/grafana
    ports:
      - 3000:3000
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=secret
```

### 9. CI/CD и тестирование

- Используйте GitHub Actions или GitLab CI.
- Пример workflow:
  - Проверка стилей (`flake8`, `mypy`).
  - Unit/Integration/E2E тесты.
  - Сбор артефактов.

```yaml
# .github/workflows/ci.yml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - run: pip install -r requirements.txt
    - run: flake8 .
    - run: mypy .
    - run: pytest -q
```

### 10. Масштабирование и Production

- Запускайте worker-ноды по LMNR на нескольких серверах.
- Используйте Kubernetes + Helm Chart.
- Мониторьте CPU/RAM, прокси latency, скорость регистрации.

---

## 📝 Лицензия

Проект распространяется под лицензией MIT. См. файл `LICENSE` для деталей.

---

**Готовы к старту?**\
Следуйте простым шагам выше, и через несколько минут вы получите пул прогретых Facebook-аккаунтов с успешным "первобил" и запущенными кампаниями!

**Удачи и ответственной автоматизации!**

