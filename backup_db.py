#!/usr/bin/env python
# -*- coding:utf8 -*-

"""备份数据库"""

import os,sys,commands,time,json,threading
import paramiko as pmk

src_hosts = ('60.205.166.72','59.110.11.16','60.205.166.74','101.201.222.104')
src_ports = [ '2282' for i in range(1,5) ]
src_users = [ 'root' for i in range(1,5) ]
src_dirs = [ '/backup_every_table','/backup_every_table','/backup_every_table','/www/backup/backup_every_tables/']
#src_pwds = ('14^871%!&87#','@78778#$1^&8','@8&#$847%177','8&41$1777^#@')
src_myusers = [ 'root' for i in range(1,5) ]
#src_mypwds = ('abcxxx123','others_app89','abcxxx123','CqdXsTPCzvs5R9zP')
yesterday = time.strftime('%Y_%m_%d',time.localtime(time.time()))
local_bakdir = '/backupdbsql/'

def getsrcfiles(host,port,user,src_dir):
	ssh = pmk.SSHClient()
	ssh.set_missing_host_key_policy(pmk.AutoAddPolicy())
	ssh.connect(host,int(port),user)
	cmd = 'ls ' + src_dir
	stdin,stdout,stderr = ssh.exec_command(cmd)
	srcfiles = stdout.readlines()
	return srcfiles
 
def executecmd(cmd):
	print cmd
	log(cmd)
	rs = commands.getstatusoutput(cmd)
	log(rs)
	

def backupdbs():
	if not os.path.exists(local_bakdir):
		os.makedirs(local_bakdir)
	for i in range(len(src_hosts)):
		host_srcfiles = getsrcfiles(src_hosts[i],src_ports[i],src_users[i],src_dirs[i])
		for srcfile in host_srcfiles:
			cmd = "scp -rp -P" + src_ports[i] + ' ' + src_users[i] +  '@' + src_hosts[i] + ':' + src_dirs[i] + '/' + srcfile.replace('\n','')  + ' ' + local_bakdir + os.sep + src_hosts[i] + '_' + srcfile.replace('\n','')
			print cmd
			t = threading.Thread(target=executecmd,args=(cmd,))
			t.setName("thread_" + str(src_hosts[i]))
			t.setDaemon(True)
			t.start()

def log(content):
	log_file = '/tmp/' + yesterday + '_backupdbs_.log'
	with open(log_file,'ab+') as f:
		f.write(json.dumps(content))
		f.write(json.dumps('\r'))

if __name__ == '__main__':
	backupdbs()
