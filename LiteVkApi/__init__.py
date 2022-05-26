try:
    import vk_api
except ImportError: raise ImportError(
        "Ошибка авторизации (login):\n =====\nНе установлена библиотека vk_api - pip3 install vk_api\n====="
    )

from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll
from threading import Thread
from json import dumps
from dataclasses import dataclass

class LiteVkApiError(Exception):
    pass

@dataclass
class Keyboard(object):
    def __init__(self, permanent:bool=True, inline:bool=False, buttons:list=[]):
        self.keyboard = self._dump({
            'one_time': not permanent,
            'inline': inline,
            'buttons': buttons
        })
    
    def _dump(self, *args, **kwargs):
        kwargs['ensure_ascii'] = False
        kwargs['separators'] = (',', ':')
        return dumps(*args, **kwargs)

class Button(object):
    def text(label, color, callback=False, payload=None):
        color = color.lower()
        m = [
            ['positive', '3', 'зеленый'],
            ['negative', '2', 'красный'],
            ['secondary', '1', 'белый'],
            ['primary', '0', 'синий'],
        ]
        for i in m:
            if color in i:
                return {
                    'color': i[0].lower(),
                    'action': {
                        'type': "callback" if callback else "text",
                        'payload': payload,
                        'label': label,
                    }
                }
    
    def url(label, link, payload=None):
        return {
            'action': {
                'type': "open_link",
                'link': link,
                'label': label,
                'payload': payload,
            }
        }
    
    def open_app(app_id, owner_id, label, hash, payload=None):
        return {
            'action': {
                'type': "open_app",
                'app_id': app_id,
                'owner_id': owner_id,
                'label': label,
                'hash': hash,
                'payload': payload,
            }
        }

    def vk_pay(hash, payload=None):
        return {
            'action': {
                'type': "vkpay",
                'hash': hash,
                'payload': payload,
            }
        }

class EmptyKeyboard():
    keyboard = ""
    keyboard_close = '{"buttons":[],"one_time":true}'

