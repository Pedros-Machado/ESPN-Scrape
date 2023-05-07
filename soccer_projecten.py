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

sns.set_style("darkgrid")
plt.rcParams.update({"font.size":15})

current_year = int(input("User, Input the Current Year: "))

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

def get_classif(league, start_date):
    executable_path = "C:/Users/Bem-vindo(a)/Downloads/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = executable_path

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'user-agent={GET_UA()}')

    driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

    result_dict = {}

    for i in range(int(start_date), current_year):
        driver.get("https://www.espn.com.br/futebol/classificacao/_/liga/"+league+"/temporada/"+str(i))
        driver.switch_to.window(driver.window_handles[0])

        time.sleep(5)

        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', {'class': 'Table Table--align-right'})
            data = []
            for row in table.find_all('tr'):
                cols = [col.text.strip() for col in row.find_all('td')]
                if cols:
                    data.append(cols)
                
            soup2 = BeautifulSoup(driver.page_source, 'html.parser')
            table2 = soup2.find('table', {'class': 'Table Table--align-right Table--fixed Table--fixed-left'})
            data2 = []
            for row in table2.find_all('tr'):
                cols2 = [col.text.strip() for col in row.find_all('td')]
                if cols2:
                    data2.append(cols2)
        except:
            pass
        
        df = pd.DataFrame(data)
        df.reset_index(inplace=True)
        
        df["index"]=data2
        df.rename(columns={"index":"Teams",0:"Games",1:"Wins",2:"Draws"
                           ,3:"Losses",4:"Goals For",5:"Goals Against",
                           6:"Goal Difference",7:"Points"},inplace=True)
        
        df['Teams'] = df['Teams'].str[0]
        df['Teams'] = df['Teams'].str.extract('(\D+)')
        df['Teams'] = df['Teams'].str[3:]
        df.iloc[:, 1:] = df.iloc[:, 1:].applymap(pd.to_numeric)


        result_dict[i] = df
    return result_dict

def team_history(start_date):
    historical_dict = {}
    for i in range(int(start_date), current_year):
        year_dict = result_dict[i].set_index('Teams').to_dict('series')
        historical_dict[i] = year_dict
    return historical_dict

def evolution_values(team,index,start_date):
    values_list = []
    years = range(int(start_date), current_year)
    for year in years:
        values_list.append(historical_dict[year][index][team])
    plt.figure(figsize=(11,7))
    plt.plot(years, values_list)
    plt.xlabel('Year')
    plt.ylabel(f"{index}")
    plt.title(f"Historical {index} - {team}")
    plt.show()

team_list = ["Manchester City","Arsenal"]

def multiple_team_plot(index, start_date,team=team_list):
    if isinstance(team, str):
        team = [team]

    values_dict = {}
    years = range(int(start_date), current_year)
    for t in team:
        values_list = []
        for year in years:
            values_list.append(historical_dict[year][index][t])
        values_dict[t] = values_list

    plt.figure(figsize=(11, 7))
    for t in team:
        plt.plot(years, values_dict[t], label=t,alpha=0.45)
    plt.xlabel('Year')
    plt.ylabel(index)
    plt.title(f"Historical {index} - Each Team")
    plt.legend(loc='upper left',framealpha=0.55)
    plt.show()


result_dict = get_classif("eng.1","2015")

historical_dict = team_history("2015")

evolution_values("Arsenal","Wins","2015")

evolution_values("Manchester City","Wins","2015")

multiple_team_plot("Losses","2015")