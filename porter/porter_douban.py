# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import urllib
import ssl
import json
import shutil



nickName = '';

class CsdnHelper:

    post_url = 'https://www.douban.com/note/create';
    ck = '';
    url = '';

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    def __init__(self):
        self._session = requests.session()
        self._session.headers = CsdnHelper.headers


    def login(self, username, password):

        form_data = self._prepare_login_form_data()
        response = self._session.post(CsdnHelper.url, data=form_data)

      

        print response.text
        # print response
        print response.cookies

    def _prepare_login_form_data(self):
       
        data_file = open('config.json') 
        data = json.load(data_file)

        CsdnHelper.url = data["douban"]["login-url"]
        captcha_id = data["douban"]["captcha-id"]
        captcha_solution = data["douban"]["captcha-text"]
        username = data["douban"]["username"]
        password = data["douban"]["password"]

        form = {
            'form_email': str(username),
            'form_password': str(password),
            'remember': 'on',
            'login': '登录',
            'captcha-id':str(captcha_id),
            'captcha-solution':str(captcha_solution),
            'source': 'main'
        }
        print form
        return form
	
    def postArticle(self, username):

        data = self._prepare_post_form_data()

    	url = 'https://www.douban.com/note/create';
    	 

    	response = self._session.post(url, data=form_data)
    	print response
    	print response.text

    def _prepare_post_form_data(self):

        url = 'https://www.douban.com/note/create';
       


        response = self._session.get(url)
        page = BeautifulSoup(response.text, 'lxml')
        note_id = page.find('input', id='note_id')['value']
        ck = page.find('input', name='ck')['value']

        print 'note_id : '+note_id
        print 'ck: '+ck

        data = {
            "ck":ck,
            "note_id":note_id,
            "note_title":'title',
            "note_text":"text",
            "note_privacy":"P",
            "is_original":"on"
        }

        return data;



    



if __name__ == '__main__':

    username = 'a422351001@gmail.com'
    password = '123mutouren789'

    csdn_helper = CsdnHelper()
  
    csdn_helper.login(username, password);
    # csdn_helper.postArticle('');
    # csdn_helper.login2(username, password);
	



else:
    print 'being imported as module'


