#!/usr/bin/env python3
"""A/B/C treklar prezentatsiyalarida ishlatiladigan grafiklarning UZ versiyalari.
Har trek uchun alt-tracks/<trek>/charts_uz/ ga yoziladi."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats
from sqlalchemy import create_engine
import sys, pathlib, os

_p = pathlib.Path(__file__).resolve().parent
while not (_p/"db_config.py").exists() and _p != _p.parent: _p = _p.parent
sys.path.insert(0, str(_p))
from db_config import DB_URL
ENGINE = create_engine(DB_URL)
BASE = str(_p)
def q(sql): return pd.read_sql(sql, ENGINE)

BLUE, AQUA, YELLOW, GREEN = "#2a78d6", "#1baf7a", "#eda100", "#008300"
CRITICAL, INK, INK2, MUTED, GRID, SURFACE = "#d03b3b", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "figure.dpi": 110,
    "axes.edgecolor": "#c3c2b7", "axes.linewidth": 0.8, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.7, "axes.axisbelow": True,
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "font.family": "sans-serif", "axes.titlesize": 12, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
})
OYLAR = ["Yan","Fev","Mar","Apr","May","Iyn","Iyl","Avg","Sen","Okt","Noy","Dek"]
def oy_fmt(ax):
    ax.xaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(
        lambda x, _: OYLAR[mdates.num2date(x).month-1]))
def save(fig, track_dir, name):
    out = f"{BASE}/alt-tracks/{track_dir}/charts_uz"
    os.makedirs(out, exist_ok=True)
    fig.savefig(f"{out}/{name}.png", bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig); print("saved", track_dir, name)

# ================= A1: o'sish =================
a1 = q("""
WITH monthly AS (
  SELECT date_trunc('month', txn_ts)::date AS month, count(*) AS txns,
         count(DISTINCT card_id) AS active_cards
  FROM ds_transactions_2 GROUP BY 1)
SELECT month, txns, active_cards,
       round(100.0*(txns - LAG(txns) OVER (ORDER BY month))/LAG(txns) OVER (ORDER BY month),1) AS mom
FROM monthly ORDER BY month""")
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(a1["month"], a1["txns"], color=BLUE, lw=2, marker="o", ms=5, label="oyiga operatsiyalar")
ax.plot(a1["month"], a1["active_cards"], color=AQUA, lw=2, marker="o", ms=4, label="faol kartalar")
ax.annotate(f"dekabr: {a1.txns.iloc[11]:,}\n(+{a1.mom.iloc[11]:.0f}% MoM, mavsum)",
            xy=(a1.month.iloc[11], a1.txns.iloc[11]), xytext=(-110, -8), textcoords="offset points",
            fontsize=9, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED))
ax.set_title("Operatsiyalar va faol kartalar butun 2023 yil o'sadi — portfel jadallashmoqda")
ax.set_ylabel("oyiga, dona"); oy_fmt(ax); ax.legend(loc="upper left")
save(fig, "track-A-uzcardxl", "a1_growth")

# ================= A2: segment radlari =================
seg = q("""
SELECT cu.customer_segment, count(*) AS txns,
       count(*) FILTER (WHERE t.txn_status='declined') AS declined,
       round(100.0*count(*) FILTER (WHERE t.txn_status='declined')/count(*), 1) AS pct
FROM ds_transactions_2 t JOIN ds_cards c USING(card_id) JOIN ds_customers cu USING(customer_id)
GROUP BY 1 ORDER BY pct DESC""")
d1 = int(seg.loc[seg.customer_segment=="student","declined"].iloc[0]); n1 = int(seg.loc[seg.customer_segment=="student","txns"].iloc[0])
d0 = int(seg.loc[seg.customer_segment!="student","declined"].sum()); n0 = int(seg.loc[seg.customer_segment!="student","txns"].sum())
p1, p0 = d1/n1, d0/n0; pp = (d1+d0)/(n1+n0)
z = (p1-p0)/np.sqrt(pp*(1-pp)*(1/n1+1/n0))
fig, ax = plt.subplots(figsize=(7, 3.4))
colors = [CRITICAL if s == "student" else BLUE for s in seg["customer_segment"]]
ax.bar(seg["customer_segment"], seg["pct"], width=0.55, color=colors)
for i, r_ in seg.iterrows():
    ax.text(i, r_["pct"]+0.25, f"{r_.pct}%", ha="center", fontsize=10, color=INK2)
ax.set_title(f"Radlar ulushi: student {p1:.1%} — boshqalardan 2 baravar yuqori (z={z:.1f}, p<0,001)")
ax.set_ylabel("% rad etilgan"); ax.set_ylim(0, 13.5)
save(fig, "track-A-uzcardxl", "a2_segments")

# ================= A3: nizolar =================
dis = q("""
SELECT mc.category_group, count(*) AS txns,
       count(*) FILTER (WHERE t.is_disputed) AS disputed,
       round(100.0*count(*) FILTER (WHERE t.is_disputed)/count(*), 2) AS pct
