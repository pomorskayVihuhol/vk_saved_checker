# -*- coding: utf-8 -*-
import time
import random
from selenium import webdriver
from fake_useragent import UserAgent
from multiprocessing import Pool
import datetime
import os
import json
import csv
from bs4 import BeautifulSoup as BS
import pickle
import requests

def get_starting_data(is_newby):
    print('Hi,sir! How many users do you want to follow? 1,2,3...?')
    number_to_follow = int(input())
    print('That\'s nice. Enter their link profiles, please:')

    urls = []
    for i in range(number_to_follow):
        urls.append('https://vk.com/'+input())

    file = open('ids.txt', 'w', encoding='utf-8')
    for url in urls:
        file.write(url + '\n')


        #добавить проверку
    file.close()
    print('Thank you! Ids are succeessfully recorded.')
    if(is_newby == 'Yes'):
        print('Enter your vk login:')
        login = input()
        print('Enter your vk password:')
        password = input()
        file = open('auth_data.txt','w')
        file.write(login+'\n')
        file.write(password)
        file.close()
        print('It worked like a swiss watch! Your authentication data was recorded.')
    #путь до webdriver


path = "B:\\Parser\\Selenium_exercise\\chrome_driver\\chromedriver.exe"

def get_last_photo(ans):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = True
    browser = webdriver.Chrome(executable_path=path,options=options)

    browser.get('https://vk.com/')
    time.sleep(5)

    #загрузка логина и пароля из файла
    with open('auth_data.txt', 'r') as wile:
        auth_list = wile.read().split('\n')
    login = auth_list[0]
    password = auth_list[1]

    #загрукза cookies
    if ans == 'No':
        for cookie in pickle.load(open(f'{login}_cookies', 'rb')):
            browser.add_cookie(cookie)
        time.sleep(5)
        print('Cookies uploaded!')

    #полная авторизация + выгрузка cookies
    if ans == 'Yes':
        email_form = browser.find_element_by_id('index_email')
        email_form.send_keys(login)
        pass_form = browser.find_element_by_id('index_pass')
        pass_form.send_keys(password)
        browser.find_element_by_id('index_login_button').click()
        time.sleep(4)
        pickle.dump( browser.get_cookies(), open(f'{login}_cookies', 'wb') )
        time.sleep(5)
        print('Cookies downloaded!')

    with open('ids.txt','r')as file:
        ids = file.read()
    ids = ids.split('\n')
    dict_last_saved_id = {}
    #сбор id последней сохранёнки
    file = open('last_saved.json', 'w', encoding='utf-8')
    for id in ids:
        if id != '':
            browser.get('https://vk.com/album'+id+'_000')
            src = browser.page_source
            soup = BS(src, 'html.parser')
            last_photo_id = soup.find('div', id='photos_container_photos').findChild('a').get('data-photo-id') #40 фото загружается
            dict_last_saved_id[id] = last_photo_id
            time.sleep(5)
    json.dump(dict_last_saved_id,file, indent=4, ensure_ascii=False)
    file.close()

    browser.quit()


def check_new_photos(ans):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = True
    browser = webdriver.Chrome(executable_path=path,
                               options=options)

    browser.get('https://vk.com/')
    time.sleep(5)

    # загрузка логина и пароля из файла
    with open('auth_data.txt', 'r') as wile:
        auth_list = wile.read().split('\n')
    login = auth_list[0]
    password = auth_list[1]

    # загрукза cookies
    if ans == 'No':
        for cookie in pickle.load(open(f'{login}_cookies', 'rb')):
            browser.add_cookie(cookie)
        time.sleep(5)
        #print('Cookies uploaded!')

    # полная авторизация + выгрузка cookies
    if ans == 'Yes':
        email_form = browser.find_element_by_id('index_email')
        email_form.send_keys(login)
        pass_form = browser.find_element_by_id('index_pass')
        pass_form.send_keys(password)
        browser.find_element_by_id('index_login_button').click()
        time.sleep(4)
        pickle.dump(browser.get_cookies(), open(f'{login}_cookies', 'wb'))
        time.sleep(5)
        #print('Cookies downloaded!')

    with open('ids.txt','r')as file:
        ids = file.read()
    ids = ids.split('\n')

    with open('last_saved.json', 'r') as file:
        last_saved_by_id = json.load(file)

    new_saved = {}
    #проверка как далеко сохранённое нами фото от последней сохранённой в альбоме
    for id in ids:
        if id!='':
            browser.get('https://vk.com/album'+id+'_000')
            src = browser.page_source
            soup = BS(src, 'html.parser')
            time.sleep(5)

            last_saved = last_saved_by_id[id]

            latest_saved = []
            for save in soup.find('div', id='photos_container_photos').findChildren('a'):
                latest_saved.append(save.get('data-photo-id'))

            if latest_saved.count(last_saved) == 1:
                news = latest_saved.index(last_saved)
            else:
                news = '40+'
            new_saved[id] = news

    return new_saved

def get_ids(ans):


    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = True
    browser = webdriver.Chrome(executable_path=path,
                               options=options)

    browser.get('https://vk.com/')
    time.sleep(5)

    # загрузка логина и пароля из файла
    with open('auth_data.txt', 'r') as wile:
        auth_list = wile.read().split('\n')
    login = auth_list[0]
    password = auth_list[1]

    # загрукза cookies
    if ans == 'No':
        for cookie in pickle.load(open(f'{login}_cookies', 'rb')):
            browser.add_cookie(cookie)
        time.sleep(5)
        #print('Cookies uploaded!')

    # полная авторизация + выгрузка cookies
    if ans == 'Yes':
        email_form = browser.find_element_by_id('index_email')
        email_form.send_keys(login)
        pass_form = browser.find_element_by_id('index_pass')
        pass_form.send_keys(password)
        browser.find_element_by_id('index_login_button').click()
        time.sleep(4)
        pickle.dump(browser.get_cookies(), open(f'{login}_cookies', 'wb'))
        time.sleep(5)
        #print('Cookies downloaded!')
    file = open('ids.txt','r', encoding='utf-8')
    ids = []
    for url in file.read().split('\n'):
        if 'vk' in url:
            url = url.strip()
            browser.get(url)
            time.sleep(5)
            src = browser.page_source
            soup = BS(src, 'html.parser')
            id = soup.find('div', class_='module clear photos_module').find('a',class_ ='module_header').get('href')
            ids.append(id[7:])
    file.close()
    browser.quit()
    file = open('ids.txt','w',encoding='utf-8')
    for id in ids:
        file.write(id+'\n')
    file.close()





if __name__=='__main__':
    print('Start!')
    print('First time here? Yes or No:' + '\n' + '*'*30)
    is_newby = input()
    get_starting_data(is_newby)
    get_ids(is_newby)
    ans = ''
    while (ans!='EXIT'):
        print('Do you want to UPDATE last photo or CHECK how many photos were added since last UPDATE? \nPrint EXIT to exit\n' + '*'*30)
        ans = input()
        if ans == 'UPDATE':
            get_last_photo(is_newby)
        if ans == 'CHECK':
            print(check_new_photos(is_newby))

