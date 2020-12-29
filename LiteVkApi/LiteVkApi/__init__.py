class Vk():
    try:import vk_api
    except: raise ValueError('Ошибка авторизации (login):\n=====\nНе установлена библиотека vk_api - pip3 install vk_api\n=====')
    from vk_api.utils import get_random_id
    longpoll = ''
    vk = ''
    vk_session = ''
    event_msg = '' 
    key = ''
    server = ''
    ts = ''
    
    def help():
        print(' 1. login <id_group> <token> <chats=False> <my_key=0> <my_server=0> <my_ts=0> - входит в бота по указанному ID группы и токену. Если бот для беседы - поставьте chats=True и укажите параметры подключения\n \
    2. msg <text> <userid> <chats=False> - отправляет текст по указанному ID пользователя/чата, если он уже писал боту/бот состоит в беседе и имеет право писать сообщения. \n \
    3. check_new_msg <chats=False> - проверяет наличие новых сообщений, выдает True/False. \n \
    4. get_event - возвращает в переменную данные о сообщении. \n \
    5. send_photo <file_name> <userid> <msg=None> <chats=False> - отправляет фото с компьютера по указанному адресу пользователю с указанным ID/беседе и сообщением (по умолчанию без него) при выполнении условий из функции "msg". \n \
    6. new_keyboard <dicts> <perm=True> - создает клавиатуру по массиву со словарями, например - [{\'кнопка 1\':\'цвет 1\'}, {\'new_line\':\' \'}, {\'кнопка 2\':\'цвет 2\'}], perm обозначает, будет ли пропадать клавиатура после нажатия на кнопку (при True - не будет). Подробнее можно узнать в документации - !!!ссылку вставить потом!!! \n \
    7. send_keyboard <keyboard> <userid> <msg=\'Клавиатура!\'> <chats=False> - отправляет пользователю/беседе по ID  указанную клавиатуру, отправляя указанное сообщение\n \
    8. delete_keyboard <userid> <msg=\'Клавиатура закрыта!\'> <chats=False> - удаляет клавиатуру у указанного пользователя, отправляя указанное сообщение\n \
    9. send_file <file_name> <userid> <msg=None> <chats=False> - отправляет файл с компьютера по указанному адресу пользователю с указанным ID/беседе и сообщением (по умолчанию без него) при выполнении условий из функции "msg"')
    
    def login(id_group, tok, chats=False, my_key=0, my_server=0, my_ts=0):
        fun = 'help, login, msg, check_new_msg, get_event, send_photo, new_keyboard, send_keyboard, delete_keyboard. \
    Чтобы узнать подробнее о командах, вызовите функцию help - Vk.help()'
        global longpoll, vk, vk_session, server, ts, key
        import vk_api
        vk_session = vk_api.VkApi(token = tok)
        from vk_api.bot_longpoll import VkBotLongPoll
        vk = vk_session.get_api()
        try:
            longpoll = VkBotLongPoll(vk_session, id_group)
        except: raise ValueError('Ошибка авторизации (login):\n=====\nНе правильно введен один из параметров: id_group, token\n=====')
        if chats == True:
            if my_key == 0 or my_server == 0 or my_ts == 0:
                raise ValueError('Ошибка авторизации (login):\n=====\nУкажите значения key, server, ts! Их можно сгененировать тут - https://vk.com/dev/groups.getLongPollServer \n=====')
            else:
                key = my_key
                server = my_server
                ts = my_ts
        print('Привет! все мои функии: {}'.format(fun))
    
    def msg(text, userid, chats=False):
        from vk_api.utils import get_random_id
        try:
            if chats == False:
                vk.messages.send(user_id = userid, random_id = get_random_id(), message = text)
            elif chats == True:
                vk.messages.send(key = key, server = server, ts = ts, chat_id = userid, random_id = get_random_id(), message = text)
            else:
                raise ValueError('Ошибка отправки сообщения (msg):\n=====\nНе правильно введен параметр chats\n=====')
        except:
            raise ValueError('Ошибка отправки сообщения (msg):\n=====\nНе правильно введен параметр userid/диалог с пользователем не обозначен\
    (бот раньше не писал ему сообщения или не находится в беседе)\n=====')
    def check_new_msg(chat=False):
        from vk_api.longpoll import VkLongPoll, VkEventType
        global longpoll, vk_session, event_msg
        event_msg = ''
        Lslongpoll = VkLongPoll(vk_session)
        if chat == False:
            for event in Lslongpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    event_msg = event
                    return True
        elif chat == True:
            for event in Lslongpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    event_msg = event
                    return True
        else:
            raise ValueError('Ошибка поиска сообщений (check_new_msg):\n=====\nНе правильно введен параметр chats\n=====')
    
    def get_event():
        return event_msg
    
    def send_photo(file_name, userid, msg=None, chats=False):
        import vk_api
        from vk_api.utils import get_random_id
        upload = vk_api.VkUpload(vk_session)
        try:photo = upload.photo_messages(file_name)[0]
        except: raise ValueError(f'Ошибка отправки фото (send_photo):\n=====\nФото с именем {file_name} нет на компьютере!\n=====')
        attachment = 'photo{}_{}_{}'.format(photo['owner_id'], photo['id'], photo['access_key'])
        try:
            if chats == False:
                if msg == None: vk.messages.send(user_id=userid, random_id = get_random_id(), attachment=attachment)
                else: vk.messages.send(user_id=userid, random_id = get_random_id(), attachment=attachment, message = msg)
            elif chats == True:
                if msg == None: vk.messages.send(key = key, server = server, ts = ts, chat_id=userid, random_id = get_random_id(), attachment=attachment)
                else: vk.messages.send(key = key, server = server, ts = ts, chat_id=userid, random_id = get_random_id(), attachment=attachment, message = msg)
            else:
                raise ValueError('Ошибка отправки фото (send_photo):\n=====\nНе правильно введен параметр chats\n=====')
        except:
            raise ValueError('Ошибка отправки фото (send_photo):\n=====\nНе правильно введен один из параметров отправки сообщений\n=====')
    
    def send_file(file_name, userid, msg=None, chats=False):
        import vk_api
        from vk_api.utils import get_random_id
        upload = vk_api.VkUpload(vk_session)
        try:mydoc = upload.document_message(file_name, peer_id=userid)['doc']
        except: raise ValueError(f'Ошибка отправки файла (send_file):\n=====\nФайла с именем {file_name} нет на компьютере!\n=====')
        attachment = ('doc{}_{}'.format(mydoc['owner_id'], mydoc['id']))
        try:
            if chats == False:
                if msg == None: vk.messages.send(user_id=userid, random_id = get_random_id(), attachment=attachment)
                else: vk.messages.send(user_id=userid, random_id = get_random_id(), attachment=attachment, message = msg)
            elif chats == True:
                if msg == None: vk.messages.send(key = key, server = server, ts = ts, chat_id=userid, random_id = get_random_id(), attachment=attachment)
                else: vk.messages.send(key = key, server = server, ts = ts, chat_id=userid, random_id = get_random_id(), attachment=attachment, message = msg)
            else:
                raise ValueError('Ошибка отправки файла (send_file):\n=====\nНе правильно введен параметр chats\n=====')
        except:
            raise ValueError('Ошибка отправки файла (send_file):\n=====\nНе правильно введен один из параметров отправки сообщений\n=====')
    
    def new_keyboard(dicts, perm=True):
        from vk_api.keyboard import VkKeyboard, VkKeyboardColor
        if perm == False:
            keyboard = VkKeyboard(one_time=True)
        elif perm == True:
            keyboard = VkKeyboard(one_time=False)
        def color(title, col):
            col = str(col).upper()
            m = [['POSITIVE', '3', 'ЗЕЛЕНЫЙ'], ['NEGATIVE', '2', 'КРАСНЫЙ'], ['SECONDARY', '1', 'БЕЛЫЙ'], ['PRIMARY', '0', 'СИНИЙ']]
            if col in m[0]:
                keyboard.add_button(title, color=VkKeyboardColor.NEGATIVE)
            elif col in m[1]:
                keyboard.add_button(title, color=VkKeyboardColor.POSITIVE)
            elif col in m[2]:
                keyboard.add_button(title, color=VkKeyboardColor.SECONDARY)
            elif col in m[3]:
                keyboard.add_button(title, color=VkKeyboardColor.PRIMARY)
            else:
                raise ValueError('Ошибка создания клавиатуры (new_keyboard):\n=====\nНеправильно указан цвет/указан специальный объект клавиатуры\n=====')
        for dt in dicts:
            try:
                for i in dt.keys():
                    if i == 'new_line':
                        keyboard.add_line()
                    elif i == 'vk_pay':
                        keyboard.add_vkpay_button(hash=dt[i])
                    elif i == 'open_app':
                        for t in range(4):
                            dti = dt[i][t]
                            for key, value in dti.items():
                                if key == 'app_id':
                                    app_id = value
                                elif key == 'owner_id':
                                    owner_id = value
                                elif key == 'label':
                                    label = value
                                elif key == 'hash':
                                    hash1 = value
                        keyboard.add_vkapps_button(app_id, owner_id, label, hash1)
                    elif i == 'open_link':
                        for t in range(2):
                            dti = dt[i][t]
                            for key, value in dti.items():
                                if key == 'label':
                                    label = value
                                elif key == 'link':
                                    link = value
                        keyboard.add_openlink_button(label, link)
                    else:
                        color(i, dt[i])
            except:
                raise ValueError('Ошибка создания клавиатуры (new_keyboard):\n=====\nНеправильно указан один из параметров клавиатуры\n=====')
        return keyboard
    
    def send_keyboard(keyboard, userid, msg='Клавиатура!', chats=False):
        from vk_api.utils import get_random_id
        try:
            if chats == False:
                vk.messages.send(user_id = userid, random_id = get_random_id(), keyboard = keyboard.get_keyboard(), message = msg)
            elif chats == True:
                vk.messages.send(key = key, server = server, ts = ts, chat_id=userid, random_id = get_random_id(), keyboard = keyboard.get_keyboard(), message = msg)
            else:
                raise ValueError('Ошибка создания клавиатуры (new_keyboard):\n=====\nНе правильно введен параметр "chats"\n=====')
        except:
            raise ValueError('Ошибка отправки клавиатуры (send_keyboard):\n=====\nНе правильно введен параметр userid/диалог с пользователем не обозначен\
    (бот раньше не писал ему сообщения или не находится в беседе)\n=====')
    
    def delete_keyboard(userid, msg='Клавиатура закрыта!', chats=False):
        from vk_api.keyboard import VkKeyboard
        from vk_api.utils import get_random_id
        keyboard = VkKeyboard(one_time=True)
        keyboard.keyboard['buttons'] = []
        try:
            if chats == False:
                vk.messages.send(user_id = userid, random_id = get_random_id(), keyboard = keyboard.get_keyboard(), message = msg)
            elif chats == True:
                vk.messages.send(key = key, server = server, ts = ts, chat_id=userid, random_id = get_random_id(), keyboard = keyboard.get_keyboard(), message = msg)
            else:
                raise ValueError('Ошибка удаления клавиатуры (delete_keyboard):\n=====\nНе правильно введен параметр chats\n=====')
        except:
            raise ValueError('Ошибка удаления клавиатуры (delete_keyboard):\n=====\nНе правильно введен параметр userid/диалог с пользователем не обозначен\
    (бот раньше не писал ему сообщения или не находится в беседе)\n=====')