FROM ds_transactions_2 t JOIN ds_merchants_2 m USING(merchant_id)
JOIN ds_mcc_categories mc ON mc.mcc_code = m.mcc_code
GROUP BY 1 ORDER BY pct DESC""")
fig, ax = plt.subplots(figsize=(7.5, 3.4))
colors = [CRITICAL if g == "Online" else BLUE for g in dis["category_group"]]
ax.bar(dis["category_group"], dis["pct"], width=0.55, color=colors)
for i, r_ in dis.iterrows():
    ax.text(i, r_["pct"]+0.03, f"{r_.pct}%", ha="center", fontsize=10, color=INK2)
ax.set_title("Nizolar chastotasi: Online 1,16 % — oflayndan 10–20 baravar yuqori (χ², p < 0,001)")
ax.set_ylabel("% nizolangan operatsiyalar")
save(fig, "track-A-uzcardxl", "a3_dispute_rate")

# ================= B1: kanallar =================
ch = q("""
SELECT c.channel_name, count(DISTINCT u.user_id) AS signups,
       count(DISTINCT e.user_id) FILTER (WHERE e.event_type='first_payment') AS payers
FROM ds_users_2 u JOIN ds_channels c USING(channel_id)
LEFT JOIN ds_app_events e USING(user_id)
GROUP BY 1 ORDER BY signups DESC""")
ch["pct"] = (100*ch.payers/ch.signups).round(1)
fig, ax = plt.subplots(figsize=(8.5, 3.4))
colors = [CRITICAL if c_=="telegram_ads" else BLUE for c_ in ch["channel_name"]]
ax.bar(ch["channel_name"], ch["pct"], width=0.55, color=colors)
for i, r_ in ch.iterrows():
    ax.text(i, r_.pct+0.8, f"{r_.pct}%", ha="center", fontsize=10, color=INK2)
ax.set_title("Ro'yxatdan o'tish → birinchi to'lov konversiyasi: telegram_ads 9,9 % (z = 15,4, p < 0,001)")
ax.set_ylabel("% ro'yxatdan o'tganlardan"); ax.set_ylim(0, 48)
save(fig, "track-B-walletapp", "b1_channels")

# ================= B2: billing =================
bill = q("""
SELECT date_trunc('month', charged_at)::date AS month, count(*) AS charges,
       round(100.0*count(*) FILTER (WHERE status='failed')/count(*), 1) AS fail_pct
FROM ds_charges GROUP BY 1 ORDER BY 1""")
feb = bill[bill.month.astype(str).str.startswith("2026-02")].iloc[0]
rest = bill[~bill.month.astype(str).str.startswith("2026-02")]
p0b = rest.apply(lambda r: r.charges*r.fail_pct/100, axis=1).sum()/rest.charges.sum()*100
fig, ax = plt.subplots(figsize=(9, 3.6))
ax.plot(bill["month"], bill["fail_pct"], color=BLUE, lw=2, marker="o", ms=4)
ax.scatter([feb.month], [feb.fail_pct], color=CRITICAL, s=70, zorder=5)
ax.annotate(f"2026-fevral: {feb.fail_pct}%\n(billing nosozligi)", xy=(feb.month, feb.fail_pct),
            xytext=(-125, -6), textcoords="offset points", fontsize=9, color=INK2,
            arrowprops=dict(arrowstyle="-", color=MUTED))
ax.axhline(p0b, color=MUTED, lw=1, ls="--")
ax.text(bill["month"].iloc[0], p0b+0.7, f"norma ~{p0b:.1f}%", fontsize=9, color=INK2)
ax.set_title("Oylik muvaffaqiyatsiz yechimlar ulushi: yagona sakrash — 2026-fevral")
ax.set_ylabel("% failed"); ax.set_ylim(0, 20)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m.%y"))
save(fig, "track-B-walletapp", "b2_failrate")

# ================= B3: tariflar =================
pl = q("""
SELECT p.plan_name, p.monthly_price, count(*) AS subs,
       count(*) FILTER (WHERE s.status='canceled') AS canceled,
       round(100.0*count(*) FILTER (WHERE s.status='canceled')/count(*), 1) AS cancel_pct
