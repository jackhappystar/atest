from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys
import os
import random
from VerificationCode import VerificationCode




options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = Service(r'driver\chromedriver.exe')

try:
    browser = webdriver.Chrome(options=options,service=service)
    
except:
    print('浏览器唤起失败')
    input('程序已终止')
    sys.exit(-1)

url = 'http://task.njust.edu.cn/infoplus/form/XSXNYQSB/start'
# url = 'https://baidu.com'
# url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=1&fenlei=256&rsv_pq=c5b4315300001861&rsv_t=e5b84acb6EJBmu3WNWynUHWgtuV3C2nGY%2FVdaZiKo3CUKP1h8H52hCz0dYQ&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_sug3=2&rsv_sug1=2&rsv_sug7=101&rsv_btype=i&inputT=1138&rsv_sug4=1664'

timeout = 5
date = '2012-11-05'


def Verify(Filepath):
    # print(Filepath)
    object = VerificationCode(Filepath)
    object.Delete_Background_Colour()
    object.twoValue()
    object.ClearNoise()
    object.ClearNoiseProcess()
    result = object.recognize_captcha()
    return result


def Get_VCode_Result(Element):
    Filepath = r'pic/vcode.png'
    if not os.path.exists('pic'):
        os.makedirs('./pic')
    if os.path.exists(Filepath):
        os.remove(Filepath)
    Element.screenshot(Filepath)
    return Verify(Filepath)
def Exit(t,promt=''):
    print(f'程序已终止,终止代码:\t{t}\n原因:\t{promt}')
    input()
    sys.exit(t)
    
def Is_Element_Exist(By,ByContent,Browser=browser):
    try:
        element = Browser.find_element(By,ByContent)
        return element
    except:
        return None
    
def Click_Element(By,Content,Browser=browser):
    element = None
    time_start = time.time()
    while element == None:
        element = Is_Element_Exist(By,Content)
        time.sleep(1)
        time_end=time.time()
        if time_end - time_start >= timeout:
            Exit(-1,f'点击失败，不存在该元素{Content}')
        
    ClickFlag = 1
    time_start = time.time()
    while ClickFlag:
        try:
            element.click()
            ClickFlag = 0
        except:
            time.sleep(1)            
            time_end=time.time()
            if time_end - time_start >= timeout:
                Exit(-1,f'点击失败，存在该元素，却无法点击{Content}')        
    return 1
    
def Submit_Element(By,Content,Browser=browser):
    element = None
    time_start = time.time()
    while element == None:
        element = Is_Element_Exist(By,Content)
        time.sleep(1)
        time_end=time.time()
        if time_end - time_start >= timeout:
            Exit(-1,f'提交失败，不存在该元素{Content}')
        
    ClickFlag = 1
    time_start = time.time()
    while ClickFlag:
        try:
            browser.execute_script("arguments[0].click();", element)
            ClickFlag = 0
        except:
            time.sleep(1)            
            time_end=time.time()
            if time_end - time_start >= timeout:
                Exit(-1,f'提交失败，存在该元素，却无法提交{Content}')        
    return 1
    
def Print_Current_Brower_Title():
    print(f'当前活动页面:\t{browser.title}')
    
def Get_Attribute(By,Content,Attribute='textContent',Browser=browser):
    element = None
    time_start = time.time()
    while element == None:
        element = Is_Element_Exist(By,Content)
        time.sleep(1)
        time_end=time.time()
        if time_end - time_start >= timeout:
            print(f'提取失败，不存在该元素{Content}')
            break
        
    GetFlag = 1
    a = ''
    time_start = time.time()
    while GetFlag:
        try:
            a = element.get_attribute(Attribute)
            GetFlag = 0
        except:
            time.sleep(1)            
            time_end=time.time()
            if time_end - time_start >= timeout:
                print(f'提取失败，存在该元素，却无法提取{Content}')
                break
                
    return a

