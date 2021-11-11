from selenium import webdriver
import time
import pandas as pd
import sys
from pathlib import Path
from Facebot import Face_bot

"""Argumentos para coleta:
     1. post_lik -> link do POST
     2. data_name -> nome do arquivo para salvar os dados
     3. count -> número de clicks no botão mais comentários"""

post_link = sys.argv[1]

data_name = sys.argv[2]

count = int(sys.argv[3])

fname = str(Path(r'C:\Users\EBMquintto\Desktop\Scrapers\facebook_scraper\Dados') / data_name) + '.xlsx'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(r"C:\Users\EBMquintto\Documents\chromedriver\chromedriver.exe", options=options)

driver.get("https://www.facebook.com/")

time.sleep(2)
bot = Face_bot(driver, post_link)

#login
bot.login('email.com', 'password')
time.sleep(10)

users, comments = bot.load_more_comment(count)

data = pd.DataFrame(columns=['usuário', 'comentário'])

data['usuário'] = pd.Series(users)
data['comentário'] = pd.Series(comments)

data.to_excel(fname, sheet_name='comentários', index=False)

print(f'Total extraido: {len(comments)}')

bot.close()
