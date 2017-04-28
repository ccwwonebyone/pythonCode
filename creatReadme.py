# -*- coding: utf-8 -*-
import os

class ListDir:

    listDir = './'  #遍历目录 当前目录
    fileUrl = 'https://github.com/{}/{}/blob/{}/'
    dirUrl  = 'https://github.com/{}/{}/tree/{}/'
    hearder = '''## [notebook](https://github.com/{}) '''
    space   = '&nbsp; &nbsp;'
    mark    = '&gt;'
    username = ''
    rn = "\r\n"
    def __init__(self,username,repository,branch):
        self.username = username
        self.fileUrl  = self.fileUrl.format(username,repository,branch)
        self.dirUrl   = self.dirUrl.format(username,repository,branch)
        self.hearder  = self.hearder.format(username)

    def getAllFile(self,path):
        files = []
        for file in os.listdir(path):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            dirname = path.replace('./','')
            if file != '.git' and file != '.gitignore':
                if os.path.isdir(path+file):
                    files.append({dirname+file:self.getAllFile(path+file+'/')})
                else:
                    files.append(dirname+file)

        return files

    def parseFiles(self,files,level):
        string = ''
        for file in files:
            if type({}) == type(file):
                name = [name for name in file][0]
                string += self.rn+'>'+'#'*level+' '+self.mark*(level-2)+' ['+os.path.basename(name)+']'+'('+self.dirUrl+name+')'
                string += self.rn+self.parseFiles(file[name],level+1)
            else:
                string += self.rn+'>'+'#'*level+' '+self.mark*(level-2)+' ['+os.path.basename(file)+']'+'('+self.fileUrl+file+')'
        return string

    def creatReadme(self):
        files = self.getAllFile(self.listDir)
        string = '# 自己的一些学习记录，以及感慨' + self.rn
        string += self.hearder + self.rn
        string += self.parseFiles(files,3)
        hander = open('./readme.md','w')
        hander.write(string)
        hander.close()

if __name__ == '__main__':
    username = 'ccwwonebyone'
    repository = 'notebook'
    branch = 'master'
    listdir = ListDir(username,repository,branch)
    listdir.creatReadme()
    print('已更新'+username+'的'+repository+'仓库的'+branch+'分支的'+'readme.md文件')
