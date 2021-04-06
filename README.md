## **vk-peoplestore-bot - многофункциональный бот для игры ["PeopleStore"](https://vk.com/app7809644) ВКонтакте.**

[Группа ВКонтакте](https://vk.com/club203597887), в ней публикуются новости и другая полезная информация. У группы есть беседа, в которой можно задавать вопросы.

**Лучшая благодарность - звёздочка на GitHub и "спасибо" в [ЛС в ВК](https://vk.com/id232357251).**

**Если хотите отблагодарить материально, пишите в [ЛС](https://vk.com/id232357251).**

## Установка на Windows

- Устанавливаем [Python](https://www.python.org/downloads/windows) (Для Windows 7 нужен [Python 3.8](https://python.org/ftp/python/3.8.8/python-3.8.8.exe)). Во время установки обязательно ставим галочку `Add Python to PATH (Добавить Python в PATH)`
- [Скачиваем архив с ботом](https://disk.yandex.ru/d/dPR3L2A5UyfYJg).
- Распаковываем архив.
- Редактируем файл `config.json` через любой текстовый редактор:
  - authorization:
    - Открываем [игру](https://vk.com/app7809644)
    - Нажимаем `F12` (Для Chromium браузеров)
    - Перезагружаем страницу горячей клавишей `F5`
    - В появившейся панели выбираем вкладку `Network`
    - Находим кнопку `Filter` (в виде воронки)
    - В появившемся поле пишем `start`
    - В панели появится поле `start?id=0`, нажимаем по нему
    - Появится еще одна панель, выбираем в ней вкладку `Headers`
    - Ищем поле `authorization`
    - Копируем его значение (начинается c **vk_access_token_settings**)
    - Вставляем скопированный текст в значение `authorization` в `config.json` между кавычками
  - my_id - **числовой** id вашей страницы ВКонтакте. Узнать можно через [сайт](https://regvk.com/id).
  - buy_slaves_mode - режим покупки рабов (0 - выкл, 1 - покупать случайных рабов, 2 - покупать рабов у игроков из топа, 3 - покупать рабов у людей из списка `"buy_from_ids"`)
  - buy_from_ids - ID людей через запятую, у которых вы хотите скупать рабов при `"mode": 3`. ID можно получить через [сайт](https://regvk.com/id).
  - buy_fetters - покупать ли оковы (0 - выкл, 1 - вкл)
  - upgrade_slaves - улучшать ли рабов для повышения дохода (0 - выкл, 1 - вкл)
  - min_price - минимальная цена для покупки раба. Значения выше 40 приведут к более долгому поиску рабов.
  - max_price - максимальная цена для покупки раба. Не советуем ставить выше 26151, потому что это будет невыгодно.
  - max_fetter_price - максимальная цена для покупки оков. Значение 35303 установлено для рабов с ценой 26151 (это выгодно).
  - job - названия устанавливаемых работ. Если хотите, чтобы была только одна работа, пишите так: `"job": ["ИмяРаботы"]`, иначе, пишите их через запятую, при этом берите каждое значение в кавычки, например: `"job": ["Повар", "Строитель", "Учитель", "Кассир"]`
  - min_delay - минимальная задержка между одинаковыми операциями в секундах. Чем ниже, тем выше вероятность получения блокировки на несколько часов.
  - max_delay - максимальная задержка между одинаковыми операциями в секундах. Чем ниже, тем выше вероятность получения блокировки на несколько часов.

Запуск: `start.bat`. Если после запуска ничего не происходит или выходит ошибка, связанная с Python или pip:

- Откройте `cmd`
- Напишите `python -V`
- Вывод должен соответстовать виду: `Python версия`. При этом версия должна быть выше **3.7.X**.
- Если вывод не соотвествует виду, нужно переустановить [Python](https://www.python.org/downloads/windows). Во время установки нужно обязательно поставить галочку `Add Python to Path (Добавить Python в PATH)`

## Установка на Termux (Android)

- Устанавливаем [Termux с F-Droid](https://f-droid.org/repo/com.termux_108.apk), т.к. в Google Play разработчик его больше не обновляет.
- Запускаем Termux.
- Пишем по порядку:
  - cd
  - pkg install -y git python
  - git clone https://github.com/
- Редактируем файл `config.json` командой `nano /config.json`. Для удобного редактирования можно скачать [приложение Hacker's Keyboard](https://play.google.com/store/apps/details?id=org.pocketworkstation.pckeyboard), в нём в горизонтальном положении есть стрелочки для управления курсором.
- Чтобы получить `authorization` с телефона, используем [приложение F12](https://play.google.com/store/apps/details?id=com.asfmapps.f12):
  - authorization:
    - Открываем приложение F12, заходим на [сайт мобильного ВКонтакте](https://m.vk.com) и авторизуемся.
    - Открываем ["PeopleStore"](https://m.vk.com/app7809644) через тот же F12.
    - Нажимаем кнопку F12, переходим на вкладку `Network` (3-я по счёту).
    - Ставим галочку около `Advance`.
    - Сворачиваем панель и нажимаем на стрелочку для перезагрузки страницы.
    - Вновь нажимаем кнопку F12, переходим на вкладку `Network`.
    - Немного листаем вверх и находим запись `https://peostore.mydzin.ru/api/start?id=0`, нажимаем по ней.
    - Появится ещё одна панель. Под записью Request Headers находим поле `authorization`.
    - Копируем его значение (начинается c **vk_access**, заканчивается при переходе на строку **User-Agent**).
    - Вставляем скопированный текст в значение `authorization` в `config.json` между кавычками.
- После редактирования файла, для сохранения нажмите Ctrl-O, Enter, Ctrl-X.

Запуск: `sh vk-peoplestore-bot/launch.sh`

## Переустановка в Termux

Ввести команды по порядку:

```
cd
rm -rf vk-peoplestore-bot
```

После этого заново установить по инструкции.
