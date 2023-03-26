# LiteVkApi
Бот в Вк? Легко!

Pypi - https://pypi.org/project/LiteVkApi/

[![Downloads](https://pepy.tech/badge/litevkapi)](https://pepy.tech/project/litevkapi)


# КРАТКАЯ ДОКУМЕНТАЦИЯ
Привет! Эта библиотека создана для быстрого написания ботов (преимущественно ЛС) в ВК. Мне захотелось, чтобы ботов писать было быстро и легко, поэтому я сделал удобную библиотеку с самыми популярными функциями vk_api. Сейчас я расскажу вам о ней!

P.s. Если вы читаете это в PypI, то у вас могут некорректно отображаться таблички с пояснениями функций. На Гитхабе все хорошо - https://github.com/Ma-Mush/LiteVkApi/

## Импорты
Для начала установите vk_api, если он не установлен - pip3 install vk_api

Скрипт библиотеки написан в виде функций и различных переменных в классе, поэтому можно использовать несколько вариантов импорта:
Рекомендую - from LiteVkApi import Client (будет описана здесь), import LiteVkApi (придется использовать LiteVkApi.Client._), < один из предыдущих вариантов > as < название > (вместо названия импортированного модуля можно использовать свое имя)

<br>======
 <details>  <summary> Что нового в обновлении 2.4.2</summary> 

### - Изменены параметры фунцкий Client.check_new_msg и Client.check_new_events
Теперь они принимают параметр botlongpoll (True/False, по умолчанию - False). Он определяет, использовать ЛонгПул для ботов или общий. Разница в том, что у общего привычный формат возращения событий - event.text и тд. ЛонгПул для ботов же имеет бОльшие возможности. Так, с его помощью можно получать отвтеты на callback кнопки с полезной нагрузкой (payload), такие как snack_bar. Но и формат ответа для "традиционных" типов событий у них другой. Так, при получении сообщения его текст будет записан в event.message.text. Пример кода с кнопкой и обработкой сообщений будет в соответсвующем разделе внизу документации.


</details> 
======<br>
<br>


# Классы

## - Client - класс взаимодействия с Вк

<details> <summary>Функции</summary> 

* ## Client.login(token, id_group, userbot, my_key, my_server, my_ts) *
    ### Функция ВСЕГДА имеет объект Client
    Функция регистрирует вас на сервере ВКонтакте и возвращает сессию в переменную.
    <details> <summary>Параметры</summary>

    Название  | Что это?
    ------------- | -------------
    token | Токен сообщества в виде строки (например 'a244f42a6eaec65dbeh1ee13aab8ce7355311448868357e545c27cd648025c8a31ee66f4528a0a4ca98be')
    id_group | id группы в числовом виде (например 200397283), если используется юзер-бот - любое число или None (нужен, только если вы используете токен группы)
    userbot | Для страницы (а не для группы) вы используете бота? (True/False) По умолчанию False
    get_session | Если True - возвращает сессию в переменную (для удобства использования вместе vk_api). По умолчанию False
    ост. | Настройки для беседы, узать тут - https://vk.com/dev/groups.getLongPollServer

    </details>

* ## _.get_session()
    Возвращает сессию Вконтакте, т.е. ели вы уже вошли через Client.login и вам надо пользоваться обычным vk_api, то вы можете использовать эту сессию, чтобы не входить снова. (Тоже самое на vk_api - vk_session = vk_api.VkApi(token = токен))

* ## Client.give_session(session) *
    #### Функция ВСЕГДА имеет объект Client
    Регистрирует вашу сессию Вк, но только если вы уже входили через другие api и передали ее в параметр session (для vk_api сессия получается через session = vk_api.VkApi(token = токен))
    <details> <summary>Параметры</summary>

    Название  | Что это?
    ------------- | -------------
    session | Сессия в Вк от vk_api
    ост. | Настройки для беседы, узать тут - https://vk.com/dev/groups.getLongPollServer
        
    </details> 
        
* ## _.msg(text, userid, photo, files, keyboard, reply_to)
    Отправляет сообщение пользователю по ID / беседе по ее номеру с заданным текстом
    <details> <summary>Параметры</summary>
        
    Название  | Что это?
    ------------- | -------------
    text | Текст сообщения 
    userid | ID пользователя/беседы для отправкии сообщеия
    photo | Массив с путями до фотографий, которые нужно отправить
    files | Массив с путями до файлов, которые нужно отправить
    keyboard | Клавиатура, полученная с помощью Keyboard (подробнее - ниже)
    reply_to | ID сообщения, на котороее нужно ответить
        
    </details> 

* ## _.send_message(text, userid, photo, files, keyboard, reply_to)
    То же самое, что и _.msg

* ## _.edit_message(text, userid, messid, photo, files, keyboard)
    Изменяет сообщение по ID
    <details> <summary>Параметры</summary>
        
    Название  | Что это?
    ------------- | -------------
    text | Текст сообщения 
    userid | ID пользователя/беседы, куда было отправлено сообщение
    messid | ID сообщения, которое нужно изменить
    photo | Массив с путями до фотографий, которые нужно отправить
    files | Массив с путями до файлов, которые нужно отправить
    keyboard | Клавиатура, полученная с помощью Keyboard (подробнее - ниже)

    </details> 

* ## _.check_new_msg(botlongpoll)
    Используется для проверки новых сообщений (возвращает True / False)
    <details> <summary>Параметры</summary>

    Название  | Что это?
    ------------- | -------------
    botlongpoll | Использовать ЛонгПул для ботов или общий (True / False)? По умолчанию False

    </details> 

* ## _.check_new_events(botlongpoll)
    Используется для проверки любых новых событий (а не только сообщений, как в check_new_msg). В остальном - аналогичная функция. (возвращает True / False)
    <details> <summary>Параметры</summary>

    Название  | Что это?
    ------------- | -------------
    botlongpoll | Использовать ЛонгПул для ботов или общий (True / False)? По умолчанию False

    </details> 
    
* ## _.get_event()
    Возвращает данные о новом сообщении при его наличии. Основные параметры выданных данных - user_id / chat_id, text. Подробнее в документации vk_api.

* ## _.send_photo(file_names, userid, msg, keyboard)
    Отправляет фото с сообщением / без него пользователю/беседе.
    <details> <summary>Параметры</summary>
        
    Название  | Что это?
    ------------- | -------------
    file_name | массив файлов в директории запущенного питон-файла или полный путь к нему
    userid | ID пользователя/беседы для отправкии сообщеия
    msg | Текст сообщения (по умолчанию без него)
    keyboard | Клавиатура, полученная с помощью Keyboard (подробнее - ниже)
        
    </details> 

* ## _.send_file(file_names, userid, msg, keyboard)
    Отправляет файл с сообщением / без него пользователю/беседе.
    <details> <summary>Параметры</summary>
        
    Название  | Что это?
    ------------- | -------------
    file_names | Массив файлов в директории запущенного питон-файла или полный путь к нему
    userid | ID пользователя/беседы для отправкии сообщеия
    msg | Текст сообщения (по умолчанию без него)
    keyboard | Клавиатура, полученная с помощью Keyboard (подробнее - ниже)

    </details> 

* ## _.send_keyboard(keyboard, userid, msg)
    Отправляем пользователю созданнуб раннее клавиатуру
    <details> <summary>Параметры</summary>
        
    Название  | Что это?
    ------------- | -------------
    keyboard | Клавиатура, созданная раннее
    userid | Ид пользователя / беседы
    msg | Сообщение при отправке клавиатуры (по умолчанию 'Клавиатура!')
        
    </details> 

* ## _.delete_keyboard(userid, msg)
    Удаляет клавиатуру у пользователя. 
    <details> <summary>Параметры</summary>
        
    Название  | Что это?
    ------------- | -------------
    userid | Ид пользователя / беседы
    msg | Сообщение при удалении клавиатуры (по умолчанию 'Клавиатура закрыта!')

    </details>  
    
* ## _.mailing(text, userids, safe)
    Делает рассылку независимо от других действий (бот будет отвечать во время рассылки).
    <details> <summary>Параметры</summary>
        
    Название  | Что это?
    ------------- | -------------
    text | Текст сообщения
    userids | Массив с ID пользователей / бесед (например - [123456, 1234567, 12345678])
    safe | Массив с ID пользователей / бесед, которые отказались от рассылки, по умолчанию таких нет

    </details> 
    
* ## _.get_all_message_data()
    Возвращает массив со словарями с данными о последних сообщениях всех чатов, где находился бот (и ЛС, и беседы, и боты). Внимание! Функция достаточно долгая для ботов с большой аудиторией. Может занимать от долей секунды до нескольких минут.
    <details> <summary>Что находится в словарях:</summary>

    Название  | Что это?
    ------------- | -------------
    date | Количиство секунд с 01.01.1970 00:00 UTC, также как time.time()
    from_id | Id группы или пользователя, кто отправил последнее сообщение (может быть как и бот, так и пользователь)
    id | Id этого сообщения
    out | 0 / 1, 0 - последнее сообщение присали вам, 1 - последнее сообщение прислали вы
    peer_id | Id чата - chat_id если это беседа, user_id если это Лс (ну или id группы если это бот)
    random_id | Какой рандомный Id у сообщения (нужен для его отправки, фактически бесполезен)
    text | Текст сообщения
    attachments | Описание вложений (фото, видео, файлы, стикеры и тд.) последнего сообщения (если это просто текст - [])
    admin_author_id | Если out=1 и писал не бот, а человек, то в этот параметр передается id админа, который писал сообщение
    update_time | Если сообщение редактировали, то передается время редактирования в формате, как в date
    conversation_message_id | Уникальный автоматически увеличивающийся номер для всех сообщений с этим peer
    fwd_messages | Массив пересланных сообщений, если они есть (если нет - [])
    important | В документации не нашел, скорее всего избарнный (важный) чат или нет (True/False)
    is_hidden | В документации не нашел, скорее всего скрытое сообщение (удалено у меня) или нет (но это не точно) (True/False)

    </details> 
        

* ## _.get_all_open_id(message_data)
    Возвращает в переменную массив с Id всех пользоватлей, которые когда-либо писали боту или id бесед, где он находится (куда ему можно писать - для рассылки)
    <details> <summary>Параметры</summary>
        
    Название  | Что это?
    ------------- | -------------
    message_data | Данные, полученные с помощью get_all_message_data*, по умолчанию None, функция * вызывается автоматически

    </details>  
    
* ## _.VkMethod(method_name, arg)
    Возвращает в переменную данные, полученные в результате запроса с помощью Вк-метода. Создана для удобства, чтобы не имортировать vk_api и получать сессию)
    <details> <summary>Параметры</summary>
    
    Название  | Что это?
    ------------- | -------------
    method_name | Назване Вк-метода (все методы тут - https://vk.com/dev/methods )
    arg | Параметры для метода в виде словаря

    </details> 
    
</details>

## - Keyboard - класс для создания клавиатуры 
<details> <summary>Описание</summary>
    
Название  | Что это?
------------- | -------------
permanent | При True - клавиатуру можно нажимать много раз, при False - пропадает после первого
inline | При True - клавиатура в сообщении, при False - как обычно, снизу экрана
buttons* | Двойной массив, заполенный массивами, в которых объекты - кнопки, полученные из класса Buttons (ниже)


    * Подробнее про праметр "buttons". Это двойной массив, имеет вид [[кнопка, кнопка], [кнопка]]. Как нетрудно догадаться - вложенные массивы подразумевают строки с кнопками. То есть, если вы хотите разместить 2 кнопки на первой строке, а еще 1 на второй - используйте конструкнию выше. При 3-ух кнопках по одной на строке - [[кнопка], [кнопка], [кнопка]]. 
</details>

## - Button - класс для создания кнопок для клавиатуры (Keyboard)
<details> <summary>Функции</summary> 

* ## Button.text(label, color, callback, payload)
    Возвращает обычную кнопку с текстом
    <details> <summary>Параметры</summary>
    
    Название  | Что это?
    ------------- | -------------
    label | Текст кнопки
    color | Цвет (Синий - 'primary', '0', 'синий'; Белый - 'secondary', '1', 'белый'; Красный - 'negative', '2', 'красный'; Зелёный - 'positive', '3', 'зеленый')
    callback | Коллбэк это кнопка или нет (True/False)
    payload | Данные для старых клиентов ВК (я сам хз че это, в доке Вк так написано)

    </details>


* ## Button.url(label, link, payload)
    Возвращает кнопку с ссылкой
    <details> <summary>Параметры</summary>

    Название  | Что это?
    ------------- | -------------
    label | Текст кнопки
    link | Ссылка, которая будет открыта при нажатии
    payload | Данные для старых клиентов ВК

    </details>

* ## Button.open_app(app_id, owner_id, label, hash, payload)
    Возвращает кнопку для открытия указанного приложения VK mini apps
    <details> <summary>Параметры</summary>

    Название  | Что это?
    ------------- | -------------
    app_id | ID приложения
    app_hash | Хэш приложения
    label | Текст кнопки
    hash | Хэш 
    payload | Данные для старых клиентов ВК

    </details>

* ## Button.vk_pay(hash, payload)
    Возвращает кнопку для открытия VK pay
    <details> <summary>Параметры</summary>

    Название  | Что это?
    ------------- | -------------
    hash | Хэш аккаунта VK pay
    payload | Данные для старых клиентов ВК

    </details>

</details> <br> 


# Примеры
## Отправка сообщения с тем же текстом, тому же пользователю, что и прислали нам:
```python
from LiteVkApi import Client
vk_session = Client.login("твой токен", твой ид)
while True:
    if vk_session.check_new_msg():
        event = vk_session.get_event()
        vk_session.msg(event.text, event.user_id)
```
## Простейший бот:
```python
from LiteVkApi import Client
vk_session = Client.login("твой токен", твой ид)
while True:
    if vk_session.check_new_msg():
        event = vk_session.get_event()
        eventxt, userid = event.text, event.user_id
        if eventxt == 'Привет':
            vk_session.msg(f'Привет, {userid}', userid)
        elif eventxt == 'Как дела?':
            vk_session.msg('Хорошо, а у тебя?', userid)
```
## Создание, отправка и удаление клавиатуры:
```python
from LiteVkApi import Client
vk_session = Client.login("твой токен", твой ид)
keyboard = Keyboard(True, False, [[Button.text("Клавиатура", "синий")], [Button.text("Закрыть клавиатуру", "синий")], [Button.url("Создатель библиотеки", "https://vk.com/maks.mushtriev2")]])
while True:
    if vk_session.check_new_msg():
        event = vk_session.get_event()
        if event.text == 'Клавиатура':
            vk_session.send_keyboard(keyboard, event.user_id, 'А вот и клавиатура!')
        elif event.text == 'Закрыть клавиатуру':
            vk_session.delete_keyboard(event.user_id, 'Теперь клавиатура закрыта!')
```
## Отправка файла и фото:
```python
from LiteVkApi import Vk
vk_session = Vk.login("твой токен", твой ид)
while True:
    if vk_session.check_new_msg():
        event = vk_session.get_event()
        try:
            vk_session.send_photo([event.text], event.user_id, 'Отправляю фото...')
            vk_session.send_file([event.text], event.user_id, 'Отправляю файл...')
        except:
            vk_session.msg('Не могу найти файл {} или указанный файл не является фотографией'.format(event.text), event.user_id)
```
## Рассылка кому только можно
```python
from LiteVkApi import Vk
vk_session = Vk.login("твой токен", твой ид)
mass_ids = vk_session.get_all_open_id()
vk_session.mailing('Рассылка!', mass_ids)
```
## Использование BotLongPoll с callback кнопкой
```python
from LiteVkApi import Client, Keyboard, Button 
from vk_api.bot_longpoll import VkBotEventType 
import json 
 
vk_session = Client.login("твой токен", айди группы, True) 
vk = vk_session.vk

keyboard = Keyboard(True, True, [[Button.text("Клавиатура", "3")], [Button.text("Закрыть клавиатуру", "1")], [Button.text("Создатель библиотеки", "2", True, {"type": "show_snackbar", "text": "MaMush"})]]) 

while True: 
    if vk_session.check_new_events(True):
        event = vk_session.get_event() 
        if event.type == VkBotEventType.MESSAGE_NEW:
            eventxt, userid = event.message.text.lower(), event.message.from_id
            if eventxt == 'привет': 
                vk_session.msg(f'Привет, {userid}', userid) 
                vk_session.send_keyboard(keyboard, userid, 'А вот и клавиатура!') 
        if event.type == VkBotEventType.MESSAGE_EVENT: 
            vk_session.VkMethod(
                "messages.sendMessageEventAnswer", 
                    {
                    "event_id":event.object.event_id, 
                    "user_id":event.object.user_id, 
                    "peer_id":event.object.peer_id,  
                    "event_data":json.dumps(event.object.payload)
                    }
                )
```

# Контакты

Что-то не работает, есть вопросы, пожелания? Пиши - [Telegram](https://t.me/Error_mak25), [VK](https://vk.com/maks.mushtriev2)

Мой блог - [Telegram](https://t.me/mamush_blog),  [VK](https://vk.com/mamush_blog)

Донат - [Киви, оплата кошельком/номером телефона/любой картой без комиссии (тык)](https://qiwi.com/n/NADEZNIEINVEST)


### Удачи!
