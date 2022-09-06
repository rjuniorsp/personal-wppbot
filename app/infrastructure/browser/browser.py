from selenium import webdriver
from pathlib import Path

class Browser:
    
    __url = None
    __browser = None
    __path_driver = None

    def __init__(self,path:str = None):
        if path == None:
            path = Path('browser\driver\chromedriver.exe').absolute()
        self.__path_driver = path
    
    def set_browser(self,browser):
        self.__browser = browser
        return self

    def get_browser(self):
        return self.__browser
    
    def set_url(self,url:str):
        self.__url = url
        return self
    
    def is_browser(self) -> bool:
        if self.__browser == None:
            return False

    def create(self):
        self.__browser = webdriver.Chrome(executable_path=self.__path_driver)
        self.__browser.get(self.__url)
        return self.__browser
    
    def redirect(self,url:tuple[str,None] = None):
        if url == None or self.__browser == None:
            self.create()
            return self.__browser
        self.__browser.get(url)
        return self.__browser
