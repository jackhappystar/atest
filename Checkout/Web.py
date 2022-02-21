import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By as ClassBy
from selenium.webdriver.common.keys import Keys


class Web(object):
    
    def __init__(self, url):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(r'driver\chromedriver.exe')
        # url = 'https://liuliss.top/auth/login'
        
        self.options = options
        self.service = service
        self.browser = None
        self.element = None
        self.By = None
        self.ByContent = None
        try :
            self.browser = webdriver.Chrome(options=options,service=service)
            self.browser.get(url)
        except: pass           

    def __str__(self):
        return f'{self.element}'
    
    def IsExist(self, By, ByContent):
        '''
        By: 请使用By传入，'from selenium.webdriver.common.by import By'\
            传入如: By.ID, By.XPATH
        '''
        self.By = By
        self.By = ByContent
        try:
            self.element = self.browser.find_element(By,ByContent)
        except: pass
        
        if not self.element:
            print(f'不存在元素:\t{By}-{ByContent}')
        return True if self.element else False
    
    def SendKeys(self, *args):
        '''
        *args: 热键请使用Keys传入，'from selenium.webdriver.common.keys import Keys'\
            传入如:  Keys.BACK_SPACE, Keys.CONTROL，后面的热键使用小写字母 如'a'
            
        '''
        if self.element:
            self.element.send_keys(*args)
        
    def Click(self):
        if self.element:
            DoFlag = 1
            while DoFlag:
                try:
                    self.element.click()
                    DoFlag = 0
                except:
                    time.sleep(0.5)
                
            
    def GetAttribute(self, Attribute='textContent'):
        '''
        Attribute: 'textContent', 'innerHTML', 'outerHTML'
        '''
        if self.element:
            msg = self.element.get_attribute(Attribute)
            # while msg =='' or msg == None:
            #     time.sleep(0.5)
            return self.element.get_attribute(Attribute)
    def MoveTo(self):
        if self.element:
            DoFlag = 1
            while DoFlag:
                try:
                    ActionChains(self.browser).move_to_element(self.element).perform()
                    DoFlag = 0
                except:
                    time.sleep(0.5)
        
    def GetTitle(self):
            print(self.browser.title)       
    def Close(self):
        self.browser.close()
    def Quit(self):
        self.browser.quit()

        
    