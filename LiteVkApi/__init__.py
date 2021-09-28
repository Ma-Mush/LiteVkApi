# =============================================================================
# Придумал и разработал - MaMush (vk.com/maks.mushtriev2, t.me/Error_mak25)
# Гитхаб - github.com/Ma-Mush/LiteVKApi
# PypI - pypi.org/project/litevkapi/


# Убрал help, лишние [], {} в клаве, LiteVkApiError, callback клава
# =============================================================================
try:
    import vk_api
except: raise ImportError(
        "Ошибка авторизации (login):\n =====\nНе установлена библиотека vk_api - pip3 install vk_api\n====="
    )

from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll
from threading import Thread

class LiteVkApiError(Exception):
    pass

class Vk(object):

    def __init__(self, vk, vk_session, key, server, ts):
        self.vk, self.vk_session, self.key, self.server, self.ts, self.event_msg = vk, vk_session, key, server, ts, ""

    def login(
        id_group,
        tok,
        userbot=False,
        chats=False,
        my_key=0,
        my_server=0,
        my_ts=0,
    ):
        try:
            vk_session = vk_api.VkApi(token=tok)
        except:
            raise LiteVkApiError(
                "Ошибка авторизации (login):\n=====\nНе действительный токен или указан id вместо токена\n====="
            )
        vk = vk_session.get_api()
        if userbot:
            try:
                VkLongPoll(vk_session)
            except:
                raise LiteVkApiError(
                    "Ошибка авторизации (login):\n=====\nНе правильно введен параметр token\n====="
                )
        else:
            try:
                VkBotLongPoll(vk_session, id_group)
            except:
                raise LiteVkApiError(
                    "Ошибка авторизации (login):\n=====\nНе правильно введен один из параметров: id_group, token\n====="
                )
            if chats == True:
                if my_key == 0 or my_server == 0 or my_ts == 0:
                    raise LiteVkApiError(
                        "Ошибка авторизации (login):\n=====\nУкажите значения key, server, ts! Их можно сгененировать тут - https://vk.com/dev/groups.getLongPollServer \n====="
                    )
        
        return Vk(vk, vk_session, my_key, my_server, my_ts) # Я знаю, что это ужасно, но не хочу отходить от Vk.login()

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
                raise LiteVkApiError(
                    "Ошибка отправки сообщения (msg):\n=====\nНе правильно введен параметр chats\n====="
                )
        except:
            raise LiteVkApiError(
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
            raise LiteVkApiError(
                "Ошибка поиска сообщений (check_new_msg):\n=====\nНе правильно введен параметр chats\n====="
            )

    def get_event(self):
        return self.event_msg
    
    def send_photo(self, file_name, userid, msg=None, chats=False):
        upload = vk_api.VkUpload(self.vk_session)
        try:
            photo = upload.photo_messages(file_name)[0]
        except:
            raise LiteVkApiError(
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
                raise LiteVkApiError(
                    "Ошибка отправки фото (send_photo):\n=====\nНе правильно введен параметр chats\n====="
                )
        except:
            raise LiteVkApiError(
                "Ошибка отправки фото (send_photo):\n=====\nНе правильно введен один из параметров отправки сообщений\n====="
            )

    def send_file(self, file_name, userid, msg=None, chats=False):
        upload = vk_api.VkUpload(self.vk_session)
        try:
            mydoc = upload.document_message(file_name, peer_id=userid)["doc"]
        except:
            raise LiteVkApiError(
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
                raise LiteVkApiError(
                    "Ошибка отправки файла (send_file):\n=====\nНе правильно введен параметр chats\n====="
                )
        except:
            raise LiteVkApiError(
                "Ошибка отправки файла (send_file):\n=====\nНе правильно введен один из параметров отправки сообщений\n====="
            )

    def new_keyboard(self, dicts, perm=True):
        from vk_api.keyboard import VkKeyboard, VkKeyboardColor
        
        keyboard = VkKeyboard(one_time=(not perm))

        def color(title, col, callback=False, payload=None):
            col = col.upper()
            m = [
                ["POSITIVE", "3", "ЗЕЛЕНЫЙ"],
                ["NEGATIVE", "2", "КРАСНЫЙ"],
                ["SECONDARY", "1", "БЕЛЫЙ"],
                ["PRIMARY", "0", "СИНИЙ"],
            ]
            if not callback:
                method = keyboard.add_button
            else:
                method = keyboard.add_callback_button
        
            for i in range(len(m)):
                if col in m[i]:
                    method(title, color=getattr(VkKeyboardColor, m[i][0]), payload=payload)
                    return 0
            raise LiteVkApiError(
                    "Ошибка создания клавиатуры (new_keyboard):\n=====\nНеправильно указан цвет/указан специальный объект клавиатуры\n====="
                )
        try:
            for i in dicts.keys():
                if i == "new_line":
                    keyboard.add_line()
                elif i == "vk_pay":
                    keyboard.add_vkpay_button(hash=dicts[i])
                elif i == "open_app":
                    for key, value in dicts[i].items():
                        if key == "app_id":
                            app_id = value
                        elif key == "owner_id":
                            owner_id = value
                        elif key == "label" or key == "text":
                            label = value
                        elif key == "hash":
                            hash1 = value
                    keyboard.add_vkapps_button(
                        app_id, owner_id, label, hash1
                    )
                elif i == "open_link":
                    for key, value in dicts[i].items():
                        if key == "label" or key == "text":
                            label = value
                        elif key == "link":
                            link = value
                    keyboard.add_openlink_button(label, link)
                elif i == "callback" or i == "inline":
                    payload = None
                    for key, value in dicts[i].items():
                        if key == "label" or key == "text":
                            label = value
                        elif key == "color":
                            col = value
                        elif key == "payload":
                            payload = value
                    color(label, col, True, payload)
                else:
                    color(i, dicts[i])
        except Exception as e:
            raise LiteVkApiError(
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
            raise LiteVkApiError(
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
            raise LiteVkApiError(
                "Ошибка удаления клавиатуры (delete_keyboard):\n=====\nНе правильно введен параметр userid/диалог с пользователем не обозначен\
(бот раньше не писал ему сообщения или не находится в беседе)\n====="
            )

    def mailing(self, text, userids, safe=[], chats=False):
        def r(text, userids):
            try:
                for i in userids:
                    try:
                        if i not in safe:
                            Vk.msg(self, text, i, chats)
                    except:
                        1
            except:
                raise LiteVkApiError(
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


