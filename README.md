#!/bin/bash

cat > README.md << 'EOF'
# 🏠 ПАРСЕР НЕДВИЖИМОСТИ CIAN

Проект для автоматического сбора данных об объявлениях недвижимости с сайта CIAN.ru.

## 📊 ОСОБЕННОСТИ

- **Двухэтапная архитектура** - сбор ID и детальный парсинг
- **Работа с PostgreSQL** - хранение в структурированной БД
- **Поддержка всех станций метро СПб** - 71 станция
- **Анти-бот защита** - случайные задержки и user-agents
- **Конфигурируемые лимиты** - контроль скорости парсинга

## 🚀 БЫСТРЫЙ СТАРТ

### Установка зависимостей
\`\`\`bash
python install_deps.py
\`\`\`
или
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Настройка базы данных
\`\`\`sql
-- Создайте базу данных в PostgreSQL
CREATE DATABASE cian_parser;
CREATE USER cian_user WITH PASSWORD 'ваш_пароль';
GRANT ALL PRIVILEGES ON DATABASE cian_parser TO cian_user;
\`\`\`

### Настройка конфигурации
Отредактируйте \`config.py\` или создайте \`.env\` файл:
\`\`\`env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cian_parser
DB_USER=postgres
DB_PASSWORD=ваш_пароль
\`\`\`

### Запуск парсера
\`\`\`bash
python cian_parser_28.py
\`\`\`

## 🗂️ СТРУКТУРА ПРОЕКТА
\`\`\`
cian_parser/
├── cian_parser_28.py          # Основной скрипт парсера
├── database.py                # Работа с PostgreSQL
├── config.py                  # Конфигурация подключения
├── create_table.py            # Создание таблиц БД
├── install_deps.py            # Установка зависимостей
├── requirements.txt           # Список зависимостей
├── db_config.json             # Конфигурация БД (шаблон)
├── db_config_fixed.json       # Исправленная конфигурация
├── cian_ids.pkl               # Пример собранных ID
├── README.md                  # Документация
└── .gitignore                 # Исключения Git
\`\`\`

## 🔧 КЛЮЧЕВЫЕ КЛАССЫ

### MetroParser
\`\`\`python
# Парсер станций метро Санкт-Петербурга
metro = MetroParser()
metro.display_metro_stations()  # Показать все станции
\`\`\`

### IDCollector (Этап 1)
\`\`\`python
# Сбор ID объявлений по станциям метро
collector = IDCollector()
ids = collector.run_collection(metros_to_process=["devyatkino", "grazhdanskiy-prospekt"])
\`\`\`

### DetailParser (Этап 2)
\`\`\`python
# Детальный парсинг собранных объявлений
parser = DetailParser()
parser.run_parsing(offers, max_total=1000)
\`\`\`

## 📊 СОБИРАЕМЫЕ ДАННЫЕ
| Поле | Тип | Описание |
|------|-----|----------|
| cian_id | VARCHAR | Уникальный ID объявления |
| price | NUMERIC | Цена в рублях |
| area_total | NUMERIC | Общая площадь (м²) |
| rooms | INTEGER | Количество комнат |
| metro_station | VARCHAR | Ближайшая станция метро |
| metro_time | VARCHAR | Время до метро |
| district | VARCHAR | Район города |
| year_built | INTEGER | Год постройки дома |
| type_building | VARCHAR | Тип дома (кирпичный, панельный) |
| floor_current | VARCHAR | Этаж (формат "X из Y") |

## ⚙️ НАСТРОЙКИ ПАРСИНГА

### Лимиты и задержки
\`\`\`python
# В коде можно настроить:
MAX_PAGES_PER_METRO = 50      # Максимум страниц на станцию
DELAY_BETWEEN_REQUESTS = 2.5  # Задержка между запросами (сек)
MAX_TOTAL_OFFERS = 5000       # Максимум объявлений для парсинга
\`\`\`

### Выбор станций метро
\`\`\`python
# Все станции СПб автоматически
metros = metro_parser.metro_stations

# Или выборочно
selected_metros = ["devyatkino", "nevskiy-prospekt", "moskovskaya"]
\`\`\`

## 🗄️ БАЗА ДАННЫХ

### Структура таблицы
\`\`\`sql
CREATE TABLE cian_offers (
    cian_id VARCHAR(50) PRIMARY KEY,
    url TEXT,
    title TEXT,
    address TEXT,
    price NUMERIC(15,2),
    old_price NUMERIC(15,2),
    area_total NUMERIC(6,2),
    area_living VARCHAR(50),
    area_kitchen VARCHAR(50),
    floor_current VARCHAR(50),
    rooms INTEGER,
    year_built INTEGER,
    district VARCHAR(200),
    metro_station VARCHAR(200),
    metro_time VARCHAR(50),
    type_building VARCHAR(100),
    publication_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_checked TIMESTAMP
);
\`\`\`

## 🚨 РЕШЕНИЕ ПРОБЛЕМ

### Ошибка подключения к БД
\`\`\`python
# Проверьте настройки в config.py
# Убедитесь что PostgreSQL запущен
# Проверьте логин и пароль
\`\`\`

### Ошибка "Element not found"
\`\`\`python
# CIAN изменил структуру сайта
# Обновите CSS-селекторы в DetailParser
\`\`\`

### Блокировка IP
\`\`\`python
# Добавьте задержки между запросами
# Используйте прокси-серверы
# Регулируйте скорость парсинга
\`\`\`

## 📈 СТАТИСТИКА И МОНИТОРИНГ
\`\`\`python
# Проверить статистику базы
python cian_parser_28.py
# Выберите пункт меню: 4. Проверить статистику базы
\`\`\`

## 🔄 РАБОЧИЙ ПРОЦЕСС

### Этап 1 - Сбор ID:
- Запустить сбор по нужным станциям метро
- ID сохраняются в \`cian_ids.pkl\`
- Примерное время: 5-10 минут на станцию

### Этап 2 - Детальный парсинг:
- Загрузить ID из файла
- Парсить детальную информацию
- Сохранять в PostgreSQL
- Примерное время: 3-5 секунд на объявление

### Анализ данных:
- Экспорт из БД в CSV/Excel
- Визуализация в Power BI/Tableau
- Анализ ценовых тенденций

## 📞 ПОДДЕРЖКА

### Частые проблемы:
- **Пустая таблица в БД** - проверьте создание таблиц через \`create_table.py\`
- **Мало объявлений** - увеличьте \`MAX_PAGES_PER_METRO\`

### Для разработчиков:
\`\`\`bash
# Установить для разработки
pip install -e .

# Запустить тесты
python -m pytest tests/

# Проверить стиль кода
flake8 cian_parser/
\`\`\`

## 📄 ЛИЦЕНЗИЯ

Проект распространяется под лицензией MIT. Используйте ответственно.

---
**Автор:** Elvira Dudii  
**Версия:** 1.0  
**Последнее обновление:** 18.12.2025

💡 *Парсер создан для образовательных целей. Соблюдайте правила использования сайта CIAN.*
EOF
