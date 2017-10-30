# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json
import urllib
import ssl
import sys
from bs4 import BeautifulSoup
from commonUtils import FileUtils
import time

class Helper:

	headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }

	def __init__(self):
		self._session = requests.session()
		self._session.headers = Helper.headers
		self.fileUtils = FileUtils()
		self.configData = self.fileUtils.loadConfigfile()
		self.blogname = 'csdn'
		self.filenameList = {}
		reload(sys)
		sys.setdefaultencoding("utf-8")
	 
	def login(self):
		form_data = self._prepare_login_form_data()
		response = self._session.post(self.configData[self.blogname]['login-url'], data=form_data)
		print response
		print response.cookies
		
		if(response.status_code == 200):
			print 'login succ!'
			if 'UserNick' in response.cookies:
				self.nickName = response.cookies['UserNick']
				return 0
			else:
				return -1
		else:
			print 'login fail'
			return -1
		

	
	def postArticle(self,filepath):
		## 文章处理
		proData = self.fileUtils.processor(filepath)
		content = self.fileUtils.mdToHtml(proData['text'])
		
		## 标签获取
		tags = self.filenameList[filename].split('|')
		tagstr = ''
		for tag in tags:
			try:
				response = self._session.post(
					self.configData[self.blogname]['tag-url'] + urllib.quote(tag.encode('utf-8')))
				jsonstr = response.text.split("(")[1][0:len(response.text.split("(")[1]) - 1]
				jsonstr = eval(jsonstr)
				lens = len(jsonstr['suggestions'])
				if(lens > 0):
					tagstr = jsonstr['suggestions'][0]
					break
			except  :
				print 'SyntaxError'
			
		if(tagstr == ''):
			tagstr = '后台'
			
		form_data = {
			'title':proData['title'],
			'description':proData['title'],
			'type':'original',
			'status':'0',
			'level':'0',
			'id':'',
			'tags':tagstr,
			'content':content ,
			'markdowncontent':'' ,
			'catagories':'mysql',
			'channel':'1',
			'articleedittype':'1'
		}
		
		print form_data
		
		response = ''
		while( response == ''):
			try:
				response = self._session.post(self.configData[self.blogname]['post-url'], data=form_data)
			except :
				time.sleep(5)
				continue
				
		print response
		print response.text
		if(response.json()['status'] == True):
			self.fileUtils.addbloglist(filepath, self.configData[self.blogname]['blog-list'])
			return 0
		else:
			return -2


	def _prepare_login_form_data(self):
		response = self._session.get(self.configData[self.blogname]['login-page'])
		login_page = BeautifulSoup(response.text, 'lxml')
		login_form = login_page.find('form', id='fm1')
		lt = login_form.find('input', attrs={'name': 'lt'})['value']
		execution = login_form.find('input', attrs={'name': 'execution'})['value']
		eventId = login_form.find('input', attrs={'name': '_eventId'})['value']
		form_data = {
		    'username': self.configData[self.blogname]['username'],
		    'password': self.configData[self.blogname]['password'],
		    'lt': lt,
		    'execution': execution,
		    '_eventId': eventId
		}
		print form_data
		return form_data
		

 	




if __name__ == '__main__':


	_helper = Helper()
	code = _helper.login()
	if code == 0:
		path = _helper.configData['blogDir']
		_helper.filenameList = _helper.fileUtils.dirCb(_helper.filenameList,path)
		print len(_helper.filenameList)
		for filename in _helper.filenameList:
			## 判断文章是否提交过
			if (_helper.fileUtils.wrongFile(_helper.filenameList,filename,_helper.configData[_helper.blogname]['blog-list'])):
				print '文件不符合上传条件'
			else:
				status = _helper.postArticle(filename)
				if(status == -2):
					break
				else:
					time.sleep(60)
	else:
		print '登录失败'
	
 
else:
	print 'being imported as module'


