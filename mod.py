# Функция для запроса к Яндексу.Диску:
import requests
from urllib.parse import urlencode
from operator import attrgetter
from datetime import timedelta
import pandas as pd
import numpy as np
import scipy
import scipy.stats as ss
from tqdm.auto import tqdm
import random as rm
import matplotlib.pyplot as plt 


def download_yandex_disk(public_key):
    """
    Эта функции предназначена для загрузки файла с Яндекс.Диска по его публичной ссылке (public_key).  
    В базовый URL, который будет использоваться для запроса на сервер Яндекс.Диска, добавляется параметр public_key,
    преобразованный в словарь и закодированный функцией urlencode. 
    С помощью библиотеки requests функция отправляет GET-запрос по сформированному URL и получает ответ в JSON формате. 
    Извлечение файла происходит путем доступа к ключу "href". 
    Функция возвращает полученную ссылку на загрузку файла с Яндекс.Диска.
    """
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']
    return download_url

def t_simulation(control, test, simulations=5000, size=100):
    result = []
    for i in tqdm(range(simulations)):
        s_1 = rm.sample(list(control), size) 
        s_2 = rm.sample(list(test), size) 
        
        result.append(ss.ttest_ind(s_1, s_2, equal_var=False)[1])
    return [result, simulations]


def chi2_simulation(control, test, simulations=5000, size=100):
    result = []
    for i in tqdm(range(simulations)):    
        s1 = control.sample(n_s, replace = False)
        s2 = test.sample(n_s, replace = False)
        a_premium = s1.sum()
        a_nopremium = s1.size - s1.sum()
        b_premium = s2.sum()
        b_nopremium = s2.size - s2.sum()
        T = np.array([[a_premium, a_nopremium], [b_premium, b_nopremium]])
        result.append(ss.chi2_contingency(T,correction=False)[1]) # сохраняем pvalue
    return [result, simulations]

def FPR_graph(result, alfa=0.05):  
    # проверка результат ложноположительных тестов не превышает alfa
    fpr = sum(np.array(result[0]) < alfa) / result[1]  
    color='tomato'       
    plt.hist(result[0], color=color, bins=50)
    plt.xlabel('p-value')
    plt.ylabel('frequency')
    text = 'p-value distribution '
    plt.title(text)
    plt.show()
    print(f'α={alfa}, FPR={fpr}')