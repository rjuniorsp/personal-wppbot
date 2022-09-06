from ..domain import WhatsApp
from ..service import Queue
import json

class Controller:

    __whatsapp = None
    __queue = None

    def __init__(self):
        self.__whatsapp = WhatsApp()
        self.__whatsapp.load()

    def has_auth(self) -> bool:
        return self.__whatsapp.is_auth()

    def has_queue(self) -> bool:
        self.__queue = Queue().get_queue_by_status(Queue.STATUS_PENDING)
        if len(self.__queue) > 0:
            return True
        self.__queue = None
        return False
    
    def process(self) -> bool:

        if not self.has_auth() or not self.has_queue() or self.__queue == None:
            return False
            
        body = []
        for queue in self.__queue:
            try:
                if queue["type"] not in Queue.get_type_service():
                    raise Exception("Tipo invalido de ação.")
                
                Queue().set_queue_update(queue["id"],Queue.STATUS_PROCESSING)
                self.__whatsapp.set_phone(queue["contact"])
                self.__whatsapp.load()

                if queue["type"] == Queue.TYPE_SERVICE_SEND:
                    list = json.loads(queue["body"])
                    for item in list:
                        if item["type"] not in Queue().get_type_service_send():
                            raise Exception("Tipo de envio inválido.")
                        if item["type"] == Queue.TYPE_SERVICE_SEND_TEXT:
                            item["status"] = self.__whatsapp.send_text(item["value"])
                        if item["type"] == Queue.TYPE_SERVICE_SEND_MEDIA:
                            item["status"] = self.__whatsapp.send_media(item["value"])
                        if item["type"] == Queue.TYPE_SERVICE_SEND_DOC:
                            item["status"] = self.__whatsapp.send_doc(item["value"])
                        body.append(item)

                if queue["type"] == Queue.TYPE_SERVICE_READ:
                    list = json.loads(queue["body"])
                    for item in list:
                        if item["type"] not in Queue().get_type_service_read():
                            raise Exception("Tipo de leitura inválido.")
                        if item["type"] == Queue.TYPE_SERVICE_READ_TEXT:
                            item["status"] = self.__whatsapp.read_conversation()
                            item["value"] = self.__whatsapp.get_messages()
                        body.append(item)

                Queue().set_queue_update(queue["id"],Queue.STATUS_PROCESSED,json.dumps(body))

            except Exception as error:
                Queue().set_queue_update(queue["id"],Queue.STATUS_FAIL,None,error)
            
            self.__whatsapp.set_phone(None)
            self.__whatsapp.load()
        return True
