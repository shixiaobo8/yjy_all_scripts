#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	requests， pycurl 模拟登陆jenkins
"""
import requests
import pycurl
from io import BytesIO


# 获取jenkins 指定job 配置信息
def getJobInfos(jobname):
	login_url = 'https://xxxx.com/login?from=%2Fapi%2F'
	job_url = 'https://xxxxxx.xxx.com/job/' + jobname + '/api/python?pretty=true'
	login_data = {'username':'xxxxx','password':'xxxxxx'}
	#建立curl 对象
	curl = pycurl.Curl()
	# 设置curl 地址
	curl.setopt(curl.URL,job_url)
	# 忽略curl ssl 证书验证
	curl.setopt(pycurl.SSL_VERIFYPEER,0)
	# 忽略curl ssl 主机验证
	curl.setopt(pycurl.SSL_VERIFYHOST,0)
	# 设置登陆信息
	curl.setopt(pycurl.USERNAME,login_data['username'])
	curl.setopt(pycurl.PASSWORD,login_data['password'])
	# 设置不打印结果到控制台
	curl.setopt(pycurl.VERBOSE,0)
	# 建立结果缓存对象
	buffer = BytesIO()
	# 设置结果保存到缓冲区
	curl.setopt(curl.WRITEDATA,buffer)
	# 发送curl请求
	curl.perform()
	# 关闭pycurl
	curl.close()
	# 获取curl 字符串结果集
	res = buffer.getvalue()
	# 去掉换行符并转化为josn对象
	res = res.replace('\n','')
	res = eval(res)
	print res
	return res

	
if __name__ == '__main__':
	h5_job = 'AT_PROD_WESURE_H5_DEPLOY'
	getJobInfos(h5_job)
