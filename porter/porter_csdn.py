# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import urllib
import ssl
import json
from bs4 import BeautifulSoup


nickName = '';

class CsdnHelper:

    csdn_login_url = 'https://passport.csdn.net/account/login?ref=toolbar'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    blog_url = 'http://write.blog.csdn.net/postlist/'

    def __init__(self):
        self._session = requests.session()
        self._session.headers = CsdnHelper.headers


    def login(self, username, password):

        form_data = self._prepare_login_form_data(username, password)
        response = self._session.post(CsdnHelper.csdn_login_url, data=form_data)

        # print response.cookies

        if 'UserNick' in response.cookies:
            global nickName;
            nickName = response.cookies['UserNick']
            print (nickName)
        else:
            raise Exception('error')

        if 'access-token' in response.cookies:
        	CsdnHelper.headers['access-token'] = response.cookies['access-token'];
        	print 'CsdnHelper.headers ---> ' + str(CsdnHelper.headers)

        print 'cookies:' + str(self._session.cookies) + '--end'


	
    def postArticle(self, username):
    	a = 'liazohida'
    	print a 

    	# url = 'http://write.blog.csdn.net/postedit?gettag=1&r=0.20706791562686844'
    	url = 'http://write.blog.csdn.net/mdeditor/setArticle';
    	form_data = {
    		'title':'测试一下性能2',
    		'description':'%E5%A4%A7%E6%A0%87%E9%A2%98%E5%B0%8F%E6%A0%87%E9%A2%98',
    		'type':'repost',
    		'status':'0',
    		'level':'0',
    		'tags':'csdn',
    		'content':'%3Ch1%20id%3D%22%E5%A4%A7%E6%A0%87%E9%A2%98%22%3E%E5%A4%A7%E6%A0%87%E9%A2%98%3C%2Fh1%3E%0A%0A%3Ch2%20id%3D%22%E5%B0%8F%E6%A0%87%E9%A2%98%22%3E%E5%B0%8F%E6%A0%87%E9%A2%98%3C%2Fh2%3E' ,
    		'markdowncontent':'%23%20%E5%A4%A7%E6%A0%87%E9%A2%98%0A%0A%23%23%20%E5%B0%8F%E6%A0%87%E9%A2%98',
    		'catagories':'mysql',
    		'channel':'1',
    		'articleedittype':'1'
    	}

    	response = self._session.post(url, data=form_data)
    	print response
    	print response.text


    def _prepare_login_form_data(self, username, password):
        response = self._session.get(CsdnHelper.csdn_login_url)
        login_page = BeautifulSoup(response.text, 'lxml')
        login_form = login_page.find('form', id='fm1')
        lt = login_form.find('input', attrs={'name': 'lt'})['value']
        execution = login_form.find('input', attrs={'name': 'execution'})['value']
        eventId = login_form.find('input', attrs={'name': '_eventId'})['value']
        form = {
            'username': username,
            'password': password,
            'lt': lt,
            'execution': execution,
            '_eventId': eventId
        }
        return form

 	




if __name__ == '__main__':

    username = 'a422351001@gmail.com'
    password = '123mutouren789'

    csdn_helper = CsdnHelper()
    
    csdn_helper.login(username, password);
    # csdn_helper.postArticle('');
    # csdn_helper.login2(username, password);
	



else:
    print 'being imported as module'


