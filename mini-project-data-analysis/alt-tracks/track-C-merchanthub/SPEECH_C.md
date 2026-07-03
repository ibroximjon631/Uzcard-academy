# Трек C (MerchantHub) — сценарий защиты 4 минуты (RU + UZ)

## 🇷🇺 Русский (4:00)

**0:00–0:40 · Задача и данные.** «Мы — команда трека C, MerchantHub, эквайринг. Заказчик
— финансовый и операционный блок: "где сосредоточен оборот, вовремя ли платим мерчантам,
что со спорами". Нашли свои 7 таблиц по JOIN-ам: 80 000 операций 2025 года, 1 200
мерчантов, 2 527 терминалов, 51 052 выплаты, 1 986 споров — все споры соединяются
именно с нашими транзакциями по txn_id».

**0:40–1:40 · C1 (концентрация).** «Годовой оборот — 23,5 млрд сумов. Разложили по
децилям мерчантов оконной NTILE: топ-10 % — это 120 мерчантов — держат 76,7 % оборота.
Коэффициент Джини 0,83 — экстремальная концентрация: уход пары якорных партнёров бьёт
по комиссии, а это 1,49 % оборота. География: столица 6,5 млрд, Юг — 1,4 млрд, всего
6 % при 106 мерчантах. Итог: риск зависимости плюс резерв роста на Юге».

**1:40–2:45 · C2 (выплаты — главная находка).** «Весь год выплаты мерчантам шли за
2,2 дня. С 1 декабря — 4,2 дня: вдвое медленнее. Скачок одномоментный: 30 ноября — 2,3,
1 декабря — 4,1, на дневном графике это ступенька, не горка. Тест Манна–Уитни:
p < 0,001. И это декабрь — пиковый месяц: задержаны выплаты на 3,5 млрд сумов, у
мерчантов кассовый разрыв в самый горячий сезон. Похоже на релиз или смену процесса
расчётов 1 декабря. Решение: разбор изменения, SLA T+2 с алертом при медиане выше
2,5 дня, приоритетная очередь крупным».

**2:45–3:30 · C3 (споры).** «Из 1 682 завершённых споров проиграно 879 — 52 %, на
281 млн сумов. Концентрация не в частоте, а в деньгах: high-risk категории — 22 %
кейсов, но 54 % проигранных сумм; средний спор там 881 тысяча — в 6 раз крупнее low.
χ² по исходам: p = 0,021. Разбор длится 17,5 дня, в бэклоге 304 кейса. Решение:
роллинг-резерв для high-risk, шаблоны доказательств, KPI ≤ 14 дней».

**3:30–4:00 · Финал.** «Три проблемные зоны: хрупкая концентрация оборота, декабрьская
деградация выплат и дорогие споры. Шесть мер на слайде. Главные числа: 76,7 %,
2,2 → 4,2 дня, −281 млн. Спасибо!»

## 🇺🇿 O'zbekcha (4:00)

**0:00–0:40.** «Biz C trek jamoasimiz — MerchantHub ekvayringi. Buyurtmachi: "aylanma
qayerda, merchantlarga o'z vaqtida to'laymizmi, nizolar qanday". JOIN orqali 7
jadvalimizni topdik: 2025-yilning 80 000 operatsiyasi, 1 200 merchant, 51 052 to'lov,
1 986 nizo — barcha nizolar txn_id orqali aynan bizning tranzaksiyalarga birlashadi».

**0:40–1:40 · C1.** «Yillik aylanma 23,5 mlrd so'm. NTILE bilan detsillarga ajratdik:
top-10 % (120 merchant) aylanmaning 76,7 % ini beradi. Jini koeffitsiyenti 0,83 —
ekstremal konsentratsiya. Geografiya: poytaxt 6,5 mlrd, Janub — 1,4 mlrd (6 %).
Xulosa: qaramlik riski + Janubda o'sish zaxirasi».

**1:40–2:45 · C2 (bosh topilma).** «Yil bo'yi merchantlarga to'lovlar 2,2 kunda borgan.
1-dekabrdan — 4,2 kun: ikki baravar sekin. Sakrash bir kunda: 30-noyabr 2,3, 1-dekabr
4,1 — grafikda zinapoya. Mann–Uitni: p < 0,001. Va bu dekabr — cho'qqi oyi: 3,5 mlrd
so'mlik to'lovlar kechiktirilgan, merchantlarda eng qizg'in mavsumda kassa uzilishi.
1-dekabrdagi reliz/jarayon o'zgarishiga o'xshaydi. Yechim: o'zgarishni tahlil qilish,
T+2 SLA, mediana > 2,5 kun bo'lsa alert».

**2:45–3:30 · C3.** «1 682 yakunlangan nizodan 879 tasi yutqazilgan — 52 %, 281 mln so'm.
Konsentratsiya chastotada emas, pulda: high-risk kategoriyalar — keyslarning 22 % i,
lekin yutqazilgan pullarning 54 % i; o'rtacha nizo 881 ming — low dan 6 baravar katta.
χ²: p = 0,021. Yechim: high-risk uchun rolling-rezerv, dalil shablonlari, 14 kunlik KPI».

**3:30–4:00.** «Uch muammoli zona: mo'rt konsentratsiya, dekabr to'lovlar degradatsiyasi,
qimmat nizolar. Bosh raqamlar: 76,7 %, 2,2 → 4,2 kun, −281 mln. Rahmat!»

## Q&A tayyorgarlik

- **Dekabr sekinlashuvi hajm tufayli emasmi?** Yo'q: noyabrda ham hajm katta bo'lgan
  (4 977 to'lov), kechikish 2,2 kun edi. Sakrash bir kunda ro'y bergan — hajm asta
  o'sadi, jarayon o'zgarishi birdan.
- **52 % yutqazish normalmi?** Sanoat benchmarki ~40–50 %; bizda low-risk kategoriyalar
  eng ko'p yutqazadi (54,3 %) — dalillar yig'ish madaniyati yo'qligi belgisi, shuning
  uchun shablonlar tavsiya qilinadi.
- **Nega komissiya 1,49 %?** ds_settlements dagi commission_uzs / gross_amount_uzs
  nisbati; bu ekvayring daromadi — konsentratsiya riskining pul o'lchovi.
