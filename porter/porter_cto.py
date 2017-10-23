# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import urllib
import ssl
import json


nickName = '';

class CsdnHelper:

    url = 'http://home.51cto.com/index?reback=http://blog.51cto.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    def __init__(self):
        self._session = requests.session()
        self._session.headers = CsdnHelper.headers


    def login(self, username, password):

        form_data = self._prepare_login_form_data(username, password)
        response = self._session.post(CsdnHelper.url, data=form_data)

        print response.cookies

        # if 'UserNick' in response.cookies:
        #     global nickName;
        #     nickName = response.cookies['UserNick']
        #     print (nickName)
        # else:
        #     raise Exception('error')

        # if 'access-token' in response.cookies:
        # 	CsdnHelper.headers['access-token'] = response.cookies['access-token'];
        # 	print 'CsdnHelper.headers ---> ' + str(CsdnHelper.headers)

        # print 'cookies:' + str(self._session.cookies) + '--end'


	
  


    def _prepare_login_form_data(self, username, password):

        response = self._session.get(CsdnHelper.url)
        login_page = BeautifulSoup(response.text, 'lxml')
        login_form = login_page.find('meta', attrs={'name': 'csrf-token'})['content'].strip()
        form = {
            'LoginForm[username]': username,
            'LoginForm[password]': password,
            'LoginForm[rememberMe]': '1',
            'login-button': '登录',
            '_csrf': str(login_form)
        }
        return form

 	




if __name__ == '__main__':

    username = '422351001@qq.com'
    password = '123mutouren789';

    csdn_helper = CsdnHelper()
    
    csdn_helper.login(username, password);
    # csdn_helper.postArticle('');
    # csdn_helper.login2(username, password);
	



else:
    print 'being imported as module'


