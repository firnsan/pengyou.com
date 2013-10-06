#!/usr/bin/env python
import sys
import re
import hashlib
import urllib
import urllib2
import cookielib

qq="123456789" #qq number
password="123456"
status="XDCTF2013" #status that you want to post to pengyou.com

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0')]
urllib2.install_opener(opener)


'''
generate password of bin(unsigned char),
just like the js function hexchar2bin() on pengyou.com
'''
def genBinpass(md5pass): 
	binpass= ""

	i=0
	while i<32:
		temp = chr(int(md5pass[i:i+2], 16))
		binpass+=temp
		i+=2
	return binpass



'''
generate id of bin(unsigned char),
just like the js function uin2hex on pengyou.com
'''
def genBinid(qq):
	
	hexid=str(hex(int(qq)))
	hexid=hexid[2:len(hexid)].upper()
	hexlen=len(hexid)
	while hexlen<16:
		hexid="0"+hexid
		hexlen=hexlen+1

	binid= ""
	i=0
	while i<16:
		temp = chr(int(hexid[i:i+2], 16))
		binid+=temp
		i+=2
	return binid


'''

def getLogsig(): 
	url = "http://ui.ptlogin2.pengyou.com/cgi-bin/login?appid=15004601&s_url=http://www.pengyou.com/index.php%3fmod%3Dlogin2%26act%3Dqqlogin"
	req = urllib2.Request(url)
	req.add_header("Referer","http://www.pengyou.com")
	html = opener.open(req).read()
	ret = re.findall('g_login_sig="([^"]*)"', html)
	return ret[0]
'''



'''
get verifycode,
I find this by spying the http request with a tool named charles,
which could set breakpoints on recv/send of http request
'''
def getVcode():
	url = "http://check.ptlogin2.pengyou.com/check?uin="+qq+"&appid=15004601&js_ver=10046&js_type=0&u1=http%3A%2F%2Fwww.pengyou.com%2Findex.php%3Fmod%3Dlogin2%26act%3Dqqlogin"
	req = urllib2.Request(url)
	req.add_header("Referer","http://www.pengyou.com")
	html = opener.open(req).read()
	ret = re.findall("(!...)", html)
	return ret[0]



def login(u,p,vc):
	url = "http://ptlogin2.pengyou.com/login?u="+u+"&p="+p+"&verifycode="+vc+"&aid=15004601&u1=http%3A%2F%2Fwww.pengyou.com%2Findex.php%3Fmod%3Dlogin2%26act%3Dqqlogin&h=1&ptredirect=1&ptlang=2052&from_ui=1&dumy=&fp=loginerroralert&action=6-20-36365&mibao_css=&t=1&g=1&js_type=0&js_ver=10046"
	req = urllib2.Request(url)
	req.add_header("Referer","http://www.pengyou.com")
	html = opener.open(req).read()
	print html



def getHostuin():
	print "please wait......"
	url = "http://home.pengyou.com/index.php?mod=home"
	req = urllib2.Request(url)
	req.add_header("Referer","http://www.pengyou.com")
	html = opener.open(req).read()
		
	ret=re.findall('"hash":"([0-9a-f]*)"', html)	
	return ret[0]

'''
we would fail(403 err) without the g_tk,when post the status
this function is writen by one player in XDCTF2013.
the function i wrote to get g_tk before XDCTF2013, is now failed
'''
def getGtk():
	for index, cookie in enumerate(cj):
	    if cookie.name == 'skey':
		skey = cookie.value
		break
	fixhash = 5381;
	l = len(skey);
	for i in range(0,l):
	    fixhash += (fixhash << 5) + ord(skey[i])

	gtk = fixhash & 2147483647	
	return gtk
	

'''
post the status
'''
def postStatus():
	gtk=str(getGtk())
	print "gtk:"+gtk

	hostuin=getHostuin()
	print "hostuin"+hostuin
	
	url="http://taotao.pengyou.com/cgi-bin/emotion_cgi_publish_v6?g_tk="+gtk;
	postdata="plattype=2&format=json&con="+status+"&feedversion=1&ver=1&hostuin="+hostuin+"&entryuin="+hostuin+"&noFormSender=1&plat=pengyou"
	req=urllib2.Request(url, postdata)
	req.add_header("Referer","http://www.pengyou.com")

	html = opener.open(req).read()
	print html
	

def main():	
	#logsig=getLogsig()
	#print "Logsig:"+logsig

	vcode=getVcode()
	print "Vcode:"+vcode

	uin=genBinid(qq)
	M=hashlib.md5(password).hexdigest().upper()
	I=genBinpass(M)

	H=hashlib.md5(I+uin).hexdigest().upper()
	G=hashlib.md5(H+vcode).hexdigest().upper()
	print "encrypted pass:"+G

	login(qq,G,vcode)

	postStatus()

if __name__ == '__main__':
	main()
