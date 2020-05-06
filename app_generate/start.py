# -*- coding: utf-8 -*-
import os,sys   
from env import Env
from database import DateBase 
import json
from php_generate import PhpGenerate

if(len(sys.argv) != 2):
    print('请输入table')

table = sys.argv[1]

base_path = '../../'
prefix = 'dhf_'
env = Env(base_path + '.env')

mysql = DateBase(
    env.get('DB_HOST'),
    env.get('DB_USERNAME'),
    env.get('DB_PASSWORD'),
    env.get('DB_DATABASE'),
    env.get('DB_CHARSET', 'utf8'),
    int(env.get('DB_PORT', 3306))
    )

sub_dir = table.split('_')[0].capitalize()

columns =  mysql.get_columns(prefix + table)


composer_handle = open(base_path + 'composer.json', 'r', encoding='utf-8')
composer = json.loads(composer_handle.read())
namespace = ''
path = ''
for key,value in composer['autoload']['psr-4'].items():
    namespace = key.replace('\\', '')
    path = value.replace('/', '')

php_generate = PhpGenerate(path, namespace, columns, table, prefix, base_path)
php_generate.generate()
