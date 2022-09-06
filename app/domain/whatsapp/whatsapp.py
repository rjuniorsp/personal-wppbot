from ...infrastructure.browser.browser import Browser
from .sender import Sender
from .reader import Reader
import time

class WhatsApp(Sender,Reader):

    __URL_HOME = "https://web.whatsapp.com"
    __url_active = None
    __phone = None
    __browser = None
    __error = None

    TIME_TO_LOAD = 60
    TIME_TO_FIND = 10
    TIME_TO_SEND = 5
    
    BUTTON_CLIP = "span[data-icon='clip']"
    BUTTON_SEND = "span[data-icon='send']"

    ELEMENT_ID_AUTH = "side"

    def __init__(self):
        self.__browser = Browser()
        self.__browser.set_url(self.__URL_HOME).create()
    
    def get_error(self) -> tuple[Exception,None]:
        return self.__error

    def get_url(self) -> tuple[str,None]:
        return self.__url_active

    def get_phone(self) -> tuple[str,None]:
        return self.__phone
    
    def set_phone(self,phone:tuple[str,None]):
        self.__phone = phone
        return self
    
    def set_url_active(self):
        if self.__phone != None:
            self.__url_active = f"{self.__URL_HOME}/send?phone={self.__phone}"
            return self
        
        self.__url_active = self.__URL_HOME
        return self
    
    def is_auth(self) -> bool:
        browser = self.__browser.get_browser()
        return False if len(browser.find_elements_by_id(self.ELEMENT_ID_AUTH)) < 1 else True
    
    def load(self):
        self.set_url_active()
        self.__browser.redirect(self.__url_active)
        return self.wait_to_find(id=self.ELEMENT_ID_AUTH,refresh=True,time_to_find=self.TIME_TO_LOAD)
    
    def wait_to_find(self,xpath:str = None,css_selector:str = None,id:str = None,refresh:bool = True,time_to_find:int = TIME_TO_FIND):
        browser = self.__browser.get_browser()

        if id != None:
            i = 0
            while len(browser.find_elements_by_id(id)) < 1 == False:
                if i > time_to_find and refresh:
                    self.__browser.redirect(self.__url_active)
                    return self.wait_to_find(id=id,refresh=refresh,time_to_find=time_to_find)
                i += 1
                time.sleep(1)
            return browser

        if xpath != None:
            i = 0
            while len(browser.find_elements_by_xpath(xpath)) < 1 == False:
                if i > time_to_find and refresh:
                    self.__browser.redirect(self.__url_active)
                    return self.wait_to_find(xpath=xpath,refresh=refresh,time_to_find=time_to_find)
                i += 1
                time.sleep(1)
            return browser
        
        if css_selector != None:
            i = 0
            while len(browser.find_elements_by_css_selector(css_selector)) < 1 == False:
                if i > time_to_find and refresh:
                    self.__browser.redirect(self.__url_active)
                    return self.wait_to_find(css_selector=css_selector,refresh=refresh,time_to_find=time_to_find)
                i += 1
                time.sleep(1)
            return browser