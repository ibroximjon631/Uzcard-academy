# Трек A (UZCARD-XL) — сценарий защиты 4 минуты (RU + UZ)

## 🇷🇺 Русский (4:00)

**0:00–0:40 · Задача и данные.** «Мы — команда трека A, UZCARD-XL. Заказчик — продуктовая
и антифрод-команда процессинга: "кто наши клиенты, где растём, где теряем деньги —
отказы и спорные операции". Среди 31 таблицы нашли свои 5 по JOIN-ам: 60 320 операций
2023 года, 3 286 карт, 2 000 клиентов, 600 мерчантов, справочник MCC. Три гипотезы,
каждая со стат. тестом».

**0:40–1:40 · A1 (рост).** «Операции выросли с 769 до 12 864 в месяц — в 16 раз. Это не
аномалия, а ramp-up портфеля: активные карты растут синхронно, карты выпускаются с
2019 года. Темп фев–ноя +23 %/мес с замедлением к насыщению; декабрь +63 % — сезонный
пик. Важно: доля отказов при этом стабильна 5,5–6,9 % — рост нагрузку не сломал».

**1:40–2:40 · A2 (отказы студентов).** «А вот где ломается: сегмент student. Отказ на
11,2 % операций — вдвое выше остальных сегментов (5,8 %). Z-тест: +5,4 п.п., 95 % ДИ
4,2–6,5, z = 11,9, p < 0,001. Причины — 73 % insufficient_funds и limit, фрод-паттернов
нет. Это продуктовая проблема: студентам нужны микроовердрафт, уведомления о балансе
и смарт-ретраи при пополнении».

**2:40–3:30 · A3 (споры онлайн).** «Деньги теряются и в спорах: Online-мерчанты —
1,16 % оспоренных операций против 0,03–0,11 % офлайна, χ² = 400, p < 0,001. В деньгах
— 91 % всех спорных сумм: 103 млн UZS. Средний спорный чек втрое выше обычного.
Решение: обязательный 3-D Secure свыше 200 тыс UZS, скоринг e-com мерчантов, порог
мониторинга 1 %».

**3:30–4:00 · Финал.** «Итого: рост здоровый, а деньги теряются в двух точках — студенты
(каждая 9-я операция) и онлайн-споры (91 % спорных сумм). Пять мер на слайде. Главные
числа: 11,2 % и 103 млн. Спасибо!»

## 🇺🇿 O'zbekcha (4:00)

**0:00–0:40.** «Biz A trek jamoasimiz — UZCARD-XL protsessingi. Buyurtmachi: "mijozlar
kim, qayerda o'samiz, qayerda pul yo'qotamiz — radlar va nizolar". 31 jadvaldan JOIN
orqali o'zimizning 5 tasini topdik: 2023-yilning 60 320 operatsiyasi, 3 286 karta,
2 000 mijoz, 600 merchant. Uch gipoteza, har biri statistik test bilan».

**0:40–1:40 · A1.** «Operatsiyalar oyiga 769 dan 12 864 ga — 16 baravar o'sgan. Bu
anomaliya emas, portfel ramp-up i: faol kartalar sinxron o'sadi. Dekabr +63 % —
mavsumiy cho'qqi. Muhimi: radlar ulushi barqaror 5,5–6,9 % — o'sish sifatni buzmagan».

**1:40–2:40 · A2.** «Buzilish qayerda: student segmenti. Operatsiyalarning 11,2 % i rad
etiladi — boshqalardan ikki baravar ko'p (5,8 %). Z-test: +5,4 f.p., z = 11,9,
p < 0,001. Sabablarning 73 % i — mablag' yetishmasligi va limit, fird yo'q. Yechim:
mikro-overdraft, balans bildirishnomalari, to'ldirilganda avto-retray».

**2:40–3:30 · A3.** «Nizolar: Online-merchantlarda operatsiyalarning 1,16 % i nizolanadi
(oflaynda 0,03–0,11 %), χ² = 400, p < 0,001. Pulda — nizoli summalarning 91 % i:
103 mln so'm. Yechim: 200 ming so'mdan yuqorisiga majburiy 3-D Secure, e-com skoring».

**3:30–4:00.** «Xulosa: o'sish sog'lom, pul ikki nuqtada yo'qoladi — studentlar (har
9-operatsiya) va onlayn-nizolar (91 %). Bosh raqamlar: 11,2 % va 103 mln. Rahmat!»

## Q&A tayyorgarlik

- **Nega studentlarda rad ko'p?** Rad sabablari tarkibi boshqa segmentlar bilan bir xil
  (insufficient_funds + limit 73 %), lekin chastota 2×. Demak muammo xulq-atvorda emas,
  balans/limitning pastligida — mahsulot yechimi kerak, blokirovka emas.
- **Disputes jadvali nega sizniki emas?** ds_disputes.txn_id barcha 1 986 yozuvi bilan
  ds_transactions_1 (C trek) ga birlashadi; bizning transactions_2 da is_disputed flagi bor.
- **Dekabr +63 % ni qanday izohlaysiz?** Mavsumiy xarid cho'qqisi; portfel o'sish trendi
  (fev–noy) dan alohida ajratib ko'rsatdik, chunki trend regressiyasini yan–noy bo'yicha qurdik.
