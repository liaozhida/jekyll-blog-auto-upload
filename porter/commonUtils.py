# -*- coding: utf-8 -*-

import os,sys
import json
import re
import markdown
import codecs
import urllib

class FileUtils:
	
	css = '''
			html { font-size: 100%; overflow-y: scroll; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }

	body{
	color:#444;
	font-family:Georgia, Palatino, 'Palatino Linotype', Times, 'Times New Roman', serif;
	font-size:12px;
	line-height:1.5em;
	padding:1em;
	margin:auto;
	max-width:42em;
	background:#fefefe;
	}

	a{ color: #0645ad; text-decoration:none;}
	a:visited{ color: #0b0080; }
	a:hover{ color: #06e; }
	a:active{ color:#faa700; }
	a:focus{ outline: thin dotted; }
	a:hover, a:active{ outline: 0; }

	::-moz-selection{background:rgba(255,255,0,0.3);color:#000}
	::selection{background:rgba(255,255,0,0.3);color:#000}

	a::-moz-selection{background:rgba(255,255,0,0.3);color:#0645ad}
	a::selection{background:rgba(255,255,0,0.3);color:#0645ad}

	p{
	margin:1em 0;
	}

	img{
	max-width:100%;
	}

	h1,h2,h3,h4,h5,h6{
	font-weight:normal;
	color:#111;
	line-height:1em;
	}
	h4,h5,h6{ font-weight: bold; }
	h1{ font-size:2.5em; }
	h2{ font-size:2em; }
	h3{ font-size:1.5em; }
	h4{ font-size:1.2em; }
	h5{ font-size:1em; }
	h6{ font-size:0.9em; }

	blockquote{
	color:#666666;
	margin:0;
	padding-left: 3em;
	border-left: 0.5em #EEE solid;
	}
	hr { display: block; height: 2px; border: 0; border-top: 1px solid #aaa;border-bottom: 1px solid #eee; margin: 1em 0; padding: 0; }
	pre, code, kbd, samp { color: #000; font-family: monospace, monospace; _font-family: 'courier new', monospace; font-size: 0.98em; }
	pre { white-space: pre; white-space: pre-wrap; word-wrap: break-word; }

	b, strong { font-weight: bold; }

	dfn { font-style: italic; }

	ins { background: #ff9; color: #000; text-decoration: none; }

	mark { background: #ff0; color: #000; font-style: italic; font-weight: bold; }

	sub, sup { font-size: 75%; line-height: 0; position: relative; vertical-align: baseline; }
	sup { top: -0.5em; }
	sub { bottom: -0.25em; }

	ul, ol { margin: 1em 0; padding: 0 0 0 2em; }
	li p:last-child { margin:0 }
	dd { margin: 0 0 0 2em; }

	img { border: 0; -ms-interpolation-mode: bicubic; vertical-align: middle; }

	table {
	border-collapse: collapse;
	border-spacing: 0;
	width: 100%;
	}
	th { border-bottom: 1px solid black; }
	td { vertical-align: top; }

	@media only screen and (min-width: 480px) {
	body{font-size:14px;}
	}

	@media only screen and (min-width: 768px) {
	body{font-size:16px;}
	}

	@media print {
	  * { background: transparent !important; color: black !important; filter:none !important; -ms-filter: none !important; }
	  body{font-size:12pt; max-width:100%;}
	  a, a:visited { text-decoration: underline; }
	  hr { height: 1px; border:0; border-bottom:1px solid black; }
	  a[href]:after { content: " (" attr(href) ")"; }
	  abbr[title]:after { content: " (" attr(title) ")"; }
	  .ir a:after, a[href^="javascript:"]:after, a[href^="#"]:after { content: ""; }
	  pre, blockquote { border: 1px solid #999; padding-right: 1em; page-break-inside: avoid; }
	  tr, img { page-break-inside: avoid; }
	  img { max-width: 100% !important; }
	  @page :left { margin: 15mm 20mm 15mm 10mm; }
	  @page :right { margin: 15mm 10mm 15mm 20mm; }
	  p, h2, h3 { orphans: 3; widows: 3; }
	  h2, h3 { page-break-after: avoid; }
	}
		'''
	
	def __init__(self):
		reload(sys)
		sys.setdefaultencoding("utf-8")
		
	## 加载配置文件返回json格式数据
	def loadConfigfile(self):
		currentProject = os.path.dirname(sys.path[0])
		configStr = os.path.abspath(os.path.join(currentProject, 'config.json'))
		data_file = open(configStr)
		return json.load(data_file)
	
	def dirCb(self,filenameList,dirname):
		for line in os.listdir(dirname):
			
			filename = os.path.abspath(os.path.join(dirname, line))
			if (os.path.isdir(filename)):
				self.dirCb(filenameList,filename)
			else:
				pattern = re.compile(r"(\d+)-(\d+)-(\d+)-(.{0,}.md)")
				result = pattern.findall(filename)
				# print result
				# print filename
				if (len(result) != 0):
					print '!=0'
					print filename
					tags = filename.split('_posts')[1]
					tagname = ''
					for tag in tags.split(os.sep):
						if (tag != '' and len(pattern.findall(tag)) == 0):
							tagname = tagname + '|' + tag
					tagname = tagname[1:]
					filenameList[filename] = tagname
		
		print 'last len:'
		print
		return filenameList
	
	def wrongFile(self, filenameList,filepath,blname):
		## 私人文章不上传
		privateTag = filenameList[filepath]
		if (str(privateTag).find('工作') != -1 or str(privateTag).find('私人') != -1):
			return True
		
		## 黑名单不上传
		blackpath = os.path.abspath(os.path.join(sys.path[0], '../bloglist/blacklist'))
		filemdname = filepath.split('/')[len(filepath.split('/')) - 1]
		blackcontent = open(blackpath).read()
		if (blackcontent.find(filemdname) != -1):
			return True
		
		## 是否上传过
		path = os.path.abspath(os.path.join(sys.path[0], '../bloglist/' + blname))
		filename = filepath.split('/')[len(filepath.split('/')) - 1]
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
				
	def mdToHtml(self,filecontent):
		## //TODO 添加样式
		html = markdown.markdown(filecontent)
		return html
	
	def addbloglist(self, filepath,blname):
		path = os.path.abspath(os.path.join(sys.path[0], '../bloglist/' + blname))
		file = open(path, 'a')
		file.write('\r\n'+filepath.split('/')[len(filepath.split('/'))-1])
		file.close()
		
	def processor(self, pathname):
		data = {}
		## 长度
		file = open(pathname)
		filecontent = file.read()
		print len(filecontent)
		
		if (len(filecontent) >= 65000):
			filecontent = filecontent[0:65000]
		
		## 链接添加
		pattern = re.compile(r"(\d+)-(\d+)-(\d+)-(.{0,}).md")
		# print filename
		result = pattern.findall(pathname)
		href = 'http://www.paraller.com/' + result[0][0] + '/' + result[0][1] + '/' + result[0][2] + '/' +  urllib.quote(result[0][3].encode('utf-8')) + '/'
		lience = '转载请注明出处 [http://www.paraller.com](http://www.paraller.com) \r\n  原文排版地址 [点击获取更好阅读体验](' + href + ')\r\n'
		# print lience
		
		## 处理头部注释
		pattern = re.compile(r"---(\n(.{0,}))*---")
		filecontent = re.sub(pattern, lience, filecontent)
		data['title'] = result[0][3]
		data['text'] = filecontent
		return data
	
if __name__ =='__main__':
	print 'main'
else:
	print 'module'