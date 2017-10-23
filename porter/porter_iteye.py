# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import urllib
import ssl
import json


nickName = '';

class CsdnHelper:

    url = 'http://www.iteye.com/login'
    index_url = '';
    authenticity_token = '';

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    def __init__(self):
        self._session = requests.session()
        self._session.headers = CsdnHelper.headers


    def login(self, username, password):

        form_data = self._prepare_login_form_data(username, password)
        response = self._session.post(CsdnHelper.url, data=form_data)

        # print response.text

        page = BeautifulSoup(response.text, 'lxml')
        CsdnHelper.index_url = page.find('a', attrs={'class': 'welcome'})['href']

        print 'CsdnHelper.index_url:' + CsdnHelper.index_url

        # print response.text

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
        CsdnHelper.authenticity_token = login_page.find('input', attrs={'name': 'authenticity_token'})['value'].strip()


        form = {
            'name': username,
            'password': password,
            'button': '登 录',
            'authenticity_token': str( CsdnHelper.authenticity_token)
        }
        return form

 	
    def _prepare_post_form_data(self):
        form = {
            'blog[blog_type]': '1',
            'blog[title]':'测试发送',
            'blog[bbcode]':'true',
            'blog[body]':'测试\r\n一下',
            'blog[diggable]':'1',
            'commit':'发布',
            'blog[whole_category_id]':'4',
            'authenticity_token':  CsdnHelper.authenticity_token
        }
        return form

    def postArticle(self):

        data = self._prepare_post_form_data()
        print 'CsdnHelper.index_url: ' + CsdnHelper.index_url
        response = self._session.post(CsdnHelper.index_url+'/admin/blogs',data=data)

        print response



    


if __name__ == '__main__':

    username = '422351001@qq.com'
    password = '123mutouren789';

    csdn_helper = CsdnHelper()
    
    csdn_helper.login(username, password);
    csdn_helper.postArticle();
	



else:
    print 'being imported as module'


