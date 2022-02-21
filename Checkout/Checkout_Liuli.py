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


from Web import Web
url = 'https://liuliss.top/auth/login'
a = Web(url)
print(a)

# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# service = Service(r'driver\chromedriver.exe')
# url = 'https://liuliss.top/auth/login'
# try:
#     browser = webdriver.Chrome(options=options,service=service)
    
# except:
#     print('浏览器唤起失败')
#     input('程序已终止')
#     sys.exit(-1)

# url = 'https://liuliss.top/auth/login'
# url = 'https://baidu.com'
# url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=1&fenlei=256&rsv_pq=c5b4315300001861&rsv_t=e5b84acb6EJBmu3WNWynUHWgtuV3C2nGY%2FVdaZiKo3CUKP1h8H52hCz0dYQ&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_sug3=2&rsv_sug1=2&rsv_sug7=101&rsv_btype=i&inputT=1138&rsv_sug4=1664'

# browser.get(url)