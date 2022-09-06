import mysql.connector as MySQL
from mysql.connector import Error as MySQLException
import dotenv as env
import os

env.load_dotenv(env.find_dotenv())

MYSQL = {}
MYSQL["host"] = os.getenv("MYSQL_LOCAL_HOST")
MYSQL["port"] = os.getenv("MYSQL_LOCAL_PORT")
MYSQL["user"] = os.getenv("MYSQL_LOCAL_USER")
MYSQL["passwd"] = os.getenv("MYSQL_LOCAL_PASSWD")
MYSQL["database"] = os.getenv("MYSQL_LOCAL_DATABASE")

class Connect:

    def __init__(self):
        self.__instance = None
        self.__error = None
    
    def getInstance(self,data:dict):
        specific = self.specific(data)
        try:
            if self.__instance == None:
                self.__instance = MySQL.connect(
                    host=specific["host"],
                    port=specific["port"],
                    user=specific["user"],
                    passwd=specific["passwd"],
                    database=specific["database"],
                )
            if not self.__instance.is_connected():
                raise MySQLException("Não foi possivel conectar ao destino")
        except MySQLException as error:
            self.__error = error
        return self.__instance

    @staticmethod
    def specific(data:dict) -> dict:
        for arg in data:
            if data[arg] == None:
                data[arg] = MYSQL[arg]
        return data

    def getError(self):
        return self.__error
