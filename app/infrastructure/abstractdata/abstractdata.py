from mysql.connector import Error as MySQLException
from .connect import Connect
from .crud import Crud

class AbstractData(Crud):
    # propriety
    # @var string entity database table
    __entity = ''

    # @var string primary table primary key field
    __primary = ''

    # @var array required table required fields
    __required = []

    # @var array fields table columns
    __fields = []

    # @var object type table type fields
    __type = {}

    # @var string timestamps control created and updated at
    __timestamps = True

    # @var string
    __statement = ''

    # @var string
    __params = None

    # @var string
    __group = ''

    # @var string
    __order = ''

    # @var int
    __limit = ''

    # @var int
    __offset = ''

    # @var MySQLException|None
    __fail = None

    # @var object|None
    __data = None

    def __init__(self,entity:str,required:list,primary:str,timestamps:bool = True):
        self.__entity = entity
        self.__primary = primary
        self.__required = required
        self.__timestamps = timestamps
        self.setConnect()
    
    @staticmethod
    def getType(type:str) -> tuple[str,None]:
        if 'int' in type:
            return 'int'
        if 'text' in type or 'char' in type:
            return 'str'
        if 'date' in type:
            return 'str'
        return None

    def getData(self):
        return self.__data

    def getFail(self):
        return self.__fail

    def getTypes(self) -> dict:
        return self.__type
    
    def setData(self,data):
        self.__data = data
        return self
    
    def setConnect(self,host:str = None,port:int = None,user:str = None,passwd:str = None,database:str = None):
        self.__connect = {}
        self.__connect['host'] = host
        self.__connect['port'] = port
        self.__connect['user'] = user
        self.__connect['passwd'] = passwd
        self.__connect['database'] = database
        self.setFields()
        return self

    def setGroup(self,group:str):
        self.__group = f" GROUP BY {group}"
        return self
    
    def setOrder(self,order:str):
        self.__order = f" ORDER BY {order}"
        return self
    
    def setOffset(self,offset:tuple[str,int]):
        self.__offset = f" OFFSET {offset}"
        return self

    def setLimit(self,limit:int):
        self.__limit = f" LIMIT {limit}"
        return self
    
    def setStatement(self,statement:str):
        self.__statement = statement
        return self

    def setFields(self) -> bool:
        try:
            connect = Connect()
            instance = connect.getInstance(self.__connect)
            if instance == None:
                raise MySQLException(connect.getError())

            cursor = instance.cursor()
            cursor.execute(
                f"DESCRIBE {self.__entity}",
                self.__params
            )
            list = cursor.fetchall()
            for item in list:
                if item != None:
                    self.__type[item[0]] = self.getType(item[1])
                    self.__fields.append(item[0])
            self.__data = self.__fields
            return True
        except MySQLException as error:
            self.__fail = error
            return False

    def findById(self,id:int,columns:str = "*"):
        return self.find(f"{self.__primary} = %(id)s",{'id':id},columns).fetch()

    def find(self,terms = None,params = None,columns = "*"):
        if terms == None:
            self.__statement = f"SELECT {columns} FROM {self.__entity}"
            return self
        self.__statement = f"SELECT {columns} FROM {self.__entity} WHERE {terms}"
        self.__params = params
        return self
    
    def fetch(self,list:bool = False):
        try:
            connect = Connect()
            instance = connect.getInstance(self.__connect)
            if instance == None:
                raise MySQLException(connect.getError())

            cursor = instance.cursor()
            cursor.execute(
                self.__statement + self.__group + self.__order + self.__limit + self.__offset,
                self.__params
            )
            if cursor.rowcount == 0:
                return None
            if list:
                return cursor.fetchall()
            return cursor.fetchone()
        except MySQLException as error:
            self.__fail = error
            return None

    def count(self) -> tuple[int,None]:
        try:
            connect = Connect()
            instance = connect.getInstance(self.__connect)
            if instance == None:
                raise MySQLException(connect.getError())

            cursor = instance.cursor()
            cursor.execute(
                f"{self.__statement}",
                self.__params
            )
            return cursor.rowcount
        except MySQLException as error:
            self.__fail = error
            return None
    
    def save(self) -> bool:
        id = None
        try:
            if not self.validate():
                raise Exception("Preencha os campos necessários com os valores corretos.")

            if self.__data[self.__primary] == None:
                id = self.create(self.safe())
            else:
                id = self.__data[self.__primary]
                self.update(self.safe(),f"{self.__primary} = %(id)s",{'id':id})

            if id == None:
                return False
            
            self.__data = self.findById(id)
            return True
        except Exception as err:
            self.__fail = err
            return False
    
    def destroy(self) -> bool:
        id = self.__data[self.__primary]
        if not id:
            return False
        if self.delete(f"{self.__primary} = %(id)s",{'id':id}) == None:
            return False
        return True

    def validate(self) -> bool:
        data = self.__data
        for field in self.__required:
            if self.__type[field] == 'int':
                if data[field] == None:
                    data[field] = 0
            if data[field] != None and self.__type[field] not in str(type(data[field])):
                return False
        return True

    def safe(self) -> dict:
        safe = self.__data
        del safe[self.__primary]
        return safe
    
    def merge(self,row,data) -> dict:
        merge = {}
        for i in range(len(self.__fields)):
            merge[self.__fields[i]] = row[i]
        for field in data:
            merge[field] = data[field]
        return merge