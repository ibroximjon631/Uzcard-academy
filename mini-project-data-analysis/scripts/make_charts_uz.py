#!/usr/bin/env python3
"""O'zbekcha grafiklar (charts_uz/) — asosiy notebook grafiklarining UZ versiyasi.
Ishga tushirish: python scripts/make_charts_uz.py (loyiha ildizidan)."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats
from sqlalchemy import create_engine
import os

import sys, pathlib
_p = pathlib.Path(__file__).resolve().parent
while not (_p/"db_config.py").exists() and _p != _p.parent: _p = _p.parent
sys.path.insert(0, str(_p))
from db_config import DB_URL
ENGINE = create_engine(DB_URL)
def q(sql): return pd.read_sql(sql, ENGINE)

BLUE, AQUA, YELLOW, GREEN = "#2a78d6", "#1baf7a", "#eda100", "#008300"
CRITICAL, INK, INK2, MUTED, GRID, SURFACE = "#d03b3b", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
SEQ = LinearSegmentedColormap.from_list("seq_blue",
    ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"])
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "figure.dpi": 110,
    "axes.edgecolor": "#c3c2b7", "axes.linewidth": 0.8, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.7, "axes.axisbelow": True,
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "font.family": "sans-serif", "axes.titlesize": 12, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
})
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "charts_uz")
os.makedirs(OUT, exist_ok=True)
def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("saved", name)

OYLAR = ["Yan","Fev","Mar","Apr","May","Iyn","Iyl","Avg","Sen","Okt","Noy","Dek"]
def oy_fmt(ax):
    ax.xaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(
        lambda x, _: OYLAR[mdates.num2date(x).month-1]))

# ---------------- H1
mom = q("""
WITH monthly AS (
  SELECT date_trunc('month', ordered_ts)::date AS month, count(*) AS orders,
         round(avg(total_amount)) AS avg_check
  FROM ds_orders GROUP BY 1)
SELECT month, orders, avg_check,
       round(100.0*(orders - LAG(orders) OVER (ORDER BY month))/LAG(orders) OVER (ORDER BY month),1) AS mom
FROM monthly ORDER BY month""")
x = np.arange(len(mom)); y = np.log(mom["orders"].values)
slope, intercept, r, p_t, se = stats.linregress(x[:10], y[:10])
trend = np.exp(intercept + slope*x)
resid_sd = np.std(y[:10] - (intercept + slope*x[:10]), ddof=2)
z_nov = (y[10]-(intercept+slope*10))/resid_sd
g = mom["mom"].dropna().values
ci = stats.t.interval(0.95, len(g)-1, loc=g.mean(), scale=stats.sem(g))

fig, ax = plt.subplots(figsize=(9, 4.2))
ax.plot(mom["month"], mom["orders"], color=BLUE, lw=2, marker="o", ms=5, label="Buyurtmalar (fakt)")
ax.plot(mom["month"], trend, color=MUTED, lw=1.5, ls="--", label=f"Trend +{(np.exp(slope)-1)*100:.1f} %/oy (yan–okt)")
ax.annotate(f"noyabr: cho'qqi\n{mom.orders[10]:,} (z={z_nov:+.1f})", xy=(mom.month[10], mom.orders[10]),
            xytext=(-95, 8), textcoords="offset points", color=INK2, fontsize=9,
            arrowprops=dict(arrowstyle="-", color=MUTED))
ax.annotate(f"dekabr: {mom.orders[11]:,}\n−12 % MoM, lekin oktabrdan +8 %", xy=(mom.month[11], mom.orders[11]),
            xytext=(-40, -42), textcoords="offset points", color=INK2, fontsize=9,
            arrowprops=dict(arrowstyle="-", color=MUTED))
ax.set_title("Buyurtmalar yil bo'yi o'sadi: biznes «pasayishi» yo'q")
ax.set_ylabel("oyiga buyurtmalar"); ax.set_ylim(0, 13500)
oy_fmt(ax); ax.legend(loc="upper left")
save(fig, "h1_orders_trend")

fig, ax = plt.subplots(figsize=(9, 3.6))
colors = [YELLOW if i == 10 else (CRITICAL if i == 11 else BLUE) for i in range(1, len(mom))]
ax.bar(mom["month"][1:], mom["mom"][1:], width=20, color=colors)
ax.axhspan(ci[0], ci[1], color=GRID, alpha=.6, zorder=0)
ax.axhline(g.mean(), color=MUTED, lw=1, ls="--")
ax.text(mom["month"].iloc[1], g.mean()+0.6, f"o'rtacha o'sish {g.mean():.1f}% (95% II {ci[0]:.1f}…{ci[1]:.1f}%)", fontsize=9, color=INK2)
for xm, v in zip(mom["month"][1:], mom["mom"][1:]):
    ax.text(xm, v + (0.5 if v >= 0 else -1.6), f"{v:+.0f}%", ha="center", fontsize=8.5, color=INK2)
ax.set_title("Oyma-oy o'sish: yagona «minus» — dekabr, noyabr cho'qqisidan (+23 %) keyin")
ax.set_ylabel("o'tgan oyga nisbatan, %"); oy_fmt(ax)
save(fig, "h1_mom_growth")

# ---------------- H2
heat = q("""
SELECT o.city, date_trunc('month', d.promised_ts)::date AS month,
       round(100.0*count(*) FILTER (WHERE d.status='late')/count(*), 1) AS late_pct
