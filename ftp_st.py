# -*- coding: utf-8 -*-
from ftplib import FTP
import paramiko
#
#ftp需要对服务器进行配置
#paramiko相当于sftp,ssh2连接
class FtpSimulate:
    ftp = FTP()
    timeout = 10
    def __init__(self,host,port,username,pwd):
        #调试模式
        self.ftp.set_debuglevel(2)
        self.ftp.connect(host,port,self.timeout)
        self.ftp.login(username,pwd)

    def creatFile(self,fileName):
        self.ftp.cwd('/')
        self.ftp.mkd(fileNmae)

class SFtpSimulate:
    #默认端口
    port = 22
    #初始化连接
    def __init__(self,host,username,pwd):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host,self.port,username,pwd)
    #执行命令，返回三元组 stdin, stdout, stderr
    def doCmd(self,cmd):
        return self.ssh.exec_command(cmd)
    #连接ftp,并进入初始目录默认home目录
    def sftpLink(self,initDir = '/home'):
        sftp = self.ssh.open_sftp()
        sftp.chdir(initDir)
        return sftp
    #关闭ssh连接
    def close(self):
        self.ssh.close()

if __name__ == '__main__':
    sftp = SFtpSimulate('192.168.0.241','root','dh123456')
    sftp.doCmd('mkdir /pythonSome')
    sftpLink = sftp.sftpLink()
    sftpLink.chdir('/njdh/html/web')
    path = sftpLink.getcwd()
    sftpLink.get('index.php','./index.php')
    print(path)
    #sftpLink.chdir('/')
    #sftp.doCmd('rm -rf /pythonSome')
    sftp.close()