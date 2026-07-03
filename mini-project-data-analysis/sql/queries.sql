-- ============================================================================
-- OqPay Super-App (Трек D) — ключевые SQL-запросы исследования
-- UZCARD Academy · Mini-project: Data analysis · 2026
-- Полная версия с выводами — в notebooks/oqpay_analysis.ipynb
-- ============================================================================

-- 0.1 Все учебные таблицы
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public' AND table_name ~ '^ds_';

-- 0.2 Проверка принадлежности таблиц треку D через JOIN (ключи должны совпадать)
SELECT
  (SELECT count(*) FROM ds_orders)                                        AS orders_total,
  (SELECT count(*) FROM ds_orders o JOIN ds_users_1 u    USING(user_id))  AS join_users,
  (SELECT count(*) FROM ds_orders o JOIN ds_deliveries d USING(order_id)) AS join_deliveries,
  (SELECT count(*) FROM ds_orders o JOIN ds_payments p   USING(order_id)) AS join_payments;

-- ============================================================================
-- H1 (Ибрахимжон Тожибоев): динамика роста — была ли «просадка»?
-- CTE + оконная функция LAG: темп роста месяц к месяцу
-- ============================================================================
WITH monthly AS (
  SELECT date_trunc('month', ordered_ts)::date AS month,
         count(*)                              AS orders,
         sum(total_amount)/1e9                 AS gmv_bln_uzs,
         round(avg(total_amount))              AS avg_check
  FROM ds_orders
  GROUP BY 1
)
SELECT month, orders, gmv_bln_uzs, avg_check,
       round(100.0*(orders - LAG(orders) OVER (ORDER BY month))
             / LAG(orders) OVER (ORDER BY month), 1) AS mom_growth_pct
FROM monthly ORDER BY month;

-- ============================================================================
-- H2 (Ибрахимжон Тожибоев): локализация сбоя доставки
-- ============================================================================
-- 2.1 Тепловая карта: % просрочки город × месяц (JOIN)
SELECT o.city,
       date_trunc('month', d.promised_ts)::date AS month,
       round(100.0*count(*) FILTER (WHERE d.status='late')/count(*), 1) AS late_pct
FROM ds_deliveries d
JOIN ds_orders o USING(order_id)
GROUP BY 1, 2 ORDER BY 1, 2;

-- 2.2 Дневная динамика в Самарканде + скользящее среднее (оконная AVG OVER)
WITH d AS (
  SELECT d.promised_ts::date AS day,
         100.0*count(*) FILTER (WHERE d.status='late')/count(*) AS late_pct
  FROM ds_deliveries d JOIN ds_orders o USING(order_id)
  WHERE o.city = 'Samarkand'
    AND d.promised_ts >= '2025-07-01' AND d.promised_ts < '2025-10-01'
  GROUP BY 1
)
SELECT day, late_pct,
       avg(late_pct) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma7
FROM d ORDER BY day;

-- 2.3 Все ли типы курьеров затронуты (тройной JOIN)
SELECT c.vehicle_type,
       round(100.0*count(*) FILTER (WHERE d.status='late' AND d.promised_ts >= '2025-08-01'
             AND d.promised_ts < '2025-09-01')
           / NULLIF(count(*) FILTER (WHERE d.promised_ts >= '2025-08-01'
             AND d.promised_ts < '2025-09-01'), 0), 1) AS aug_late_pct,
       round(100.0*count(*) FILTER (WHERE d.status='late' AND (d.promised_ts < '2025-08-01'
             OR d.promised_ts >= '2025-09-01'))
           / count(*) FILTER (WHERE d.promised_ts < '2025-08-01'
             OR d.promised_ts >= '2025-09-01'), 1) AS normal_late_pct
FROM ds_deliveries d
JOIN ds_couriers c USING(courier_id)
JOIN ds_orders  o USING(order_id)
WHERE o.city = 'Samarkand' AND c.city = 'Samarkand'
GROUP BY 1;

-- 2.4 Данные для z-теста двух долей (Самарканд: август vs остальное)
SELECT (d.promised_ts >= '2025-08-01' AND d.promised_ts < '2025-09-01') AS is_aug,
       count(*) FILTER (WHERE d.status='late') AS late, count(*) AS total