FROM ds_deliveries d JOIN ds_orders o USING(order_id)
GROUP BY 1, 2 ORDER BY 1, 2""")
hp = heat.pivot(index="city", columns="month", values="late_pct")
hp.columns = [OYLAR[c.month-1] for c in hp.columns]
fig, ax = plt.subplots(figsize=(9.5, 4.6))
im = ax.imshow(hp.values, cmap=SEQ, aspect="auto", vmin=0, vmax=100)
ax.set_xticks(range(hp.shape[1]), hp.columns)
ax.set_yticks(range(hp.shape[0]), hp.index)
for i in range(hp.shape[0]):
    for j in range(hp.shape[1]):
        v = hp.values[i, j]
        ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=8,
                color="white" if v > 55 else INK2, fontweight="bold" if v > 55 else "normal")
ax.grid(False)
ax.set_title("Kechikkan yetkazmalar, % (shahar × oy): anomaliya bitta — Samarqand, avgust (93,5 %)")
fig.colorbar(im, ax=ax, label="% kechikkan", shrink=.85)
save(fig, "h2_heatmap")

daily = q("""
WITH d AS (
  SELECT d.promised_ts::date AS day,
         100.0*count(*) FILTER (WHERE d.status='late')/count(*) AS late_pct
  FROM ds_deliveries d JOIN ds_orders o USING(order_id)
  WHERE o.city='Samarkand' AND d.promised_ts >= '2025-07-01' AND d.promised_ts < '2025-10-01'
  GROUP BY 1)
SELECT day, late_pct,
       avg(late_pct) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma7
FROM d ORDER BY day""")
fig, ax = plt.subplots(figsize=(9, 3.8))
ax.axvspan(pd.Timestamp("2025-08-01"), pd.Timestamp("2025-08-31"), color="#f0efec", zorder=0)
ax.plot(daily["day"], daily["late_pct"], color="#9ec5f4", lw=1, label="kunlik % kechikkan")
ax.plot(daily["day"], daily["ma7"], color=CRITICAL, lw=2.2, label="7 kunlik sirg'aluvchi o'rtacha")
ax.text(pd.Timestamp("2025-08-16"), 55, "insident:\n1–31 avgust", ha="center", fontsize=10, color=INK2)
ax.set_title("Samarqand: kechikish 1-avgustda boshlanib 1-sentabrda tugaydi — chegaralari aniq")
ax.set_ylabel("% kechikkan yetkazmalar"); ax.set_ylim(0, 105)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
ax.legend(loc="center left")
save(fig, "h2_daily")

veh = q("""
SELECT c.vehicle_type,
       round(100.0*count(*) FILTER (WHERE d.status='late' AND d.promised_ts >= '2025-08-01'
             AND d.promised_ts < '2025-09-01')
           / NULLIF(count(*) FILTER (WHERE d.promised_ts >= '2025-08-01'
             AND d.promised_ts < '2025-09-01'), 0), 1) AS aug,
       round(100.0*count(*) FILTER (WHERE d.status='late' AND (d.promised_ts < '2025-08-01'
             OR d.promised_ts >= '2025-09-01'))
           / count(*) FILTER (WHERE d.promised_ts < '2025-08-01'
             OR d.promised_ts >= '2025-09-01'), 1) AS normal
