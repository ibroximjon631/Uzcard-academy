# 🏦 UZCARD Academy — Foundation Program (3-й поток)

> Полная программа обучения Python, Data Science и ML для специалистов финтех-отрасли.  
> Официальный сайт: [academy-avu.pages.dev/syllabus](https://academy-avu.pages.dev/syllabus)

---

## 🎯 Целевая аудитория

Программа разработана для:
- Аналитиков, работающих с Excel и SQL, которые хотят перейти к Python и ML
- Разработчиков, желающих освоить Data Science в финтех-контексте
- Специалистов, нуждающихся в целостной образовательной траектории — «от первого скрипта до защиты модели»

---

## 👨‍🎓 Профиль выпускникаii

После прохождения блоков 1–3 выпускник будет обладать следующими компетенциями:

- ✅ Уверенно работает в структурированных Python-проектах: модули, `/src`, `/tests`, виртуальные среды, README, pytest
- ✅ Знает основную механику Python: типы, циклы, функции, ООП, файлы, JSON, обработка ошибок
- ✅ Владеет полным Git-workflow: ветки, pull request, разрешение конфликтов, код-ревью
- ✅ Получает данные через REST API: requests, аутентификация (API key, Bearer), pagination, обработка ошибок
- ✅ Готовит и анализирует данные с Pandas + NumPy, проводит первичный EDA
- ✅ Свободно пишет SQL: агрегации, JOIN, подзапросы, CTE, оконные функции; подключается к Postgres из Python
- ✅ Понимает полный цикл ML: постановка задачи → формирование таргета → валидация → метрики → выбор модели
- ✅ Применяет ML в реальных финтех-кейсах: churn, dropper, soft collection, NBO, antifraud, A/B тестирование
- ✅ Использует AI как рабочий инструмент: написание кода, debug, анализ данных, prompt engineering
- ✅ Соблюдает единый стандарт сдачи работ: чистая структура проекта, воспроизводимый репозиторий, защита перед комиссией

---

## 📐 Академическая структура

- **1 академический час** = 45 минут
- **1 занятие** = 2 академических часа (90 минут)
- Каждое занятие завершается проверяемым результатом
- **30%** времени — объяснение материала, **70%** — практика

---

## 🗺️ Структура программы

```
Блоки 1–3 — строго последовательно (каждый следующий опирается на предыдущий)
Блоки 4–5 — расширение программы, проводятся в отдельных циклах
```

---

## 📦 Блок 1. Python + OOP + Defensive Programming + Web/API *(10 занятий)*

| № | Тема занятия |
|---|--------------|
| 1 | Почему бизнес-контекст важнее модели |
| 2 | Python: переменные, типы данных, I/O, арифметика, if/elif/else |
| 3 | Python: циклы и списки — for/while/range, строки, списки, словари, кортежи, множества |
| 4 | Python: функции и коллекции — def, scope, *args/**kwargs, lambda |
| 5 | Повторение занятий 2–4 — быстрый recap по основам Python |
| 6 | ООП часть 1 — классы, атрибуты, методы, основные концепции |
| 7 | ООП часть 2 — наследование, dunder-методы, @property |
| 8 | ООП часть 3 — расширенные темы, паттерны проектирования, практика |
| 9 | Defensive Programming — обработка ошибок, try/except, logging, debugging |
| 10 | Web + API + HTTPS — HTTP/HTTPS, REST, requests, GET/POST, аутентификация, мини-кейс |

---

## 📦 Блок 2. Data Science + SQL + Базы данных + Мини-проект *(13 занятий)*

| № | Тема занятия |
|---|--------------|
| 1 | NumPy: ndarray, dtype, индексация, срезы, broadcasting, axis |
| 2 | Pandas основы: Series/DataFrame, read_csv/to_csv, loc/iloc, фильтрация по маске |
| 3 | Pandas: пустые значения (isna/fillna/dropna), преобразования, groupby, агрегации |
| 4 | Pandas advanced: merge/join/concat, apply/map/lambda |
| 5 | Визуализация и EDA: describe, value_counts, matplotlib, seaborn, матрица корреляций |
| 6 | Основы БД + начальный SQL: реляционная модель, PK/FK, нормализация, ER + SELECT/WHERE/ORDER BY/LIMIT/DISTINCT |
| 7 | SQL: агрегации + JOIN — COUNT/SUM/AVG/GROUP BY/HAVING + INNER/LEFT/RIGHT/FULL JOIN |
| 8 | SQL: подзапросы и CTE (WITH) — inline view, EXISTS, многоуровневые CTE |
| 9 | SQL: оконные функции — ROW_NUMBER/RANK/LAG/LEAD, PARTITION BY, running total, скользящее среднее |
| 10 | PostgreSQL + Python: psycopg2/SQLAlchemy, параметризованные запросы, pd.read_sql, df.to_sql, EXPLAIN |
| 11 | Data Cleaning: дубликаты, inconsistent strings, типы, форматы дат, скрытые пробелы, выбросы (IQR, z-score) |
| 12 | ETL и воспроизводимый анализ: Extract/Transform/Load, структура проекта, config.yaml, идемпотентность |
| 13 | Защита мини-проекта + ретроспектива блока |

---

## 📦 Блок 3. Прикладной ML + Индустриальные кейсы + AI + Карьера *(22 занятия)*

| № | Тема занятия |
|---|--------------|
| 1 | Статистика для DS: распределения, mean vs median, корреляция, p-value, доверительные интервалы |
| 2 | Prompt Engineering: структура промпта, few-shot, chain-of-thought, AI как инструмент DS |
| 3 | Аналитический EDA — методология: ограничение первого взгляда, аномалии, сегментный анализ, гипотезы |
| 4 | Feature Engineering: LabelEncoder, OneHot, scaling, бакетизация, фичи из дат, data leakage |
| 5 | Основы ML: train/test split, логистическая регрессия, дерево решений, confusion matrix, baseline |
| 6 | Стратегии валидации: переобучение, k-fold, time-based split, OOT-валидация |
| 7 | Метрики и выбор модели: ROC-AUC, PR-AUC, gain/lift, KS, expected value, выбор порога |
| 8 | Дизайн целевой переменной: observation point, performance period, label leakage, стабильность таргета |
| 9 | Источники данных и сэмплирование: репрезентативность, sampling bias, population drift, стратифицированная выборка |
| 10 | End-to-end ML pipeline: жизненный цикл, роли в команде, experiment tracking, model card |
| 11 | Imbalanced learning: undersampling, SMOTE, class weights, threshold tuning, stratified k-fold |
| 12 | Модель churn: RFM-фичи, logreg, LightGBM, ROC-AUC, gain chart, топ-N рискованных клиентов |
| 13 | Модель dropper: воронкообразный анализ, фичи из onboarding-шагов, feature importance, рекомендации продукта |
| 14 | Soft Collection: скоринг задержки, DPD-таргет, KS/Lift, приоритизация портфеля, recovery rate |
| 15 | NBO — Next Best Offer: collaborative filtering, rule-based baseline, precision@k, маркетинговая логика |
| 16 | Antifraud: velocity-фичи, поведенческие отклонения, дисбаланс 99:1, PR-AUC, матрица стоимостей |
| 17 | A/B тестирование: дизайн эксперимента, t-test, power analysis, p-value, ошибки I и II рода |
| 18 | Гиперпараметрическая настройка: Grid Search, Random Search, Optuna, nested cross-validation, early stopping |
| 19 | Deploy, мониторинг и Feature Store: batch/online inference, data drift, PSI, model drift, training-serving skew |
| 20 | Обзор AI-продуктов в индустрии: LLM, RAG, Speech Analytics, OCR — разработка и применение в финтехе |
| 21 | CV + карьера: сильное CV для DS/финтех, GitHub-портфолио, LinkedIn, подготовка к интервью |
| 22 | Защита финального проекта + ретроспектива программы |

---

## 📦 Блок 4. Информационная безопасность *(15 занятий)*

Расширение программы для специалистов с инженерной базой. Контекст ИБ. Проводится в отдельном цикле.

---

## 📦 Блок 5. Внутренние лекции UZCARD *(6 занятий)*

Экспертиза предметной области от внутренних специалистов UZCARD. Проводится в отдельном цикле.

---

## 📁 Содержимое репозитория

| Файл | Описание |
|------|----------|
| `main.py` | Решения и ответы на тесты — блок 1, занятия 4–13 |
| `week01_python_basics.ipynb` | Домашнее задание 1: аналитика транзакций (6 функций) |
| `week02_uzcard_currency_service.ipynb` | Домашнее задание 2: сервис курсов валют (классы + API) |
| `UZCARD Academy.pdf` | Полная программа курса |

---

*UZCARD ACADEMY · FOUNDATION PROGRAM · 3-й поток*
