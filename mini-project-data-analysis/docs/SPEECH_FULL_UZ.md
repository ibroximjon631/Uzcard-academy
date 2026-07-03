# To'liq himoya nutqi (UZ) — 10–15 daqiqalik versiya

> ⚠️ **MUHIM OGOHLANTIRISH:** Topshiriq reglamentida qat'iy yozilgan: **doklad 4 daqiqadan
> oshsa, to'xtatiladi va ko'rsatilmagan qism baholanmaydi**. Bu fayl — sizga materialni
> **to'liq tushunish va savollarga chuqur javob berish** uchun. Himoyaning o'zida
> `SPEECH_UZ.md` dagi 4 daqiqalik versiyani ishlating! Agar o'qituvchi qo'shimcha vaqt
> bersa yoki seminar formatida so'zlash imkoni bo'lsa — mana bu to'liq versiya.

---

## 1-qism. Kirish va masala qo'yilishi (~1,5 daqiqa)

Assalomu alaykum, hurmatli ustozlar va kursdoshlar! Biz D trek jamoasimiz, loyihamiz —
OqPay Super-App: to'lovlar, marketpleys va yetkazib berish xizmatini birlashtirgan
super-ilova.

Bizga shartli buyurtmachi — OqPay rahbariyati — shunday masala qo'ydi: «Bir oyda biz
buyurtmalar pasayishi va shikoyatlar sonining o'sishini qayd etdik, lekin sababini
aniqlay olmadik. O'sish dinamikasi, marketpleys va yetkazib berishni tahlil qilib,
sababni toping va harakatlar rejasini taklif qiling».

E'tibor bering: bu klassik "root cause analysis" — ildiz sababni izlash masalasi.
Bizga tayyor savollar ham, jadval ro'yxati ham berilmadi. Bazada 31 ta `ds_` prefiksli
jadval bor edi va ularda to'rt xil biznes sohasining ma'lumotlari aralashgan.

**Birinchi ishimiz — ma'lumotlarni arxeologiya qilish bo'ldi:**
- `information_schema` orqali barcha jadvallar va ustunlarini chiqardik;
- ustun nomlari va namunaviy qiymatlar bo'yicha qaysi jadval qaysi trekka tegishli
  ekanini aniqladik;
- eng muhimi — bog'lanishlarni **haqiqiy JOIN bilan** tekshirdik: masalan,
  `ds_orders.user_id` bilan `ds_users_1.user_id` 100 000 tadan 100 000 tasi birlashadi,
  `ds_users_2` bilan esa umuman birlashmaydi. Shunday qilib, nom o'xshashligiga
  aldanmasdan, qiymatlar mosligiga tayandik.

Natijada D trekning 12 ta jadvalini aniqladik — jami **1,4 million qator**: 15 000
foydalanuvchi, 100 000 buyurtma, 220 000 buyurtma pozitsiyasi, 100 000 yetkazma,
106 000 to'lov urinishi, 780 000 ilova hodisasi, 54 000 sharh, 6 600 support-tiket,
6 000 mahsulot, 1 500 sotuvchi, 400 kuryer. Davr — 2025-yil 1-yanvardan 28-dekabrgacha.

To'rtta gipoteza ilgari surdik — har birimiz bittadan himoya qilamiz — va har birini
uch qatlamda tekshirdik: SQL so'rovi → grafik → statistik test. Endi navbati bilan.

---

## 2-qism. H1 — «Buyurtmalar pasayishi» aslida bo'lganmi? (~2,5 daqiqa)

Buyurtmachi «buyurtmalar pasaydi» dedi. Tekshirishdan boshladik — va bu juda muhim
qadam: **mijoz his qilgan muammo har doim ham ma'lumotlarda tasdiqlanavermaydi**.

SQL tomonda `WITH monthly` CTE ichida oylik buyurtmalarni sanab, `LAG` oynali
funksiyasi bilan oyma-oy o'sish sur'atini hisobladik. Natija:

