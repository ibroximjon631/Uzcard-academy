# Himoya ssenariysi (UZ) — roppa-rosa 4 daqiqa

> Reglament: **4 daqiqa ma'ruza** (qat'iy, keyin to'xtatishadi) + 1 daqiqa savollar.
> Uyda taymer bilan kamida 3 marta mashq qiling. Quyida rollarga bo'lingan matn.

---

## 0:00–0:35 · 1–2-slaydlar · Ibroximjon — masala qo'yilishi

«Assalomu alaykum! Biz — D trek jamoasi, OqPay Super-App.

Buyurtmachi — OqPay rahbariyati — bizga xavotir bilan murojaat qildi: "bir oyda
buyurtmalar pasayishi va shikoyatlar o'sishini qayd etdik, sababini topa olmadik".

Biz bazadagi 31 ta jadvalni tahlil qilib, ustunlar va JOIN orqali o'z trekimizning
12 ta jadvalini aniqladik — bu 1,4 million qator: buyurtmalar, yetkazmalar, to'lovlar,
sharhlar, tiketlar va ilova hodisalari. 4 ta gipoteza ilgari surdik, har birini SQL
so'rovi, grafik va statistik test bilan tekshirdik».

## 0:35–1:20 · 3-slayd · Ibroximjon — 1-gipoteza (o'sish)

«Birinchi gipoteza: buyurtmalar pasayishi umuman bo'lganmi? Yo'q, bo'lmagan.

Buyurtmalar yil davomida o'rtacha oyiga 6 % o'sgan, trend dispersiyaning 99 % ini
tushuntiradi. Noyabr — mavsumiy cho'qqi: oktabrga nisbatan +23 %, trenddan 7,5 sigma
yuqori. Dekabr noyabrga nisbatan −12 % — lekin bu baribir oktabrdan 8 % ko'p va trend
chizig'idan atigi 5 % past. Ya'ni dekabrdagi "pasayish" — savdo cho'qqisidan keyin
trendga qaytish, biznes pasayishi emas. O'rtacha chek yil davomida barqaror.

Demak, buyurtmachini xavotirga solgan narsa boshqa joyda. Va biz uni topdik —
shikoyatlarda».

## 1:20–2:10 · 4-slayd · Ibroximjon — 2-gipoteza (ildiz sabab)

«Mana yetkazmalar kechikishining issiqlik xaritasi: shahar × oy. Yil davomida barcha
shaharlar 8–10 % atrofida. Va bitta katak — Samarqand, avgust: **93,5 %**. Butun oy
davomida shahardagi har o'nta yetkazmadan to'qqiztasi kechikkan.

Statistik jihatdan bu tasodif emas: 8,2 % normaga nisbatan farq 85 foiz punkti,
ikki ulush z-testi p < 0,001 beradi.

Muhimi: kechikish barcha kuryer turlarida bir xil — velosiped, mashina, piyoda,
samokat: 92–96 %. Inqiroz roppa-rosa 1-avgustda boshlanib, 31-avgustda tugagan.
Demak, aybdor kuryerlar emas, shahar tizimi: logistika habi, dispetcherlik yoki
pudratchi. Buyurtmachi izlagan ildiz sabab — shu».

## 2:10–2:55 · 5-slayd · 2-ishtirokchi — 3-gipoteza (oqibatlar)

«Endi oqibatlar. Avgustda qo'llab-quvvatlashga murojaatlar 73 % ga oshdi — 518 dan
896 ga. Butun o'sish bitta sabab — late_delivery, va bunday tiketlarning 62 % i
Samarqanddan.

Reyting: kechikkan yetkazmalarda o'rtacha baho 2,60, o'z vaqtidagilarda 4,37 —
Mann–Uitni testi bo'yicha farq yuqori darajada ahamiyatli. Samarqandning oylik
reytingi 4,2 dan 2,76 ga qulab, faqat oktabrga kelib tiklandi.

Lekin yaxshi yangilik bor: mijozlar oqib ketmadi. 60 kunlik takroriy xaridlar —
jabrlanganlar orasida 68,6 %, qolganlarda 67,4 %, p = 0,47 — farq yo'q. Mijozlar
OqPay ga ikkinchi imkoniyat berdi — lekin ikkinchi inqirozni kechirishmaydi».

## 2:55–3:30 · 6-slayd · 3-ishtirokchi — 4-gipoteza (fon risklari)

«Biz marketpleys va to'lovlarni ham tekshirdik — u yerda ikkita fon riski bor.

Birinchisi: bo'lib to'lash. Installment usuli to'lov urinishlarining 10,3 % ida rad
etadi — kartalardan ikki baravar ko'p; xi-kvadrat testi farqni tasdiqlaydi. Yil
davomida 458 buyurtma yakunlanmagan — qariyb bir milliard so'm.

