from mysql.connector import Error as MySQLException
from datetime import datetime
from .connect import Connect

class Crud:

    @staticmethod
    def filter(data:dict) -> dict:
        filter = {}
        for key in data:
            if data[key] == None:
                filter[key] = None
                continue
            filter[key] = data[key]
        return filter
    
    @staticmethod
    def format(data:dict) -> dict:
        format = {}
        format['columns'] = []
        format['values'] = []
        format['set'] = []
        for key in data:
            format['columns'].append(f"{key}")
            format['values'].append(f"%({key})s")
            format['set'].append(f"{key} = %({key})s")
        return format
        
    def create(self,data:dict) -> tuple[int, None]:
        if self.__timestamps:
            data['created_at'] = datetime.now().strftime('%Y-%d-%m %H:%M:%S')
            data['updated_at'] = data['created_at']

        format = self.format(data)
        columns = ", ".join(format['columns'])
        values = ", ".join(format['values'])

        try:
            connect = Connect()
            instance = connect.getInstance(self.__connect)
            if instance == None:
                raise MySQLException(connect.getError())

            cursor = instance.cursor()
            cursor.execute(
                f"INSERT INTO {self.__entity} ({columns}) VALUES ({values})",
                self.filter(data)
            )
            instance.commit()
            return cursor.lastrowid
        except MySQLException as error:
            self.__fail = error
            return None

    def update(self,data:dict,terms:str,params:tuple[dict, None]) -> tuple[int, None]:
        if self.__timestamps:
            data['updated_at'] = datetime.now().strftime('%Y-%d-%m %H:%M:%S')
        
        format = self.format(data)
        set = ", ".join(format['set'])

        try:
            connect = Connect()
            instance = connect.getInstance(self.__connect)
            if instance == None:
                raise MySQLException(connect.getError())

            cursor = instance.cursor()
            cursor.execute(
                f"UPDATE {self.__entity} SET {set} WHERE {terms}"
                ,self.filter({**data,**params})
            )
            instance.commit()
            return cursor.rowcount
        except MySQLException as error:
            self.__fail = error
            return None

    def delete(self,terms:str,params:tuple[dict, None] = None) -> tuple[int, None]:

        try:
            connect = Connect()
            instance = connect.getInstance(self.__connect)

            if instance == None:
                raise MySQLException(connect.getError())

            cursor = instance.cursor()
            if params != None:
                cursor.execute(
                    f"DELETE FROM {self.__entity} WHERE {terms}",
                    params
                )
                instance.commit()
                return cursor.rowcount

            cursor.execute(
                f"DELETE FROM {self.__entity} WHERE {terms}",
                params
            )
            instance.commit()
            return cursor.rowcount
        except MySQLException as error:
            self.__fail = error
            return None