- Yanvar: 5 658 buyurtma. Dekabr: 10 564. Yil davomida **har oy o'sish**.
- O'rtacha o'sish sur'ati: **+6,1 % oyiga** (95 % ishonch intervali: 0,7 % dan 11,5 % gacha).
- Log-chiziqli trend regressiyasi: oyiga +6,0 %, **R² = 0,99** — ya'ni dispersiyaning
  99 % i oddiy eksponensial trend bilan tushuntiriladi, p < 0,001.

Faqat bitta oyda "minus" bor: dekabr, noyabrga nisbatan −12 %. Xo'sh, bu pasayishmi?
Yo'q, va buni statistik ko'rsatamiz:

- **Noyabr** trenddan +14 % yuqorida turibdi — qoldiq z-bahosi **+7,5 sigma**. Bu
  mavsumiy savdo cho'qqisi (Black Friday tipidagi noyabr aksiyalari).
- **Dekabr** esa trend chizig'idan atigi −5 % pastda va **oktabrdan +8 % yuqori**.
  Ya'ni dekabr "yomon oy" emas — noyabr "g'ayrioddiy zo'r oy" bo'lgan. Talabning bir
  qismi noyabrda oldindan xarid qilingan (pull-forward effekti).

Yana bir tekshiruv o'tkazdik — halollik uchun: sintetik ma'lumotlarda har oyda
roppa-rosa 28 kunlik savdo borligini aniqladik, demak oylarni bir-biri bilan
taqqoslash to'g'ri, kalendar uzunligi xalaqit bermaydi.

O'rtacha chek ham barqaror: yil davomida 1,70–1,81 million so'm oralig'ida.

**H1 xulosasi:** biznes pasaymagan, aksincha barqaror o'smoqda. Demak, buyurtmachini
xavotirga solgan narsa buyurtmalar hajmida emas. Qayerda? Shikoyatlarda. Va shikoyatlar
bizni to'g'ri manzilga olib bordi.

---

## 3-qism. H2 — Ildiz sabab: Samarqand, avgust (~3 daqiqa)

Yetkazib berish jadvalini (`ds_deliveries`) buyurtmalar bilan JOIN qilib, har bir
shahar va oy uchun kechikish foizini hisobladik — mana bu issiqlik xaritasi
(heatmap) chiqdi.

Rasmni ko'ring: butun yil, o'nta shahar — hamma katakchalar 6–13 % oralig'ida.
Va **bitta katak: Samarqand, avgust — 93,5 %**. O'nta yetkazmadan to'qqiztasi kechikkan.
Butun oy davomida.

Bu tasodif emasligini isbotlaymiz. Ikki ulushni taqqoslovchi z-test:
- Samarqand, avgust: 1 033 yetkazmadan 966 tasi kechikkan = 93,5 %;
- Samarqand, qolgan 11 oy: 11 101 tadan 911 tasi = 8,2 %;
- Farq: **+85,3 foiz punkti**, 95 % ishonch intervali [83,7; 86,9], z = 72,5,
  **p-qiymat amalda nol**. Bunday farq tasodifan yuzaga kelishi mumkin emas.

Endi eng qiziq savol: **aybdor kim?** Uchta versiyani tekshirdik:

**1-versiya: kuryerlar yetishmagan / yuk oshgan?** Yo'q. Kuryer boshiga yuk butun yil
silliq o'sgan (oyiga 16 tadan 33 tagacha yetkazma), avgustda sakrash yo'q. Avgustdagi
yetkazmalar soni (1 033) iyuldagi bilan bir xil. Hajm odatiy — kechikish anomal.

**2-versiya: muayyan transport turi (masalan, velosipedchilar)?** Yo'q. Kunlik kesimda
qaradik: velosiped — 93 %, avtomobil — 93 %, piyoda — 92 %, samokat — 96 %. **Hammasi
birdek kechikkan.** Agar sabab kuryerlarda bo'lsa, turlar orasida farq bo'lardi.

