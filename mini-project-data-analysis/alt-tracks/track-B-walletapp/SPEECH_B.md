# Трек B (WalletApp) — сценарий защиты 4 минуты (RU + UZ)

## 🇷🇺 Русский (4:00)

**0:00–0:40 · Задача и данные.** «Мы — команда трека B, WalletApp: кошелёк с подпиской.
Заказчик — продуктовый отдел: "пользователей много, платящих и удерживаемых мало —
найдите, где и почему теряем". Нашли свои 6 таблиц по JOIN-ам: 8 000 пользователей,
54 801 событие приложения, 1 659 подписок, 13 089 списаний, каналы с ценой установки.
Период: январь 2025 — июнь 2026».

**0:40–1:45 · B1 (воронка и каналы).** «Сквозная воронка: из 8 000 регистраций KYC
проходят 61 %, до первого платежа доходят 28 %. Главная утечка — верификация. Но
канальный разрез интереснее: telegram_ads доводит до платежа только 9,9 % против
28–42 % у остальных, z = 15,4, p < 0,001. В юнит-экономике: платящий из telegram стоит
91 тысячу сумов — в 13 раз дороже реферального (7 тысяч). Мы платим за мёртвый трафик.
Решение: бюджет telegram → referral, KYC упростить».

**1:45–2:45 · B2 (сбой биллинга).** «Смотрим собираемость подписочных списаний по
месяцам: весь период 2–5 % отказов, и один выброс — февраль 2026: 17,6 %, 201 списание
из 1 141 не прошло. Z-тест против остальных месяцев: z = 18,4, p < 0,001. Выручка
февраля упала на 9 % при растущем тренде. До и после — норма, значит сбой разовый:
шлюз или провайдер. Решение: dunning-ретраи 72 часа, резервный шлюз, алерт при
fail-rate выше 8 % за день».

**2:45–3:30 · B3 (подписки).** «Монетизация растёт: MRR с 1,9 до 54 млн сумов в месяц.
Но подписку отменяет каждый пятый: 18–21 % во всех тарифах, средняя жизнь 150 дней.
χ²-тест: p = 0,61 — отмены НЕ зависят от цены тарифа. Значит, проблема не в цене,
а в ценности. Решение: оффер удержания к 5-му месяцу, пауза вместо отмены, годовой тариф».

**3:30–4:00 · Финал.** «Ответ заказчику: теряем на KYC и в telegram-канале, разово
потеряли февраль из-за биллинга, а отток подписок — вопрос ценности, не цены. Пять мер
на слайде. Главные числа: 9,9 %, 17,6 %, 150 дней. Спасибо!»

## 🇺🇿 O'zbekcha (4:00)

**0:00–0:40.** «Biz B trek jamoasimiz — WalletApp obunali hamyoni. Buyurtmachi:
"foydalanuvchi ko'p, to'lovchi kam — qayerda yo'qotayotganimizni toping". JOIN orqali
6 jadvalimizni aniqladik: 8 000 foydalanuvchi, 54 801 hodisa, 1 659 obuna, 13 089
yechim. Davr: 2025-yanvar — 2026-iyun».

**0:40–1:45 · B1.** «Voronka: 8 000 ro'yxatdan o'tgandan KYC ni 61 % o'taydi, birinchi
to'lovga 28 % yetadi. Asosiy yo'qotish — verifikatsiya. Kanallar kesimi esa qiziqroq:
telegram_ads dan to'lovga atigi 9,9 % yetadi (boshqalarda 28–42 %), z = 15,4, p < 0,001.
To'lovchi narxi: telegram — 91 ming so'm, referral — 7 ming: 13 baravar farq. Yechim:
byudjetni referralga ko'chirish, KYC ni soddalashtirish».

**1:45–2:45 · B2.** «Obuna yechimlari: butun davr 2–5 % rad, bitta sakrash — 2026-fevral:
17,6 % (1 141 tadan 201 tasi o'tmagan), z = 18,4, p < 0,001. Fevral daromadi o'suvchi
trendda −9 %. Oldin va keyin norma — demak nosozlik bir martalik: shlyuz/provayder.
Yechim: 72 soatlik dunning-retray, zaxira shlyuz, kunlik fail-rate > 8 % alerti».

**2:45–3:30 · B3.** «MRR 1,9 dan 54 mln so'mga o'sdi. Lekin obunaning 18–21 % i bekor
qilinadi, o'rtacha umri 150 kun. χ²: p = 0,61 — bekor qilish tarif narxiga bog'liq EMAS.
Muammo narxda emas, qiymatda. Yechim: 5-oyga ushlab qolish taklifi, bekor o'rniga pauza,
yillik tarif».

**3:30–4:00.** «Javob: KYC va telegram kanalida yo'qotamiz, fevralni billing yedi,
obuna oqimi — qiymat masalasi. Bosh raqamlar: 9,9 %, 17,6 %, 150 kun. Rahmat!»

## Q&A tayyorgarlik

- **KYC nega 61 %?** Ma'lumotlarda KYC bosqichining ichki qadamlar yo'q — faqat kyc_done
  hodisasi. Chuqurroq diagnostika uchun bosqich ichi loglari kerak — buni tavsiyada aytdik.
- **Telegram trafigi nega yomon?** Ma'lumotlar javob bermaydi (kreativ/auditoriya
  ko'rinmaydi); biz faktni o'lchadik — kanal sifatining o'zi emas, natijasi. Qayta
  targeting yoki to'xtatish — marketing qarori.
- **MRR o'sishi qayerdan?** Yangi obunachilar oqimi (signup 2025–26 davomida) + tarif
  aralashmasi barqaror. LTV ≈ 5 × oylik narx (150 kun).
