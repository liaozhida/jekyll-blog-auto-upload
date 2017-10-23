# -*- coding: utf-8 -*-

import json
import requests
import sys, os
import time
import re
import urllib


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
		self.loadConfig()
		self._session = requests.session()
		self._session.headers = Helper.initheaders
		self._session.max_redirects = 60
		if (self.initHeader() != None):
			print 'use cached headers'
			self._session.headers = self.initHeader()
			print self._session.headers
		self.filenameList = {}
	
	def loadConfig(self):
		# 获取配置文件
		
		currentProject = os.path.dirname(sys.path[0])
		configStr = os.path.abspath(os.path.join(currentProject, 'config.json'))
		data_file = open(configStr)
		
		data = json.load(data_file)
		self.loginUrl = data["segment"]["login-url"]
		self.loginPage = data["segment"]["login-page"]
		self.postUrl = data["segment"]["post-url"]
		self.username = data["segment"]["username"]
		self.password = data["segment"]["password"]
		self.draftUrl = data["segment"]["draft-url"]
		self.tagUrl = data["segment"]["tag-url"]
		self.bloglist = data["segment"]["blog-list"]
	
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
					self.saveHeader()
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
		## 私人文章不上传
		privateTag = self.filenameList[filename]
		# print '---tag:'
		# print privateTag
		# print str(privateTag).find('工作')
		if (str(privateTag).find('工作') != -1 or str(privateTag).find('私人') != -1):
			return None
		
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
					self.addbloglist(filename)
				elif(res.json()['status'] == 1):
					print '文章发布失败:'
					print res.json()['data']
					shuzu = res.json()['data']
					for sz in shuzu:
						if(str(sz) != 'form'):
							print sz['captcha']
				else:
					print '文章发布失败:' + formdata['title'] + "  -:" + res.json()
			except:
				print '发布异常--'
				time.sleep(3)
				continue
		
		print '-- post end --'
	
	def _prepare_post_form_data(self, filename):
		
		## 获取提交文章需要的信息
		draftData = self.extractFile(filename)
		if (draftData == None):
			return None
		
		# print draftData
		# return None
		
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
	
	def addbloglist(self, filename):
		path = os.path.abspath(os.path.join(sys.path[0], '../bloglist/' + self.bloglist))
		file = open(path, 'a')
		file.write('\r\n'+filename.split('/')[len(filename.split('/'))-1])
		file.close()
	
	def isbloglist(self, filename):
		path = os.path.abspath(os.path.join(sys.path[0], '../bloglist/' + self.bloglist))
		# print 'path:' + filename
		# print path
		# print os.path.exists(path)
		
		filename = filename.split('/')[len(filename.split('/'))-1]
		
		if (os.path.exists(path)):
			filecontent = open(path).read()
			if (filecontent.find(filename) != -1):
				return True
			else:
				print '发现新文章 <<' + filename + '>>, 准备提交'
				return False
		else:
			file = open(path, 'w')
			file.write('过往提交文章记录:\r\n')
			file.close()
	
	def saveHeader(self):
		cookiepath = os.path.abspath(os.path.join(os.path.dirname('.'), 'cookie/segment_cookies'))
		file = open(cookiepath, 'w')
		cookies = self._session.headers
		json.dump(cookies, file)
		file.close()
	
	def dirCb(self, dirname):
		for line in os.listdir(dirname):
			filename = os.path.abspath(os.path.join(dirname, line))
			if (os.path.isdir(filename)):
				self.dirCb(filename)
			else:
				pattern = re.compile(r"(\d+)-(\d+)-(\d+)-(.{0,}.md)")
				result = pattern.findall(filename)
				if (len(result) != 0):
					tags = filename.split('_posts')[1]
					# print tags
					tagname = ''
					for tag in tags.split(os.sep):
						if (tag != '' and len(pattern.findall(tag)) == 0):
							tagname = tagname + '|' + tag
					tagname = tagname[1:]
					self.filenameList[filename] = tagname
				
				# for fn in self.filenameList:
				# 	print fn +' -t- '+self.filenameList[fn]
	
	def destroy(self):
		self._session.close()
	
	def extractFile(self, filename):
		
		data = {}
		## 长度
		file = open(filename)
		filecontent = file.read()
		print len(filecontent)
		
		if (len(filecontent) >= 75000):
			filecontent = filecontent[0:75000]
		
		## 链接添加
		pattern = re.compile(r"(\d+)-(\d+)-(\d+)-(.{0,}).md")
		# print filename
		result = pattern.findall(filename)
		# print result
		href = 'http://www.paraller.com/' + result[0][0] + '/' + result[0][1] + '/' + result[0][2] + '/' + urllib.quote_plus(result[0][3]) + '/'
		lience = '转载请注明出处 [http://www.paraller.com](http://www.paraller.com) \r\n  原文排版地址 [点击跳转](' + href + ')\r\n'
		# print lience
		
		## 处理头部注释
		pattern = re.compile(r"---(\n(.{0,}))*---")
		filecontent = re.sub(pattern, lience, filecontent)
		
		## 封装数据
		data = {
			"do": "saveArticle",
			"type": "1",
			"title": result[0][3],
			"text": filecontent,
			"weibo": "0",
			"blogId": "0",
			"aticleId": "",
			"id": "",
			"url": ""
		}
		
		print self.filenameList[filename]
		
		# 获取标签
		tags = self.filenameList[filename].split('|')
		tagsDict = []
		for tag in tags:
			# print tag + ' --> ' + filename
			data['tags[]'] = self.getTags(tag)
		
		return data
	
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
				res = self._session.get(self.tagUrl + urllib.quote_plus(tagname), timeout=5)
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
	code = _helper.login()
	
	# time.sleep(1200)
	
	if (code == 0):
		path = os.path.abspath(os.path.join(sys.path[0], '../../'))
		_helper.dirCb(path)
		for filename in _helper.filenameList:
			## 判断文章是否提交过
			if (_helper.isbloglist(filename)):
				print '文件存在 bl'
			else:
				_helper.postArticle(filename)
				time.sleep(120)
	else:
		print '登录失败'
	
	_helper.destroy()

	
	# _helper.extractFile('/Users/zhidaliao/Desktop/zhida_blog/_posts/运维 & 主机 & 系统搭建/2016-05-22-gitlab-runner-maven卡死的情况.md')
	
	# _helper.postArticle('/Users/zhidaliao/Desktop/zhida_blog/_posts/运维 & 主机 & 系统搭建/2016-05-22-gitlab-runner-maven卡死的情况.md')
	
	# _helper._prepare_post_form_data('/Users/zhidaliao/Desktop/zhida_blog/_posts/运维 & 主机 & 系统搭建/2016-05-22-gitlab-runner-maven卡死的情况.md')
	# 遍历文章
	# _helper.loopDir()
	#	_helper.dirCb('docker')
	# if(code == 0):
	# 	_helper.postArticle()
	# _helper.destroy()




else:
	print 'being imported as module'


