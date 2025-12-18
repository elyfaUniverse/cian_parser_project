
# 🏠 ПАРСЕР НЕДВИЖИМОСТИ CIAN

Проект для автоматического сбора данных об объявлениях недвижимости с сайта CIAN.ru.

## 📊 ОСОБЕННОСТИ

- **Двухэтапная архитектура** - сбор ID и детальный парсинг
- **Работа с PostgreSQL** - хранение в структурированной БД
- **Поддержка всех станций метро СПб** - 71 станция
- **Анти-бот защита** - случайные задержки и user-agents
- **Конфигурируемые лимиты** - контроль скорости парсинга

## 🚀 БЫСТРЫЙ СТАРТ

## Установка зависимостей
\`\`\`bash
python install_deps.py
\`\`\`
или
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Настройка базы данных
\`\`\`sql
-- Создайте базу данных в PostgreSQL
CREATE DATABASE cian_parser;
CREATE USER cian_user WITH PASSWORD 'ваш_пароль';
GRANT ALL PRIVILEGES ON DATABASE cian_parser TO cian_user;
\`\`\`

## Настройка конфигурации
Отредактируйте \`config.py\` или создайте \`.env\` файл:
\`\`\`env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cian_parser
DB_USER=postgres
DB_PASSWORD=ваш_пароль
\`\`\`

## Запуск парсера
\`\`\`bash
python cian_parser_28.py
\`\`\`

## 🗂️ СТРУКТУРА ПРОЕКТА

| Файл | Назначение |
|------|------------|
| \`cian_parser_28.py\` | Основной скрипт парсера |
| \`database.py\` | Работа с PostgreSQL |
| \`config.py\` | Конфигурация подключения |
| \`create_table.py\` | Создание таблиц БД |
| \`install_deps.py\` | Установка зависимостей |
| \`requirements.txt\` | Список зависимостей |
| \`db_config.json\` | Конфигурация БД (шаблон) |
| \`db_config_fixed.json\` | Исправленная конфигурация |
| \`cian_ids.pkl\` | Пример собранных ID |
| \`README.md\` | Документация |
| \`.gitignore\` | Исключения Git |

## 🔧 КЛЮЧЕВЫЕ КЛАССЫ

## MetroParser
\`\`\`python
# Парсер станций метро Санкт-Петербурга
metro = MetroParser()
metro.display_metro_stations()  # Показать все станции
\`\`\`

## IDCollector (Этап 1)
\`\`\`python
## Сбор ID объявлений по станциям метро
collector = IDCollector()
ids = collector.run_collection(metros_to_process=["devyatkino", "grazhdanskiy-prospekt"])
\`\`\`

## DetailParser (Этап 2)
\`\`\`python
## Детальный парсинг собранных объявлений
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

## Лимиты и задержки
\`\`\`python
# В коде можно настроить:
MAX_PAGES_PER_METRO = 50      # Максимум страниц на станцию
DELAY_BETWEEN_REQUESTS = 2.5  # Задержка между запросами (сек)
MAX_TOTAL_OFFERS = 5000       # Максимум объявлений для парсинга
\`\`\`

## Выбор станций метро
\`\`\`python
# Все станции СПб автоматически
metros = metro_parser.metro_stations

# Или выборочно
selected_metros = ["devyatkino", "nevskiy-prospekt", "moskovskaya"]
\`\`\`
## 🗄️ БАЗА ДАННЫХ

### Структура таблицы
| Поле | Тип | Описание |
|------|-----|----------|
| cian_id | VARCHAR(50) | Уникальный ID объявления |
| url | TEXT | Ссылка на объявление |
| title | TEXT | Заголовок объявления |
| address | TEXT | Адрес объекта |
| price | NUMERIC(15,2) | Цена в рублях |
| old_price | NUMERIC(15,2) | Старая цена (если есть скидка) |
| area_total | NUMERIC(6,2) | Общая площадь (м²) |
| area_living | VARCHAR(50) | Жилая площадь |
| area_kitchen | VARCHAR(50) | Площадь кухни |
| floor_current | VARCHAR(50) | Этаж (формат "X из Y") |
| rooms | INTEGER | Количество комнат |
| year_built | INTEGER | Год постройки дома |
| district | VARCHAR(200) | Район города |
| metro_station | VARCHAR(200) | Станция метро |
| metro_time | VARCHAR(50) | Время до метро |
| type_building | VARCHAR(100) | Тип дома |
| publication_date | DATE | Дата публикации |
| is_active | BOOLEAN | Активно ли объявление |
| created_at | TIMESTAMP | Дата создания записи |
| updated_at | TIMESTAMP | Дата обновления |
| last_checked | TIMESTAMP | Дата последней проверки |

## 🚨 РЕШЕНИЕ ПРОБЛЕМ

## Ошибка подключения к БД
\`\`\`python
### Проверьте настройки в config.py
### Убедитесь что PostgreSQL запущен
### Проверьте логин и пароль
\`\`\`

## Ошибка "Element not found"
\`\`\`python
### CIAN изменил структуру сайта
### Обновите CSS-селекторы в DetailParser
\`\`\`

## Блокировка IP
\`\`\`python
### Добавьте задержки между запросами
### Используйте прокси-серверы
### Регулируйте скорость парсинга
\`\`\`

## 📈 СТАТИСТИКА И МОНИТОРИНГ
\`\`\`python
### Проверить статистику базы
python cian_parser_28.py
### Выберите пункт меню: 4. Проверить статистику базы
\`\`\`

## 🔄 РАБОЧИЙ ПРОЦЕСС

## Этап 1 - Сбор ID:
- Запустить сбор по нужным станциям метро
- ID сохраняются в \`cian_ids.pkl\`

## Этап 2 - Детальный парсинг:
- Загрузить ID из файла
- Парсить детальную информацию
- Сохранять в PostgreSQL

## Частые проблемы:
- **Пустая таблица в БД** - проверьте создание таблиц через \`create_table.py\`
- **Мало объявлений** - увеличьте \`MAX_PAGES_PER_METRO\`

## Для разработчиков:
\`\`\`bash
pip install -e .


## 📄 ЛИЦЕНЗИЯ https://github.com/elyfaUniverse/cian_parser_project/blob/main/LICENSE.txt

Проект распространяется под лицензией MIT. Используйте ответственно.

---
**Автор:** Elvira Dudii  
**Версия:** 1.0  
**Последнее обновление:** 18.12.2025

💡 *Парсер создан для образовательных целей. Соблюдайте правила использования сайта CIAN.*
EOF








