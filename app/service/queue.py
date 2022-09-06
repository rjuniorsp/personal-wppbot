from ..infrastructure import AbstractData

class Queue(AbstractData):
    
    schema = {
        "id":"bigint(20)",
        "type":"int(11)",
        "contact":"varchar(20)",
        "error":"longtext",
        "body":"longtext",
        "status":"tinyint(1)",
        "created_at":"datetime",
        "updated_at":"datetime",
    }

    # TYPE SERVICE SEND (BODY)
    # [
    #     {
    #         "type":1, 
    #         "value":"Teste Bot envio de texto",
    #         "status":False
    #     },
    #     {
    #         "type":1, 
    #         "value":"Teste Bot envio de media",
    #         "status":False
    #     },
    #     {
    #         "type":2,
    #         "value":"C:\Users\User\Downloads\audioteste.ogg",
    #         "status":False
    #     },
    #     {
    #         "type":2,
    #         "value":"C:\Users\User\Downloads\6ea655b0c487dd8017b6cda134f233eaf0dd9cf6_full.jpg",
    #         "status":False
    #     },
    #     {
    #         "type":1,
    #         "value":"Teste Bot envio de documento",
    #         "status":False
    #     },
    #     {
    #         "type":3,
    #         "value":"C:\Users\User\Downloads\2022_05_I-CjuNAJbd81.pdf",
    #         "status":False
    #     },
    # ]

    # TYPE SERVICE SEND (BODY)
    # [
    #     {
    #         "type":1, 
    #         "value":"Teste Bot leitura de mensagens",
    #         "status":False
    #     },
    # ]

    STATUS_PENDING = 1
    STATUS_PROCESSING = 2
    STATUS_PROCESSED = 3
    STATUS_FAIL = 4

    TYPE_SERVICE_SEND = 1
    TYPE_SERVICE_READ = 2

    TYPE_SERVICE_SEND_TEXT = 1
    TYPE_SERVICE_SEND_MEDIA = 2
    TYPE_SERVICE_SEND_DOC = 3

    TYPE_SERVICE_READ_TEXT = 1

    def __init__(self):
        super().__init__("Queue",
            [
                "type",
                "contact",
                "status"
            ],
            "id",
            True
            )

    def get_status(self) -> list:
        return [
            self.STATUS_PENDING,
            self.STATUS_PROCESSING,
            self.STATUS_PROCESSED,
            self.STATUS_FAIL
        ]
    
    def get_type_service(self) -> list:
        return [
            self.TYPE_SERVICE_SEND,
            self.TYPE_SERVICE_READ
        ]
    
    def get_type_service_send(self) -> list:
        return [
            self.TYPE_SERVICE_SEND_TEXT,
            self.TYPE_SERVICE_SEND_MEDIA,
            self.TYPE_SERVICE_SEND_DOC
        ]
    
    def get_type_service_read(self) -> list:
        return [
            self.TYPE_SERVICE_READ_TEXT
        ]
    
    def get_queue_by_status(self,status:int):
        if status not in self.get_status():
            return None
        return self.find("status = %(status)s",{"status":status}).setOrder(1).fetch(True)

    def set_queue_update(self,id:int,status:int,body:str = None,error:str = None) -> bool:
        row = self.findById(id)
        if row == None:
            return False
            
        data = {}
        if body != None:
            data["body"] = body
        if error != None:
            data["error"] = error
        data["status"] = status

        self.__data = self.merge(row,data)
        return self.save()
    
    def save(self) -> bool:
        if not self.validate_type():
            return False
        if not self.validate_status():
            return False
        if not self.validate_contact():
            return False
        if not super().save():
            return False
        return True
    
    def validate_type(self) -> bool:
        if self.__data["type"] == None:
            self.__fail = Exception("type não pode ser vazio.")
            return False
        if self.__data["type"] not in self.get_type_service():
            self.__fail = Exception("type fora dos parâmetros.")
            return False
        return True
    
    def validate_contact(self) -> bool:
        if self.__data["contact"] == None:
            self.__fail = Exception("contact não pode ser vazio.")
            return False
        if len(self.__data["contact"]) < 13:
            self.__fail = Exception("contact não contem DDD do estado e do pais. Exempo: 55 11 926369857")
            return False
        return True
    
    def validate_status(self) -> bool:
        if self.__data["status"] == None:
            self.__fail = Exception("status não pode ser vazio.")
            return False
        if self.__data["status"] not in self.get_status():
            self.__fail = Exception("status fora dos parâmetros.")
            return False
        return True
    