**3-versiya: tizimli shahar darajasidagi nosozlik.** Mana bu tasdiqlandi. Kunlik
grafikka qarang (7 kunlik sirg'aluvchi o'rtacha bilan, buni SQL da `AVG OVER (ORDER BY
day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` oynali funksiyasi bilan hisobladik):
kechikish **roppa-rosa 1-avgustda** 10 % dan 90+ % ga sakraydi va **roppa-rosa
1-sentabrda** joyiga tushadi. Chegaralar kalendar oyiga aniq mos — bu oylik shartnoma,
relíz yoki ombor ko'chishiga o'xshaydi: shahardagi logistika habi, marshrutlash tizimi
yoki pudratchi bilan bog'liq muammo.

**H2 xulosasi:** buyurtmachi izlagan ildiz sabab — 2025-yil 1–31 avgustda Samarqand
shahridagi tizimli logistika inqirozi. Bitta shahar, bitta oy — lekin oqibatlari
butun kompaniyaga urilgan. Buni keyingi gipotezada ko'ramiz.

---

## 4-qism. H3 — Oqibatlar: shikoyat, reyting, ushlab qolish (~3 daqiqa)

Insident mijozlarga qanday ta'sir qildi? Uch o'lchovda o'lchadik.

**Birinchi o'lchov — shikoyatlar.** Iyulda 518 ta support-tiket bo'lgan, avgustda 896 ta
— **+73 %**. Tiketlarni sabablarga ajratsak (stacked bar grafik): butun o'sish yagona
sabab — `late_delivery`. Avgustda bunday tiketlar 661 ta bo'lgan, shundan **408 tasi
(62 %) Samarqand buyurtmalariga** tegishli — bu deyarli oyning butun prirostiga teng
(+378). Ya'ni: shikoyatlar sakrashi = Samarqand insidenti. Zanjir yopildi.

**Ikkinchi o'lchov — reyting.** Barcha buyurtmalar bo'yicha: o'z vaqtida yetkazilgan
buyurtmalarning o'rtacha bahosi 4,37, kechikkanlarniki — 2,60. Bu farq ahamiyatlimi?
Reyting — tartibli (ordinal) shkala, shuning uchun o'rtachalar t-testi emas,
**Mann–Uitni U-testini** qo'lladik: p < 0,001, farq yuqori darajada ahamiyatli.
Shahar kesimida: Samarqandning oylik reytingi avgustda 4,2 dan **2,76 ga** qulagan
va faqat oktabrga kelib tiklangan. Boshqa shaharlarda reyting qimirlamagan — bu ham
insidentning lokalligini tasdiqlaydi.

