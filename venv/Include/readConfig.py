import os, configparser

path = os.path.split(os.path.realpath(__file__))[0]  # 得到readConfig.py文件的上级目录C:\Users\songlihui\PycharmProjects\test001keshanchu\test_db
config_path = os.path.join(path, 'config.ini')  # 得到配置文件目录，配置文件目录为path下的\config.ini
config = configparser.ConfigParser()  # 调用配置文件读取
config.read(config_path, encoding='utf-8')


class ReadConfig():

    def get_mysql(self, key,name):
        value = config.get(key, name)  # 通过config.get拿到配置文件中DATABASE的name的对应值
        return value

    def get_config(self, name):
        value = config.get('CONFIG',name)  # 通过config.get拿到配置文件中CONFIG的设置
        return value


if __name__ == '__main__':
    print('path值为：', path)  # 测试path内容
    print('config_path', config_path)  # 打印输出config_path测试内容是否正确
   # print(ReadConfig().get_mysql('many_source'))
    database=ReadConfig().get_mysql('DATABASE_1','master_database')
    print(database)
    value1 = config.get('CONFIG', 'default_source')
    print(value1)
    #print('通过config.get拿到配置文件中DATABASE的host的对应值:',ReadConfig().get_mysql('host'),'\n',ReadConfig().get_mysql('host'))  # 通过上面的ReadConfig().get_mysql方法获取配置文件中DATABASE的'host'的对应值为10.182.27.158