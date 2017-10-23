fragment.md

```
def browserSubmit():
	br = mechanize.Browser()
	br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')] 
	br.set_handle_robots(False)
	br.open('https://www.segmentfault.com/api/user/login?_=68a4ef6cadd98d965e90b4878300ed67')
	br.select_form(predicate = lambda f: 'id' in f.attrs and f.attrs['id'] == 'sic_login_form_user_login')
	br.form['username']='422351001@qq.com'
	br.form['password']='123mutouren789'
	br.submit()
```


```
# 将cookie存为一个文件
cookies.save(filename="cookie.txt")
```


```
 pattern = re.compile(r"(\d*)条\s*共(\d*)页")
        result = pattern.findall(span)
        print 'result is : ' + str(result)
        
        blog_count = int(result[0][0])
        page_count = int(result[0][1])
```


link = re.compile("\d+")
	content = "laowang-222haha"
	info = re.sub(link, 'www.cnpythoner.com', content)
	print info
	