**Uchinchi o'lchov — mijozlarni yo'qotdikmi?** Bu eng muhim biznes-savol. Metodika:
avgustda birinchi buyurtmasi kechikkan foydalanuvchilarni (940 kishi) va o'z vaqtida
olganlarni (4 093 kishi) olib, har biri **keyingi 60 kun ichida yana buyurtma
berganmi** — tekshirdik (SQL da korrelyatsiyalangan `EXISTS` pastki so'rovi bilan).

Natija kutilmagan bo'ldi: kechikkanlarning 68,6 % i qaytib xarid qilgan, o'z
vaqtidagilarning 67,4 % i. z = 0,71, **p = 0,47 — statistik farq YO'Q**.

Bu nimani anglatadi? Mijozlar oqib ketmagan — OqPay ga ikkinchi imkoniyat berishgan.
Ehtimol kuchli odat yoki muqobil yo'qligi sabab. **Lekin bu omad, strategiya emas:**
reyting 2,76 — bu to'plangan obro' qarzi. Ikkinchi bunday insident kechirilmaydi.
Shuning uchun tavsiyalarimizda jabrlangan 940 mijozga proaktiv promo-kampaniya bor —
ular hali mijoz, ularni mustahkamlash hozir arzon.

**H3 xulosasi:** zarar hozircha operatsion (896 tiket — bu support xarajati) va
reputatsion (reyting 2,76), lekin oqim (churn) boshlanmagan. Harakat qilish oynasi ochiq.

---

## 5-qism. H4 — Fon risklari: konsentratsiya va bo'lib to'lash (~2,5 daqiqa)

Buyurtmachi marketpleys haqida ham so'ragan edi. Insidentdan tashqari ikkita tizimli
xavfni aniqladik.

**Birinchi xavf — daromad konsentratsiyasi.** `ds_order_items` ni mahsulotlar va
kategoriyalar bilan JOIN qilib, `SUM OVER` oynali funksiyasi bilan jamlanma ulushlarni
hisobladik:
- **Smartfonlar — daromadning 40 %** (70 mlrd so'mdan ortiq);
- top-3 kategoriya (smartfonlar, mebel, audio) — **67 %**;
- Herfindal–Hirshman indeksi: **HHI = 2 133** — 1 800 dan yuqori, ya'ni rasman yuqori
  konsentratsiya zonasi;
- sotuvchilar kesimida `NTILE(10)` bilan detsillarga ajratdik: **top-10 % sotuvchilar
  aylanmaning 49,5 % ini** beradi.

Nega bu muhim? Chunki konsentratsiya — mo'rtlik. Avgust insidenti buni jonli ko'rsatdi:
bitta bo'g'in ishdan chiqsa, butun kompaniya ko'rsatkichlari buziladi.

**Ikkinchi xavf — to'lovlarda.** To'lov usullari bo'yicha rad etish foizlari: UZCARD
4,9 %, HUMO 5,0 %, VISA 5,1 % — bir tekis. **Installment (bo'lib to'lash) esa 10,3 %**
— ikki baravar yuqori. χ²-testi: χ² = 809, p < 0,001 — farq mutlaqo ahamiyatli.
Yil davomida 458 ta buyurtma umuman to'lanmay qolgan — bu **0,85 mlrd so'm** GMV.

Muhim halollik: ma'lumotlarda to'lov rad sababi yozilmagan (payments jadvalida
decline_reason ustuni yo'q), shuning uchun biz «nega» degan savolga ma'lumotlar bilan
javob bera olmaymiz — shlyuz auditi kerak, deb tavsiya qilamiz. Taxmin emas, fakt
chegarasida qolamiz.

**Voronka esa sog'lom:** ilova hodisalari (`ds_events`, 780 000 qator) bo'yicha:
mahsulot ko'rish → savat 69 %, savat → checkout 85 %, checkout → muvaffaqiyatli to'lov
99,5 %. Asosiy yo'qotish yuqori voronkada (ko'rish→savat) — bu normal e-commerce holati,
pastki voronka ideal ishlaydi.

**H4 xulosasi:** ikki fon riski — konsentratsiya (HHI 2133) va bo'lib to'lash (10,3 %
rad, 0,85 mlrd yo'qotish). Ikkalasi ham boshqariladigan, quyida rejada.

---

## 6-qism. Tavsiyalar va yakun (~2 daqiqa)

Endi hammasi bir rasmga yig'iladi. Buyurtmachining savoliga javobimiz:

> **«Pasayish» aslida bo'lmagan — dekabr noyabr cho'qqisidan keyingi normal korreksiya.
> Shikoyatlar sakrashining ildiz sababi — 2025-yil avgustida Samarqanddagi bir oylik
> tizimli logistika inqirozi. Mijozlar hali ketmagan, lekin reyting jarohatlangan.**

Besh bandlik harakatlar rejasi, ustuvorlik tartibida:

1. **Insident tahlili** — Samarqand logistika pudratchisi/habi bilan 1-avgustda nima
   o'zgargganini aniqlash; kechikish uchun jarimali SLA imzolash. *Effekt: takrorlanishdan
   himoya.*
2. **Erta ogohlantirish tizimi** — har shahar uchun kunlik kechikish monitoringi: agar
   shahar kechikishi o'z bazasidan 5 foiz punktga 3 kun ketma-ket oshsa — avtomatik
   eskalatsiya. *Effekt: keyingi insident bir oyda emas, 3 kunda ushlanadi. Bu oddiy
   SQL so'rov + alert — arzon va samarali.*
3. **Ishonchni qaytarish kampaniyasi** — avgustda jabrlangan 940 foydalanuvchiga
   personal promo/uzr. *Effekt: yuz bermagan oqimni mustahkamlash; 940 kishiga promo
   — yangi mijoz jalb qilishdan ancha arzon.*
4. **Bo'lib to'lash shlyuzi auditi** — 10,3 % rad sababini provayder loglaridan topish.
   *Effekt: radlarni karta darajasiga (5 %) tushirsak, yiliga ~0,4 mlrd so'm GMV qaytadi.*
5. **Diversifikatsiya strategiyasi** — top-3 kategoriyadan tashqari kategoriyalarni
   rivojlantirish, o'rta sotuvchilar qatlamini kengaytirish. *Effekt: HHI pasayadi,
   biznes lokal zarbalarga chidamli bo'ladi.*

Va yakuniy bosh raqam — butun tadqiqotni bir jumlaga sig'diradigan:

> **Bitta shaharda bir oylik 93,5 % kechikish — butun kompaniya bo'ylab +73 % shikoyat
> va shahar reytingining 4,2 dan 2,76 ga qulashi.**

Lokal muammolar lokal bo'lib qolmaydi. Ularni erta ushlash tizimini qurish — bizning
asosiy tavsiyamiz.

E'tiboringiz uchun rahmat! Savollarga tayyormiz.

---

## Texnik lug'at — savol kelsa tushuntirib bera olishingiz uchun

| Atama | Oddiy tilda |
|---|---|
| **CTE (`WITH ...`)** | So'rov ichidagi "vaqtinchalik jadval" — murakkab so'rovni bosqichlarga bo'lish usuli |
| **Oynali funksiya (`OVER`)** | Qatorlarni guruhlab yig'madan turib, har qator uchun "qo'shnilar bo'yicha" hisob: `LAG` — oldingi qator qiymati, `AVG OVER ... ROWS 6 PRECEDING` — 7 kunlik sirg'aluvchi o'rtacha, `SUM OVER` — jamlanma yig'indi, `NTILE(10)` — detsillarga bo'lish, `RANK` — tartib raqami |
| **z-test (ikki ulush)** | Ikki foizni taqqoslash: farq tasodifiymi? z qancha katta bo'lsa, tasodif ehtimoli shuncha kichik |
| **p-qiymat** | «Agar aslida farq bo'lmasa, shunday natija tasodifan chiqish ehtimoli». p < 0,05 → farq ahamiyatli deymiz |
| **95 % ishonch intervali (II/ДИ)** | Haqiqiy qiymat 95 % ishonch bilan yotadigan oraliq |
| **Mann–Uitni U-testi** | O'rtacha o'rniga rang (tartib) bo'yicha taqqoslash — reyting kabi ordinal shkalalar uchun to'g'ri test |
| **χ² (xi-kvadrat)** | Jadvaldagi ulushlar (masalan, to'lov usuli × rad) bir-biridan bog'liqmi-yo'qmi tekshiradi |
| **R²** | Trend ma'lumotlarni qancha yaxshi tushuntirishi (0–1); bizda 0,99 |
| **z-baho (sigma)** | Nuqta trenddan necha "standart og'ish" uzoqda: ±2 dan tashqarisi — anomaliya |
| **HHI** | Konsentratsiya indeksi: ulushlar kvadratlari yig'indisi; > 1 800 — yuqori konsentratsiya |
| **Pull-forward** | Aksiya paytida kelajak talabning oldindan xarid qilinishi (noyabr → dekabr effekti) |
| **GMV** | Gross Merchandise Value — platformadan o'tgan tovar aylanmasi |
| **Churn / retention** | Mijozlarning ketishi / ushlanib qolishi |