FROM ds_deliveries d JOIN ds_orders o USING(order_id)
WHERE o.city = 'Samarkand' GROUP BY 1;

-- ============================================================================
-- H3 (Участник 2): жалобы, рейтинги, удержание
-- ============================================================================
-- 3.1 Тикеты по месяцам и причинам
SELECT date_trunc('month', opened_ts)::date AS month, reason, count(*) AS n
FROM ds_support_tickets
WHERE opened_ts < '2026-01-01'
GROUP BY 1, 2 ORDER BY 1;

-- 3.2 Рейтинг: Самарканд vs остальные города
SELECT date_trunc('month', r.review_ts)::date AS month,
       round(avg(r.rating) FILTER (WHERE o.city='Samarkand'), 2)  AS samarkand,
       round(avg(r.rating) FILTER (WHERE o.city<>'Samarkand'), 2) AS other_cities
FROM ds_reviews r JOIN ds_orders o USING(order_id)
GROUP BY 1 ORDER BY 1;

-- 3.3 Повторные заказы за 60 дней: late vs on_time
--     (CTE + DISTINCT ON + коррелированный подзапрос EXISTS)
WITH first_aug AS (
  SELECT DISTINCT ON (o.user_id) o.user_id, o.ordered_ts, d.status
  FROM ds_orders o JOIN ds_deliveries d USING(order_id)
  WHERE o.ordered_ts >= '2025-08-01' AND o.ordered_ts < '2025-09-01'
    AND d.status IN ('late', 'on_time')
  ORDER BY o.user_id, o.ordered_ts
)
SELECT f.status,
       count(*) AS users,
       count(*) FILTER (WHERE EXISTS (
          SELECT 1 FROM ds_orders o2
          WHERE o2.user_id = f.user_id
            AND o2.ordered_ts > f.ordered_ts
            AND o2.ordered_ts <= f.ordered_ts + interval '60 days')) AS repeated
FROM first_aug f GROUP BY 1;

-- ============================================================================
-- H4 (Участник 3): концентрация выручки и платёжные потери
-- ============================================================================
-- 4.1 Выручка по категориям: доля и накопленная доля (SUM OVER, RANK)
WITH cat_rev AS (
  SELECT c.category_name, sum(oi.quantity * oi.unit_price)/1e9 AS revenue_bln
  FROM ds_order_items oi
  JOIN ds_products  p USING(product_id)
  JOIN ds_categories c ON c.category_id = p.category_id
  GROUP BY 1
)
SELECT category_name, revenue_bln,
       round(100*revenue_bln/sum(revenue_bln) OVER (), 1) AS share_pct,
       round(100*sum(revenue_bln) OVER (ORDER BY revenue_bln DESC)
             / sum(revenue_bln) OVER (), 1) AS cum_share_pct,
       RANK() OVER (ORDER BY revenue_bln DESC) AS rnk
FROM cat_rev ORDER BY revenue_bln DESC;

-- 4.2 Доля топ-10% продавцов в выручке (NTILE)
WITH m_rev AS (
  SELECT p.merchant_id, sum(oi.quantity*oi.unit_price) AS rev
  FROM ds_order_items oi JOIN ds_products p USING(product_id)
  GROUP BY 1
), ranked AS (
  SELECT rev, NTILE(10) OVER (ORDER BY rev DESC) AS decile FROM m_rev
)
SELECT round(100.0*sum(rev) FILTER (WHERE decile=1)/sum(rev), 1) AS top10pct_share
FROM ranked;

-- 4.3 Отказы оплат по методам (для χ²-теста)
SELECT method, count(*) AS attempts,
       count(*) FILTER (WHERE status='failed') AS failed,
       round(100.0*count(*) FILTER (WHERE status='failed')/count(*), 1) AS fail_pct
FROM ds_payments GROUP BY 1 ORDER BY attempts DESC;

-- 4.4 Потерянный GMV из-за неоплаченных заказов
SELECT count(*) AS lost_orders, sum(total_amount)/1e9 AS lost_gmv_bln
FROM ds_orders WHERE status = 'payment_failed';

-- 4.5 Воронка приложения
SELECT event_type, count(*) AS n
FROM ds_events
WHERE event_type IN ('view_product','add_to_cart','checkout_start','payment_success')
GROUP BY 1 ORDER BY n DESC;