Ikkinchisi: konsentratsiya. Smartfonlar daromadning 40 % ini, top-3 kategoriya uchdan
ikki qismini, sotuvchilarning top-10 % i aylanmaning yarmini beradi; Herfindal indeksi
2100 — yuqori konsentratsiya. Aynan shuning uchun bitta lokal nosozlik butun
kompaniyaga qattiq zarba beradi».

## 3:30–4:00 · 7-slayd · 3-ishtirokchi (yoki sardor) — tavsiyalar

«Buyurtmachiga harakatlar rejamiz, ustuvorlik bo'yicha:
bir — Samarqand logistikasi bilan insidentni tahlil qilish va jarimali SLA;
ikki — alert: shahar kechikishi bazadan 5 punktga 3 kun ketma-ket oshsa — eskalatsiya;
insident bir oyda emas, 3 kunda ko'rinadi;
uch — avgustda jabrlangan 940 foydalanuvchiga promo-aksiya, ular ketib qolmasidan;
to'rt — bo'lib to'lash shlyuzini audit qilish — yiliga 0,4 milliard so'mgacha GMV;
besh — daromadni top-3 kategoriyadan tashqariga diversifikatsiya qilish.

Tadqiqotimizning bosh raqami: bitta shahardagi bir oylik 93,5 % kechikish butun
kompaniya bo'ylab +73 % shikoyat berdi. E'tiboringiz uchun rahmat! Savollarga tayyormiz».

---

# Savollarga tayyorgarlik (1 daqiqa Q&A)

**— Kuryerlarga yuk oshgani sabab emasligini qayerdan bilasiz?**
Yuk barcha shaharlarda asta-sekin o'sgan (yil davomida kuryer boshiga 16 dan 33
yetkazmagacha), kechikish esa bir kunda 11 baravar sakragan va faqat bitta shaharda.
Ortiqcha yuk bo'lsa, noyabr cho'qqisida eng yomon raqamlarni ko'rardik — ular yo'q.

**— Balki avgustda Samarqandda buyurtma ko'p bo'lgandir?**
Yo'q: 1 033 yetkazma — iyuldagi (1 033) va sentabrdagi (1 091) bilan bir xil.
Hajm odatiy, kechikish anomal.

**— Mijozlar shunchalik norozi bo'lsa, nega oqib ketishmadi?**
60 kunlik takroriy buyurtmalarni tekshirdik: 68,6 % vs 67,4 %, z = 0,71, p = 0,47 —
statistik farq yo'q. Talqinimiz: kuchli odat/muqobil yo'qligi; lekin 2,76 reyting —
to'plangan obro' qarzi.

**— Qanday oynali funksiyalar ishlatdingiz?**
LAG — oyma-oy o'sish uchun, AVG OVER (6 PRECEDING) — 7 kunlik sirg'aluvchi o'rtacha,
SUM OVER va RANK/NTILE — daromadning jamlanma ulushi va sotuvchilar detsillari uchun.

**— Installment nega 10 % rad etadi?**
Ma'lumotlarda rad sababi belgilanmagan (to'lovlarda decline_reason ustuni yo'q). Biz
ikki baravar farq faktini qayd etamiz va shlyuz auditini tavsiya qilamiz — sababni
provayder loglaridan izlash kerak. «Bunga ma'lumot yetarli emas» degan halol javob —
o'ylab topilganidan yaxshi.

**— O'z trekingiz jadvallarini qanday ajratdingiz?**
Ustunlar va kalit qiymatlarining JOIN orqali mosligi bo'yicha: masalan, ds_orders.user_id
ds_users_1 bilan to'liq birlashadi (100 000 dan 100 000), ds_users_2 bilan esa yo'q.

**— Dekabr "pasayishi" — ma'lumotlar qirqilgan bo'lishi mumkinmi?**
Tekshirdik: ma'lumotlarda har oy roppa-rosa 28 kun savdoni o'z ichiga oladi (sintetika),
shuning uchun oylarni solishtirish to'g'ri; dekabr = kuniga 377 buyurtma, noyabrda 430,
oktabrda 349.

---

## Tayming eslatmasi

| Vaqt | Slayd | Kim | Blok |
|---|---|---|---|
| 0:00–0:35 | 1–2 | Ibroximjon | Masala va ma'lumotlar |
| 0:35–1:20 | 3 | Ibroximjon | H1 — pasayish yo'q |
| 1:20–2:10 | 4 | Ibroximjon | H2 — Samarqand/avgust |
| 2:10–2:55 | 5 | 2-ishtirokchi | H3 — shikoyat/reyting/ushlab qolish |
| 2:55–3:30 | 6 | 3-ishtirokchi | H4 — bo'lib to'lash/konsentratsiya |
| 3:30–4:00 | 7 | 3-ishtirokchi | Tavsiyalar + yakun |

*Jamoa 2 kishi bo'lsa: Ibroximjon 1–4 bloklarni (2:10 gacha), ikkinchi ishtirokchi H3, H4 va tavsiyalarni oladi.*