FROM ds_subscriptions s JOIN ds_plans p USING(plan_id)
GROUP BY 1, 2 ORDER BY p.monthly_price""")
obs = np.array([pl["canceled"], pl["subs"] - pl["canceled"]]).T
chi2, p_chi, dof, _ = stats.chi2_contingency(obs)
fig, ax = plt.subplots(figsize=(8, 3.4))
xpos = np.arange(len(pl)); w = 0.38
ax.bar(xpos - w/2, pl["subs"], w, color=BLUE, label="jami obunalar")
ax.bar(xpos + w/2, pl["canceled"], w, color=YELLOW, label="bekor qilingan")
for i, r_ in pl.iterrows():
    ax.text(i - w/2, r_.subs+12, f"{r_.subs}", ha="center", fontsize=9, color=INK2)
    ax.text(i + w/2, r_.canceled+12, f"{r_.canceled} ({r_.cancel_pct}%)", ha="center", fontsize=9, color=INK2)
ax.set_xticks(xpos, [f"{n} ({p_//1000} ming)" for n, p_ in zip(pl.plan_name, pl.monthly_price)])
ax.set_title(f"Bekor qilish barcha tariflarda bir xil: 18–21 % (χ² = {chi2:.1f}, p = {p_chi:.2f} — bog'liq emas)")
ax.set_ylabel("obunalar"); ax.legend()
save(fig, "track-B-walletapp", "b3_plans")

# ================= C1: Pareto =================
par = q("""
WITH m_rev AS (
  SELECT m.merchant_id, sum(t.amount_uzs) AS rev
  FROM ds_transactions_1 t JOIN ds_terminals_1 tr USING(terminal_id)
  JOIN ds_merchants_1 m ON m.merchant_id = tr.merchant_id
  WHERE t.status = 'approved' GROUP BY 1),
ranked AS (SELECT rev, NTILE(10) OVER (ORDER BY rev DESC) AS decile FROM m_rev)
SELECT decile, sum(rev)/1e9 AS rev_bln,
       round(100*sum(sum(rev)) OVER (ORDER BY decile)/sum(sum(rev)) OVER (), 1) AS cum
FROM ranked GROUP BY decile ORDER BY decile""")
fig, ax = plt.subplots(figsize=(8.5, 3.6))
ax.bar(par["decile"], par["rev_bln"], color=["#184f95"]+[BLUE]*9, width=0.6)
for i, r_ in par.iterrows():
    ax.text(r_.decile, r_.rev_bln+0.25, f"{r_.cum:.0f}%", ha="center", fontsize=9, color=INK2)
ax.set_title(f"Merchant detsillari bo'yicha aylanma: top-10 % = {par.cum[0]} % (raqam — jamlanma ulush; Jini 0,83)")
ax.set_xlabel("merchantlar detsili (1 = eng yiriklari)"); ax.set_ylabel("mlrd so'm")
ax.set_xticks(range(1, 11))
save(fig, "track-C-merchanthub", "c1_pareto")

# ================= C2: kunlik to'lovlar =================
daily = q("""
SELECT batch_date::date AS day,
       avg(EXTRACT(epoch FROM settled_ts - batch_date)/86400) AS delay_d
FROM ds_settlements
WHERE batch_date >= '2025-11-10' AND batch_date < '2025-12-28'
GROUP BY 1 ORDER BY 1""")
fig, ax = plt.subplots(figsize=(9, 3.4))
ax.axvspan(pd.Timestamp("2025-12-01"), pd.Timestamp("2025-12-27"), color="#f0efec", zorder=0)
ax.plot(daily["day"], daily["delay_d"], color=CRITICAL, lw=2, marker="o", ms=3.5)
ax.annotate("sakrash roppa-rosa 1-dekabrda:\nbir kunda 2,3 → 4,1 kun", xy=(pd.Timestamp("2025-12-01"), 4.12),
            xytext=(-155, -30), textcoords="offset points", fontsize=9, color=INK2,
            arrowprops=dict(arrowstyle="-", color=MUTED))
ax.set_title("Kunlik dinamika: degradatsiya asta-sekin emas, bir lahzada")
ax.set_ylabel("to'lovgacha kunlar"); ax.set_ylim(1.5, 4.8)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
save(fig, "track-C-merchanthub", "c2_daily")

# ================= C3: yutqazilgan pullar =================
ds_ = q("""
SELECT cat.risk_tier, count(*) AS disputes,
       round(sum(dp.dispute_amount_uzs) FILTER (WHERE dp.status='lost')/1e6, 1) AS lost_mln
FROM ds_disputes dp
JOIN ds_transactions_1 t ON t.txn_id = dp.txn_id
JOIN ds_terminals_1 tr USING(terminal_id)
JOIN ds_merchants_1 m ON m.merchant_id = tr.merchant_id
JOIN ds_merchant_categories cat ON cat.category_id = m.category_id
GROUP BY 1 ORDER BY lost_mln DESC""")
tot = ds_.lost_mln.sum()
colors = {"high": CRITICAL, "medium": YELLOW, "low": BLUE}
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.bar(ds_["risk_tier"], ds_["lost_mln"], width=0.55, color=[colors[t_] for t_ in ds_["risk_tier"]])
for i, r_ in ds_.iterrows():
    ax.text(i, r_.lost_mln+3, f"{r_.lost_mln:.0f} mln\n({r_.disputes} nizo)", ha="center", fontsize=9, color=INK2)
ax.set_title(f"Risk-tier bo'yicha yutqazilgan summalar: high = pullarning {100*ds_.lost_mln.iloc[0]/tot:.0f}% i, keyslarning {100*ds_.disputes.iloc[0]/ds_.disputes.sum():.0f}% ida")
ax.set_ylabel("mln so'm"); ax.set_ylim(0, 185)
save(fig, "track-C-merchanthub", "c3_lost_money")

print("Barcha alt-trek UZ grafiklari tayyor")