FROM ds_deliveries d JOIN ds_couriers c USING(courier_id) JOIN ds_orders o USING(order_id)
WHERE o.city='Samarkand' AND c.city='Samarkand' GROUP BY 1 ORDER BY 1""")
fig, ax = plt.subplots(figsize=(7.5, 3.4))
xpos = np.arange(len(veh)); w = 0.38
ax.bar(xpos - w/2, veh["normal"], w, color=BLUE, label="boshqa oylar")
ax.bar(xpos + w/2, veh["aug"], w, color=CRITICAL, label="2025-avgust")
for i, r_ in veh.iterrows():
    ax.text(i - w/2, r_["normal"]+2, f"{r_.normal:.0f}%", ha="center", fontsize=9, color=INK2)
    ax.text(i + w/2, r_["aug"]+2, f"{r_.aug:.0f}%", ha="center", fontsize=9, color=INK2)
ax.set_xticks(xpos, veh["vehicle_type"]); ax.set_ylim(0, 108)
ax.set_title("Samarqand: avgustda BARCHA transport turlarida kechikish → sabab tizimli")
ax.set_ylabel("% kechikkan"); ax.legend()
save(fig, "h2_vehicles")

# ---------------- H3
tk = q("""
SELECT date_trunc('month', opened_ts)::date AS month, reason, count(*) AS n
FROM ds_support_tickets WHERE opened_ts < '2026-01-01' GROUP BY 1, 2 ORDER BY 1""")
tp = tk.pivot(index="month", columns="reason", values="n").fillna(0)
tp.index = pd.to_datetime(tp.index)
order = ["late_delivery", "refund", "product_quality", "payment_issue", "other"]
tp = tp[order]
fig, ax = plt.subplots(figsize=(9, 4))
bottom = np.zeros(len(tp))
cols = {"late_delivery": CRITICAL, "refund": BLUE, "product_quality": AQUA,
        "payment_issue": YELLOW, "other": MUTED}
for reason in order:
    ax.bar(tp.index, tp[reason], width=20, bottom=bottom, color=cols[reason],
           label=reason, edgecolor=SURFACE, linewidth=1)
    bottom += tp[reason].values
aug_t = int(tp.loc["2025-08-01"].sum()); jul_t = int(tp.loc["2025-07-01"].sum())
ax.set_ylim(0, 1000)
ax.annotate(f"avgust: {aug_t} (iyulga +{100*(aug_t-jul_t)/jul_t:.0f}%),\nbutun o'sish — late_delivery",
            xy=(pd.Timestamp("2025-08-01"), aug_t), xytext=(18, -6), textcoords="offset points",
            fontsize=9, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED))
ax.set_title("Qo'llab-quvvatlash murojaatlari: avgust sakrashi to'liq «late_delivery» sababidan")
ax.set_ylabel("oyiga tiketlar"); ax.legend(ncol=3, fontsize=8.5)
oy_fmt(ax)
save(fig, "h3_tickets")

rt = q("""
SELECT date_trunc('month', r.review_ts)::date AS month,
       round(avg(r.rating) FILTER (WHERE o.city='Samarkand'), 2)  AS samarkand,
       round(avg(r.rating) FILTER (WHERE o.city<>'Samarkand'), 2) AS other_cities
FROM ds_reviews r JOIN ds_orders o USING(order_id)
WHERE r.review_ts < '2026-01-01' GROUP BY 1 ORDER BY 1""")
fig, ax = plt.subplots(figsize=(9, 3.8))
ax.plot(rt["month"], rt["other_cities"], color=BLUE, lw=2, marker="o", ms=4, label="boshqa shaharlar")
ax.plot(rt["month"], rt["samarkand"], color=CRITICAL, lw=2, marker="o", ms=4, label="Samarqand")
ax.annotate("2,76 — insident oyida\nreyting quladi", xy=(pd.Timestamp("2025-08-01"), 2.76),
            xytext=(12, 6), textcoords="offset points", fontsize=9, color=INK2)
ax.set_title("Buyurtma reytingi: faqat Samarqandda va faqat avgustda pasaygan (4,2 → 2,76)")
ax.set_ylabel("o'rtacha baho (1–5)"); ax.set_ylim(2.4, 4.7)
oy_fmt(ax); ax.legend()
save(fig, "h3_ratings")

rep = q("""
WITH first_aug AS (
  SELECT DISTINCT ON (o.user_id) o.user_id, o.ordered_ts, d.status
  FROM ds_orders o JOIN ds_deliveries d USING(order_id)
  WHERE o.ordered_ts >= '2025-08-01' AND o.ordered_ts < '2025-09-01'
    AND d.status IN ('late', 'on_time')
  ORDER BY o.user_id, o.ordered_ts)
SELECT f.status, count(*) AS users,
       count(*) FILTER (WHERE EXISTS (
          SELECT 1 FROM ds_orders o2 WHERE o2.user_id = f.user_id
            AND o2.ordered_ts > f.ordered_ts
            AND o2.ordered_ts <= f.ordered_ts + interval '60 days')) AS repeated
