# 📖 To'liq hisobot: nima qilindi, qanday qilindi va nima topildi

*Bu hujjat — loyihani boshidan oxirigacha tushunib olishingiz uchun. Har bir qadam,
har bir raqam va uning ma'nosi shu yerda. O'qib chiqsangiz, himoyada har qanday
savolga javob bera olasiz.*

---

## 1. Topshiriq nima edi?

UZCARD Academy mini-loyihasi: jamoa (2–3 kishi) shartli buyurtmachidan biznes-masala
oladi va ma'lumotlar bo'yicha tadqiqot o'tkazadi. Muhim shartlar:

- Tayyor savollar va jadvallar ro'yxati **berilmaydi** — ma'lumotlarni o'zing tahlil
  qilib topasan;
- Bazada 4 ta trekning jadvallari **aralashtirilgan** (31 ta `ds_*` jadval);
- Har bir ishtirokchi kamida **bitta o'z gipotezasini** olib boradi va himoya qiladi;
- Majburiy texnik minimum: **JOIN, GROUP BY, CTE yoki pastki so'rov, oynali funksiya**,
  har gipotezaga kamida 2 ta grafik;
- **ML ishlatish mumkin emas** — faqat SQL, pandas, vizualizatsiya va statistika;
- D trek uchun **har bir ishtirokchining topilmasi statistik metod bilan** tasdiqlanishi
  shart (boshqa treklarda — jamoaga bitta, qo'shimcha ball);
- Himoya: jamoaga 4 daqiqa doklad + 1 daqiqa savollar. **4 daqiqadan oshsa — to'xtatiladi.**

## 2. Nega D trekni tanladik?

To'rt trekdan D (OqPay Super-App) tanlandi, sabablari:

1. **Eng katta ma'lumotlar to'plami** (~1,4 mln qator) — topshiriqda ham «самый крупный
   набор» deb ta'kidlangan, bu tahlil chuqurligini ko'rsatish imkonini beradi;
2. **Detektiv syujet**: buyurtmachi aniq hodisa («bir oyda pasayish va shikoyatlar»)
   haqida so'raydi — demak ma'lumotlarda topilishi kerak bo'lgan yashirin insident bor.
   Va biz uni topdik. Bunday "ildiz sababni topdik" hikoyasi himoyada eng ta'sirli;
3. Statistika har bir ishtirokchi uchun majburiyligi — qo'shimcha ball mezoni bilan mos.

*(Ehtiyot uchun A, B, C treklar ham to'liq tayyorlandi — `alt-tracks/` papkasida,
pastda 9-bo'limga qarang.)*

## 3. Ma'lumotlarni qanday ajratdik? (Data arxeologiyasi)

Bazada 31 ta jadval bor edi. Qadamlar:

1. `information_schema.tables` dan barcha `ds_*` jadvallar ro'yxatini oldik;
2. Har jadvalning ustunlarini (`information_schema.columns`) ko'rib chiqdik;
3. Jadvallarni **kalitlarning haqiqiy mosligi** bo'yicha guruhladik — nom o'xshashligiga
   ishonmasdan JOIN bilan tekshirdik:

```sql
-- misol: ds_orders kimning useri? 100% mos kelishi kerak
SELECT count(*) FROM ds_orders o JOIN ds_users_1 u USING(user_id);  -- 100 000 ✓
SELECT count(*) FROM ds_orders o JOIN ds_users_2 u USING(user_id);  -- mos emas ✗
```

Natijada 4 klaster chiqdi:
- **A trek (UZCARD-XL):** ds_customers, ds_cards, ds_transactions_2, ds_merchants_2, ds_mcc_categories (2023-yil operatsiyalari);
- **B trek (WalletApp):** ds_users_2, ds_channels, ds_app_events, ds_subscriptions, ds_plans, ds_charges (2025–2026);
- **C trek (MerchantHub):** ds_merchants_1, ds_merchant_categories, ds_regions, ds_terminals_1, ds_transactions_1, ds_settlements, ds_disputes (2025);
- **D trek (OqPay):** ds_users_1, ds_orders, ds_order_items, ds_products, ds_merchants_3, ds_categories, ds_payments, ds_deliveries, ds_couriers, ds_reviews, ds_support_tickets, ds_events (2025).

Qiziq nuqta: `ds_disputes.txn_id` ikkala tranzaksiya jadvaliga ham "yopishadi", lekin
**barcha 1 986 nizo faqat `ds_transactions_1` bilan to'liq birlashadi** → disputes C
trekniki. `ds_terminals_2` esa A trekka tegishli (transactions_2 dagi terminal_id bilan mos).

## 4. D trek: to'rt gipoteza va topilmalar

### H1. «Buyurtmalar pasayishi» aslida bo'lganmi? — YO'Q

**Qanday tekshirdik:** oylik buyurtmalar soni (CTE + `LAG` oynali funksiya bilan oyma-oy
o'sish), yanvar–oktabr bo'yicha eksponensial trend regressiyasi, noyabr/dekabr
og'ishlarining z-bahosi.

**Raqamlar:**
| Ko'rsatkich | Qiymat |
|---|---|
| Yanvar → dekabr buyurtmalar | 5 658 → 10 564 (har oy o'sish) |
| O'rtacha oylik o'sish | +6,1 % (95 % II: 0,7–11,5 %) |
| Trend (yan–okt) | +6,0 %/oy, R² = 0,99, p < 0,001 |
| Noyabr | +23 % MoM, trenddan +14 % (z = +7,5) — mavsumiy cho'qqi |
| Dekabr | −12 % MoM, LEKIN oktabrdan +8 %, trenddan atigi −5 % |
| O'rtacha chek | barqaror: 1,70–1,81 mln so'm |

**Ma'nosi:** buyurtmachi ko'rgan «pasayish» — noyabr aksiya-cho'qqisidan keyingi normal
korreksiya (talabning bir qismi noyabrda oldindan xarid qilingan — pull-forward).
Biznes o'sishda davom etgan. Demak, xavotir manbai boshqa joyda — shikoyatlarda.

### H2. Ildiz sabab: Samarqand, 1–31 avgust 2025 — logistika kollapsi

**Qanday tekshirdik:** shahar × oy kesimida kechikish foizi (heatmap), Samarqand bo'yicha
kunlik dinamika (7 kunlik sirg'aluvchi o'rtacha — `AVG OVER ... ROWS 6 PRECEDING`),
transport turlari kesimi, ikki ulush z-testi.

**Raqamlar:**
| Ko'rsatkich | Qiymat |
|---|---|
| Samarqand, avgust | 966/1033 = **93,5 %** kechikkan |
| Samarqand, boshqa oylar | 911/11101 = 8,2 % |
| Farq | +85,3 f.p. (95 % II: 83,7–86,9), z = 72,5, p ≈ 0 |
| Transport turlari (avgust) | velosiped 93 %, mashina 93 %, piyoda 92 %, samokat 96 % |
| Boshqa 9 shahar (avgust) | 7–10 % (norma) |
| Insident chegaralari | aniq 01.08 boshlanib, 31.08 tugagan |

**Muqobil versiyalarni rad etdik:**
- *Kuryer yetishmovchiligi emas:* kuryer boshiga yuk yil davomida silliq o'sgan (16→33),
  avgustda sakrash yo'q; avgust hajmi (1 033) iyul bilan bir xil;
- *Kuryer turi emas:* hamma turlar birdek kechikkan;
- *Demak — tizimli sabab:* shahar habi / marshrutlash / pudratchi. Kalendar oyga aniq
  moslik oylik shartnoma yoki relizga ishora qiladi.

### H3. Oqibatlar: shikoyat +73 %, reyting quladi, LEKIN mijozlar ketmadi

**Qanday tekshirdik:** tiketlar sabablar kesimida, reyting Samarqand vs boshqa shaharlar,
kechikkan vs o'z vaqtidagi buyurtmalar reytingi (Mann–Uitni testi), 60 kunlik takroriy
xarid (korrelyatsiyalangan `EXISTS` + z-test).

**Raqamlar:**
| Ko'rsatkich | Qiymat |
|---|---|
| Tiketlar iyul → avgust | 518 → 896 (**+73 %**) |
| Avgust late_delivery tiketlari | 661, shundan 408 (62 %) Samarqand |
| Reyting: o'z vaqtida vs kechikkan | 4,37 vs 2,60 (Mann–Uitni, p < 0,001) |
| Samarqand oylik reytingi | 4,2 → **2,76** (avgust) → 4,08 (sentabr) → normal (oktabr) |
| Takroriy xarid 60 kun: kechikkan | 645/940 = 68,6 % |
| Takroriy xarid 60 kun: o'z vaqtida | 2759/4093 = 67,4 % |
| Farq | z = 0,71, **p = 0,47 — ahamiyatsiz** |

**Ma'nosi:** zarar operatsion (tiketlar = support xarajati) va reputatsion (reyting),
lekin mijozlar oqimi boshlanmagan — bu **omad, strategiya emas**. «Farq yo'q» degan
statistik natija ham qimmatli topilma: u aniq biznes-xulosaga olib keladi — 940 jabrlangan
mijozni hozir promo bilan mustahkamlash arzon, ikkinchi insidentni esa kechirishmaydi.

### H4. Fon risklari: konsentratsiya va bo'lib to'lash

**Qanday tekshirdik:** kategoriya daromadlari (`SUM OVER` jamlanma ulush, HHI),
sotuvchilar detsillari (`NTILE(10)`), to'lov usullari radlari (χ²-test), ilova voronkasi.

**Raqamlar:**
| Ko'rsatkich | Qiymat |
|---|---|
| Smartfonlar daromad ulushi | **40 %** (70+ mlrd so'm) |
| Top-3 kategoriya | 67 % |
| HHI (kategoriyalar) | **2 133** (>1 800 = yuqori konsentratsiya) |
| Top-10 % sotuvchilar | aylanmaning 49,5 % i |
| Rad: UZCARD/HUMO/VISA | 4,9 / 5,0 / 5,1 % |
| Rad: **Installment** | **10,3 %** (χ² = 809, p < 0,001) |
| To'lanmagan buyurtmalar | 458 ta ≈ **0,85 mlrd so'm** GMV |
| Voronka | ko'rish→savat 69 % → checkout 85 % → to'lov 99,5 % |

**Ma'nosi:** pastki voronka sog'lom, asosiy platejlarda yo'qotish — bo'lib to'lash
shlyuzida. Konsentratsiya esa avgust insidenti nima uchun butun kompaniyani "og'ritganini"
tushuntiradi: mo'rt tuzilma.

## 5. Buyurtmachiga yakuniy javob

> «Pasayish» bo'lmagan — dekabr trendga qaytish. Shikoyatlar sakrashining sababi —
> Samarqanddagi bir oylik (01–31.08.2025) tizimli logistika inqirozi: 93,5 % kechikish,
> +73 % shikoyat, shahar reytingi 2,76. Mijozlar hali ketmagan — harakat oynasi ochiq.

**Harakatlar rejasi:** (1) pudratchi bilan insident tahlili + jarimali SLA;
(2) shaharlar bo'yicha kunlik kechikish alerti («baza +5 f.p., 3 kun» qoidasi);
(3) 940 jabrlangan mijozga promo; (4) Installment shlyuzi auditi (~0,4 mlrd/yil qaytimi);
(5) daromad diversifikatsiyasi (HHI pasaytirish).

## 6. Statistik metodlar — nima uchun aynan shular?

| Metod | Qayerda | Nega |
|---|---|---|
| Log-chiziqli regressiya + qoldiq z-bahosi | H1 | eksponensial o'sishda trenddan og'ishni o'lchash uchun |
| O'rtacha uchun t-ishonch intervali | H1 | oylik o'sish sur'atining barqarorligini ko'rsatish |
| Ikki ulush z-testi | H2, H3 | ikki foizni taqqoslash (kechikish, takroriy xarid) |
| Mann–Uitni U-testi | H3 | reyting ordinal shkala — o'rtacha o'rniga ranglar bo'yicha taqqoslash to'g'ri |
| χ²-test | H4 | to'lov usuli × natija jadvalida bog'liqlikni tekshirish |
| HHI + Pareto/detsil ulushi | H4 | konsentratsiyani bitta raqam bilan ifodalash |

## 7. Texnik talablar qayerda bajarilgan

| Talab | Joyi |
|---|---|
| JOIN | H2 (orders⋈deliveries⋈couriers — 3 jadval), H4 (order_items⋈products⋈categories), H3 (reviews⋈orders, tickets⋈orders) |
| GROUP BY | hamma gipotezalarda |
| CTE | `WITH monthly` (H1), `WITH d` (H2), `WITH first_aug` (H3), `WITH cat_rev` (H4) |
| Pastki so'rov | H3 dagi korrelyatsiyalangan `EXISTS` (takroriy xarid) |
| Oynali funksiyalar | `LAG` (H1), `AVG OVER ROWS 6 PRECEDING` (H2), `SUM OVER`, `RANK`, `NTILE` (H4) |
| ≥2 grafik/gipoteza | H1: 2, H2: 3, H3: 3, H4: 3 (jami 11) |
| Statistika har ishtirokchida | H1 trend+II · H2 z-test · H3 Mann–Uitni+z · H4 χ²+HHI |
| ML yo'q | faqat SQL, pandas, matplotlib, scipy.stats |

## 8. Loyiha fayllari — nima qayerda

```
oqpay-mini-project/
├── notebooks/oqpay_analysis.ipynb    ← ASOSIY TOPSHIRILADIGAN FAYL (bajarilgan holda)
├── presentation/OqPay_TrackD.pptx    ← prezentatsiya (ruscha)
├── presentation/OqPay_TrackD_UZ.pptx ← prezentatsiya (o'zbekcha)
├── charts/                           ← 11 grafik (RU)
├── charts_uz/                        ← o'sha grafiklar (UZ)
├── scripts/make_charts_uz.py         ← UZ grafiklarni qayta yaratish skripti
├── sql/queries.sql                   ← barcha asosiy SQL so'rovlar izohlar bilan
├── docs/
│   ├── SPEECH_RU.md / SPEECH_UZ.md         ← 4 daqiqalik himoya matni (reglament!)
│   ├── SPEECH_FULL_RU.md / SPEECH_FULL_UZ.md ← 10–15 daqiqalik to'liq versiya + lug'at
│   ├── HISOBOT_UZ.md                       ← shu fayl
│   └── CHECKLIST.md                        ← himoyagacha qilinadigan ishlar
├── alt-tracks/                       ← ZAXIRA: A, B, C treklar to'liq
│   ├── track-A-uzcardxl/    (notebook + 6 grafik + pptx)
│   ├── track-B-walletapp/   (notebook + 7 grafik + pptx)
│   └── track-C-merchanthub/ (notebook + 6 grafik + pptx)
└── README.md
```

## 9. Zaxira treklar (agar jamoa boshqa trek tanlasa)

Har biri to'liq ishlaydigan notebook + prezentatsiya + xulosalar bilan:

**A trek — UZCARD-XL (protsessing, 2023):**
- A1: operatsiyalar ×16 o'sgan — portfel ramp-up, dekabr +63 % mavsum; radlar barqaror;
- A2: **student segmenti — 11,2 % rad** (boshqalarda 5,8 %; z = 11,9), sabab: balans/limit
  → mikro-overdraft, bildirishnomalar;
- A3: **onlayn-nizolar: operatsiyalarning 1,16 % i, nizoli pullarning 91 % i** (103 mln)
  → 3-D Secure, e-com skoring.

**B trek — WalletApp (hamyon+obuna, 2025–26):**
- B1: voronka signup→to'lov 28 %, asosiy yo'qotish KYC; **telegram_ads: 9,9 % konversiya,
  to'lovchi narxi 91 ming so'm (referraldan ×13)** → byudjetni ko'chirish;
- B2: **2026-fevral billing nosozligi: 17,6 % muvaffaqiyatsiz yechim** (norma 4,5 %) →
  dunning-retray, zaxira shlyuz;
- B3: MRR 1,9→54 mln, lekin obunalarning 18–21 % i bekor qilinadi, tarifga bog'liq emas
  (χ², p = 0,61) → qiymat/ushlab qolish dasturi.

**C trek — MerchantHub (ekvayring, 2025):**
- C1: **top-10 % merchantlar aylanmaning 76,7 % i** (Jini 0,83), Janub — 6 % → yirik
  hamkorlarni ushlab qolish + Janubga ekspansiya;
- C2: **1-dekabrdan to'lovlar 2,2 → 4,2 kunga sekinlashgan** (bir kunda, Mann–Uitni
  p < 0,001), mavsum cho'qqisida 3,5 mlrd kechiktirilgan → 01.12 relizini tekshirish, SLA;
- C3: nizolarning 52 % i yutqaziladi (281 mln), **high-risk = keyslarning 22 %, pullarning
  54 % i** → rolling-rezerv, dalil shablonlari.

## 10. Himoyagacha qilinadigan ishlaringiz (qisqa)

1. Platformada jamoa tuzish + slot band qilish (07.07 / 09.07 / 10.07 / 14.07);
2. Notebook, pptx, speech fayllarida «Участник 2/3» → jamoadoshlar ismi;
3. Har kim o'z gipotezasini o'zlashtirsin (SPEECH_FULL o'qish + notebookda o'z SQL ini
   ishlatib ko'rish);
4. 4 daqiqalik nutqni taymer bilan 3 marta mashq qilish;
5. Himoyadan oldin https://academy-avu.pages.dev/teams ga notebook + pptx yuklash.

*Batafsil: `docs/CHECKLIST.md`*
