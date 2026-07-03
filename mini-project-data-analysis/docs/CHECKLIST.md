# ✅ Checklist — nimalar qilishingiz kerak / Что вам нужно сделать

> **Yangi fayllar:** to'liq tushuntirish — `docs/HISOBOT_UZ.md` (o'qishdan boshlang!),
> 10–15 daqiqalik to'liq nutq — `docs/SPEECH_FULL_UZ.md` / `_RU.md` (tayyorgarlik uchun;
> himoyada baribir 4 daqiqalik versiya ishlatiladi — reglament qat'iy!),
> o'zbekcha prezentatsiya — `presentation/OqPay_TrackD_UZ.pptx`,
> zaxira treklar A/B/C — `alt-tracks/` (agar jamoa boshqa trek tanlasa).

## 🇺🇿 O'zbekcha

### Darhol (bugun)
- [ ] **Jamoa tuzing** — platformadagi «Проект» bo'limida: 2–3 kishi, o'z guruhingizdan
      (ertalabki yoki kechki). Sardor jamoa yaratadi va ishtirokchilarni taklif qiladi.
- [ ] **Guruhingizni ko'rsating** (ertalab/kech) — birinchi kirishda so'raladi.
- [ ] **Slot band qiling** — kamida 2 tasdiqlangan ishtirokchi bo'lgach, sardor
      himoya kunlaridan birini tanlaydi: 07.07, 09.07, 10.07 yoki 14.07.2026.
      Erta band qilgan — qulay vaqtni oladi.

### Loyihani moslashtirish (himoyadan 2–3 kun oldin)
- [ ] `notebooks/oqpay_analysis.ipynb` da **«Участник 2» va «Участник 3» o'rniga
      jamoadoshlaringiz ismlarini yozing** (sarlavha jadvali + H3, H4 bo'limlari).
- [ ] `presentation/OqPay_TrackD.pptx` da ham xuddi shu ismlarni almashtiring
      (1, 5, 6-slaydlar).
- [ ] Har bir jamoadosh **o'z gipotezasini o'qib chiqsin va tushunsin** — himoyada
      har kim o'z qismini o'zi gapiradi va savollarga o'zi javob beradi.
- [ ] Jamoadoshlar notebookdagi o'z bo'limining SQL so'rovlarini **o'zi ishlatib
      ko'rsin** (bazaga har kimning o'z logini bor).
- [ ] Agar jamoa 2 kishi bo'lsa: gipotezalarni 2+2 qilib bo'lib oling
      (SPEECH fayllarida taqsimot varianti yozilgan).

### Mashq (himoyadan 1–2 kun oldin)
- [ ] `docs/SPEECH_UZ.md` yoki `SPEECH_RU.md` ni **taymer bilan 3 marta** o'qib mashq
      qiling — 4 daqiqadan oshmang, oshgan joyda gapni qisqartiring.
- [ ] Q&A bo'limidagi 7 ta savol-javobni har kim o'qib chiqsin.
- [ ] Slaydlarni ochib, kim qaysi slaydda gapirishini kelishib oling.

### Topshirish (himoya boshlanishidan OLDIN)
- [ ] Notebook + prezentatsiyani https://academy-avu.pages.dev/teams ga yuklang:
      `notebooks/oqpay_analysis.ipynb` va `presentation/OqPay_TrackD.pptx`.
- [ ] Yuklashdan oldin notebookni oxirgi marta to'liq ishga tushirib tekshiring
      (Kernel → Restart & Run All) — barcha kataklarda natija bo'lsin.

---

## 🇷🇺 Русский

### Сразу (сегодня)
- [ ] **Соберите команду** в разделе «Проект» на платформе: 2–3 человека из своей
      группы (утренней или вечерней). Капитан создаёт команду и приглашает участников.
- [ ] **Укажите свою группу** (утро/вечер) при первом входе.
- [ ] **Забронируйте слот защиты**, когда будет ≥2 подтверждённых участника:
      07.07, 09.07, 10.07 или 14.07.2026. Кто раньше бронирует — выбирает время.

### Персонализация проекта (за 2–3 дня до защиты)
- [ ] В `notebooks/oqpay_analysis.ipynb` **замените «Участник 2» и «Участник 3»
      на имена сокомандников** (таблица в шапке + заголовки H3, H4).
- [ ] То же в `presentation/OqPay_TrackD.pptx` (слайды 1, 5, 6).
- [ ] Каждый участник **разбирает свою гипотезу**: на защите каждый представляет
      свою часть сам и сам отвечает на вопросы по ней.
- [ ] Сокомандники должны **сами прогнать SQL своего раздела** (у каждого свой
      логин к базе).
- [ ] Если в команде 2 человека — делите гипотезы 2+2 (вариант расписан в SPEECH).

### Репетиция (за 1–2 дня)
- [ ] Прогоните `docs/SPEECH_RU.md` **с таймером 3 раза** — строго ≤ 4 минут;
      что не влезает — режьте.
- [ ] Каждый читает блок Q&A (7 готовых ответов на вероятные вопросы).
- [ ] Договоритесь, кто щёлкает слайды.

### Сдача (ДО начала защиты)
- [ ] Загрузите на https://academy-avu.pages.dev/teams:
      `notebooks/oqpay_analysis.ipynb` и `presentation/OqPay_TrackD.pptx`.
- [ ] Перед загрузкой прогоните notebook целиком (Kernel → Restart & Run All).

---

## Покрытие критериев оценивания / Baholash mezonlari qoplanishi

| Критерий (балл) | Чем закрыто |
|---|---|
| Гипотезы, оригинальность — 15 | 4 гипотезы, не дублируются: рост/сезонность, корневая причина, CX+удержание, платежи+концентрация; у каждой — нетривиальный вывод («просадки нет», «оттока нет») |
| Анализ SQL+Python — 20 | JOIN (5+ таблиц), CTE, коррелированный подзапрос EXISTS, LAG/AVG OVER/SUM OVER/RANK/NTILE, pandas, 11 графиков |
| Представление своей части — 15 | готовый сценарий с хронометражем + Q&A (docs/SPEECH_*) |
| Интеграция гипотез — 15 | единый сюжет: «просадки нет → причина в Самарканде → последствия для CX → фоновые риски → план» |
| Практическая рекомендация — 15 | 5 мер с ожидаемым эффектом (слайд 7, итоговый раздел notebook) |
| Презентация и тайминг — 20 | 7 слайдов, 1 слайд = 1 мысль, ключевое число + график на каждом; тайминг расписан по 30-секундным блокам |
| Стат. обоснованность (обязательно для трека D — у каждого участника!) | H1: тренд-регрессия + 95% ДИ; H2: z-тест долей + ДИ; H3: Манна–Уитни + z-тест; H4: χ² + HHI/Парето |
