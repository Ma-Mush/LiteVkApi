# =============================================================================
# Придумал и разработал - MaMush (vk.com/maks.mushtriev2, t.me/Error_mak25)
# Гитхаб - github.com/Ma-Mush/LiteVKApi
# PypI - pypi.org/project/litevkapi/
# =============================================================================
try:
    import vk_api
except ImportError as err:
    raise ImportError(
        "Ошибка авторизации (login):\n"
        "=====\nНе установлена библиотека "
        "vk_api - pip3 install vk_api\n====="
    ) from err

from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll
from threading import Thread

class Vk(object):

    def __init__(self, vk, vk_session, key, server, ts):
        self.vk, self.vk_session, self.key, self.server, self.ts, self.event_msg = vk, vk_session, key, server, ts, ""

    def help(self=0):
        print(
            "     1. login <id_group> <token> <userbot=False> <chats=False> <my_key=0> <my_server=0> <my_ts=0> - входит в бота по указанному ID группы и токену. Если бот (НО НЕ ЮЗЕР-БОТ!) для беседы - поставьте chats=True и укажите параметры подключения\n \
2. get_session - возвращает в переменную сессию в Вконтакте, чтобы при необходимости использования чистого Vk_api не входить и не нагружать сервер второй раз. \n \
3. give_session <session> <my_key=0> <my_server=0> <my_ts=0> - получает уже готовую Вк-сессию, если вы уже в нее вошли через vk_api или другие api для обхода login. \n \
4. msg <text> <userid> <chats=False> - отправляет текст по указанному ID пользователя/чата, если он уже писал боту/бот состоит в беседе и имеет право писать сообщения. \n \
5. check_new_msg <chats=False> - проверяет наличие новых сообщений, выдает True/False. \n \
6. get_event - возвращает в переменную данные о сообщении. \n \
7. send_photo <file_name> <userid> <msg=None> <chats=False> - отправляет фото с компьютера по указанному адресу пользователю с указанным ID/беседе и сообщением (по умолчанию без него) при выполнении условий из функции \"msg\". \n \
8. new_keyboard <dicts> <perm=True> - возвращает в переменную клавиатуру по массиву со словарями, например - [{'кнопка 1':'цвет 1'}, {'new_line':' '}, {'кнопка 2':'цвет 2'}], perm обозначает, будет ли пропадать клавиатура после нажатия на кнопку (при True - не будет). Подробнее можно узнать в документации - github.com/Ma-Mush/LiteVkApi \n \
9. send_keyboard <keyboard> <userid> <msg='Клавиатура!'> <chats=False> - отправляет пользователю/беседе по ID  указанную клавиатуру, отправляя указанное сообщение \n \
10. delete_keyboard <userid> <msg='Клавиатура закрыта!'> <chats=False> - удаляет клавиатуру у указанного пользователя, отправляя указанное сообщение \n \
11. send_file <file_name> <userid> <msg=None> <chats=False> - отправляет файл с компьютера по указанному адресу пользователю с указанным ID/беседе и сообщением (по умолчанию без него) при выполнении условий из функции \"msg\" \n \
12. mailing <text> <userids> <chats=False> - рассылка по ID пользователей/бесед \n \
13. get_all_message_data - возвращает в переменную массив со словарями. В словарях данные о последнем сообщении чата (беседы, ЛС) \n \
14. get_all_open_id <message_data=None> - возвращает в переменную id всех чатов/пользователей которые писали боту/где он находится. \n \
15. VkMethod <method_name> <arg> - возвращает в переменную результат метода Вконтакте (сделано для удобства)."
        )

    def login(
        id_group,
        tok,
        userbot=False,
        chats=False,
        my_key=0,
        my_server=0,
        my_ts=0,
    ):
        fun = "help, login, get_session, give_session, msg, check_new_msg, get_event, send_photo, new_keyboard, send_keyboard, delete_keyboard, send_file, mailing, get_all_message_data, get_all_open_id.\n\
Чтобы узнать подробнее о командах, вызовите функцию help - Vk.help()"
        try:
            vk_session = vk_api.VkApi(token=tok)
        except:
            raise ValueError(
                "Ошибка авторизации (login):\n=====\nНе действительный токен или указан id вместо токена\n====="
            )
        vk = vk_session.get_api()
        if userbot:
            try:
                VkLongPoll(vk_session)
            except:
                raise ValueError(
                    "Ошибка авторизации (login):\n=====\nНе правильно введен параметр token\n====="
                )
        else:
            try:
                VkBotLongPoll(vk_session, id_group)
            except:
                raise ValueError(
                    "Ошибка авторизации (login):\n=====\nНе правильно введен один из параметров: id_group, token\n====="
                )
            if chats == True:
                if my_key == 0 or my_server == 0 or my_ts == 0:
                    raise ValueError(
                        "Ошибка авторизации (login):\n=====\nУкажите значения key, server, ts! Их можно сгененировать тут - https://vk.com/dev/groups.getLongPollServer \n====="
                    )
        
        print("Привет! все мои функии: {}".format(fun))
        return Vk(vk, vk_session, my_key, my_server, my_ts)

    def get_session(self):
        return self.vk_session

    def give_session(session, my_key=0, my_server=0, my_ts=0):
        vk = session.get_api()
        return Vk(vk, session, my_key, my_server, my_ts)

    def msg(self, text, userid, chats=False):
        def _sysmsg_(**k):
            def _sysmsg2_(**k):
                self.vk.messages.send(**k)
            t = Thread(target=_sysmsg2_, kwargs=k)
            t.start()
        try:
            if chats == False:
                _sysmsg_(
                    peer_id=userid, random_id=get_random_id(), message=text
                )
            elif chats == True:
                _sysmsg_(
                    key=self.key,
                    server=self.server,
                    ts=self.ts,
                    peer_id=userid,
                    random_id=get_random_id(),
                    message=text,
                )
            else:
                raise ValueError(
                    "Ошибка отправки сообщения (msg):\n=====\nНе правильно введен параметр chats\n====="
                )
        except:
            raise ValueError(
                "Ошибка отправки сообщения (msg):\n=====\nНе правильно введен параметр userid/диалог с пользователем не обозначен\
(бот раньше не писал ему сообщения или не находится в беседе)\n====="
            )

    def check_new_msg(self, chat=False):
        longpoll = VkLongPoll(self.vk_session)
        if not chat:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    self.event_msg = event
                    return True
        elif chat:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    self.event_msg = event
                    return True
        else:
            raise ValueError(
                "Ошибка поиска сообщений (check_new_msg):\n=====\nНе правильно введен параметр chats\n====="
            )

    def get_event(self):
        return self.event_msg

    def send_photo(self, file_name, userid, msg=None, chats=False):
        upload = vk_api.VkUpload(self.vk_session)
        try:
            photo = upload.photo_messages(file_name)[0]
        except:
            raise ValueError(
                f"Ошибка отправки фото (send_photo):\n=====\nФото с именем {file_name} нет на компьютере!\n====="
            )
        attachment = "photo{}_{}_{}".format(
            photo["owner_id"], photo["id"], photo["access_key"]
        )
        
        def _sysmsg_(**k):
            def _sysmsg2_(**k):
                self.vk.messages.send(**k)
            t = Thread(target=_sysmsg2_, kwargs=k)
            t.start()
        
        try:
            if not chats:
                if msg == None:
                    _sysmsg_(
                        peer_id=userid,
                        random_id=get_random_id(),
                        attachment=attachment,
                    )
                else:
                    _sysmsg_(
                        peer_id=userid,
                        random_id=get_random_id(),
                        attachment=attachment,
                        message=msg,
                    )
            elif chats:
                params = dict(
                    key=self.key,
                    server=self.server,
                    ts=self.ts,
                    peer_id=userid,
                    random_id=get_random_id(),
                    attachment=attachment,
                )
                if msg is not None:
                    params.update(message=msg)

                _sysmsg_(**params)
            else:
                raise ValueError(
                    "Ошибка отправки фото (send_photo):\n=====\nНе правильно введен параметр chats\n====="
                )
        except:
            raise ValueError(
                "Ошибка отправки фото (send_photo):\n=====\nНе правильно введен один из параметров отправки сообщений\n====="
            )

    def send_file(self, file_name, userid, msg=None, chats=False):
        upload = vk_api.VkUpload(self.vk_session)
        try:
            mydoc = upload.document_message(file_name, peer_id=userid)["doc"]
        except:
            raise ValueError(
                f"Ошибка отправки файла (send_file):\n=====\nФайла с именем {file_name} нет на компьютере!\n====="
            )
        attachment = "doc{}_{}".format(mydoc["owner_id"], mydoc["id"])
        def _sysmsg_(**k):
            def _sysmsg2_(**k):
                self.vk.messages.send(**k)
            t = Thread(target=_sysmsg2_, kwargs=k)
            t.start()
        try:
            if not chats:
                if msg == None:
                    _sysmsg_(
                        peer_id=userid,
                        random_id=get_random_id(),
                        attachment=attachment,
                    )
                else:
                    _sysmsg_(
                        peer_id=userid,
                        random_id=get_random_id(),
                        attachment=attachment,
                        message=msg,
                    )
            elif chats:
                if msg is None:
                    _sysmsg_(
                        key=self.key,
                        server=self.server,
                        ts=self.ts,
                        peer_id=userid,
                        random_id=get_random_id(),
                        attachment=attachment,
                    )
                else:
                    _sysmsg_(
                        key=self.key,
                        server=self.server,
                        ts=self.ts,
                        peer_id=userid,
                        random_id=get_random_id(),
                        attachment=attachment,
                        message=msg,
                    )
            else:
                raise ValueError(
                    "Ошибка отправки файла (send_file):\n=====\nНе правильно введен параметр chats\n====="
                )
        except:
            raise ValueError(
                "Ошибка отправки файла (send_file):\n=====\nНе правильно введен один из параметров отправки сообщений\n====="
            )

    def new_keyboard(self, dicts, perm=True):
        from vk_api.keyboard import VkKeyboard, VkKeyboardColor
        
        if not perm:
            keyboard = VkKeyboard(one_time=True)
        elif perm:
            keyboard = VkKeyboard(one_time=False)
            
        def color(title, col):
            col = str(col).upper()
            m = [
                ["POSITIVE", "3", "ЗЕЛЕНЫЙ"],
                ["NEGATIVE", "2", "КРАСНЫЙ"],
                ["SECONDARY", "1", "БЕЛЫЙ"],
                ["PRIMARY", "0", "СИНИЙ"],
            ]
            if col in m[0]:
                keyboard.add_button(title, color=VkKeyboardColor.NEGATIVE)
            elif col in m[1]:
                keyboard.add_button(title, color=VkKeyboardColor.POSITIVE)
            elif col in m[2]:
                keyboard.add_button(title, color=VkKeyboardColor.SECONDARY)
            elif col in m[3]:
                keyboard.add_button(title, color=VkKeyboardColor.PRIMARY)
            else:
                raise ValueError(
                    "Ошибка создания клавиатуры (new_keyboard):\n=====\nНеправильно указан цвет/указан специальный объект клавиатуры\n====="
                )
        
        for dt in dicts:
            try:
                for i in dt.keys():
                    if i == "new_line":
                        keyboard.add_line()
                    elif i == "vk_pay":
                        keyboard.add_vkpay_button(hash=dt[i])
                    elif i == "open_app":
                        for t in range(4):
                            dti = dt[i][t]
                            for key, value in dti.items():
                                if key == "app_id":
                                    app_id = value
                                elif key == "owner_id":
                                    owner_id = value
                                elif key == "label":
                                    label = value
                                elif key == "hash":
                                    hash1 = value
                        keyboard.add_vkapps_button(
                            app_id, owner_id, label, hash1
                        )
                    elif i == "open_link":
                        for t in range(2):
                            dti = dt[i][t]
                            for key, value in dti.items():
                                if key == "label":
                                    label = value
                                elif key == "link":
                                    link = value
                        keyboard.add_openlink_button(label, link)
                    else:
                        color(i, dt[i])
            except:
                raise ValueError(
                    "Ошибка создания клавиатуры (new_keyboard):\n=====\nНеправильно указан один из параметров клавиатуры\n====="
                )
        return keyboard

    def send_keyboard(self, keyboard, userid, msg="Клавиатура!", chats=False):
        def _sysmsg_(**k):
            def _sysmsg2_(**k):
                self.vk.messages.send(**k)
            t = Thread(target=_sysmsg2_, kwargs=k)
            t.start()
        try:
            if chats:
                _sysmsg_(
                    key=self.key,
                    server=self.server,
                    ts=self.ts,
                    peer_id=userid,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message=msg,
                )
            
            else:
                _sysmsg_(
                    peer_id=userid,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message=msg,
                )
        except:
            raise ValueError(
                "Ошибка отправки клавиатуры (send_keyboard):\n=====\nНе правильно введен параметр userid/диалог с пользователем не обозначен\
(бот раньше не писал ему сообщения или не находится в беседе)\n====="
            )

    def delete_keyboard(self, userid, msg="Клавиатура закрыта!", chats=False):
        from vk_api.keyboard import VkKeyboard
        from vk_api.utils import get_random_id
        
        keyboard = VkKeyboard(one_time=True)
        keyboard.keyboard["buttons"] = []
        
        def _sysmsg_(**k):
            def _sysmsg2_(**k):
                self.vk.messages.send(**k)
            t = Thread(target=_sysmsg2_, kwargs=k)
            t.start()
        
        try:
            if chats:
                _sysmsg_(
                    key=self.key,
                    server=self.server,
                    ts=self.ts,
                    peer_id=userid,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message=msg,
                )
            else:
                _sysmsg_(
                    peer_id=userid,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message=msg,
                )
        except:
            raise ValueError(
                "Ошибка удаления клавиатуры (delete_keyboard):\n=====\nНе правильно введен параметр userid/диалог с пользователем не обозначен\
(бот раньше не писал ему сообщения или не находится в беседе)\n====="
            )

    def mailing(self, text, userids, safe=[], chats=False):
        def r(text, userids):
            try:
                for i in userids:
                    try:
                        if i not in safe:
                            Vk.msg(text, i, chats)
                    except:
                        1
            except:
                raise ValueError(
                    "Ошибка рассылки (mailing):\n=====\nПередан НЕ массив в значение userids или ошибка отправки сообщения\n====="
                )
                
        t = Thread(target=r, args=(text, userids))
        t.start()

    def get_all_message_data(self):
        v = self.vk_session.method("messages.getConversations", {"count": 200})
        ret = []
        ch = 0
        vv = 0
        for i in v["items"]:
            ret.append(i["last_message"])
            ch += 1
        while True:
            if ch == 200 or vv == 199:
                vv = 0
                v = self.vk_session.method(
                    "messages.getConversations",
                    {"count": 200, "start_message_id": ret[ch - 1]["id"]},
                )
                del v["items"][0]
                for i in v["items"]:
                    ret.append(i["last_message"])
                    ch += 1
                    vv += 1
            else:
                break
        del ch, vv, v
        return ret

    def get_all_open_id(self, message_data=None):
        if message_data is None:
            message_data = Vk.get_all_message_data(self)
        ret = []
        for i in message_data:
            ret.append(i["peer_id"])
        del message_data
        return ret

    def VkMethod(self, method_name, arg):
        return self.vk_session.method(method_name, arg)
