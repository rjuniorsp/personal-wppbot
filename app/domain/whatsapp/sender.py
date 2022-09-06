import time

class Sender:

    INPUT_TEXT = '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span'
    INPUT_FILE_MEDIA = "input[accept='image/*,video/mp4,video/3gpp,video/quicktime' type='file']"
    INPUT_FILE_DOC = "input[accept='*' type='file']"

    def __init__(self):
        pass
    
    def send_text(self,text:str) -> bool:
        try:
            self.inject_input_text(text)
            self.click_button_send()
            time.sleep(self.TIME_TO_SEND)
            return True
        except Exception as error:
            self.__error = error
            return False
    
    def send_doc(self,doc:str) -> bool:
        try:
            self.click_button_clip()
            self.inject_input_doc(doc)
            self.click_button_send()
            time.sleep(self.TIME_TO_SEND)
            return True
        except Exception as error:
            self.__error = error
            return False
    
    def send_media(self,media:str) -> bool:
        try:
            self.click_button_clip()
            self.inject_input_media(media)
            self.click_button_send()
            time.sleep(self.TIME_TO_SEND)
            return True
        except Exception as error:
            self.__error = error
            return False

    def click_button_send(self):
        browser = self.wait_to_find(css_selector=self.BUTTON_SEND,refresh=False)
        browser.find_element_by_css_selector(self.BUTTON_SEND).click()
    
    def click_button_clip(self):
        browser = self.wait_to_find(css_selector=self.BUTTON_CLIP)
        browser.find_element_by_css_selector(self.BUTTON_CLIP).click()

    def inject_input_text(self,text:str):
        browser = self.wait_to_find(xpath=self.INPUT_TEXT)
        browser.find_element_by_xpath(self.INPUT_TEXT).send_keys(text)
    
    def inject_input_media(self,media:str):
        browser = self.wait_to_find(css_selector=self.INPUT_FILE_MEDIA,refresh=False)
        browser.find_element_by_css_selector(self.INPUT_FILE_MEDIA).send_keys(media)

    def inject_input_doc(self,doc:str):
        browser = self.wait_to_find(css_selector=self.INPUT_FILE_DOC,refresh=False)
        browser.find_element_by_css_selector(self.INPUT_FILE_DOC).send_keys(doc)