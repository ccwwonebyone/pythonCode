# -*- coding: utf-8 -*-
import os


class ListDir:
    # 遍历目录 当前目录
    listDir = './'
    fileUrl = 'https://github.com/{}/{}/blob/{}/'
    dirUrl = 'https://github.com/{}/{}/tree/{}/'
    header = '''## [notebook](https://github.com/{}) '''
    space = '&nbsp; &nbsp;'
    mark = '&gt;'
    username = ''
    passFile = ['png', 'jpg', 'gif']
    rn = "\r\n"

    def __init__(self, username, repository, branch):
        self.username = username
        self.fileUrl = self.fileUrl.format(username, repository, branch)
        self.dirUrl = self.dirUrl.format(username, repository, branch)
        self.header = self.header.format(username)

    def get_all_file(self, path):
        files = []
        for file in os.listdir(path):
            dirname = path.replace('./','')
            if file != '.git' and file != '.gitignore':
                if os.path.isdir(path+file):
                    files.append({dirname+file:self.get_all_file(path+file+'/')})
                else:
                    files.append(dirname+file)

        return files

    def parse_files(self, files, level):
        string = ''
        for file in files:
            if type({}) == type(file):
                name = [name for name in file][0]
                string += self.rn+'>'+'#'*level+' '+self.mark*(level-2)+' ['+os.path.basename(name)+']'+'('+self.dirUrl+name+')'
                string += self.rn+self.parse_files(file[name], level+1)
            else:
                fileType = file.split('.')[-1]
                if fileType in self.passFile:
                    pass
                else:
                    string += self.rn+'>'+'#'*level+' '+self.mark*(level-2)+' ['+os.path.basename(file)+']'+'('+self.fileUrl+file+')'
        return string

    def creat_readme(self):
        files = self.get_all_file(self.listDir)
        string = '# 自己的一些学习记录，以及感慨' + self.rn
        string += self.header + self.rn
        string += self.parse_files(files, 3)
        handler = open('./readme.md', 'w')
        handler.write(string)
        handler.close()


if __name__ == '__main__':
    username = 'ccwwonebyone'
    repository = 'notebook'
    branch = 'master'
    listdir = ListDir(username, repository, branch)
    listdir.creat_readme()
    print('已更新'+username+'的'+repository+'仓库的'+branch+'分支的'+'readme.md文件')
    input('回车退出')