class Client(object):
    def __init__(self, vk, vk_session, key, server, ts):
        self.vk, self.vk_session, self.key, self.server, self.ts, self.event_msg = vk, vk_session, key, server, ts, ""

    def _upload_photo(self, file_names, peer):
        if type(file_names) == str:
            file_names = [file_names]
        upload = vk_api.VkUpload(self.vk_session)
        attachment = []
        for file_name in file_names:
            try:
                photo = upload.photo_messages(file_name, peer_id=peer)[0]
            except:
                raise LiteVkApiError(
                    f"Ошибка отправки фото:\n=====\nФото с именем {file_name} нет на компьютере!\n====="
                )
            attachment.append("photo{}_{}_{}".format(
                photo["owner_id"], photo["id"], photo["access_key"]
            ))
        return attachment
    
    def _upload_file(self, file_names, peer):
        if type(file_names) == str:
            file_names = [file_names]
        upload = vk_api.VkUpload(self.vk_session)
        attachment = []
        for file_name in file_names:
            try:
                mydoc = upload.document_message(file_name, peer_id=peer)["doc"]
            except:
                raise LiteVkApiError(
                    f"Ошибка отправки файла (send_file):\n=====\nФайла с именем {file_name} нет на компьютере!\n====="
                )
            attachment.append("doc{}_{}".format(mydoc["owner_id"], mydoc["id"]))
        return attachment

    def login(
        token:str,
        id_group:int=None,
        userbot:bool=False,
        my_key=None,
        my_server=None,
        my_ts=None,
    ):
        try:
            vk_session = vk_api.VkApi(token=token)
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
                    "Ошибка авторизации (login):\n=====\nНеправильно введен параметр token\n====="
                )
        else:
            try:
                VkBotLongPoll(vk_session, id_group)
            except:
                raise LiteVkApiError(
                    "Ошибка авторизации (login):\n=====\nНеправильно введен один из параметров: id_group, token\n====="
                )
            if my_key == 0 or my_server == 0 or my_ts == 0:
                raise LiteVkApiError(
                    "Ошибка авторизации (login):\n=====\nУкажите значения key, server, ts! Их можно сгененировать тут - https://vk.com/dev/groups.getLongPollServer \n====="
                )
        
        return Client(vk, vk_session, my_key, my_server, my_ts) # Я знаю, что это ужасно, но не хочу отходить от Client.login()

    def get_session(self):
        return self.vk_session

    def give_session(session, my_key=None, my_server=None, my_ts=None):
        vk = session.get_api()
        return Client(vk, session, my_key, my_server, my_ts)

    def msg(
        self, 
        text:str, 
        userid:int or str,
        photos:list or tuple or set=[], 
        files:list or tuple or set=[], 
        keyboard:Keyboard=EmptyKeyboard,
        reply_to:int=None
    ):
        if photos:
            photos = self._upload_photo(photos, userid)
        if files:
            files = self._upload_file(files, userid)
        try:
            return self.vk.messages.send(
                key=self.key,
                server=self.server,
                ts=self.ts,
                message=text,
                peer_id=userid,
                random_id=get_random_id(),
                attachment=photos + files,
                keyboard=keyboard.keyboard,
                reply_to=reply_to)
        except:
            raise LiteVkApiError(
                "Ошибка отправки сообщения (msg):\n=====\nНеправильно введен параметр userid/диалог с пользователем не обозначен\
(бот раньше не писал ему сообщения или не находится в беседе)\n====="
            )

    def send_message(
        self, 
        text:str, 
        userid:int or str,
        photos:list or tuple or set=[], 
        files:list or tuple or set=[], 
        keyboard:Keyboard=EmptyKeyboard,
        reply_to:int=None   
    ): # Кому удобнее так, чем msg
        return self.msg(text=text, userid=userid, photos=photos, files=files, keyboard=keyboard, reply_to=reply_to)
    
    def edit_message(
        self, 
        text:str, 
        userid:int or str, 
        messid:int, 
        photo:list or tuple or set=[], 
        files:list or tuple or set=[], 
        keyboard:Keyboard=EmptyKeyboard
    ):
        if photo != []:
            photo = self._upload_photo(photo, userid)
        if files != []:
            files = self._upload_file(files, userid)
        try:    
            return self.vk.messages.edit(
                key=self.key,
                server=self.server,
                ts=self.ts,
                message=text,
                peer_id=userid,
                message_id=messid,
                attachment=photo + files,
                keyboard=keyboard.keyboard,
            )
        except:
            raise LiteVkApiError(
                "Ошибка изменения сообщения (edit_message):\n=====\nНеправильно введены параметры\n====="
            )

    def check_new_msg(self, chat:bool=False):
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
                "Ошибка поиска сообщений (check_new_msg):\n=====\nНеправильно введен параметр chats\n====="
            )

    def get_event(self):
        return self.event_msg

    def send_photo(
        self, 
        file_names:list or set or tuple, 
        userid:int or str, 
        msg:str=None,
        keyboard:Keyboard=EmptyKeyboard
    ):
        attachment = self._upload_photo(file_names, userid)
        try:
            return self.vk.messages.send(
                key=self.key,
                server=self.server,
                ts=self.ts,
                peer_id=userid,
                message=msg,
                random_id=get_random_id(),
                attachment=attachment,
                keyboard=keyboard.keyboard,
            )
        except:
            raise LiteVkApiError(
                "Ошибка отправки фото (send_photo):\n=====\nНеправильно введен один из параметров отправки сообщений\n====="
            )

    def send_file(
        self, 
        file_names:list or set or tuple, 
        userid:int or str, 
        msg:str=None,
        keyboard:Keyboard=EmptyKeyboard
    ):
        attachment = self._upload_file(file_names, userid)
        try:
            return self.vk.messages.send(
                key=self.key,
                server=self.server,
                ts=self.ts,
                peer_id=userid,
                message=msg,
                random_id=get_random_id(),
                attachment=attachment,
                keyboard=keyboard.keyboard,
            )
        except:
            raise LiteVkApiError(
                "Ошибка отправки файла (send_file):\n=====\nНеправильно введен один из параметров отправки сообщений\n====="
            )

    def send_keyboard(
        self, 
        keyboard:Keyboard, 
        userid:int or str, 
        msg:str="Клавиатура!"
    ):
        try:
            return self.vk.messages.send(
                key=self.key,
                server=self.server,
                ts=self.ts,
                peer_id=userid,
                message=msg,
                random_id=get_random_id(),
                keyboard=keyboard.keyboard
            )
        except:
            raise LiteVkApiError(
                "Ошибка отправки клавиатуры (send_keyboard):\n=====\nНеправильно введен параметр userid/диалог с пользователем не обозначен\
(бот раньше не писал ему сообщения или не находится в беседе)\n====="
            )

    def delete_keyboard(
        self, 
        userid:int or str, 
        msg:str="Клавиатура закрыта!"
    ):        
        try:
            return self.vk.messages.send(
                key=self.key,
                server=self.server,
                ts=self.ts,
                peer_id=userid,
                message=msg,
                random_id=get_random_id(),
                keyboard=EmptyKeyboard.keyboard_close,
            )
        except:
            raise LiteVkApiError(
                "Ошибка удаления клавиатуры (delete_keyboard):\n=====\nНеправильно введен параметр userid/диалог с пользователем не обозначен\
(бот раньше не писал ему сообщения или не находится в беседе)\n====="
            )

    def mailing(
        self, 
        text:str, 
        userids:list or set or tuple, 
        safe:list=[],
        photos:list or tuple or set=[], 
        files:list or tuple or set=[], 
        keyboard:Keyboard=EmptyKeyboard,
        ):
        def r(text, userids):
            try:
                for i in userids:
                    try:
                        if i not in safe:
                            Client.msg(self, text, i, photos, files, keyboard)
                    except:
                        pass
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
            message_data = self.get_all_message_data()
        ret = []
        for i in message_data:
            ret.append(i["peer_id"])
        del message_data
        return ret

    def VkMethod(self, method_name, arg):
        return self.vk_session.method(method_name, arg)


