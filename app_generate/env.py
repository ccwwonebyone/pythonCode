# -*- coding: utf-8 -*-

class Env:
    env_path = ''
    env = {}
    def __init__(self, env_path):
        self.env_path = env_path
        self.setAllEnv()

    def setAllEnv(self):
        env_info = open(self.env_path, 'r')
        replaces = {
            'null':None,
            'false':False,
            'true':True
        }
        for line in env_info.readlines():
            if line in ['\n', '\r', '', '\n\r']:
                continue
            info = line.strip().split('=')
            if info[1].lower() in replaces.keys():
                self.env[info[0]] = replaces[info[1].lower()]
            else:
                self.env[info[0]] = info[1]
    
    def get(self, key, default = ''):
        if key in self.env.keys():
            return self.env[key]
        else:
            return default
