# -*- coding: utf-8 -*-
from database import DateBase
import os,json

class PhpGenerate:
    app_path = '' # app路径
    namespace = '' #命名空间
    columns = [] #字段信息
    table = ''  #数据表 无前缀
    base_name = '' # 基础类名
    sub_dir = ''    #二级目录
    table_prefix = '' #表前缀
    save_info = []  # 保存信息
    base_path = '' #存储路径
    generate_info = {} #生成信息
    def __init__(self, app_path, namespace, columns, table, table_prefix, base_path):
        self.app_path = app_path 
        self.namespace = namespace 
        self.columns = columns 
        self.table = table  
        self.base_name = ''.join(temp.capitalize() for temp in table.split('_'))    #基础类名
        self.sub_dir = table.split('_')[0].capitalize()
        self.table_prefix = table_prefix
        self.base_path = base_path

    def set_model_content(self):
        model_dir = 'Model'
        fillable = []
        for column in self.columns:
            if column['name'] not in ['id', 'updated_at', 'deleted_at']:
                fillable.append("'{}',{}".format(column['name'], ' //' + column['comment']))

        fillable = '[\n        ' + '\n        '.join(fillable) + '\n    ]'
        namespace_model = self.namespace + '\\' + model_dir + '\\' + self.sub_dir
        model = self.base_name
        
        self.generate_info['namespace_model'] = namespace_model
        self.generate_info['model'] = model

        content = self.get_file_content('./stubs/model.stub')
        content = content.format(**{
            "NamespaceModel":namespace_model,
            "RootNamespace":self.namespace,
            "Model":model,
            "table":self.table_prefix + self.table,
            "ModelDir": model_dir,
            "fillable": fillable,
        })
        self.save_info.append({
            'content':content,
            'path': self.base_path + self.app_path + '/' + model_dir + '/' + self.sub_dir + '/' + model + '.php'
        })

    def set_filter_content(self):
        filter_dir = 'Filters'
        namespace_filter = self.namespace + '\\' + filter_dir + '\\' + self.sub_dir
        filter_str = self.base_name + 'Filter'
        
        self.generate_info['namespace_filter'] = namespace_filter
        self.generate_info['filter_str'] = filter_str
        
        filter_function = []
        filter_function_temp =  """
    /**
    * ${name} {comment}
    */
    public function {name}(${name})
    {{
        $this->builder->where('{name}', ${name});
    }}
    """
        for column in self.columns:
            if column['name'] in ['deleted_at', 'updated_at']:
                continue
            filter_function.append(filter_function_temp.format(**{
                "comment":column['comment'] if column['comment'] != '' else  column['name'], 
                "name":column['name'], 
                "name":column['name']
            }))
        filter_function = "\n".join(filter_function)

        content = self.get_file_content('./stubs/filter.stub')
        content = content.format(**{
            "RootNamespace":self.namespace,
            "FiltersDir":'Filters',
            "NamespaceFilter":namespace_filter,
            "Filter":filter_str,
            "filter_function":filter_function
        })
        self.save_info.append({
            'content':content,
            'path': self.base_path + self.app_path + '/' + filter_dir + '/' + self.sub_dir + '/' + filter_str + '.php'
        })

    '''
    枚举
    '''
    def set_enum_content(self):
        enums = []
        enum_dir = "Enum"
        namespace_enum = self.namespace + '\\' + enum_dir + '\\' + self.sub_dir

        # comment = "测试 enum 成功:TEST_SUCCESS:1,失败:TEST_FAIL:2"

        enum_content = self.get_file_content('./stubs/enum.stub')

        for column in self.columns:
            # column['comment'] = comment
            if 'enum' in column['comment']:
                enum_colums = column['comment'].split('enum')[1].strip().split(',')
                consts = []
                enum = self.base_name + ''.join(name.capitalize() for name in column['name'].split('_')) + 'Enum'
                
                for enum_colum in enum_colums:
                    enum_colum_info = enum_colum.split(':')
                    const = """
    /**
    * {}
    */
    const {} = {};
                            """
                    consts.append(const.format(*enum_colum_info))

                consts = "\r\n".join(consts)
                content = enum_content.format(**{
                    "NamespaceEnum": namespace_enum,
                    "RootNamespace": self.namespace,
                    "EnumsDir": enum_dir,
                    "const": consts,
                    "Enum":enum
                })
                self.save_info.append({
                    'content':content,
                    'path': self.base_path + self.app_path + '/' + enum_dir + '/' + self.sub_dir + '/' + enum + '.php'
                })

    def set_service_content(self):
        service_dir = 'Service'
        namespace_service = self.namespace + '\\' + service_dir + '\\' + self.sub_dir
        service = self.base_name + 'Service'

        self.generate_info['service'] = service
        self.generate_info['namespace_service'] = namespace_service

        content = self.get_file_content('./stubs/service.stub')
        content = content.format(**{
            "Service":service,
            "Model":self.base_name,
            "NamespaceService":namespace_service,
            "NamespaceModel":self.generate_info['namespace_model'],
            "variable":self.table
        })

        self.save_info.append({
            'content':content,
            'path': self.base_path + self.app_path + '/' + service_dir + '/' + self.sub_dir + '/' + service + '.php'
        })

    def set_controller_content(self):
        controller_dir = 'Http/Controllers/Admin'

        namespace_controller = self.namespace + '\\' + 'Http\Controllers\Admin' + '\\' + self.sub_dir
        controller = self.base_name + 'Controller'

        content = open('./stubs/controller.stub', 'r',  encoding='utf-8').read()

        valids = []
        for column in self.columns:
            if column['name'] not in ['id', 'created_at', 'updated_at', 'deleted_at']:
                valids.append("'" + column['name'] + "' => 'required',")

        valid_str = '[\n            ' + '\n            '.join(valids) + '\n        ]'
        content = self.get_file_content('./stubs/controller.stub')
        content = content.format(**{
            "NamespaceController":namespace_controller,
            "Service":self.generate_info['service'],
            "NamespaceService":self.generate_info['namespace_service'],
            "Controller":controller,
            "NamespaceFilter":self.generate_info['namespace_filter'],
            "Filter":self.generate_info['filter_str'],
            "Model":self.generate_info['model'],
            "valid":valid_str
        })
        self.save_info.append({
            'content':content,
            'path': self.base_path + self.app_path + '/' + controller_dir + '/' + self.sub_dir + '/' + controller + '.php'
        })

    def get_file_content(self, file_path):
        handler = open(file_path, 'r', encoding='utf-8')
        content = handler.read()
        handler.close()
        return content

    def write_file_content(self, file_path, content):
        dir_name = os.path.dirname(file_path)

        if os.path.exists(dir_name) is not True:
                os.makedirs(dir_name)

        if os.path.exists(file_path):
            print(file_path + ' has exists')
        else:
            open(file_path, 'w+', encoding='utf-8').write(content)
            print(file_path + ' generate')

    def get_columns_json(self):
        columns_json = {}
        for column in self.columns:
            if column['name'] in ['id', 'created_at', 'updated_at', 'deleted_at']:
                continue
            columns_json[column['name']] = column['comment']
        return json.dumps(columns_json)

    def generate(self):
        self.set_model_content()
        self.set_enum_content()
        self.set_filter_content()
        #前面三个一定要先执行
        self.set_service_content()
        #controller一定放到最后执行
        self.set_controller_content()
        for info in self.save_info:
            self.write_file_content(info['path'], info['content'])
        print(self.get_columns_json())