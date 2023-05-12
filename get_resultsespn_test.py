import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import time
from scipy import stats
import statsmodels.api as sm
import sklearn.model_selection as model
import sklearn.neighbors as neighbors
import sklearn.metrics as metrics
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from bs4 import BeautifulSoup
from scipy.stats import norm
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import warnings
warnings.filterwarnings('ignore') # Ignorar qualquer aviso...

# Warning - This is only a draft since the code is considering '20230432' as a valid date, which is not correct.

sns.set_style("darkgrid")
plt.rcParams.update({"font.size":15})

current_date = int(input("User, Input the Current Date: "))

def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                ]
 
    return random.choice(uastrings)

def scrape_game_results(league, start_date):
    executable_path = "C:/Users/Bem-vindo(a)/Downloads/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = executable_path

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'user-agent={GET_UA()}')

    driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

    result_list = []

    for i in range(int(start_date), current_date+1):
        try:
            driver.get("https://www.espn.com.br/futebol/resultados/_/liga/"+league+"/data/"+str(i))
            driver.switch_to.window(driver.window_handles[0])

            time.sleep(5)

            # Check if game results are available on page
            if "Não há jogos para o filtro selecionado" in driver.page_source:
                continue

            # Scrape game results
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            games = soup.find_all('div', {'class': 'scoreboard football'})
            for game in games:
                # Extract data from game
                home_team = game.find('div', {'class': 'team-a'}).text.strip()
                away_team = game.find('div', {'class': 'team-b'}).text.strip()
                home_score = game.find('div', {'class': 'score icon-font-before'}).text.strip()
                away_score = game.find('div', {'class': 'score icon-font-after'}).text.strip()
                date = game.find('div', {'class': 'date-time'}).text.strip()
                # Store data in result_list
                game_data = {
                'date': date,
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score}
                result_list.append(game_data)
        except:
            continue

    driver.quit()

    return result_list

result_dict = scrape_game_results("bra.1","20230429")