FROM first_aug f GROUP BY 1""").set_index("status")
r1, n1 = rep.loc["late", ["repeated","users"]]; r0, n0 = rep.loc["on_time", ["repeated","users"]]
p1, p0 = r1/n1, r0/n0
pp = (r1+r0)/(n1+n0)
z = (p1-p0)/np.sqrt(pp*(1-pp)*(1/n1+1/n0)); p_val = 2*stats.norm.sf(abs(z))
fig, ax = plt.subplots(figsize=(6.5, 3.4))
groups = ["o'z vaqtida", "kechikkan"]; vals = [p0*100, p1*100]
errs = [1.96*np.sqrt(p0*(1-p0)/n0)*100, 1.96*np.sqrt(p1*(1-p1)/n1)*100]
ax.bar(groups, vals, width=0.5, color=[BLUE, CRITICAL])
ax.errorbar(groups, vals, yerr=errs, fmt="none", ecolor=INK2, capsize=5, lw=1.4)
for i, (v, e) in enumerate(zip(vals, errs)):
    ax.text(i, v + e + 2, f"{v:.1f}% ±{e:.1f}", ha="center", fontsize=10, color=INK2)
ax.set_title(f"60 kun ichida takroriy buyurtma: farq yo'q (z={z:.2f}, p={p_val:.2f})")
ax.set_ylabel("% foydalanuvchilar"); ax.set_ylim(0, 90)
save(fig, "h3_repeat")

# ---------------- H4
cat = q("""
WITH cat_rev AS (
  SELECT c.category_name, sum(oi.quantity * oi.unit_price)/1e9 AS revenue_bln
  FROM ds_order_items oi JOIN ds_products p USING(product_id)
  JOIN ds_categories c ON c.category_id = p.category_id GROUP BY 1)
SELECT category_name, revenue_bln,
       round(100*revenue_bln/sum(revenue_bln) OVER (), 1) AS share,
       round(100*sum(revenue_bln) OVER (ORDER BY revenue_bln DESC)/sum(revenue_bln) OVER (), 1) AS cum
FROM cat_rev ORDER BY revenue_bln DESC""")
hhi = int((cat["share"]**2).sum())
fig, ax = plt.subplots(figsize=(8.5, 4.4))
top = cat.head(10).iloc[::-1]
colors = [BLUE if s < 20 else "#184f95" for s in top["share"]]
ax.barh(top["category_name"], top["revenue_bln"], color=colors, height=0.62)
for yv, (rev, share, cum) in enumerate(zip(top["revenue_bln"], top["share"], top["cum"])):
    ax.text(rev + 0.8, yv, f"{share:.0f}%  (jamlanma {cum:.0f}%)", va="center", fontsize=8.5, color=INK2)
ax.set_title(f"Smartfonlar = daromadning {cat.share[0]:.0f} %; top-3 kategoriya = {cat.cum[2]:.0f} %  (HHI = {hhi})")
ax.set_xlabel("daromad, mlrd so'm"); ax.set_xlim(0, 92)
save(fig, "h4_categories")

pay = q("""
SELECT method, count(*) AS attempts,
       round(100.0*count(*) FILTER (WHERE status='failed')/count(*), 1) AS fail_pct
FROM ds_payments GROUP BY 1 ORDER BY attempts DESC""")
fig, ax = plt.subplots(figsize=(7.5, 3.4))
colors = [CRITICAL if m == "Installment" else BLUE for m in pay["method"]]
ax.bar(pay["method"], pay["fail_pct"], width=0.55, color=colors)
for i, r_ in pay.iterrows():
    ax.text(i, r_["fail_pct"] + 0.25, f"{r_.fail_pct}%", ha="center", fontsize=10, color=INK2)
ax.set_title("To'lov radlari: bo'lib to'lash (Installment) kartalardan 2 baravar yomon (χ², p < 0,001)")
ax.set_ylabel("% muvaffaqiyatsiz urinishlar"); ax.set_ylim(0, 12.5)
save(fig, "h4_fail_rates")

fun = q("""
SELECT event_type, count(*) AS n FROM ds_events
WHERE event_type IN ('view_product','add_to_cart','checkout_start','payment_success')
GROUP BY 1""").set_index("event_type").loc[["view_product","add_to_cart","checkout_start","payment_success"]]
steps = ["Mahsulot ko'rish","Savat","Checkout","To'lov o'tdi"]
vals = fun["n"].values
ramp = ["#86b6ef", "#5598e7", "#2a78d6", "#184f95"]
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.barh(range(len(vals))[::-1], vals, color=ramp, height=0.6)
for i, v in enumerate(vals):
    conv = "" if i == 0 else f"   (oldingidan {100*v/vals[i-1]:.0f}%)"
    ax.text(v + 3000, len(vals)-1-i, f"{v:,}{conv}", va="center", fontsize=9.5, color=INK2)
ax.set_yticks(range(len(vals))[::-1], steps); ax.set_xlim(0, 235000)
ax.set_title("Ilova voronkasi: asosiy yo'qotish — ko'rish → savat (69 %), checkoutdan keyin yo'qotish yo'q")
ax.set_xlabel("yillik hodisalar")
save(fig, "h4_funnel")

print("Barcha UZ grafiklar tayyor:", OUT)
