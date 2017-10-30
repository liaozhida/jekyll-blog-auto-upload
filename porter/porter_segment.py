# -*- coding: utf-8 -*-
import json
import requests
import sys, os
import time
import re
import urllib
from commonUtils import FileUtils

class Helper:
	initheaders = {
		"Host": "segmentfault.com",
		"Connection": "keep-alive",
		"Content-Length": "55",
		"Accept": "*/*",
		"Origin": "https://segmentfault.com",
		"X-Requested-With": "XMLHttpRequest",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"DNT": "1",
		"Referer": "https://segmentfault.com/",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2",
		"Pragma": "no-cache",
		"Cache-Control": "no-cache",
		"Cookie": "PHPSESSID=web3~fdf535b2518f7f061780d987bb65934a; _gat=1; io=onpREhr-L-d7pRxJHvSF; Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1508383051,1508500169,1508563643,1508565378; Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1508569683; _ga=GA1.2.613128477.1495522770; _gid=GA1.2.1217955936.1508498183"
	}
	
	def __init__(self):
		self.filenameList = {}
		self.fileUtils = FileUtils()
		self.loadConfig()
		self._session = requests.session()
		self._session.headers = Helper.initheaders
		self._session.max_redirects = 60
		if (self.initHeader() != None):
			print 'use cached headers'
			self._session.headers = self.initHeader()
			print self._session.headers
		
		reload(sys)
		sys.setdefaultencoding("utf-8")
	
	def loadConfig(self):
		# 获取配置文件
		
		self.configData = self.fileUtils.loadConfigfile()
		self.loginUrl = self.configData["segment"]["login-url"]
		self.loginPage = self.configData["segment"]["login-page"]
		self.postUrl = self.configData["segment"]["post-url"]
		self.username = self.configData["segment"]["username"]
		self.password = self.configData["segment"]["password"]
		self.draftUrl = self.configData["segment"]["draft-url"]
		self.tagUrl = self.configData["segment"]["tag-url"]
		self.bloglist = self.configData["segment"]["blog-list"]
	
	def initHeader(self):
		try:
			cookiepath = os.path.abspath(os.path.join(os.path.dirname('.'), 'cookie/segment_cookies'))
			data_file = open(cookiepath, 'r')
			data = json.load(data_file)
			return data
		except ValueError, e:
			print 'cache-cookie is None'
			return None
		except IOError, e:
			print 'file is not found'
			return None
	
	def login(self):
		
		# 使用緩存登陸 //TODO   //TODO token
		# try:
		# 	print self._session.headers
		# 	res = self._session.post(self.loginUrl + '?_=b56c39ea0c0d50b3dd9e5fa11d9e2f00', timeout=10)
		# except requests.exceptions.ReadTimeout,e:
		# 	print '使用緩存登錄失敗'
		
		res = ''
		while (res == ''):
			try:
				data = self._prepare_login_form_data()
				res = self._session.post(self.loginUrl, data=data, timeout=10)
				print res
				if (res.status_code == 200):
					print 'login succ'
					return 0
				else:
					print 'login fail'
			
			except ValueError, e:
				print e
				print 'use cached login is succ'
				return 'succ'
			except requests.exceptions.ConnectionError:
				print 'requests.exceptions.ConnectionError  try again'
				time.sleep(2)
				print 'sleep over'
				continue
	
	def _prepare_login_form_data(self):
		
		# 封装返回数据
		form = {
			'username': str(self.username),
			'password': str(self.password),
			'remember': "1"
		}
		print form
		return form
	
	def postArticle(self, filename):
		
		self._session.headers['Referer'] = 'https://segmentfault.com/write?freshman=1'
		formdata = self._prepare_post_form_data(filename)
		if (formdata == None):
			return None
		else:
			print 'post article data:'
			print formdata
		
		res = ''
		while (res==''):
			try:
				res = self._session.post(self.postUrl, data=formdata, timeout=10)
				print res
				print res.text
				if (res.json()['status'] == 0):
					print '文章发布成功:' + formdata['title']
					self.fileUtils.addbloglist(filename,self.bloglist)
				elif(res.json()['status'] == 1):
					print '文章发布失败:'
					print res.json()['data']
					return -2
					# shuzu = res.json()['data']
					# for sz in shuzu:
					# 	if(str(sz) != 'form'):
					# 		print sz['captcha']
				else:
					print '文章发布失败:' + formdata['title'] + "  -:" + res.json()
			except:
				print '发布异常--'
				time.sleep(3)
				continue
		
		print '-- post end --'
	
	def _prepare_post_form_data(self, filename):
	
		## 获取提交文章需要的信息
		proData = self.fileUtils.processor(filename)
		
		## 封装数据
		data = {
			"do": "saveArticle",
			"type": "1",
			"title": proData['title'],
			"text": proData['text'],
			"weibo": "0",
			"blogId": "0",
			"aticleId": "",
			"id": "",
			"url": ""
		}
		
		# 获取标签
		tags = self.filenameList[filename].split('|')
		tagsDict = []
		for tag in tags:
			# print tag + ' --> ' + filename
			data['tags[]'] = self.getTags(tag)
			
		draftData = data
		
		
		if (draftData == None):
			return None
		
		print draftData
		# return None
		
		print 'text size:'
		print len(draftData['text'])
		
		print '-- save draft --'
		artId = ''
		res = ''
		while (res == ''):
			try:
				res = self._session.post(self.draftUrl, data=draftData, timeout=10)
				status = res.json()['status']
				if (status == 0):
					artId = res.json()['data']
					print '保存草稿成功'
				else:
					print res.text
					print res.json()['data']
					shuzu = res.json()['data']
					for sz in shuzu:
						if (str(sz) != 'form'):
							print sz['text']
					print '保存草稿失败'
					return None
			except:
				print '保存草稿出现异常'
				time.sleep(2)
				continue
		
		del draftData['do']
		del draftData['aticleId']
		draftData['license'] = '1'
		draftData['draftId'] = artId
		draftData['createId'] = ''
		draftData['newsType'] = '1490000006201495'
		
		return draftData
	
	
	

	
	

	
	def destroy(self):
		self._session.close()
	
	def getTags(self, tagname):
		## 标签处理
		self._session.headers['Referer'] = 'https://segmentfault.com/write?freshman=1'
		if (self._session.headers.has_key('Origin')):
			del self._session.headers['Origin']
			del self._session.headers['Content-Length']
			del self._session.headers['Content-Type']
		
		res = ''
		while res == '':
			try:
				# print 'getTags:'
				# print self.tagUrl + urllib.quote_plus(tagname)
				res = self._session.get(self.tagUrl + tagname, timeout=5)
			except:
				time.sleep(2)
				print 'ag'
				continue
		
		print res.text
		if (len(res.json()['data']) == 0):
			print 'could not found tag,ag'
			## 如果最后没有找到合适的标签 统一置为 后台类型
			if(len(tagname) == 1):
				tagname = '后台 '
			print tagname[0:len(tagname) - 1]
			return self.getTags(tagname[0:len(tagname) - 1])
		else:
			print res.json()['data'][0]['name']
			return res.json()['data'][0]['id']


if __name__ == '__main__':
	
	_helper = Helper()
	code = 0
	# code = _helper.login()
	
	# time.sleep(1200)
	
	if (code == 0):
		path = _helper.configData['blogDir']
		print path
		_helper.filenameList = _helper.fileUtils.dirCb(_helper.filenameList,path)
		print len(_helper.filenameList)
		for filename in _helper.filenameList:
			## 判断文章是否提交过
			if (_helper.fileUtils.wrongFile(_helper.filenameList,filename,_helper.bloglist)):
				print '文件不符合上传条件'
			else:
				status = _helper.postArticle(filename)
				if(status == -2):
					break
				else:
					time.sleep(300)
	else:
		print '登录失败'
	
	_helper.destroy()


else:
	print 'being imported as module'


