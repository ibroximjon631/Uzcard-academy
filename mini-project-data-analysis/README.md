# OqPay Super-App — Mini-project: Data Analysis (Трек D)

**UZCARD Academy · 2026** · Команда: Ибрахимжон Тожибоев, Участник 2, Участник 3

## 🇷🇺 О проекте

Заказчик (руководство OqPay Super-App) зафиксировал «просадку заказов и рост жалоб»,
но не нашёл причину. Мы разобрали 12 таблиц трека D (~1,4 млн строк) и установили:

- **«Просадки» бизнеса нет** — заказы растут +6,0 %/мес (R² = 0,99); декабрьское
  снижение — возврат к тренду после сезонного пика ноября (+23 % MoM).
- **Корневая причина жалоб** — логистический сбой в **Самарканде, 01–31.08.2025**:
  93,5 % доставок просрочено против нормы 8,2 % (z = 72,5, p < 0,001), все типы
  курьеров → сбой системный (хаб/диспетчеризация/подрядчик).
- **Последствия:** тикеты +73 % (весь прирост — late_delivery), рейтинг города
  4,2 → 2,76 (Манна–Уитни p < 0,001). Оттока нет: повторные покупки 68,6 % vs
  67,4 % (p = 0,47) — окно для удержания открыто.
- **Фоновые риски:** Installment отказывает в 10,3 % оплат (2× хуже карт, χ²
  p < 0,001, ≈0,85 млрд UZS потерянного GMV); Smartphones = 40 % выручки,
  топ-10 % продавцов = 49,5 % (HHI = 2133).

Рекомендации заказчику — 5 мер: разбор инцидента + SLA, алерты по городам
(правило «5 п.п. / 3 дня»), промо для 940 задетых пользователей, аудит шлюза
рассрочки, диверсификация выручки.

## 🇺🇿 Loyiha haqida

Buyurtmachi (OqPay rahbariyati) «buyurtmalar pasayishi va shikoyatlar o'sishini»
qayd etgan, lekin sababini topa olmagan. Biz D trekning 12 ta jadvalini (~1,4 mln
qator) tahlil qilib aniqladik:

- **Biznes pasayishi yo'q** — buyurtmalar oyiga +6,0 % o'sadi; dekabrdagi kamayish —
  noyabr mavsumiy cho'qqisidan keyin trendga qaytish.
- **Ildiz sabab** — **Samarqand, 2025-yil 1–31 avgust** logistika inqirozi: yetkazmalarning
  93,5 % i kechikkan (norma 8,2 %, p < 0,001), barcha kuryer turlari — sabab tizimli.
- **Oqibatlar:** tiketlar +73 %, shahar reytingi 4,2 → 2,76; mijozlar oqib ketmagan
  (p = 0,47) — ushlab qolish imkoniyati hali bor.
- **Fon risklari:** Installment to'lovlarining 10,3 % i rad etiladi (kartalardan 2×
  yomon); daromad kuchli konsentratsiyalangan (HHI = 2133).

## Структура репозитория

```
notebooks/oqpay_analysis.ipynb      — основной notebook (4 гипотезы, SQL+Python+стат.тесты)
presentation/OqPay_TrackD.pptx      — презентация для защиты (RU, 7 слайдов)
presentation/OqPay_TrackD_UZ.pptx   — prezentatsiya (UZ, 7 slayd)
charts/*.png · charts_uz/*.png      — 11 графиков (RU и UZ версии)
scripts/make_charts_uz.py           — генератор UZ-графиков
sql/queries.sql                     — ключевые SQL-запросы отдельным файлом
docs/SPEECH_RU.md · SPEECH_UZ.md    — сценарий защиты на 4 минуты + Q&A
docs/SPEECH_FULL_RU.md · _UZ.md     — полная версия на 10–15 минут + словарь терминов
docs/HISOBOT_UZ.md                  — to'liq tushuntirish hisoboti (nima/qanday/nega)
docs/CHECKLIST.md                   — что сделать до защиты (RU/UZ)
alt-tracks/                         — ЗАПАСНЫЕ ТРЕКИ (полностью готовые):
  track-A-uzcardxl/                 — A: процессинг (notebook + pptx + speech)
  track-B-walletapp/                — B: кошелёк с подпиской (notebook + pptx + speech)
  track-C-merchanthub/              — C: эквайринг (notebook + pptx + speech)
```

> Команда защищает **один** трек. Основной и самый проработанный — **D** (корень
> репозитория). A/B/C подготовлены как запасные варианты выбора.

## Как запустить

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp db_config.example.py db_config.py   # впишите свой логин/пароль академии
jupyter notebook notebooks/oqpay_analysis.ipynb   # Kernel → Restart & Run All
```

Доступы к учебной БД (host `thomas.proxy.rlwy.net:51432`, база `academy_db`) хранятся
в `db_config.py` — файл в `.gitignore` и **не попадает в публичный репозиторий**.
Notebooks уже выполнены: все результаты и графики видны без запуска.

## Требования проекта — где что выполнено

| Требование | Раздел |
|---|---|
| JOIN | H2–H4 (до 5 таблиц в запросе) |
| GROUP BY | все гипотезы |
| CTE / подзапрос | `WITH` в H1–H4, коррелированный `EXISTS` в H3 |
| Оконные функции | `LAG` (H1), `AVG OVER` (H2), `SUM OVER`, `RANK`, `NTILE` (H4) |
| ≥2 графика на гипотезу | H1: 2, H2: 3, H3: 3, H4: 3 |
| Стат. метод у каждого участника (трек D) | H1: тренд + 95% ДИ · H2: z-тест долей · H3: Манна–Уитни + z-тест · H4: χ² + HHI |
| Без ML | только SQL, pandas, matplotlib, scipy.stats |
