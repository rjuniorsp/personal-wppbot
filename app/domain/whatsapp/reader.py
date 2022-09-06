from selenium.common.exceptions import (
    NoSuchElementException, 
    StaleElementReferenceException
)
from selenium.webdriver.common.by import By
import datetime, time, re

class Reader:

    __allElementsMessage = []
    __allElementsVisited = set()
    __allElementsChecked = []

    DIV_CHATBOX_CSS_SELECTOR = 'div[data-testid="conversation-panel-messages"]'
    DIV_MESSAGE_CLASS_NAME = [
        'message-in',
        'message-out'
    ]

    def __init__(self):
        pass
    
    def get_messages(self) -> list:
        return self.__allElementsChecked

    def get_element(self,by:str = By.XPATH,value:str = ''):
        browser = self.__browser.get_browser()
        try:
            elements = browser.find_element(by=by, value=value)
            return elements
        except (NoSuchElementException) as e:
            return None

    def get_elements(self,by:str = By.XPATH,value:str = ''):
        browser = self.__browser.get_browser()
        try:
            element = browser.find_elements(by=by, value=value)
            return element
        except (NoSuchElementException) as e:
            return None
    
    @staticmethod
    def get_element_text(element):
        try:
            return element.get_attribute("innerHTML")
        except StaleElementReferenceException:
            return ''

    @staticmethod
    def remove_tag_html(text:str) -> str:
        return re.sub(re.compile('<.*?>'), '', text)

    @staticmethod
    def get_contact_info(text):
        info = {}
        extract = re.search(r'\[(.+?), (.+?)\] (.+?):', text)
        _time, _date, _name = extract.group(1), extract.group(2), extract.group(3)

        if 'AM' in _time or 'PM' in _time:
            _time = time.strptime(_time, '%H:%M %p')
        else:
            _time = time.strptime(_time, '%H:%M')
        _date = datetime.datetime.strptime(_date, '%d/%m/%Y')

        info["hour"] = _time.tm_hour
        info["minute"] = _time.tm_min
        info["day"] = _date.day
        info["month"] = _date.month
        info["year"] = _date.year
        info["contact"] = _name

        return info

    @staticmethod
    def validate_tag(element, tag:str) -> bool:
        if element == None:
            return False
        try:
            if element.tag_name != tag:
                return False
            return True
        except (StaleElementReferenceException, NoSuchElementException) as e:
            return False

    @staticmethod
    def validate_tag_span(element) -> bool:
        try:
            if element.get_attribute("class") == None or element.get_attribute("class") == '':
                if element.get_attribute("dir") == None or element.get_attribute("dir") == '':
                    return True
            return False
        except (StaleElementReferenceException, NoSuchElementException) as e:
            return False

    def validate_text_message(self,children) -> None:
        try:
            children.tag_name
            textExtracted = None

            if self.validate_tag(children, 'img') and children.get_attribute("src") and 'blob:' in children.get_attribute("src"):
                return

            if self.validate_tag(children, 'a'):
                return

            if self.validate_tag(children, 'div'):

                if children.get_attribute('data-id') != None:
                    if 'album-' in children.get_attribute('data-id'):
                        return

                if children.get_attribute("data-pre-plain-text") != None and children.get_attribute("data-pre-plain-text") != '':
                    textExtracted = self.get_contact_info(children.get_attribute("data-pre-plain-text"))
                    
                    auxChildren = children.find_elements(by=By.XPATH, value=".//*")

                    for child in auxChildren:
                        if self.validate_tag(child, 'img'):
                            continue
                        if not self.validate_tag(child, 'span'):
                            continue
                        if not self.validate_tag_span(child): 
                            continue
                        
                        text = self.get_element_text(child)

                        if '<img' in text and 'emoji' in text:
                            continue
                        
                        if len(text) == 0:
                            continue

                        if '<' in text and '>' in text:
                            text = self.remove_tag_html(text)

                        textExtracted['msg'] = text.replace('\n', ' ').replace(':', ' ')

                        if textExtracted in self.__allElementsChecked:
                            continue

                        self.__allElementsChecked.append(textExtracted)

        except (StaleElementReferenceException, NoSuchElementException,Exception) as e:
            return

    def validate_active_messages(self) -> bool:
        for class_name in self.DIV_MESSAGE_CLASS_NAME:
            elements = self.get_elements(By.CLASS_NAME,value=class_name)
            if elements == None:
                continue
            self.__allElementsMessage += elements
        return False if len(self.__allElementsMessage) == 0 else True
    
    def validate_active_contact(self) -> bool:
        return False if self.get_elements(By.CSS_SELECTOR,value=self.DIV_CHATBOX_CSS_SELECTOR) == None else True

    def read_conversation(self) -> bool:
        self.__allElementsMessage = []
        self.__allElementsVisited = set()
        self.__allElementsChecked = []
        
        try:
            if self.__phone == None:
                raise Exception("Sem contato definido.")
            
            if not self.validate_active_contact():
                raise Exception("Sem painel de mensagens.")

            if self.validate_active_messages():
                raise Exception("Sem mensagens exibidas no painel de mensagens.")

            for elementMessage in self.__allElementsMessage:
                if elementMessage in self.__allElementsVisited:
                    continue
                self.__allElementsVisited.add(elementMessage)
                self.validate_text_message(elementMessage)
            
            if len(self.__allElementsChecked) == 0:
                raise Exception("Sem mensagens de texto validadas no painel de mensagens.")

            return True
        except Exception as error:
            self.__error = error
            return False