def CheckOut_NJUST(id,password):
    try:
        browser.get(url)
    except:
        browser.close()
        Exit(-1,'打开网页异常')
    
    # browser.find_element_by_name("wd").send_keys("11selenium")
    # element = browser.find_element(By.ID,'su')
    
    # loginFlag = [Is_Element_Exist(By.CLASS_NAME,'login-title'),Is_Element_Exist(By.CLASS_NAME,'login-title')]
    Print_Current_Brower_Title()
    # 检查是否登录
    loginFlag = [0,0]
    time_start=time.time()
    while not (loginFlag[0] or loginFlag[1]):
        loginFlag = [1 if '统一身份认证平台'in browser.title else 0,1 if '填报防疫信息' in browser.title else 0]
        
        time.sleep(1)
        time_end=time.time()
        if time_end - time_start >= timeout:
            # 若超时则 loginFlag 保持 [0,0]
            break
    
    # 未登录
    if loginFlag[0] == 1:
        loginSucess = 1
        while loginSucess :
            # 用户名
            element = Is_Element_Exist(By.ID,'username')
            if element:
                element.send_keys(Keys.CONTROL,'a')
                element.send_keys(Keys.BACK_SPACE)
                element.send_keys(id)
            # 用密码
            element = Is_Element_Exist(By.ID,'password')
            if element:
                element.send_keys(password)
            # 验证码
            xpath = '//span[@class="captcha-img"]//img[contains(@src,"getCaptcha")]'
            element = Is_Element_Exist(By.XPATH,xpath)
            # print(element)
            if element:
                result = Get_VCode_Result(element)
                
                vcode_element = Is_Element_Exist(By.ID,'captcha')
                if vcode_element:
                    vcode_element.send_keys(result)
            # 登录
            element = Is_Element_Exist(By.ID,'login_submit')
            if element:
                element.click()
            # 判断验证码正确与否
            xpath = '//span[@id="showErrorTip" and contains(@title,"验证码")]'
            vcode_element = Is_Element_Exist(By.XPATH,xpath)
            time.sleep(0.5) 
            if vcode_element == None:
                loginSucess = 0
    # 已登录
    elif loginFlag[1] == 1:
        1
    # 未加载出登录界面，也未加载出填报页面
    else:
        browser.close()
        Exit(-1,'加载网页不正确')
    
    Print_Current_Brower_Title()
    
    # 检查今日是否已经填写
    
    # 检查是否进入填报页
    element = None
    time_start = time.time()
    while element == None:
        element = Is_Element_Exist(By.XPATH,'//h1//font[@color="#000000" and text()="向“理”报平安"]')
        if element == None:
            # 密码是否错误
            element = Is_Element_Exist(By.XPATH,'//span[@id="showErrorTip" and @title="您提供的用户名或者密码有误"]')
            # 密码错误
            if element:
                # browser.quit()
                Exit(-1,'密码错误，请查证后修改配置文件后，重新启动程序')
                
            # 今日是否已经填写
            element = Is_Element_Exist(By.XPATH,'//div[@class="dialog_content"]')
            # 今日已经填写，直接结束
            if element:
                # browser.quit()
                Exit(0,'今日已报平安，自动结束')
                    
        time_end = time.time()
        time.sleep(1)
        if time_end - time_start >= timeout:
            # 若超时则退出
            Exit(-1,f'进入填报页面超时')
            
    Print_Current_Brower_Title()
    
    # 点击温度
    temperature = random.randint(0,20)/10 + 35
    xpath = f'//select//option[@value="{temperature}"]'
    Click_Element(By.XPATH,xpath)
    
    # 核酸日期
    global date
    date = date.split('-')
    for i in range(len(date)):
        date[i] = int(date[i])
    [year,month,day] = date
    month -= 1
    
    # 点击(激活)日期选项
    xpath = '''//input[@id="V1_CTRL212"]'''
    Click_Element(By.XPATH,xpath)
    # 点击年月日
    xpath = f'''//select[@class="ui-datepicker-year"]//option[@value="{year}"]'''
    Click_Element(By.XPATH,xpath)
    xpath = f'''//select[@class="ui-datepicker-month"]//option[@value="{month}"]'''
    Click_Element(By.XPATH,xpath)
    xpath = f'''//td//a[@class="ui-state-default" and text()='{day}']'''
    Click_Element(By.XPATH,xpath)
    
    # 中高风险区
    xpath = '''//strong//input[@id="V1_CTRL167"]'''
    Click_Element(By.XPATH,xpath)
    
    # 本人承诺
    xpath = '''//font//input[@id="V1_CTRL142"]'''
    Click_Element(By.XPATH,xpath)
       
    
    # 提交
    xpath = '''//a[@class="command_button_content"]'''
    Submit_Element(By.XPATH,xpath)
    
    # 提示信息
    xpath = '//div[@id="form_do_action_show_remark"]//span[2]'
    promt = Get_Attribute(By.XPATH,xpath)
    if '相关说明' not in promt:
        Exit(-1,'内容不完整')
    # 点击好
    xpath = '//div//button[@class="dialog_button default fr"]'
    Click_Element(By.XPATH,xpath)
    
    # 办理成功
    xpath = '//div[@class="dialog_content" and text()="办理成功!"]'
    if Is_Element_Exist(By.XPATH,xpath):
        xpath = '//div//button[@class="dialog_button default fr"]'
        Click_Element(By.XPATH,xpath)
        print('Done'.center(50,'-'))
        browser.quit()
        Exit(0,'正常退出')
        return 0
    else: 
        return 1
    # 直接退出
    
    # browser.quit()
    # Exit(0,'正常退出')
def Get_Config(FilePath = r'Config.txt'):
    with open(FilePath,'r') as fr:
        lines = fr.readlines()
        [id,password,date,timeout] = [lines[i].strip('\n') for i in range(4)]
        timeout = int(timeout)
    return id,password,date,timeout
    
def main():
    global timeout, date 
    timeout, date = 5, '2022-01-05'
    '''
    # id, password = '120101010040','Zyt262520'
    
    id,password,date,timeout = Get_Config()
    
    # print([id,password,date,timeout])
    success_flag = 1
    while success_flag:
        success_flag = CheckOut_NJUST(id, password)
    '''     
if __name__ == '__main__':
    main()